"""Generate the animated neofetch-style profile card. STATIC=1 disables animation."""
import os

static = os.getenv("STATIC") == "1"
rows = [
    ("Now", "Java Full-Stack Developer"),
    ("Stack", "Java · Spring Boot · REST · MySQL"),
    ("Web", "React · Vite · Node.js · Tailwind"),
    ("Tools", "Git · Docker · VS Code"),
    ("Builds", "FLOWVA OS · CampusFits"),
    ("Focus", "scalable full-stack systems"),
]
parts = []
for i, (key, value) in enumerate(rows):
    y = 94 + i * 28
    delay = 0 if static else 0.22 + i * 0.14
    cls = "row static" if static else "row"
    parts.append(f'<text class="{cls}" style="animation-delay:{delay:.2f}s" x="24" y="{y}"><tspan class="key">{key:&lt;6}</tspan><tspan>{value}</tspan></text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="500" height="286" viewBox="0 0 500 286">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#c9d1d9;font-size:14px}}
.title{{fill:#39d353;font-size:18px;font-weight:700}}.key{{fill:#58a6ff;font-weight:700}}
.row{{opacity:0;transform:translateY(6px);animation:show .36s ease forwards}}.static{{opacity:1;transform:none}}
@keyframes show{{to{{opacity:1;transform:translateY(0)}}}}
</style>
<rect x="1" y="1" width="498" height="284" rx="12" fill="#0d1117" stroke="#30363d"/>
<circle cx="20" cy="20" r="5" fill="#ff5f56"/><circle cx="38" cy="20" r="5" fill="#ffbd2e"/><circle cx="56" cy="20" r="5" fill="#27c93f"/>
<text class="title" x="24" y="60">PiyushVpatil23@github</text>
{''.join(parts)}
<text x="24" y="270" fill="#8b949e">$ ship --learn --repeat</text>
</svg>'''
open("info-card.svg", "w", encoding="utf-8").write(svg)
print("Wrote info-card.svg")
