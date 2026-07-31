import json, html
from datetime import datetime
D=json.load(open('data/contributions.json'))
days=D['days'][-371:]
W,H=860,170; size=11; gap=4; ox=48; oy=36
pal=['#161b22','#0e4429','#006d32','#26a641','#39d353']
rects=[]
for i,d in enumerate(days):
    dt=datetime.fromisoformat(d['date']); col=i//7; row=dt.weekday()
    x=ox+col*(size+gap); y=oy+row*(size+gap); lvl=max(0,min(4,int(d.get('level',0))))
    delay=(col+row)*.018
    rects.append(f'<rect class="d" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" width="{size}" height="{size}" rx="2" fill="{pal[lvl]}"><title>{html.escape(d["date"])}: {d.get("count",0)} contributions</title></rect>')
total=sum(x.get('count',0) for x in days)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e;font-size:12px}}.d{{opacity:0;transform:translateY(8px);animation:in .32s ease forwards}}@keyframes in{{to{{opacity:1;transform:translateY(0)}}}}</style><rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/><text x="24" y="24">PiyushVpatil23 / contributions</text>{''.join(rects)}<text x="24" y="154">{total:,} contributions · refreshed {D['updated']}</text><text x="690" y="154">Less  ▪ ▪ ▪ ▪ ▪  More</text></svg>'''
open('contrib-heatmap.svg','w').write(svg)
