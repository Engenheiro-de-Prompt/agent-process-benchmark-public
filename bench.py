#!/usr/bin/env python3
"""Portable, offline campaign custody and objective business evaluation."""
import argparse
import collections
import datetime
import hashlib
import html
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from processbench import load_cases,verify,build_controls

DOMAINS=('finance','meeting','inventory')
ARMS=('baseline','sop')
CAMPAIGN=ROOT/'runs/campaign-001'
REPLICAS=2

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,value):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def strict_json(raw):
 def unique(pairs):
  out={}
  for key,value in pairs:
   if key in out:raise ValueError('duplicate_json_key')
   out[key]=value
  return out
 def invalid_constant(value):raise ValueError('nonfinite_json_number')
 return json.loads(raw,object_pairs_hook=unique,parse_constant=invalid_constant)
def guarded_manifest():
 m=read(CAMPAIGN/'manifest.json')
 for p,d in m['frozen_files'].items():
  if digest(ROOT/p)!=d:raise ValueError('frozen_input_changed:'+p)
 if [c['case_id'] for c in load_cases(ROOT)]!=m['case_ids']:raise ValueError('case_set_changed')
 return m

def freeze():
 if (CAMPAIGN/'manifest.json').exists():raise ValueError('campaign_exists_use_new_version')
 cases=load_cases(ROOT)
 if len(cases)!=12 or collections.Counter(c['domain'] for c in cases)!=dict.fromkeys(DOMAINS,4):raise ValueError('invalid_case_set')
 files=['cases/catalog.json','cases/contracts.json','tests/oracles.json','src/processbench/__init__.py','methods/DELIVERY_SOP.md','docs/PROTOCOL.md','docs/CAMPAIGN_DESIGN.md','docs/WORKER_INSTRUCTIONS.txt','bench.py']
 oracles=read(ROOT/'tests/oracles.json')
 # Gate validates the independent expected outputs before any agent is launched.
 controls=[]
 for c in cases:
  oracle=oracles[c['case_id']]
  if not verify(c,oracle,oracle)['passed']:raise ValueError('inconsistent_oracle')
  for control in build_controls(c,oracle):controls.append(dict(control,case_id=c['case_id'],domain=c['domain']))
 save(CAMPAIGN/'controls.json',controls)
 files.append('runs/campaign-001/controls.json')
 order=[('baseline','finance'),('sop','inventory'),('baseline','meeting'),('sop','finance'),('baseline','inventory'),('sop','meeting')]
 plan=[{'arm':arm,'domain':domain,'replica':r,'case_ids':[c['case_id'] for c in cases if c['domain']==domain]} for r in range(1,REPLICAS+1) for arm,domain in (order if r==1 else list(reversed(order)))]
 save(CAMPAIGN/'manifest.json',{'campaign_id':'campaign-001','created_at':now(),'case_ids':[c['case_id'] for c in cases],'replicas':REPLICAS,'planned_pairs':len(cases)*REPLICAS,'worker_plan':plan,'frozen_files':{p:digest(ROOT/p) for p in files},'executor_profile':{'runtime':'Hermes native delegated agents','model':'gpt-6.1-sol','provider':'openai-codex','profile_evidence':'current native subagent session metadata; seeds and parameters not exposed','tools':'read/write/terminal limited by instruction to worker directory','scope_budget':'four small public cases per worker; identical arms','hard_os_sandbox':False,'feedback_from_grader':False,'tokens_and_monetary_cost':'not exposed per run; unavailable'},'success_threshold':{'improved_pairs_min':1,'regressions_max':0,'all_planned_pairs_required':True,'control_false_accepts_max':0,'control_false_rejects_max':0}})
 return {'frozen':True,'planned_pairs':len(cases)*REPLICAS,'workers':len(plan),'controls':len(controls)}

def worker_task(slot):
 arm=slot['arm']
 cases=[c for c in load_cases(ROOT) if c['case_id'] in slot['case_ids']]
 task={'case_ids':slot['case_ids'],'cases':cases,'delivery':'Write deliveries.json, a JSON object mapping EXACTLY these four case_ids to their requested output objects. No wrapper, comments, Markdown, assessment or extra keys. Do not read any evaluator, oracle, other worker or other directory. Baseline may self-check voluntarily; no grader feedback is available.'}
 if arm=='sop':task['procedure']=(ROOT/'methods/DELIVERY_SOP.md').read_text()
 return task

def stage(arm,domain,replica,directory):
 m=guarded_manifest();slot=next((s for s in m['worker_plan'] if (s['arm'],s['domain'],s['replica'])==(arm,domain,replica)),None)
 if slot is None:raise ValueError('unplanned_worker')
 task=worker_task(slot)
 directory=Path(directory)
 if directory.exists():raise ValueError('worker_directory_exists')
 directory.mkdir(parents=True,mode=0o700);save(directory/'task.json',task)
 return {'staged':True,'public_case_count':len(task['cases']),'input_sha256':digest(directory/'task.json')}

def ingest(arm,domain,replica,file):
 m=guarded_manifest();slot=next((s for s in m['worker_plan'] if (s['arm'],s['domain'],s['replica'])==(arm,domain,replica)),None)
 if slot is None:raise ValueError('unplanned_worker')
 expected_task=(json.dumps(worker_task(slot),ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
 if (Path(file).parent/'task.json').read_bytes()!=expected_task:raise ValueError('worker_input_changed')
 target=CAMPAIGN/'outputs'/f'{arm}-{domain}-{replica}.json'
 if target.exists():raise ValueError('first_delivery_already_preserved')
 raw=Path(file).read_bytes()
 try:
  data=strict_json(raw);valid=isinstance(data,dict) and set(data)==set(slot['case_ids'])
 except (ValueError,UnicodeError,RecursionError):data=None;valid=False
 save(target,{'arm':arm,'domain':domain,'replica':replica,'imported_at':now(),'response_sha256':hashlib.sha256(raw).hexdigest(),'envelope_valid':valid,'deliveries':data if valid else None})
 return {'preserved':True,'envelope_valid':valid,'case_count':len(slot['case_ids'])}

def evaluate():
 m=guarded_manifest();cases={c['case_id']:c for c in load_cases(ROOT)};oracles=read(ROOT/'tests/oracles.json')
 control_results=[]
 for c in read(CAMPAIGN/'controls.json'):
  verdict=verify(cases[c['case_id']],c['output'],oracles[c['case_id']])
  control_results.append({'case_id':c['case_id'],'domain':c['domain'],'control_id':c['control_id'],'expected_pass':c['expected_pass'],'actual_pass':verdict['passed'],'correct':verdict['passed'] is c['expected_pass'],'reason_codes':verdict['reason_codes']})
 controls_ok=bool(control_results) and all(r['correct'] for r in control_results)
 for domain in DOMAINS:
  relevant=[r for r in control_results if r['domain']==domain]
  controls_ok=controls_ok and any(r['expected_pass'] for r in relevant) and any(not r['expected_pass'] for r in relevant)
 rows=[];by_key={}
 for s in m['worker_plan']:
  p=CAMPAIGN/'outputs'/f"{s['arm']}-{s['domain']}-{s['replica']}.json"
  observed=read(p) if p.exists() else None
  for cid in s['case_ids']:
   actual=observed['deliveries'].get(cid) if observed and observed.get('envelope_valid') else None
   verdict=verify(cases[cid],actual,oracles[cid])
   row={'case_id':cid,'domain':s['domain'],'arm':s['arm'],'replica':s['replica'],'delivery_present':observed is not None,'passed':verdict['passed'],'reason_codes':verdict['reason_codes'],'actual':actual,'ideal':oracles[cid]}
   rows.append(row);by_key[(cid,s['replica'],s['arm'])]=row
 pairs=[]
 for replica in range(1,m['replicas']+1):
  for cid in m['case_ids']:
   b=by_key[(cid,replica,'baseline')];s=by_key[(cid,replica,'sop')]
   outcome='improved' if s['passed'] and not b['passed'] else 'regressed' if b['passed'] and not s['passed'] else 'tied_accepted' if b['passed'] else 'tied_rejected'
   pairs.append({'case_id':cid,'domain':cases[cid]['domain'],'replica':replica,'outcome':outcome})
 counts=dict(collections.Counter(p['outcome'] for p in pairs));complete=all(r['delivery_present'] for r in rows)
 promotion=complete and controls_ok and counts.get('improved',0)>0 and counts.get('regressed',0)==0
 summary={'campaign_id':m['campaign_id'],'as_of':now(),'complete':complete,'planned_pairs':m['planned_pairs'],'received_deliveries':sum(r['delivery_present'] for r in rows),'ideal_accepted_per_arm':m['planned_pairs'],'accepted':{arm:sum(r['passed'] for r in rows if r['arm']==arm) for arm in ARMS},'paired_outcomes':counts,'procedure_generation_improvement_qualified':bool(promotion),'gate_qualified_on_known_controls':bool(controls_ok),'controls_total':len(control_results),'valid_controls':sum(r['expected_pass'] for r in control_results),'invalid_controls':sum(not r['expected_pass'] for r in control_results),'false_accepts':sum(r['actual_pass'] and not r['expected_pass'] for r in control_results),'false_rejects':sum(not r['actual_pass'] and r['expected_pass'] for r in control_results),'business_roi_measured':False,'generalizes_to_all_agents':False,'hard_os_sandbox':False,'replicas_are_not_independent_new_cases':True,'rows':rows,'pairs':pairs,'control_results':control_results}
 save(ROOT/'reports/results.json',summary)
 parts=['<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Benchmark de processos</title><style>body{font:16px system-ui;max-width:1100px;margin:32px auto;padding:16px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere}.ok{color:#075}.bad{color:#a21}</style><h1>Resultado de negócio: realizado × ideal</h1>']
 if not complete:headline='Execução incompleta: não há conclusão comparativa.'
 elif promotion:headline='Procedimento melhorou aceitações nesta amostra sintética, sem regressões observadas.'
 else:headline='Não foi demonstrada superioridade do procedimento na geração das entregas.'
 parts.extend(['<p><strong>'+html.escape(headline)+'</strong></p>',f"<p>Baseline: {summary['accepted']['baseline']}/{m['planned_pairs']}. Procedimento: {summary['accepted']['sop']}/{m['planned_pairs']}. Ideal: {m['planned_pairs']} por braço.</p>",f"<p>Gate em controles conhecidos: {len(control_results)} controles; {summary['false_accepts']} erros aceitos, {summary['false_rejects']} válidos recusados. Controles NÃO são execuções reais nem ganhos de cliente.</p>",'<p>Pequena amostra sintética; réplicas reutilizam casos. Não comprova ROI, eficiência, confiabilidade universal ou ganho em produção. Segregação por contexto/instrução; não sandbox OS.</p><table><tr><th>Caso</th><th>Réplica</th><th>Baseline</th><th>Procedimento</th></tr>'])
 for pair in pairs:
  cid=pair['case_id'];rep=pair['replica'];b=by_key[(cid,rep,'baseline')];s=by_key[(cid,rep,'sop')]
  parts.append('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in [cid,rep,'Aceito' if b['passed'] else 'Reprovado','Aceito' if s['passed'] else 'Reprovado'])+'</tr>')
 parts.append('</table><h2>Entregas e gabaritos</h2>')
 for row in rows:
  parts.append('<details><summary>'+html.escape(f"{row['case_id']} / {row['arm']} / réplica {row['replica']}")+'</summary><pre>'+html.escape(json.dumps({'ideal':row['ideal'],'realizado':row['actual'],'diagnostico':row['reason_codes']},ensure_ascii=False,indent=2))+'</pre></details>')
 out=ROOT/'reports/index.html';out.write_text(''.join(parts),encoding='utf-8')
 return {k:v for k,v in summary.items() if k not in ('rows','pairs','control_results')}

def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest='cmd',required=True)
 sub.add_parser('freeze');sub.add_parser('evaluate')
 for cmd in ('stage','ingest'):
  q=sub.add_parser(cmd);q.add_argument('--arm',choices=ARMS,required=True);q.add_argument('--domain',choices=DOMAINS,required=True);q.add_argument('--replica',type=int,required=True);q.add_argument('--directory' if cmd=='stage' else '--file',type=Path,required=True)
 a=p.parse_args()
 try:
  result=freeze() if a.cmd=='freeze' else evaluate() if a.cmd=='evaluate' else stage(a.arm,a.domain,a.replica,a.directory) if a.cmd=='stage' else ingest(a.arm,a.domain,a.replica,a.file)
 except (ValueError,OSError,KeyError) as e:
  print(json.dumps({'status':'blocked','error_class':type(e).__name__}));return 1
 print(json.dumps(result,ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
