"""
Cloud-optimized main script for Weekly Job Report Emailer
Uses cloud_config.py for environment variable configuration
"""

import pandas as pd
from datetime import datetime
import sys
import os

# Import our modules
from job_scraper import scrape_ai_jobs, filter_top_jobs
from email_sender import create_html_email, create_plain_text_email, send_email

# Use cloud_config if available, fallback to regular config
try:
    import cloud_config as config
    print("Using cloud configuration")
except ImportError:
    import cloud_config as config
    print("Using local configuration")

def save_data(df, filename=None):
    """Save scraped data to CSV"""
    if not config.SAVE_DATA_TO_CSV:
        return
        
    if filename is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = config.CSV_FILENAME.format(date=date_str)
    
    try:
        df.to_csv(filename, index=False)
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"⚠️ Could not save CSV: {e}")

def generate_and_send_report():
    """
    Main function to scrape jobs, generate report, and send email
    """
    print("=" * 50)
    print("WEEKLY AI JOBS REPORT GENERATOR (CLOUD)")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Validate configuration
    if not config.SENDER_EMAIL or not config.SENDER_PASSWORD or not config.RECIPIENT_EMAIL:
        print("❌ Error: Email credentials not configured!")
        print("\nFor cloud deployment, set these environment variables:")
        print("  - SENDER_EMAIL")
        print("  - SENDER_PASSWORD")
        print("  - RECIPIENT_EMAIL")
        sys.exit(1)
    
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
    
    success_count = 0
    for recipient in config.RECIPIENT_EMAILS:
        if recipient:  # Skip None/empty recipients
            if send_email(
                config.SENDER_EMAIL,
                config.SENDER_PASSWORD,
                recipient,
                config.EMAIL_SUBJECT,
                html_body,
                text_body
            ):
                success_count += 1
    
    print(f"\n✅ Successfully sent {success_count}/{len([r for r in config.RECIPIENT_EMAILS if r])} emails")
    
    # Step 6: Summary
    print("\n" + "=" * 50)
    print("REPORT SUMMARY")
    print("=" * 50)
    print(f"Total jobs scraped: {len(jobs_df)}")
    print(f"Top jobs selected: {len(top_jobs)}")
    print(f"Emails sent: {success_count}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    return success_count > 0

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
    
    return send_email(
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
        success = test_email_only()
        sys.exit(0 if success else 1)
    else:
        success = generate_and_send_report()
        sys.exit(0 if success else 1)