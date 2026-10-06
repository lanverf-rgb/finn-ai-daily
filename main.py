import os
import datetime
from google import genai

key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=key)

today = datetime.datetime.now().strftime("%Y-%m-%d")

prompt = f"""You are FINN, AI Daily newsletter writer. Date: {today}.

Write a complete AI Daily newsletter in English:

# AI Daily - {today}

Start with 1 sentence intro about AI today.

Then 4 stories, each format:
## 1. [Headline]
**What happened:** 2 sentences, real news from last 24-48h
**Why it matters:** 1 sentence
**Source:** Name of real source

Then:
## Quick Hits
- 2 bullet points with small AI news

## Tool of the Day
- 1 useful AI tool

Keep concise, real."""

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=prompt
)

text = response.text

# Save files
with open("substack_today.md", "w", encoding="utf-8") as f:
    f.write(text)
with open("x_posts_today.md", "w", encoding="utf-8") as f:
    f.write(text[:2000])

print("Generated OK")

# Try to publish to Substack if secrets exist
sub_email = os.environ.get("SUBSTACK_EMAIL")
sub_pass = os.environ.get("SUBSTACK_PASSWORD")
sub_pub = os.environ.get("SUBSTACK_PUB_URL", "")

if sub_email and sub_pass:
    try:
        print(f"Attempting Substack publish to {sub_pub}...")
        from substack import Api
        
        # Clean pub url to get name
        pub_name = sub_pub.replace("https://", "").replace("http://", "").split(".")[0].split("/")[0]
        if "substack.com" in sub_pub:
            pub_name = sub_pub.split("://")[1].split(".")[0]
        
        print(f"Pub name: {pub_name}")
        
        api = Api(email=sub_email, password=sub_pass, publication_url=sub_pub)
        
        # Create draft
        title = f"AI Daily - {today}"
        # Convert markdown to simple HTML for Substack
        html_body = text.replace("\n", "<br>\n")
        
        draft = api.create_draft(
            title=title,
            subtitle="Your daily AI briefing",
            body_html=f"<p>{html_body}</p>",
            audience="everyone"
        )
        print(f"Draft created: {draft}")
        
        # Publish draft
        # api.publish_draft(draft['id'])  # Uncomment to auto-publish, keeping as draft for safety first
        
        print("SUCCESS - Draft created in Substack! Check your drafts.")
        
        # For now create draft only - safer. After you verify draft, we enable auto-publish
        
    except Exception as e:
        print(f"Substack publish failed (will still save files): {e}")
        import traceback
        traceback.print_exc()
else:
    print("No Substack secrets - skipping publish, files saved only")
