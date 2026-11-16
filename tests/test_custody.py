import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bench_under_test',ROOT/'bench.py')
bench=importlib.util.module_from_spec(spec);spec.loader.exec_module(bench)

class CustodyTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)/'repo';self.root.mkdir()
  for name in ['cases/catalog.json','cases/contracts.json','tests/oracles.json','src/processbench/__init__.py','methods/DELIVERY_SOP.md','docs/PROTOCOL.md','docs/CAMPAIGN_DESIGN.md','docs/WORKER_INSTRUCTIONS.txt','bench.py']:
   out=self.root/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,out)
  self.enterContext(patch.object(bench,'ROOT',self.root));self.enterContext(patch.object(bench,'CAMPAIGN',self.root/'runs/campaign-001'))
  bench.freeze()
 def delivery(self):
  worker=Path(self.tmp.name)/'worker';bench.stage('baseline','finance',1,worker)
  ideal=json.loads((self.root/'tests/oracles.json').read_text())
  outputs={k:v for k,v in ideal.items() if k.startswith('finance-')}
  out=worker/'deliveries.json';out.write_text(json.dumps(outputs))
  return out
 def test_duplicate_keys_are_not_silently_accepted(self):
  out=self.delivery();out.write_text('{"finance-01":null,'+out.read_text()[1:])
  result=bench.ingest('baseline','finance',1,out)
  self.assertFalse(result['envelope_valid'])
 def test_first_delivery_is_immutable(self):
  out=self.delivery();bench.ingest('baseline','finance',1,out)
  with self.assertRaisesRegex(ValueError,'already_preserved'):bench.ingest('baseline','finance',1,out)
 def test_changed_worker_input_blocks_import(self):
  out=self.delivery();(out.parent/'task.json').write_text('{}')
  with self.assertRaisesRegex(ValueError,'worker_input_changed'):bench.ingest('baseline','finance',1,out)
 def test_stage_never_exposes_oracles(self):
  worker=Path(self.tmp.name)/'worker';bench.stage('sop','meeting',1,worker)
  task=json.loads((worker/'task.json').read_text())
  self.assertEqual(4,len(task['cases']));self.assertIn('procedure',task)
  self.assertEqual({'task.json'},{p.name for p in worker.iterdir()})
 def test_changed_frozen_files_block_evaluation(self):
  (self.root/'cases/catalog.json').write_text('[]')
  with self.assertRaisesRegex(ValueError,'frozen_input_changed'):bench.evaluate()
 def test_missing_deliveries_remain_in_denominator(self):
  result=bench.evaluate()
  self.assertEqual(24,result['planned_pairs']);self.assertFalse(result['complete'])
  self.assertEqual({'baseline':0,'sop':0},result['accepted'])
  self.assertFalse(result['procedure_generation_improvement_qualified'])
  self.assertTrue(result['gate_qualified_on_known_controls'])

if __name__=='__main__':unittest.main()
