#!/usr/bin/env python3
"""Replay the public synthetic campaign offline, without changing evidence."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import bench

def comparable(value):
 if isinstance(value,dict):return {k:comparable(v) for k,v in value.items() if k!='as_of'}
 if isinstance(value,list):return [comparable(v) for v in value]
 return value

def verify():
 original=bench.read(ROOT/'reports/results.json')
 manifest=bench.guarded_manifest();controls=[]
 for case in bench.load_cases(ROOT):
  oracle=bench.read(ROOT/'tests/oracles.json')[case['case_id']]
  for c in bench.build_controls(case,oracle):controls.append(dict(c,case_id=case['case_id'],domain=case['domain']))
 if controls!=bench.read(ROOT/'runs/campaign-001/controls.json'):raise ValueError('stored_controls_do_not_replay')
 with tempfile.TemporaryDirectory(prefix='public-process-replay-') as directory:
  target=Path(directory)/'bundle';target.mkdir()
  # Copy only the evidence/inputs needed for grading, never local configuration.
  names=set(manifest['frozen_files'])|{'runs/campaign-001/manifest.json'}
  names.update('runs/campaign-001/outputs/'+p.name for p in (ROOT/'runs/campaign-001/outputs').glob('*.json'))
  for name in names:
   relative=Path(name)
   if relative.is_absolute() or '..' in relative.parts:raise ValueError('invalid_bundle_path')
   source=ROOT/relative
   if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()):raise ValueError('bundle_path_escape')
   dest=target/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
  with patch.object(bench,'ROOT',target),patch.object(bench,'CAMPAIGN',target/'runs/campaign-001'):
   result=bench.evaluate()
  if not result['complete']:raise ValueError('incomplete_public_campaign')
  if comparable(original)!=comparable(bench.read(target/'reports/results.json')):raise ValueError('published_result_does_not_replay')
 return {'replay_verified':True,'native_deliveries':result['received_deliveries'],'known_controls':result['controls_total'],'real_llm_calls_in_replay':0,'writes_to_original_bundle':False,'scope':'public_synthetic_campaign_only'}

if __name__=='__main__':print(json.dumps(verify()))
