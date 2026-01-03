
import os

# Email Configuration - Load from environment variables
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL')

# Validate that credentials are set
if not SENDER_EMAIL or not SENDER_PASSWORD or not RECIPIENT_EMAIL:
    print("Email credentials not set in environment variables!")
    print("Please set: SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL")

# Can send to multiple recipients
RECIPIENT_EMAILS = [
    RECIPIENT_EMAIL,
    # Add more recipients as needed
]

# Scraping Configuration
MAX_PAGES_TO_SCRAPE = 3
JOB_SEARCH_KEYWORDS = [
    'AI Engineer',
    'Machine Learning Engineer',
    'ML Engineer',
    'Data Scientist',
    'AI Researcher',
    'Deep Learning',
    'NLP Engineer'
]

TOP_N_JOBS = 5

# Email Configuration
EMAIL_SUBJECT = "Your Weekly AI Jobs Report"
SEND_HTML_EMAIL = True

# Schedule Configuration
SEND_DAY = 'monday'
SEND_TIME = '09:00'

# Data Storage
SAVE_DATA_TO_CSV = True
CSV_FILENAME = 'jobs_data_{date}.csv'

# Cloud-specific settings
IS_CLOUD_DEPLOYMENT = os.environ.get('CLOUD_DEPLOYMENT', 'false').lower() == 'true'

print("Cloud configuration loaded")
if SENDER_EMAIL:
    print(f"   Sender: {SENDER_EMAIL}")
if RECIPIENT_EMAIL:
    print(f"   Recipient: {RECIPIENT_EMAIL}")