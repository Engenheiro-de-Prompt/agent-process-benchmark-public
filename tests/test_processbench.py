"""Public API contract tests, using hand-authored independent answer fixtures."""
import copy
import json
from pathlib import Path
import unittest

from processbench import build_controls, load_cases, verify

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'cases/catalog.json').read_text())
ORACLES = json.loads((ROOT / 'tests/oracles.json').read_text())


class DeliveryTests(unittest.TestCase):
    def test_finance_centavos_cancellation_and_evidence(self):
        case = CASES[0]
        result = verify(case, ORACLES['finance-01'], ORACLES['finance-01'])
        self.assertTrue(result['passed'], result)
        wrong = copy.deepcopy(ORACLES['finance-01'])
        wrong['balances'][0]['ledger_cents'] = 1501
        wrong['totals']['ledger_cents'] = 1300
        wrong['balances'][0]['difference_cents'] = 501
        wrong['totals']['difference_cents'] = 501
        self.assertFalse(verify(case, wrong, ORACLES['finance-01'])['passed'])

    def test_meeting_only_owned_acceptances_and_literal_deadlines(self):
        for case in CASES[4:8]:
            oracle = ORACLES[case['case_id']]
            self.assertTrue(verify(case, oracle, oracle)['passed'])
        candidate = copy.deepcopy(ORACLES['meeting-02'])
        candidate['obligations'][1]['deadline'] = '2030-04-09'
        self.assertFalse(verify(CASES[5], candidate, ORACLES['meeting-02'])['passed'])
        candidate = copy.deepcopy(ORACLES['meeting-01'])
        candidate['obligations'].append({'id':'S2', 'action':'Criar painel sintético',
            'owner':'Pessoa-B', 'deadline':'2030-04-04', 'evidence':['S2']})
        self.assertFalse(verify(CASES[4], candidate, ORACLES['meeting-01'])['passed'])

    def test_inventory_unique_confirmed_unit_movements_and_reversals(self):
        for case in CASES[8:]:
            oracle = ORACLES[case['case_id']]
            self.assertTrue(verify(case, oracle, oracle)['passed'])
        candidate = copy.deepcopy(ORACLES['inventory-03'])
        candidate['items'][0]['net_units'] = -6
        candidate['items'][0]['closing_units'] = 2
        self.assertFalse(verify(CASES[10], candidate, ORACLES['inventory-03'])['passed'])
        candidate = copy.deepcopy(ORACLES['inventory-02'])
        candidate['items'][0]['net_units'] = -2
        candidate['items'][0]['closing_units'] = 0
        self.assertFalse(verify(CASES[9], candidate, ORACLES['inventory-02'])['passed'])

    def test_load_public_cases_with_contracts_without_oracles(self):
        cases = load_cases(ROOT)
        self.assertEqual(len(cases), 12)
        self.assertEqual([c['case_id'] for c in cases], sorted(ORACLES))
        self.assertEqual({d: sum(c['domain'] == d for c in cases)
                          for d in ('finance', 'meeting', 'inventory')},
                         {'finance':4, 'meeting':4, 'inventory':4})
        self.assertEqual(load_cases(ROOT / 'cases'), cases)
        for case in cases:
            self.assertTrue(case['contract']['output_schema'])
            self.assertEqual(case['domain'], case['contract']['domain'])
            self.assertNotIn('oracle', case)
            self.assertTrue(verify(case, ORACLES[case['case_id']], ORACLES[case['case_id']])['passed'])
        self.assertEqual(load_cases(ROOT / 'cases/missing'), [])

    def test_controls_are_labeled_probes_not_real_runs(self):
        for case in CASES:
            oracle = ORACLES[case['case_id']]
            before = copy.deepcopy(oracle)
            controls = build_controls(case, oracle)
            by_id = {control['control_id']: control for control in controls}
            self.assertIn('valid_delivery', by_id)
            self.assertTrue(by_id['valid_delivery']['expected_pass'])
            for cid in ('missing_output', 'wrong_json_type', 'extra_field', 'wrong_business_value'):
                self.assertIn(cid, by_id)
                self.assertIs(by_id[cid]['expected_pass'], False)
            for control in controls:
                self.assertEqual(set(control), {'control_id','output','expected_pass'})
                self.assertIs(verify(case, control['output'], oracle)['passed'], control['expected_pass'])
            self.assertEqual(oracle, before)
        self.assertEqual(build_controls(None, None), [])

    def test_evidence_gate_has_separate_content_free_diagnostics(self):
        actual = copy.deepcopy(ORACLES['finance-01'])
        actual['balances'][0]['evidence'] = ['E-SYNTHETIC-SECRET']
        result = verify(CASES[0], actual, ORACLES['finance-01'])
        self.assertFalse(result['passed'])
        self.assertIn('EVIDENCE_MISMATCH', result['reason_codes'])
        self.assertIn({'check_id':'business_values', 'passed':True}, result['checks'])
        self.assertIn({'check_id':'evidence', 'passed':False}, result['checks'])
        encoded = json.dumps(result)
        for forbidden in ('E-SYNTHETIC-SECRET', 'T1', '1001', 'B1', 'L1'):
            self.assertNotIn(forbidden, encoded)
        self.assertEqual(verify(CASES[0], None, ORACLES['finance-01'])['reason_codes'], ['MISSING_OUTPUT'])
        malformed = copy.deepcopy(ORACLES['finance-01'])
        malformed['balances'][0]['ledger_cents'] = True
        self.assertEqual(verify(CASES[0], malformed, ORACLES['finance-01'])['reason_codes'], ['OUTPUT_SCHEMA'])

    def test_malformed_case_containers_fail_closed(self):
        malformed = []
        for index, field in ((4, 'statements'), (8, 'opening'), (8, 'movements')):
            case = copy.deepcopy(CASES[index])
            case['input'][field] = {}
            malformed.append(case)
        case = copy.deepcopy(CASES[0])
        case['input']['unexpected'] = 'not authorized by schema'
        malformed.append(case)
        for case in malformed:
            oracle = ORACLES[case['case_id']]
            self.assertEqual(verify(case, oracle, oracle)['reason_codes'], ['INVALID_CASE'])
        for case in (None, [], {}, 'not a case', {'domain':'unknown'}, {'domain':[]}):
            self.assertFalse(verify(case, None, None)['passed'])
        for candidate in (None, [], {}, '', '```json {} ```', 1, True, float('nan')):
            result = verify(CASES[0], candidate, ORACLES['finance-01'])
            self.assertFalse(result['passed'])
            self.assertEqual(set(result), {'passed','checks','reason_codes'})


if __name__ == '__main__':
    unittest.main()
