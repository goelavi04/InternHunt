from scraper import get_all_internships
from ai_filter import filter_relevant
from emailer import send_email
from datetime import datetime

print(f"InternHunt starting — {datetime.now().strftime('%d %b %Y %H:%M')}")
listings = get_all_internships()
filtered = filter_relevant(listings)
send_email(filtered)
print("Done!")
