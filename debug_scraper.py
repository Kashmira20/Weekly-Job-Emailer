import requests
from bs4 import BeautifulSoup

def debug_website_structure(url):
    """
    Debug helper to inspect the actual HTML structure of a website
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"Fetching: {url}")
    print("=" * 60)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save HTML to file for inspection
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(soup.prettify())
        print("HTML saved to 'debug_page.html'\n")
        
        # Find all common job-related elements
        print("ANALYZING PAGE STRUCTURE:")
        print("-" * 60)
        
        # Check for common patterns
        patterns = [
            ('div', 'job'),
            ('article', None),
            ('li', 'job'),
            ('div', 'card'),
            ('div', 'listing'),
            ('a', 'job'),
        ]
        
        for tag, class_pattern in patterns:
            if class_pattern:
                elements = soup.find_all(tag, class_=lambda x: x and class_pattern in x.lower() if x else False)
            else:
                elements = soup.find_all(tag)
            
            if elements and len(elements) > 0:
                print(f"\nFound {len(elements)} <{tag}> elements" + (f" with '{class_pattern}' in class" if class_pattern else ""))
                
                # Show first element structure
                first = elements[0]
                print(f"   Classes: {first.get('class', 'No class')}")
                print(f"   Sample text: {first.get_text(strip=True)[:100]}...")
                
                # Look for links
                links = first.find_all('a')
                if links:
                    print(f"   Contains {len(links)} links")
                    print(f"   First link: {links[0].get('href', 'No href')}")
        
        print("\n" + "=" * 60)
        print("COMMON CLASS NAMES FOUND:")
        print("-" * 60)
        
        # Find all unique class names
        all_classes = set()
        for element in soup.find_all(class_=True):
            classes = element.get('class', [])
            if isinstance(classes, list):
                all_classes.update(classes)
        
        # Filter for job-related classes
        job_related = [c for c in all_classes if any(keyword in c.lower() 
                      for keyword in ['job', 'position', 'listing', 'card', 'item', 'post'])]
        
        for cls in sorted(job_related)[:20]:  # Show first 20
            print(f"   .{cls}")
        
        if not job_related:
            print("No obvious job-related classes found")
            print("Showing all classes (first 30):")
            for cls in sorted(all_classes)[:30]:
                print(f"   .{cls}")
        
    except Exception as e:
        print(f"Error: {e}")

# Test different job sites
if __name__ == "__main__":
    print("JOB SITE STRUCTURE DEBUGGER")
    print("=" * 60)
    
    # List of sites to try
    sites_to_test = [
        "https://ai-jobs.net/",
        "https://www.aimljobs.fyi/",
        "https://aijobs.app/",
    ]
    
    print("\nWhich site do you want to debug?")
    for i, site in enumerate(sites_to_test, 1):
        print(f"{i}. {site}")
    print(f"{len(sites_to_test) + 1}. Enter custom URL")
    
    choice = input("\nEnter number (or press Enter for default): ").strip()
    
    if choice == '' or choice == '1':
        url = sites_to_test[0]
    elif choice.isdigit() and 1 <= int(choice) <= len(sites_to_test):
        url = sites_to_test[int(choice) - 1]
    elif choice == str(len(sites_to_test) + 1):
        url = input("Enter URL: ").strip()
    else:
        url = sites_to_test[0]
    
    print()
    debug_website_structure(url)