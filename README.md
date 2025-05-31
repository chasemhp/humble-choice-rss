# Humble Choice RSS Feed

This repository automatically scrapes the current Humble Choice bundle and updates a GitHub Gist with a formatted RSS feed once per month (on the first Tuesday).

## Setup Instructions

1. Add your Gist ID and filename in `generate_rss.py`
2. Create a GitHub secret in this repo:
   - **Name**: `GIST_TOKEN`
   - **Value**: A GitHub token with Gist access
3. Deploy. The Action will run on the first Tuesday of each month or manually.

Feed is compatible with MonitoRSS.
