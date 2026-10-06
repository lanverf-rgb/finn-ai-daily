import os
import datetime
from google import genai

key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=key)
today = datetime.datetime.now().strftime("%Y-%m-%d")

prompt = f"""You are FINN, AI Daily newsletter writer for finnaidaily.substack.com. Date: {today}.

Write today's AI Daily in English, ready to paste into Substack.

Format EXACTLY like this:

# AI Daily - {today}

Good morning! Here are the 4 most important AI stories in the last 24h.

## 1. [Catchy Headline]
**What happened:** 2-3 sentences with real news from last 24-48h
**Why it matters:** 1 sentence impact
**Source:** Real source name

## 2. [Headline]
**What happened:** ...
**Why it matters:** ...
**Source:** ...

## 3. [Headline]
**What happened:** ...
**Why it matters:** ...
**Source:** ...

## 4. [Headline]
**What happened:** ...
**Why it matters:** ...
**Source:** ...

## Quick Hits
- Bullet 1 with quick AI news
- Bullet 2 with quick AI news

## Tool of the Day
**[Tool Name]** - 1 sentence what it does + why cool. Link if possible.

---
That's all for today! See you tomorrow.

Keep it concise, factual, no hype, real news only."""

resp = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
text = resp.text

# Save files
with open("substack_today.md", "w", encoding="utf-8") as f:
    f.write(text)

with open("x_posts_today.md", "w", encoding="utf-8") as f:
    f.write(text[:2000] + "\n\n#AI #ArtificialIntelligence")

print("="*50)
print(text)
print("="*50)
print("Files saved: substack_today.md + x_posts_today.md")
