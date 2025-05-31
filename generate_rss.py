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

# Extract Game Titles using grid caption or fallback
games = []
for card in soup.find_all("div", class_="dd-image-box-caption"):
    text = card.get_text(strip=True)
    if text and text not in games:
        games.append(text)

if not games:
    for game in soup.select("div[data-human-name]"):
        title = game["data-human-name"]
        if title and title not in games:
            games.append(title)

# Format RSS content
bundle_title = datetime.now().strftime("%B %Y") + " Humble Choice"
bundle_url = "https://www.humblebundle.com/membership"

# Build game list + optional "...and more!"
max_expected = 8
game_lines = [f"- {g}" for g in games]
if len(games) < max_expected:
    game_lines.append("...and more!")

bundle_description = (
    "🎮 **New Humble Choice Bundle is out!**\nIncludes:\n"
    + "\n".join(game_lines)
    + "\n\n🔗 https://www.humblebundle.com/membership"
)

# Hash for GUID and set date
bundle_hash = hashlib.md5(bundle_description.encode()).hexdigest()
pub_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# RSS layout
rss_template = """<?xml version=\"1.0\" encoding=\"UTF-8\" ?>
<rss version=\"2.0\">
<channel>
  <title>Humble Choice Monthly Feed</title>
  <link>{bundle_url}</link>
  <description>Automatically generated feed for Humble Choice bundles</description>
  <lastBuildDate>{pub_date}</lastBuildDate>
  <item>
    <title>{bundle_title}</title>
    <link>{bundle_url}</link>
    <guid isPermaLink=\"false\">{bundle_hash}</guid>
    <description><![CDATA[{bundle_description}]]></description>
    <pubDate>{pub_date}</pubDate>
  </item>
</channel>
</rss>"""

# Final formatted RSS string
rss = rss_template.format(
    bundle_url=bundle_url,
    pub_date=pub_date,
    bundle_title=bundle_title,
    bundle_description=bundle_description,
    bundle_hash=bundle_hash
)

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
