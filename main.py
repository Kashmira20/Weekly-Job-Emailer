"""
Main application for Weekly Job Report Emailer
"""

import pandas as pd
from datetime import datetime
import sys

# Import our modules
from job_scraper import scrape_ai_jobs, filter_top_jobs
from email_sender import create_html_email, create_plain_text_email, send_email
import config

def save_data(df, filename=None):
    """Save scraped data to CSV"""
    if filename is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = config.CSV_FILENAME.format(date=date_str)
    
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

def generate_and_send_report():
    """
    Main function to scrape jobs, generate report, and send email
    """
    print("=" * 50)
    print("WEEKLY AI JOBS REPORT GENERATOR")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Scrape jobs
    print("Step 1: Scraping job listings...")
    try:
        jobs_df = scrape_ai_jobs(max_pages=config.MAX_PAGES_TO_SCRAPE)
        print(f"✅ Successfully scraped {len(jobs_df)} jobs\n")
    except Exception as e:
        print(f"❌ Error scraping jobs: {e}")
        sys.exit(1)
    
    if jobs_df.empty:
        print("⚠️ No jobs found. Exiting.")
        sys.exit(0)
    
    # Step 2: Filter and analyze
    print("Step 2: Filtering top jobs...")
    top_jobs = filter_top_jobs(
        jobs_df, 
        keywords=config.JOB_SEARCH_KEYWORDS,
        top_n=config.TOP_N_JOBS
    )
    print(f"✅ Found {len(top_jobs)} top jobs matching criteria\n")
    
    # Step 3: Save data (optional)
    if config.SAVE_DATA_TO_CSV:
        print("Step 3: Saving data to CSV...")
        save_data(jobs_df)
        print()
    
    # Step 4: Generate email content
    print("Step 4: Generating email content...")
    html_body = create_html_email(jobs_df, top_jobs)
    text_body = create_plain_text_email(jobs_df, top_jobs)
    print("✅ Email content generated\n")
    
    # Step 5: Send email
    print("Step 5: Sending email report...")
    
    # Validate configuration
    if config.SENDER_EMAIL == 'your.email@gmail.com' or config.SENDER_PASSWORD == 'your-app-password-here':
        print("❌ Error: Please configure your email credentials in config.py")
        print("\nTo set up Gmail App Password:")
        print("1. Go to Google Account settings")
        print("2. Security > 2-Step Verification")
        print("3. App passwords > Select Mail and your device")
        print("4. Copy the password to config.py")
        sys.exit(1)
    
    success_count = 0
    for recipient in config.RECIPIENT_EMAILS:
        if send_email(
            config.SENDER_EMAIL,
            config.SENDER_PASSWORD,
            recipient,
            config.EMAIL_SUBJECT,
            html_body,
            text_body
        ):
            success_count += 1
    
    print(f"\n✅ Successfully sent {success_count}/{len(config.RECIPIENT_EMAILS)} emails")
    
    # Step 6: Summary
    print("\n" + "=" * 50)
    print("REPORT SUMMARY")
    print("=" * 50)
    print(f"Total jobs scraped: {len(jobs_df)}")
    print(f"Top jobs selected: {len(top_jobs)}")
    print(f"Emails sent: {success_count}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

def test_email_only():
    """
    Test function to send a test email with sample data
    """
    print("Testing email functionality with sample data...\n")
    
    sample_jobs = pd.DataFrame({
        'title': ['AI Engineer', 'ML Engineer', 'Data Scientist'],
        'company': ['Tech Corp', 'AI Startup', 'Big Data Inc'],
        'location': ['Remote', 'San Francisco', 'New York'],
        'link': ['https://example.com/job1', 'https://example.com/job2', 'https://example.com/job3'],
        'scraped_date': [datetime.now().strftime('%Y-%m-%d')] * 3
    })
    
    html_body = create_html_email(sample_jobs, sample_jobs)
    text_body = create_plain_text_email(sample_jobs, sample_jobs)
    
    send_email(
        config.SENDER_EMAIL,
        config.SENDER_PASSWORD,
        config.RECIPIENT_EMAIL,
        "TEST: " + config.EMAIL_SUBJECT,
        html_body,
        text_body
    )

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_email_only()
    else:
        generate_and_send_report()