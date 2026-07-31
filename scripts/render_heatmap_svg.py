import html
import json
from datetime import datetime

with open("data/contributions.json", encoding="utf-8") as handle:
    data = json.load(handle)

days = data["days"][-371:]
W, H = 860, 205
SIZE, GAP = 11, 4
OX, OY = 48, 42
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

# Align columns by calendar week instead of raw list position.
first = datetime.fromisoformat(days[0]["date"]).date()
first_sunday = first
while first_sunday.weekday() != 6:
    first_sunday = first_sunday.replace(day=first_sunday.day)  # keep type stable
    from datetime import timedelta
    first_sunday -= timedelta(days=1)

rects = []
for item in days:
    dt = datetime.fromisoformat(item["date"]).date()
    delta = (dt - first_sunday).days
    col, row = divmod(delta, 7)
    # Python weekday: Mon=0; GitHub calendar: Sun=0.
    row = (dt.weekday() + 1) % 7
    x = OX + col * (SIZE + GAP)
    y = OY + row * (SIZE + GAP)
    level = max(0, min(5, int(item.get("level", 0))))
    # Give the highest native GitHub level a brighter neon endpoint.
    if level == 4 and item.get("count", 0) > 0:
        level = 5
    delay = (col + row) * 0.016
    title = html.escape(f"{item['date']}: {item.get('count', 0)} contributions")
    rects.append(
        f'<rect class="day" style="animation-delay:{delay:.3f}s" x="{x}" y="{y}" '
        f'width="{SIZE}" height="{SIZE}" rx="2" fill="{PALETTE[level]}"><title>{title}</title></rect>'
    )

legend = "".join(
    f'<rect x="{702 + i * 16}" y="178" width="11" height="11" rx="2" fill="{color}"/>'
    for i, color in enumerate(PALETTE)
)

best = data.get("best_day", {"date": "—", "count": 0})
footer = (
    f"{data.get('total', 0):,} contributions  ·  current {data.get('current_streak', 0)}d  ·  "
    f"longest {data.get('longest_streak', 0)}d  ·  best {best.get('count', 0)}"
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8b949e;font-size:12px}}
.title{{fill:#c9d1d9;font-size:13px}}
.day{{opacity:0;transform:translateY(-8px);animation:reveal .36s cubic-bezier(.2,.8,.2,1) forwards}}
@keyframes reveal{{to{{opacity:1;transform:translateY(0)}}}}
</style>
<rect x="1" y="1" width="858" height="203" rx="12" fill="#0d1117" stroke="#30363d"/>
<text class="title" x="24" y="25">PiyushVpatil23@github ~ $ contributions --year</text>
{''.join(rects)}
<text x="24" y="187">{html.escape(footer)}</text>
<text x="663" y="187">Less</text>{legend}<text x="804" y="187">More</text>
</svg>'''

with open("contrib-heatmap.svg", "w", encoding="utf-8") as handle:
    handle.write(svg)
