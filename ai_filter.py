import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def filter_relevant(listings):
    # Separate real listings from platform links
    platform_links = [l for l in listings if l["company"] in ("Multiple companies", "Multiple startups")]
    to_filter     = [l for l in listings if l not in platform_links]

    if not to_filter:
        return platform_links

    # Build prompt for Groq
    listings_text = "\n".join([
        f"{i+1}. {l['title']} at {l['company']}"
        for i, l in enumerate(to_filter)
    ])

    prompt = f"""You are a smart internship filter for an AI & Data Science student.

Here are internship listings scraped from job portals:
{listings_text}

Your job: return ONLY the numbers of listings that are relevant to:
- Artificial Intelligence
- Machine Learning
- Data Science
- Data Analytics
- Python development
- Business Analytics with data focus

Exclude: Content Writing, Social Media, Marketing, Sales, HR, Design, Lead Management.

Return ONLY a JSON array of relevant index numbers (1-based). Example: [1, 3, 5]
No explanation, just the JSON array."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw = response.choices[0].message.content.strip()
        # Clean up in case model adds extra text
        raw = raw[raw.find("["):raw.rfind("]")+1]
        indices = json.loads(raw)
        relevant = [to_filter[i-1] for i in indices if 1 <= i <= len(to_filter)]
        print(f"Groq kept {len(relevant)} relevant listings out of {len(to_filter)}")
        return relevant + platform_links

    except Exception as e:
        print(f"Groq filter error: {e}")
        # Fallback: return everything if Groq fails
        return listings


# ── Test ──────────────────────────────────────────────
if __name__ == "__main__":
    from scraper import get_all_internships
    all_listings = get_all_internships()
    print("\nSending to Groq for filtering...\n")
    filtered = filter_relevant(all_listings)
    print(f"\n✓ Final relevant listings ({len(filtered)}):\n")
    for l in filtered:
        print(f"  [{l['platform']}] {l['title']} @ {l['company']}")
        print(f"  Stipend: {l['stipend']} | {l['url']}\n")