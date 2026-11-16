import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('check_publication',ROOT/'tools/check_publication.py')
scanner=importlib.util.module_from_spec(spec);spec.loader.exec_module(scanner)

class PrivacyTests(unittest.TestCase):
 def test_token_and_private_database_rejected_without_echoing_secret(self):
  token='gh'+'p_'+'a'*32
  issues=scanner.inspect_file('docs/example.md',token.encode())
  self.assertEqual('github_token',issues[0]['rule']);self.assertNotIn(token,json.dumps(issues))
  self.assertTrue(scanner.inspect_file('private/source.db',b'not permitted'))
 def test_personal_paths_and_symlinks_rejected(self):
  path='/'+'home'+'/'+'fictional-user'+'/data'
  self.assertTrue(scanner.inspect_file('docs/example.md',path.encode()))
  self.assertTrue(scanner.inspect_file('docs/example.md',b'generic',True))
 def test_synthetic_content_allowed(self):
  self.assertEqual([],scanner.inspect_file('cases/example.json',b'{"owner":"Pessoa-A"}'))
 def test_fine_grained_github_token_rejected_without_value(self):
  token='github'+'_pat_'+'z'*70
  issues=scanner.inspect_file('docs/example.md',token.encode())
  self.assertIn('github_token',[x['rule'] for x in issues])
  self.assertNotIn(token,json.dumps(issues))

if __name__=='__main__':unittest.main()
