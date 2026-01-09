# 📧 WEEKLY JOB EMAILER

Automated job scraper that emails you the top AI/ML positions every Monday. Built with Python and GitHub Actions.

## What It Does

- Scrapes AI/ML jobs from multiple job boards
- Filters top 5 positions based on keywords
- Sends you a weekly email report every Monday


## Quick Setup

### 1. Get Gmail App Password

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Enable 2-Step Verification if not enabled
3. Generate password for "Mail"
4. Copy the 16-character password (remove spaces)

### 2. Add GitHub Secrets

Go to your repo: **Settings → Secrets → Actions → New secret**

Add these three:
- `SENDER_EMAIL` = your.email@gmail.com
- `SENDER_PASSWORD` = your-16-char-password
- `RECIPIENT_EMAIL` = your.email@gmail.com

### 3. That's It!
The workflow runs automatically every Monday at 9 AM UTC.
Want to test now? Go to **Actions → Weekly AI Jobs Report → Run workflow**

## What You'll Get

**Email every Monday with:**
- Total jobs found
- Top 5 AI/ML positions
- Company names & locations
- Direct apply links

**Example:**
```
Weekly AI Jobs Report
January 6, 2026

This Week: 20 jobs found

Top AI Engineering Roles:
1. Account Manager
Paymentology
Berlin
2.SEA Manager (All Genders) - Düsseldorf
Digitl GmbH
Hamburg
...

```

---

## Customize

Edit `cloud_config.py` to change:

**Job keywords:**
```python
JOB_SEARCH_KEYWORDS = [
    'AI Engineer',
    'Deep Learning',
    'Computer Vision',
]
```

**Number of jobs:**
```python
TOP_N_JOBS = 10  # Instead of 5
```

**Add more recipients:**
```python
RECIPIENT_EMAILS = [
    RECIPIENT_EMAIL,
    'friend@email.com',
    'colleague@example.com',
    'team@company.com',
]
# Everyone in this list will receive the weekly report
```

**Schedule:**

Edit `.github/workflows/weekly-report.yml`:
```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC (2:30 PM IST)
  # For Indian time: 9 AM IST = '30 3 * * 1'
  # Use https://crontab.guru/ for custom schedules
```

---

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
SENDER_EMAIL=your.email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=your.email@gmail.com

# Test
python cloud_main.py --test
```

---

## Files
```
├── cloud_main.py          # Main script - runs everything
├── job_scraper.py         # Scrapes jobs from RemoteOK & Arbeitnow
├── email_sender.py        # Creates & sends HTML/text emails
├── cloud_config.py        # Settings (keywords, recipients, schedule)
├── requirements.txt       # Python packages needed
├── .env                   # Local credentials (not in GitHub)
├── .gitignore            # Protects sensitive files
└── .github/workflows/
    └── weekly-report.yml  # GitHub Actions automation
```

**What each file does:**

- cloud_main.py - Entry point. Calls scraper → filters jobs → sends email
- job_scraper.py - Visits job sites, extracts listings, returns pandas DataFrame
- email_sender.py - Formats job data into beautiful HTML emails, sends via Gmail
- cloud_config.py - All your settings (keywords, email addresses, job count)
- weekly-report.yml - Tells GitHub Actions when to run (schedule) and what to do
- requirements.txt - List of libraries: requests, beautifulsoup4, pandas, etc.

---

## Common issue occur which can be solved by following ways: 
**Email not received?**
- Check spam folder
- Verify GitHub Secrets are correct
- Make sure App Password has no spaces

**Workflow failed?**
- Click on failed run in Actions
- Check error logs
- Usually: wrong credentials in Secrets

**No jobs found?**
- Normal! Some sources block scrapers like WeWorkRemotly
- Arbeitnow usually works (gets 20+ jobs)
- Sample data will be used as fallback

---

## Tech Stack

Python • BeautifulSoup • Pandas • Gmail SMTP • GitHub Actions

---
