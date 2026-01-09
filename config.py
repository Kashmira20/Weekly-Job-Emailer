"""
Configuration file for Weekly Job Report Emailer

IMPORTANT: For Gmail, you MUST use an App Password, not your regular password
How to get Gmail App Password:
1. Go to your Google Account settings
2. Security > 2-Step Verification (must be enabled)
3. App passwords > Select app: Mail, Select device: Other
4. Copy the 16-character password
"""

import os

# Email Configuration
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'your.email@gmail.com')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD', 'your-app-password-here')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'recipient@example.com')

# Can send to multiple recipients
RECIPIENT_EMAILS = [
    RECIPIENT_EMAIL,
    # 'another.recipient@example.com',
]

# Scraping Configuration
MAX_PAGES_TO_SCRAPE = 3
JOB_SEARCH_KEYWORDS = [
    'AI Engineer',
    'Machine Learning Engineer',
    'ML Engineer',
    'Data Scientist',
    'AI Researcher'
]

TOP_N_JOBS = 5

# Email Configuration
EMAIL_SUBJECT = "Your Weekly AI Jobs Report"
SEND_HTML_EMAIL = True  # Set to False for plain text only

# Schedule Configuration (for use with scheduler)
SEND_DAY = 'monday'  # Day of week to send report
SEND_TIME = '09:00'  # Time to send (24-hour format)

# Data Storage
SAVE_DATA_TO_CSV = True
CSV_FILENAME = 'jobs_data_{date}.csv'  # {date} will be replaced with current date

# Alternative: Load from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', SENDER_EMAIL)
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', SENDER_PASSWORD)
    RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', RECIPIENT_EMAIL)
except ImportError:
    pass  # dotenv not installed, use default values