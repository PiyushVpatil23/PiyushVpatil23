import json
import re
from collections import defaultdict
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = "PiyushVpatil23"
URL = f"https://github.com/users/{USERNAME}/contributions"

response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 GitHub-profile-art"}, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

days = []
for cell in soup.select("[data-date][data-level]"):
    day = cell.get("data-date")
    if not day:
        continue
    level = int(cell.get("data-level", "0"))
    label = cell.get("aria-label", "")
    count = 0
    match = re.search(r"([\d,]+) contribution", label)
    if match:
        count = int(match.group(1).replace(",", ""))
    else:
        tool_id = cell.get("id")
        if tool_id:
            tip = soup.select_one(f"tool-tip[for='{tool_id}']")
            if tip:
                match = re.search(r"([\d,]+) contribution", tip.get_text(" ", strip=True))
                if match:
                    count = int(match.group(1).replace(",", ""))
    days.append({"date": day, "count": count, "level": level})

days = sorted({item["date"]: item for item in days}.values(), key=lambda item: item["date"])
if not days:
    raise RuntimeError("No contribution cells found; GitHub markup may have changed.")

# Derived statistics.
active_dates = {datetime.fromisoformat(d["date"]).date() for d in days if d["count"] > 0}

def streak_ending_on(end):
    streak = 0
    cursor = end
    while cursor in active_dates:
        streak += 1
        cursor -= timedelta(days=1)
    return streak

today = date.today()
current_streak = streak_ending_on(today)
if current_streak == 0:
    current_streak = streak_ending_on(today - timedelta(days=1))

longest_streak = 0
running = 0
previous = None
for d in sorted(active_dates):
    running = running + 1 if previous and d == previous + timedelta(days=1) else 1
    longest_streak = max(longest_streak, running)
    previous = d

best = max(days, key=lambda item: item["count"])
monthly = defaultdict(int)
for item in days:
    monthly[item["date"][:7]] += item["count"]

payload = {
    "username": USERNAME,
    "updated": today.isoformat(),
    "total": sum(item["count"] for item in days),
    "current_streak": current_streak,
    "longest_streak": longest_streak,
    "best_day": best,
    "monthly_totals": dict(sorted(monthly.items())),
    "days": days,
}

with open("data/contributions.json", "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2)

print(f"Fetched {len(days)} days / {payload['total']} contributions")
