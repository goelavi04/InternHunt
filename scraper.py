import requests
from bs4 import BeautifulSoup
import time

# ── Internshala ──────────────────────────────────────
def scrape_internshala():
    url = "https://internshala.com/internships/ai-ml-internship,data-science-internship"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    results = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all("div", class_="individual_internship")
        for card in cards[:10]:
            # title
            title_tag = card.find("h3", class_="job-internship-name")
            title = title_tag.text.strip() if title_tag else "N/A"

            # company — try multiple possible class names
            company_tag = (card.find("h4", class_="company-name") or
                           card.find("p",  class_="company-name") or
                           card.find("a",  class_="company-name"))
            company = company_tag.text.strip() if company_tag else "N/A"

            # stipend
            stipend_tag = card.find("span", class_="stipend")
            stipend = stipend_tag.text.strip() if stipend_tag else "Not mentioned"

            # location
            loc_tag = (card.find("a", class_="location_link") or
                       card.find("p", class_="location_names"))
            location = loc_tag.text.strip() if loc_tag else "Remote"

            # individual URL
            link_tag = card.find("a", class_="view_detail_button")
            if not link_tag:
                link_tag = card.find("a", href=True)
            link = ("https://internshala.com" + link_tag["href"]
                    if link_tag else url)

            results.append({
                "platform": "Internshala",
                "title":    title,
                "company":  company,
                "stipend":  stipend,
                "location": location,
                "url":      link,
            })
    except Exception as e:
        print(f"Internshala error: {e}")
    return results

# ── WellFound (AngelList) ─────────────────────────────
def get_wellfound_link():
    # WellFound blocks scrapers — return direct search link for email
    return [{
        "platform": "WellFound",
        "title":    "Browse AI/ML & Data Science roles",
        "company":  "Multiple startups",
        "stipend":  "Varies",
        "location": "Remote / India",
        "url":      "https://wellfound.com/jobs?role=Data+Scientist&remote=true",
    }]

# ── LinkedIn ──────────────────────────────────────────
def get_linkedin_link():
    # LinkedIn blocks scrapers — return direct search link for email
    return [{
        "platform": "LinkedIn",
        "title":    "Browse AI/ML & Data Science internships",
        "company":  "Multiple companies",
        "stipend":  "Varies",
        "location": "Mumbai / Remote",
        "url":      "https://www.linkedin.com/jobs/search/?keywords=AI+ML+Data+Science+intern&location=India",
    }]

# ── Master function ───────────────────────────────────
def get_all_internships():
    print("Scraping Internshala...")
    internshala = scrape_internshala()
    time.sleep(2)
    print("Adding LinkedIn & WellFound links...")
    linkedin  = get_linkedin_link()
    wellfound = get_wellfound_link()
    all_listings = internshala + linkedin + wellfound
    print(f"Total found: {len(all_listings)} listings")
    return all_listings

# ── Test ──────────────────────────────────────────────
if __name__ == "__main__":
    listings = get_all_internships()
    for l in listings:
        print(f"\n[{l['platform']}] {l['title']} @ {l['company']}")
        print(f"  Stipend: {l['stipend']} | {l['location']}")
        print(f"  {l['url']}")