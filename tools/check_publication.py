#!/usr/bin/env python3
"""Scan the actual Git index, never print matched secret values.
Heuristic defense in depth, not proof that every possible secret is recognizable.
"""
import argparse
import json
from pathlib import Path,PurePosixPath
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PREFIXES={'src','cases','tests','docs','methods','tools','runs','reports','.github'}
ROOT_FILES={'README.md','.gitignore','bench.py'}
EXTENSIONS={'.py','.json','.md','.txt','.html','.yml','.yaml','.csv'}
PATTERNS={
 'github_token':r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}',
 'service_token':r'(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}',
 'aws_access_id':r'AKIA[A-Z0-9]{16}',
 'private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
 'personal_path':r'/ho[m]e/[^\s"\x27]+|/Us[e]rs/[^\s"\x27]+|[A-Za-z]:\\Us[e]rs\\',
 'private_source_marker':r'(?i)(?:source_event_ids|raw_transcript|telegram_chat_id)\s*["\x27]?\s*:\s*["\x27\[]',
}

def inspect_file(name,blob,symlink=False):
 issues=[];p=PurePosixPath(name)
 if symlink:issues.append('symlink')
 if p.is_absolute() or '..' in p.parts or (len(p.parts)==1 and name not in ROOT_FILES) or (len(p.parts)>1 and p.parts[0] not in PREFIXES):issues.append('outside_allowlist')
 if p.name.startswith('.env') or p.suffix.lower() in {'.db','.sqlite','.sqlite3','.key','.pem','.log','.ogg','.wav','.mp4'}:issues.append('private_file_type')
 if name not in ROOT_FILES and p.suffix not in EXTENSIONS:issues.append('unsupported_type')
 if len(blob)>2_000_000:issues.append('oversized')
 try:text=blob.decode('utf-8')
 except UnicodeError:issues.append('binary_content');text=''
 for rule,pattern in PATTERNS.items():
  if re.search(pattern,text):issues.append(rule)
 return [{'file':name,'rule':rule} for rule in issues]

def scan_index(root=ROOT):
 names=subprocess.check_output(['git','ls-files','-z'],cwd=root).decode().split('\0')
 names=[n for n in names if n];issues=[]
 for name in names:
  mode=subprocess.check_output(['git','ls-files','--stage','--',name],cwd=root).decode().split()[0]
  blob=subprocess.check_output(['git','show',':'+name],cwd=root)
  issues.extend(inspect_file(name,blob,mode=='120000'))
 return {'safe':bool(names) and not issues,'files_scanned':len(names),'findings':issues,'scope':'actual_git_index','guarantee':'heuristic_allowlist_and_patterns_not_universal_secret_detection'}

def main():
 result=scan_index();print(json.dumps(result,ensure_ascii=False));return 0 if result['safe'] else 1
if __name__=='__main__':raise SystemExit(main())
