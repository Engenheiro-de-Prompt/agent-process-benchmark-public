import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]

class PublicReleaseTests(unittest.TestCase):
 def test_public_bundle_replays_without_private_discovery_or_local_runtime(self):
  self.assertFalse((ROOT/'reports/discovery-aggregate.json').exists())
  self.assertFalse((ROOT/'tools/discover_local.py').exists())
  self.assertFalse((ROOT/'runs/campaign-002').exists())
  p=subprocess.run([sys.executable,'tools/verify_release.py'],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
  self.assertEqual(0,p.returncode,'public replay failed')
  data=json.loads(p.stdout)
  self.assertTrue(data['replay_verified']);self.assertEqual(48,data['native_deliveries'])
  self.assertEqual(109,data['known_controls']);self.assertEqual(0,data['real_llm_calls_in_replay'])
  self.assertFalse(data['writes_to_original_bundle'])

if __name__=='__main__':unittest.main()
