# InternHunt — Automated Internship Digest Agent

An AI-powered agent that scrapes internship platforms daily, filters
relevant AI/ML and Data Science roles using an LLM, and delivers a
formatted HTML digest to your inbox every day automatically.

Built by [Aviral Goel](https://linkedin.com/in/aviral-goel04)

---

## Features

- Scrapes Internshala daily for fresh internship listings
- Uses Groq (Llama 3.3) to intelligently filter out irrelevant roles
- Sends a clean HTML email digest via Gmail SMTP
- Runs automatically every day via Windows Task Scheduler
- Includes direct browse links for LinkedIn and WellFound

---

## Tech Stack

| Component        | Technology                        |
|------------------|-----------------------------------|
| Scraping         | Python, Requests, BeautifulSoup4  |
| AI Filtering     | Groq API (Llama 3.3 70B)          |
| Email Delivery   | Gmail SMTP, Python smtplib        |
| Scheduling       | Windows Task Scheduler            |
| Config           | python-dotenv                     |

---

## Project Structure

```
InternHunt/
├── scraper.py       # Scrapes Internshala for internship listings
├── ai_filter.py     # Filters listings using Groq LLM
├── emailer.py       # Builds HTML email and sends via Gmail
├── main.py          # Entry point — runs the full pipeline
├── .env             # API keys and credentials (not committed)
└── requirements.txt # Python dependencies
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/goelavi04/InternHunt.git
cd InternHunt
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key
GMAIL_SENDER=your_email@gmail.com
GMAIL_PASSWORD=your_gmail_app_password
RECIPIENT_EMAIL=your_email@gmail.com
```

Get your Groq API key free at: https://console.groq.com
Get a Gmail App Password at: https://myaccount.google.com/apppasswords

### 5. Run manually
```bash
python main.py
```

### 6. Schedule daily at 12 PM (Windows)
```bash
schtasks /create /tn "InternHunt" /tr "C:\InternHunt\venv\Scripts\python.exe C:\InternHunt\main.py" /sc daily /st 12:00
```

---

## How It Works

```
main.py
  │
  ├── scraper.py
  │     └── Scrapes Internshala → returns list of listings
  │
  ├── ai_filter.py
  │     └── Sends listings to Groq LLM → keeps only AI/ML/DS roles
  │
  └── emailer.py
        └── Builds HTML email → sends via Gmail SMTP
```

---

## Sample Email Output

Each morning you receive a digest like this:

- Role title and company name
- Stipend range
- Location (Remote / City)
- Direct apply link button
- Browse links for LinkedIn and WellFound

---

## Future Improvements

- [ ] Add Unstop scraping (currently JS-rendered, needs Selenium)
- [ ] Track seen listings to avoid duplicates across days
- [ ] Add Telegram bot notification as alternative to email
- [ ] Deploy to a cloud server so it runs even when laptop is off

---

## License

MIT License — free to use and modify.