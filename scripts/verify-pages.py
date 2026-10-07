#!/usr/bin/env python3
"""Compare the public page and all loader inputs to this checkout."""
import argparse, ast, concurrent.futures, datetime, hashlib, json, pathlib, re, urllib.request
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--commit',required=True)
 parser.add_argument('--report',default='reports/refinement-pages-verification-2026-10-07.json')
 args=parser.parse_args();base='https://hunghvt-cyber.github.io/CongchungVND/'
 match=re.search(r'const files = (\[[^;]+\]);',(ROOT/'app.js').read_text())
 files=['index.html','app.js']+['data/'+name for name in ast.literal_eval(match.group(1))]
 checked=datetime.datetime.now(datetime.timezone.utc).isoformat();nonce=checked.replace(':','')
 def check(path):
  row={'path':path,'url':base+path,'localSha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()}
  try:
   request=urllib.request.Request(base+path+'?verify='+nonce,headers={'Cache-Control':'no-cache'})
   with urllib.request.urlopen(request,timeout=25) as response:
    raw=response.read();row['httpStatus']=response.status
   row['servedSha256']=hashlib.sha256(raw).hexdigest();row['matches']=row['servedSha256']==row['localSha256']
   if path.endswith('.json'):
    questions=json.loads(raw);row['stored']=len(questions)
    row['active']=sum(q['status'] in ('active','verified') for q in questions)
  except Exception as error:row.update(matches=False,error=str(error))
  return row
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(check,files))
 report={'checkedAt':checked,'commit':args.commit,'files':rows,'allMatch':all(row['matches'] for row in rows),
  'servedBankStored':sum(row.get('stored',0) for row in rows),'servedBankActive':sum(row.get('active',0) for row in rows),
  'uiVerification':'HTTP và Node DOM giả lập; chưa xác nhận thao tác trình duyệt thật.'}
 (ROOT/args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['allMatch','servedBankStored','servedBankActive']}))
 if not report['allMatch']:
  print(json.dumps([row for row in rows if not row['matches']],ensure_ascii=False));raise SystemExit(1)
if __name__=='__main__':main()
