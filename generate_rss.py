import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib

# Gist Config
GIST_ID = "ea3ae1c23827b0be1f94dbb1f824f98c"
GIST_FILENAME = "humble_choice_feed.xml"
GIST_TOKEN = os.environ["GIST_TOKEN"]

# Scrape Humble Choice Page
url = "https://www.humblebundle.com/membership"
res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(res.text, "html.parser")

# Extract Game Titles
games = []
for game in soup.select("div[data-human-name]"):
    title = game["data-human-name"]
    if title not in games:
        games.append(title)

# Format RSS content
bundle_title = datetime.now().strftime("%B %Y") + " Humble Choice"
bundle_url = "https://www.humblebundle.com/membership"
bundle_description = "🎮 **New Humble Choice Bundle is out!**\nIncludes:\n" + "\n".join(f"- {g}" for g in games[:12]) + f"\n\n🔗 {bundle_url}"
bundle_hash = hashlib.md5(bundle_description.encode()).hexdigest()
pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

rss = f"""{rss_template}"""

# Push to Gist
response = requests.patch(
    f"https://api.github.com/gists/{GIST_ID}",
    headers={"Authorization": f"token {GIST_TOKEN}"},
    json={"files": {GIST_FILENAME: {"content": rss}}}
)

if response.status_code == 200:
    print("✅ Gist updated successfully.")
else:
    print("❌ Failed to update Gist:", response.text)
