import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import json

def scrape_remoteok_ai_jobs(max_jobs=30):
    """
    Scrape AI jobs from RemoteOK - works reliably without JavaScript
    """
    jobs_data = []
    url = "https://remoteok.com/remote-ai-jobs"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    try:
        print(f"Scraping RemoteOK AI jobs...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # RemoteOK has job data in table rows
        job_rows = soup.find_all('tr', class_='job')

        print(f"  Found {len(job_rows)} job listings")

        for job in job_rows[:max_jobs]:
            try:
                # Try multiple approaches to extract data
                # Method 1: Using itemprop
                title_elem = job.find('h2', itemprop='title')
                if not title_elem:
                    # Method 2: Find any h2
                    title_elem = job.find('h2')
                if not title_elem:
                    # Method 3: Look in td with class
                    title_elem = job.find('td', class_='company_and_position')
                    if title_elem:
                        title_elem = title_elem.find('h2')

                title = title_elem.get_text(strip=True) if title_elem else None

                # Extract company
                company_elem = job.find('h3', itemprop='name')
                if not company_elem:
                    company_elem = job.find('h3', class_='company')
                if not company_elem:
                    company_elem = job.find('h3')
                company = company_elem.get_text(strip=True) if company_elem else 'N/A'

                # Extract link
                link_data = job.get('data-url')
                if not link_data:
                    link_elem = job.find('a', class_='preventLink')
                    link_data = link_elem.get('href') if link_elem else None
                link = f"https://remoteok.com{link_data}" if link_data else None

                # Extract location
                location = 'Remote'

                if title and len(title) > 3 and link:
                    jobs_data.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'link': link,
                        'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'RemoteOK'
                    })

            except Exception as e:
                continue

        print(f"Successfully parsed {len(jobs_data)} jobs from RemoteOK")

    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")

    return pd.DataFrame(jobs_data)

def scrape_weworkremotely_ai_jobs(max_jobs=20):
    """
    Scrape from WeWorkRemotely - Programming jobs section
    """
    jobs_data = []
    url = "https://weworkremotely.com/remote-jobs/search?term=ai+machine+learning"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"Scraping WeWorkRemotely...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find job listings
        job_listings = soup.find_all('li', class_='feature')

        print(f"  Found {len(job_listings)} job listings")

        for job in job_listings[:max_jobs]:
            try:
                # Get the link element
                link_elem = job.find('a', href=True)
                if not link_elem:
                    continue

                # Title is in span with title class
                title_elem = link_elem.find('span', class_='title')
                title = title_elem.get_text(strip=True) if title_elem else None

                # Company is in span with company class
                company_elem = link_elem.find('span', class_='company')
                company = company_elem.get_text(strip=True) if company_elem else 'N/A'

                # Link
                link = f"https://weworkremotely.com{link_elem['href']}"

                # Location/Region
                region_elem = link_elem.find('span', class_='region')
                location = region_elem.get_text(strip=True) if region_elem else 'Remote'

                if title and len(title) > 3:
                    jobs_data.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'link': link,
                        'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'WeWorkRemotely'
                    })

            except Exception as e:
                continue

        print(f"Successfully parsed {len(jobs_data)} jobs from WeWorkRemotely")

    except Exception as e:
        print(f"Error scraping WeWorkRemotely: {e}")

    return pd.DataFrame(jobs_data)

def scrape_himalayas_ai_jobs(max_jobs=25):
    """
    Scrape from Himalayas.app - excellent for remote AI/ML jobs
    """
    jobs_data = []
    url = "https://himalayas.app/jobs/ai-ml"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"Scraping Himalayas.app...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find job cards
        job_cards = soup.find_all('div', {'data-test': 'job-card'})
        if not job_cards:
            job_cards = soup.find_all('article')

        print(f"  Found {len(job_cards)} job listings")

        for job in job_cards[:max_jobs]:
            try:
                # Title
                title_elem = job.find('h3')
                if not title_elem:
                    title_elem = job.find('a')
                title = title_elem.get_text(strip=True) if title_elem else None

                # Company
                company_elem = job.find('span', {'data-test': 'job-card-company'})
                if not company_elem:
                    company_elem = job.find('div', class_=lambda x: x and 'company' in str(x).lower())
                company = company_elem.get_text(strip=True) if company_elem else 'N/A'

                # Link
                link_elem = job.find('a', href=True)
                link = None
                if link_elem:
                    href = link_elem['href']
                    link = f"https://himalayas.app{href}" if not href.startswith('http') else href

                # Location
                location = 'Remote'

                if title and len(title) > 3 and link:
                    jobs_data.append({
                        'title': title,
                        'company': company,
                        'location': location,
                        'link': link,
                        'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'Himalayas'
                    })

            except Exception as e:
                continue

        print(f"Successfully parsed {len(jobs_data)} jobs from Himalayas")

    except Exception as e:
        print(f"Error scraping Himalayas: {e}")

    return pd.DataFrame(jobs_data)

def scrape_arbeitnow_ai_jobs(max_jobs=30):
    """
    Scrape from Arbeitnow.com - has a nice API-like structure
    Filter for English-language AI/ML jobs
    """
    jobs_data = []
    url = "https://www.arbeitnow.com/api/job-board-api"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"Scraping Arbeitnow API...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        jobs = data.get('data', [])

        print(f"  Found {len(jobs)} job listings")

        # AI/ML keywords for filtering
        ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml engineer',
            'data scientist', 'deep learning', 'nlp', 'computer vision',
            'neural network', 'pytorch', 'tensorflow', 'llm', 'generative ai'
        ]

        for job in jobs:
            try:
                title = job.get('title', '')
                description = job.get('description', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()

                # Check if job is AI/ML related
                is_ai_job = any(keyword in title.lower() or keyword in description or keyword in tags
                               for keyword in ai_keywords)

                # Filter for English-speaking locations (US, UK, Remote, etc.)
                location = job.get('location', '')

                if is_ai_job and len(jobs_data) < max_jobs:
                    jobs_data.append({
                        'title': title,
                        'company': job.get('company_name', 'N/A'),
                        'location': location if location else 'Remote',
                        'link': job.get('url', 'N/A'),
                        'scraped_date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'Arbeitnow'
                    })

            except Exception as e:
                continue

        print(f"Successfully parsed {len(jobs_data)} AI/ML jobs from Arbeitnow")

    except Exception as e:
        print(f"Error scraping Arbeitnow: {e}")

    return pd.DataFrame(jobs_data)

def create_sample_data():
    """
    Fallback: Create sample data if scraping fails
    """
    print("📝 Creating sample data as fallback...")

    sample_jobs = [
        {
            'title': 'Senior AI Engineer',
            'company': 'OpenAI',
            'location': 'Remote',
            'link': 'https://openai.com/careers',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
        {
            'title': 'Machine Learning Engineer',
            'company': 'Google DeepMind',
            'location': 'London, UK',
            'link': 'https://www.deepmind.com/careers',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
        {
            'title': 'AI Research Scientist',
            'company': 'Meta AI',
            'location': 'Menlo Park, CA',
            'link': 'https://ai.facebook.com/join-us',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
        {
            'title': 'Data Scientist - ML',
            'company': 'Netflix',
            'location': 'Los Gatos, CA',
            'link': 'https://jobs.netflix.com',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
        {
            'title': 'NLP Engineer',
            'company': 'Anthropic',
            'location': 'San Francisco, CA',
            'link': 'https://anthropic.com/careers',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
        {
            'title': 'Computer Vision Engineer',
            'company': 'Tesla',
            'location': 'Palo Alto, CA',
            'link': 'https://tesla.com/careers',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
        {
            'title': 'ML Infrastructure Engineer',
            'company': 'Databricks',
            'location': 'Remote',
            'link': 'https://databricks.com/company/careers',
            'scraped_date': datetime.now().strftime('%Y-%m-%d'),
            'source': 'Sample'
        },
    ]

    return pd.DataFrame(sample_jobs)

def scrape_ai_jobs(max_pages=3):
    """
    Main scraper function that tries multiple sources
    Returns DataFrame with job listings
    """
    all_jobs = pd.DataFrame()

    print("\n" + "=" * 60)
    print("STARTING MULTI-SOURCE JOB SCRAPER")
    print("=" * 60 + "\n")

    # Try RemoteOK (most reliable)
    print("Source 1: RemoteOK")
    print("-" * 60)
    try:
        remoteok_jobs = scrape_remoteok_ai_jobs(max_jobs=25)
        if not remoteok_jobs.empty:
            all_jobs = pd.concat([all_jobs, remoteok_jobs], ignore_index=True)
            print(f"Added {len(remoteok_jobs)} jobs\n")
        else:
            print("No jobs found\n")
    except Exception as e:
        print(f"Failed: {e}\n")

    time.sleep(2)  # Be respectful

    # Try WeWorkRemotely
    print("Source 2: WeWorkRemotely")
    print("-" * 60)
    try:
        wwr_jobs = scrape_weworkremotely_ai_jobs(max_jobs=20)
        if not wwr_jobs.empty:
            all_jobs = pd.concat([all_jobs, wwr_jobs], ignore_index=True)
            print(f"Added {len(wwr_jobs)} jobs\n")
        else:
            print("No jobs found\n")
    except Exception as e:
        print(f"Failed: {e}\n")

    time.sleep(2)

    # Try Arbeitnow
    print("Source 3: Arbeitnow")
    print("-" * 60)
    try:
        arbeit_jobs = scrape_arbeitnow_ai_jobs(max_jobs=20)
        if not arbeit_jobs.empty:
            all_jobs = pd.concat([all_jobs, arbeit_jobs], ignore_index=True)
            print(f"Added {len(arbeit_jobs)} jobs\n")
        else:
            print("No jobs found\n")
    except Exception as e:
        print(f"Failed: {e}\n")

    time.sleep(2)

    # Try Himalayas
    print("Source 4: Himalayas")
    print("-" * 60)
    try:
        himalayas_jobs = scrape_himalayas_ai_jobs(max_jobs=25)
        if not himalayas_jobs.empty:
            all_jobs = pd.concat([all_jobs, himalayas_jobs], ignore_index=True)
            print(f"Added {len(himalayas_jobs)} jobs\n")
        else:
            print("No Jobs Found\n")
    except Exception as e:
        print(f"Failed: {e}\n")

    # If no jobs found from any source, use sample data
    if all_jobs.empty:
        print("No jobs scraped from any source!")
        print("Using sample data for demonstration...\n")
        all_jobs = create_sample_data()

    # Clean up data
    if not all_jobs.empty:
        # Remove duplicates
        all_jobs = all_jobs.drop_duplicates(subset=['title', 'company'], keep='first')
        all_jobs = all_jobs.reset_index(drop=True)

    return all_jobs

def filter_top_jobs(df, keywords=['AI Engineer', 'Machine Learning', 'Data Scientist'], top_n=5):
    """
    Filter and return top N jobs based on keywords
    """
    if df.empty:
        return df

    # Create case-insensitive regex pattern
    pattern = '|'.join(keywords)
    mask = df['title'].str.contains(pattern, case=False, na=False)
    filtered_df = df[mask]

    # If filtered results are too few, return all jobs up to top_n
    if len(filtered_df) < top_n:
        return df.head(top_n)

    return filtered_df.head(top_n)

# Test the scraper
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("JOB SCRAPER TEST")
    print("=" * 60)

    jobs_df = scrape_ai_jobs(max_pages=2)

    print("=" * 60)
    print(f"RESULTS: {len(jobs_df)} TOTAL JOBS FOUND")
    print("=" * 60 + "\n")

    if not jobs_df.empty:
        print("📊Sample Data (First 5 jobs):")
        print("-" * 60)
        print(jobs_df[['title', 'company', 'location', 'source']].head())

        print("\n" + "=" * 60)
        top_jobs = filter_top_jobs(
            jobs_df,
            keywords=['AI Engineer', 'ML Engineer', 'Machine Learning', 'Data Scientist'],
            top_n=5
        )
        print(f"TOP {len(top_jobs)} AI/ML ROLES:")
        print("=" * 60)
        for idx, job in top_jobs.iterrows():
            print(f"\n{idx + 1}. {job['title']}")
            print(f"    {job['company']}")
            print(f"    {job['location']}")
            print(f"    {job['link']}")
    else:
        print("No jobs found!")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Try running again (sites may be temporarily down)")
        print("3. The script will use sample data for testing if scraping fails")