import os
import datetime
from google import genai
from substack import Api

# Gemini
key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=key)
today = datetime.datetime.now().strftime("%Y-%m-%d")

prompt = f"""You are FINN, AI Daily newsletter writer. Date: {today}.

Write AI Daily in English, format:

# AI Daily - {today}

Intro: 1 sentence.

## 1. [Headline]
**What happened:** 2 sentences real news last 24-48h
**Why it matters:** 1 sentence
**Source:** Real source

(Repeat for 4 stories)

## Quick Hits
- 2 bullets

## Tool of the Day
- 1 tool

Keep concise, real news."""

resp = client.models.generate_content(model="gemini-flash-lite-latest", contents=prompt)
text = resp.text

with open("substack_today.md", "w", encoding="utf-8") as f:
    f.write(text)
with open("x_posts_today.md", "w", encoding="utf-8") as f:
    f.write(text[:2000])

print("Generated")

# Substack publish
email = os.environ.get("SUBSTACK_EMAIL")
pwd = os.environ.get("SUBSTACK_PASSWORD")
pub_url = os.environ.get("SUBSTACK_PUB_URL", "https://finnaidaily.substack.com")

if email and pwd:
    try:
        print(f"Publishing to {pub_url} as {email}")
        api = Api(email=email, password=pwd, publication_url=pub_url)
        
        draft_data = {
            "title": f"AI Daily - {today}",
            "subtitle": f"Your AI briefing for {today}",
            "body": text,  # markdown supported
            "audience": "everyone"
        }
        
        draft = api.post_draft(draft_data)
        print(f"DRAFT CREATED: {draft}")
        print(f"Draft ID: {draft.get('id')}")
        print("Check https://finnaidaily.substack.com/publish/drafts")
        
        # Auto-publish - uncomment next 2 lines when you want auto-publish
        # print("Publishing...")
        # api.publish_draft(draft['id'])
        # print("PUBLISHED!")
        
    except Exception as e:
        print(f"Substack error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Missing Substack secrets")
