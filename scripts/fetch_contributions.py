import json, re, requests
from bs4 import BeautifulSoup
from datetime import date

USERNAME='PiyushVpatil23'
url=f'https://github.com/users/{USERNAME}/contributions'
r=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=30)
r.raise_for_status()
soup=BeautifulSoup(r.text,'html.parser')
days=[]
for cell in soup.select('td.ContributionCalendar-day'):
    d=cell.get('data-date')
    level=int(cell.get('data-level','0'))
    count=0
    label=cell.get('aria-label','')
    m=re.search(r'([\d,]+) contribution',label)
    if m: count=int(m.group(1).replace(',',''))
    if d: days.append({'date':d,'count':count,'level':level})
if not days:
    for cell in soup.select('[data-date][data-level]'):
        d=cell.get('data-date'); level=int(cell.get('data-level','0'))
        if d: days.append({'date':d,'count':0,'level':level})
days=sorted({x['date']:(x) for x in days}.values(),key=lambda x:x['date'])
with open('data/contributions.json','w') as f: json.dump({'username':USERNAME,'updated':date.today().isoformat(),'days':days},f,indent=2)
print('Fetched',len(days),'days')
