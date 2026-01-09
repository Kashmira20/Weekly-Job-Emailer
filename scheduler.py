"""
Scheduler for Weekly Job Report Emailer
Runs the report generation at scheduled times
"""

import schedule
import time
from datetime import datetime
from main import generate_and_send_report
import config

def job():
    """Wrapper function for the scheduled job"""
    print(f"\n{'='*60}")
    print(f"SCHEDULED JOB TRIGGERED: {datetime.now()}")
    print(f"{'='*60}\n")
    
    try:
        generate_and_send_report()
    except Exception as e:
        print(f"Error running scheduled job: {e}")

def start_scheduler():
    """
    Start the scheduler to run weekly reports
    """
    # Schedule based on config
    day = config.SEND_DAY.lower()
    send_time = config.SEND_TIME
    
    # Map day names to schedule methods
    day_mapping = {
        'monday': schedule.every().monday,
        'tuesday': schedule.every().tuesday,
        'wednesday': schedule.every().wednesday,
        'thursday': schedule.every().thursday,
        'friday': schedule.every().friday,
        'saturday': schedule.every().saturday,
        'sunday': schedule.every().sunday,
    }
    
    if day not in day_mapping:
        print(f"Invalid day: {day}. Using Monday as default.")
        day = 'monday'
    
    # Schedule the job
    day_mapping[day].at(send_time).do(job)
    
    print("=" * 60)
    print("WEEKLY JOB REPORT SCHEDULER STARTED")
    print("=" * 60)
    print(f"Schedule: Every {day.capitalize()} at {send_time}")
    print(f"Recipients: {', '.join(config.RECIPIENT_EMAILS)}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the scheduler\n")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("SCHEDULER STOPPED")
        print("=" * 60)

if __name__ == "__main__":
    start_scheduler()