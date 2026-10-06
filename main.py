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
**Source:** Name of real source (The Verge, TechCrunch, etc.)

Then:
## Quick Hits
- 2 bullet points with small AI news

## Tool of the Day
- 1 useful AI tool

Keep it concise, real, no hallucinations. Use your knowledge of recent AI news."""

response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=prompt
)

text = response.text

# Save files
with open("substack_today.md", "w", encoding="utf-8") as f:
    f.write(text)

with open("x_posts_today.md", "w", encoding="utf-8") as f:
    f.write(f"Posts for {today}:\n\n")
    # Simple split into posts
    f.write(text[:2000])

print(f"SUCCESS - {today}")
print(text[:800])
