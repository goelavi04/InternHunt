import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
from dotenv import load_dotenv

load_dotenv()

def build_email_html(listings):
    today = date.today().strftime("%d %b %Y")
    count = len([l for l in listings if l["company"] not in ("Multiple companies", "Multiple startups")])

    cards_html = ""
    for l in listings:
        is_link = l["company"] in ("Multiple companies", "Multiple startups")
        badge_color = "#E1F5EE" if not is_link else "#E6F1FB"
        badge_text  = "#085041" if not is_link else "#0C447C"
        btn_label   = "Apply Now" if not is_link else "Browse Roles"

        cards_html += f"""
        <div style="background:#fff;border:1px solid #e5e7eb;border-radius:10px;
                    padding:18px 20px;margin-bottom:14px;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;">
            <div>
              <span style="background:{badge_color};color:{badge_text};font-size:11px;
                           font-weight:600;padding:3px 10px;border-radius:20px;">
                {l['platform']}
              </span>
              <h3 style="margin:8px 0 4px;font-size:16px;color:#111827;">{l['title']}</h3>
              <p style="margin:0;font-size:13px;color:#6b7280;">{l['company']}</p>
            </div>
          </div>
          <div style="margin-top:12px;display:flex;gap:16px;flex-wrap:wrap;">
            <span style="font-size:13px;color:#374151;">
              <b>Stipend:</b> {l['stipend']}
            </span>
            <span style="font-size:13px;color:#374151;">
              <b>Location:</b> {l['location']}
            </span>
          </div>
          <a href="{l['url']}"
             style="display:inline-block;margin-top:14px;padding:8px 20px;
                    background:#1a56a0;color:#fff;text-decoration:none;
                    border-radius:6px;font-size:13px;font-weight:600;">
            {btn_label} →
          </a>
        </div>"""

    html = f"""
    <!DOCTYPE html>
    <html><body style="font-family:Arial,sans-serif;background:#f3f4f6;margin:0;padding:20px;">
      <div style="max-width:600px;margin:0 auto;">

        <div style="background:#1a56a0;border-radius:12px;padding:24px 28px;margin-bottom:20px;">
          <h1 style="color:#fff;margin:0;font-size:22px;">InternHunt Daily Digest</h1>
          <p style="color:#bfdbfe;margin:6px 0 0;font-size:14px;">
            {today} — {count} AI/ML & Data Science internship(s) found
          </p>
        </div>

        {cards_html}

        <p style="text-align:center;font-size:12px;color:#9ca3af;margin-top:20px;">
          InternHunt Agent • Built by Aviral Goel • Runs daily at 8 AM
        </p>
      </div>
    </body></html>"""
    return html


def send_email(listings):
    sender   = os.getenv("GMAIL_SENDER")
    password = os.getenv("GMAIL_PASSWORD")
    recipient = os.getenv("RECIPIENT_EMAIL")
    today    = date.today().strftime("%d %b %Y")
    count    = len([l for l in listings if l["company"] not in ("Multiple companies", "Multiple startups")])

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"InternHunt {today} — {count} new AI/ML listings"
    msg["From"]    = sender
    msg["To"]      = recipient

    html = build_email_html(listings)
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


# ── Test ──────────────────────────────────────────────
if __name__ == "__main__":
    from scraper import get_all_internships
    from ai_filter import filter_relevant
    listings  = get_all_internships()
    filtered  = filter_relevant(listings)
    send_email(filtered)