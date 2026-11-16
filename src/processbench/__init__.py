"""Stdlib-only deterministic gates for synthetic business deliveries.

Public inputs and contracts are loaded separately from private test oracles.
Diagnostics contain fixed identifiers and booleans, never supplied content.
"""
import copy
import csv
import io
import json
from pathlib import Path

__all__ = ["load_cases", "verify", "build_controls"]


def load_cases(root):
    """Return public cases with embedded contracts, sorted by case_id.

    root is the repository directory or its cases directory. Only catalog.json
    and contracts.json are read. Missing/malformed catalogs return [] atomically,
    never a misleading partial selection. No test oracle is loaded here.
    """
    try:
        directory = Path(root)
        if directory.name != 'cases':
            directory = directory / 'cases'
        catalog = json.loads((directory / 'catalog.json').read_text(encoding='utf-8'))
        contracts = json.loads((directory / 'contracts.json').read_text(encoding='utf-8'))
        if type(catalog) is not list or type(contracts) is not dict:
            return []
        cases, seen = [], set()
        for case in catalog:
            if set(case) != {'case_id', 'domain', 'contract_id', 'title', 'input'}:
                return []
            cid = case['case_id']
            if not isinstance(cid, str) or not cid or cid in seen:
                return []
            seen.add(cid)
            contract = contracts[case['contract_id']]
            required = {'domain', 'task', 'input_schema', 'rules', 'output_schema', 'acceptance'}
            if set(contract) != required or contract['domain'] != case['domain']:
                return []
            if (not all(isinstance(contract[k], str) and contract[k]
                        for k in ('task', 'input_schema', 'acceptance'))
                    or not isinstance(contract['rules'], list) or not contract['rules']
                    or not isinstance(contract['output_schema'], dict) or not contract['output_schema']):
                return []
            _derive(case)
            cases.append(dict(copy.deepcopy(case), contract=copy.deepcopy(contract)))
        return sorted(cases, key=lambda case: case['case_id'])
    except (OSError, ValueError, TypeError, KeyError, AttributeError,
            csv.Error, OverflowError, RecursionError):
        return []


def _same(left, right):
    """JSON equality with exact types: True and 1 are not interchangeable."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _finance(data):
    sides = []
    for name in ('ledger_csv', 'bank_csv'):
        reader = csv.DictReader(io.StringIO(data[name]))
        if reader.fieldnames != ['row_id', 'id', 'revision', 'status', 'amount_cents']:
            raise ValueError('schema')
        selected, seen_rows, versions = {}, set(), {}
        for row in reader:
            if set(row) != set(reader.fieldnames) or any(v is None for v in row.values()):
                raise ValueError('schema')
            rid, tid = row['row_id'], row['id']
            rev, cents = int(row['revision']), int(row['amount_cents'])
            if not rid or not tid or rid in seen_rows or rev < 1 or row['status'] not in ('confirmed', 'cancelled'):
                raise ValueError('input')
            seen_rows.add(rid)
            key = (tid, rev)
            business = (row['status'], cents)
            if key in versions and versions[key] != business:
                raise ValueError('conflicting duplicate')
            versions[key] = business
            if tid not in selected or rev > selected[tid][0]:
                selected[tid] = (rev, row['status'], cents, rid)
        sides.append({k: v for k, v in selected.items() if v[1] == 'confirmed'})
    ledger, bank = sides
    balances = []
    totals = dict(ledger_cents=0, bank_cents=0, difference_cents=0)
    for tid in sorted(ledger.keys() | bank.keys()):
        lc = ledger[tid][2] if tid in ledger else 0
        bc = bank[tid][2] if tid in bank else 0
        evidence = sorted(side[tid][3] for side in sides if tid in side)
        balances.append(dict(id=tid, ledger_cents=lc, bank_cents=bc,
                             difference_cents=lc-bc, evidence=evidence))
        totals['ledger_cents'] += lc
        totals['bank_cents'] += bc
        totals['difference_cents'] += lc-bc
    return dict(balances=balances, totals=totals)


def _meeting(data):
    obligations, seen = [], set()
    for row in data['statements']:
        if set(row) != {'id', 'decision', 'action', 'owner', 'deadline'}:
            raise ValueError('schema')
        if not isinstance(row['id'], str) or not row['id'] or row['id'] in seen:
            raise ValueError('id')
        seen.add(row['id'])
        if row['decision'] not in ('accepted', 'proposed', 'rejected'):
            raise ValueError('decision')
        if not isinstance(row['action'], str) or not row['action']:
            raise ValueError('action')
        if row['owner'] is not None and (not isinstance(row['owner'], str) or not row['owner']):
            raise ValueError('owner')
        if row['deadline'] is not None and not isinstance(row['deadline'], str):
            raise ValueError('deadline')
        if row['decision'] == 'accepted' and row['owner'] is not None:
            obligations.append({key: row[key] for key in ('id', 'action', 'owner', 'deadline')})
            obligations[-1]['evidence'] = [row['id']]
    return {'obligations': sorted(obligations, key=lambda row: row['id'])}


def _inventory(data):
    opening, applied, unique, reversed_ids = {}, {}, {}, set()
    for row in data['opening']:
        if set(row) != {'sku', 'units'} or not isinstance(row['sku'], str) or not row['sku']:
            raise ValueError('schema')
        if row['sku'] in opening or type(row['units']) is not int or row['units'] < 0:
            raise ValueError('opening')
        opening[row['sku']] = row['units']
    for row in data['movements']:
        if set(row) != {'id', 'sku', 'status', 'kind', 'qty_units', 'reverses'}:
            raise ValueError('schema')
        mid = row['id']
        if not isinstance(mid, str) or not mid or row['sku'] not in opening:
            raise ValueError('id or sku')
        if mid in unique:
            if not _same(unique[mid], row):
                raise ValueError('conflicting duplicate')
            continue
        if row['status'] not in ('confirmed', 'pending', 'cancelled'):
            raise ValueError('status')
        qty = row['qty_units']
        if type(qty) is not int or qty <= 0:
            raise ValueError('unit quantity')
        if row['kind'] == 'reversal':
            target = unique.get(row['reverses'])
            if (not target or target['status'] != 'confirmed' or target['kind'] not in ('in', 'out')
                    or target['sku'] != row['sku'] or target['qty_units'] != qty
                    or target['id'] in reversed_ids):
                raise ValueError('reversal')
            effect = -qty if target['kind'] == 'in' else qty
            if row['status'] == 'confirmed':
                reversed_ids.add(target['id'])
        elif row['kind'] in ('in', 'out') and row['reverses'] is None:
            effect = qty if row['kind'] == 'in' else -qty
        else:
            raise ValueError('kind')
        unique[mid] = row
        if row['status'] == 'confirmed':
            applied[mid] = (row['sku'], effect)
    items = []
    for sku, units in sorted(opening.items()):
        ids = sorted(mid for mid, (item, _) in applied.items() if item == sku)
        net = sum(applied[mid][1] for mid in ids)
        items.append(dict(sku=sku, opening_units=units, net_units=net,
                          closing_units=units+net, evidence=ids))
    return {'items': items}


def _derive(case):
    if type(case) is not dict or type(case.get('input')) is not dict:
        raise ValueError('case')
    domain, data = case.get('domain'), case['input']
    required = {'finance': {'ledger_csv', 'bank_csv'}, 'meeting': {'statements'},
                'inventory': {'opening', 'movements'}}
    if not isinstance(domain, str) or domain not in required or set(data) != required[domain]:
        raise ValueError('input schema')
    if domain == 'finance':
        if any(type(v) is not str for v in data.values()):
            raise ValueError('CSV strings')
        return _finance(data)
    if any(type(v) is not list for v in data.values()):
        raise ValueError('input arrays')
    if domain == 'meeting':
        return _meeting(data)
    return _inventory(data)


def _result(checks, reason=None):
    return {'passed': reason is None, 'checks': checks,
            'reason_codes': [] if reason is None else [reason]}


_MONEY = {'ledger_cents': int, 'bank_cents': int, 'difference_cents': int}
_SCHEMAS = {
    'finance': {'balances': [dict(id=str, evidence=[str], **_MONEY)], 'totals': _MONEY},
    'meeting': {'obligations': [dict(id=str, action=str, owner=str,
                                      deadline=(str, type(None)), evidence=[str])]},
    'inventory': {'items': [dict(sku=str, opening_units=int, net_units=int,
                                 closing_units=int, evidence=[str])]},
}


def _schema(value, schema):
    if isinstance(schema, dict):
        return (type(value) is dict and value.keys() == schema.keys()
                and all(_schema(value[k], schema[k]) for k in schema))
    if isinstance(schema, list):
        return type(value) is list and all(_schema(v, schema[0]) for v in value)
    if isinstance(schema, tuple):
        return type(value) in schema
    return type(value) is schema


def _without_evidence(value):
    if isinstance(value, dict):
        return {k: _without_evidence(v) for k, v in value.items() if k != 'evidence'}
    if isinstance(value, list):
        return [_without_evidence(v) for v in value]
    return value


def verify(case, actual, oracle):
    """Check one parsed JSON object; emit only fixed codes and booleans.

    Missing or malformed inputs fail closed. JSON text is not a parsed object;
    callers must parse exactly one JSON document and reject duplicate JSON keys
    before invoking this API. The oracle is checked against source invariants,
    not trusted merely because the candidate agrees with it.
    """
    checks = []
    try:
        expected = _derive(case)
    except (ValueError, TypeError, KeyError, AttributeError, csv.Error, OverflowError, RecursionError):
        return _result([{'check_id': 'case_input', 'passed': False}], 'INVALID_CASE')
    checks.append({'check_id': 'case_input', 'passed': True})
    valid_oracle = _same(expected, oracle)
    checks.append({'check_id': 'oracle_invariants', 'passed': valid_oracle})
    if not valid_oracle:
        return _result(checks, 'INVALID_ORACLE')
    shape = _schema(actual, _SCHEMAS[case['domain']])
    checks.append({'check_id': 'output_schema', 'passed': shape})
    if not shape:
        return _result(checks, 'MISSING_OUTPUT' if actual is None else 'OUTPUT_SCHEMA')
    business = _same(_without_evidence(actual), _without_evidence(oracle))
    checks.append({'check_id': 'business_values', 'passed': business})
    key = {'finance': 'balances', 'meeting': 'obligations', 'inventory': 'items'}[case['domain']]
    evidence = _same([row['evidence'] for row in actual[key]],
                     [row['evidence'] for row in oracle[key]])
    checks.append({'check_id': 'evidence', 'passed': evidence})
    codes = ([] if business else ['BUSINESS_MISMATCH']) + ([] if evidence else ['EVIDENCE_MISMATCH'])
    return {'passed': not codes, 'checks': checks, 'reason_codes': codes}


def build_controls(case, oracle):
    """Build explicitly synthetic verifier probes, never agent executions.

    expected_pass is fixed by each mutation's design, not by running verify.
    Callers must keep these probes out of agent-quality/improvement metrics.
    Invalid case/oracle returns [] rather than inventing a positive control.
    """
    if not verify(case, oracle, oracle)['passed']:
        return []
    controls = []

    def add(cid, output, expected_pass=False):
        controls.append(dict(control_id=cid, output=output, expected_pass=expected_pass))

    add('valid_delivery', copy.deepcopy(oracle), True)
    add('missing_output', None)
    add('wrong_json_type', [])
    extra = copy.deepcopy(oracle)
    extra['approved'] = True
    add('extra_field', extra)
    wrong = copy.deepcopy(oracle)
    if case['domain'] == 'finance':
        key = 'balances'
        wrong['totals']['difference_cents'] += 1
    elif case['domain'] == 'inventory':
        key = 'items'
        if wrong[key]:
            wrong[key][0]['closing_units'] += 1
        else:
            wrong[key].append(dict(sku='SKU-INVENTED', opening_units=0,
                                   net_units=0, closing_units=0, evidence=[]))
    else:
        key = 'obligations'
        if wrong[key]:
            wrong[key][0]['owner'] = 'Pessoa-INVENTADA'
        else:
            wrong[key].append(dict(id='S-INVENTED', action='Inventar compromisso',
                                   owner='Pessoa-INVENTADA', deadline=None, evidence=['S-INVENTED']))
    add('wrong_business_value', wrong)
    if oracle[key]:
        duplicate = copy.deepcopy(oracle)
        duplicate[key].append(copy.deepcopy(duplicate[key][0]))
        add('duplicate_item', duplicate)
        missing = copy.deepcopy(oracle)
        missing[key].pop(0)
        add('omitted_item', missing)
        fabricated = copy.deepcopy(oracle)
        fabricated[key][0]['evidence'].append('E-INVENTED')
        add('fabricated_evidence', fabricated)
        absent = copy.deepcopy(oracle)
        del absent[key][0]['evidence']
        add('missing_evidence_field', absent)
        if oracle[key][0]['evidence']:
            empty = copy.deepcopy(oracle)
            empty[key][0]['evidence'] = []
            add('omitted_evidence', empty)
    return controls
