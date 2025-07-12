#!/usr/bin/env python3
"""
Business Data Collector - Personal Use
Ethical business data collection using legitimate APIs and sources
"""

import requests
import csv
import json
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
import os
from urllib.parse import quote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('business_collector.log'),
        logging.StreamHandler()
    ]
)

class BusinessDataCollector:
    """Ethical business data collection using legitimate sources"""
    
    def __init__(self, google_api_key: Optional[str] = None):
        self.google_api_key = google_api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BusinessDataCollector/1.0 (Personal Use)',
            'Accept': 'application/json, text/plain, */*',
        })
        
        # Rate limiting
        self.request_delay = 1  # seconds between requests
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Implement respectful rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def get_google_businesses(self, query: str, location: str, radius: int = 5000, max_results: int = 20) -> List[Dict]:
        """Get businesses using Google Places API"""
        if not self.google_api_key:
            logging.warning("Google API key not provided. Skipping Google Places search.")
            return []
        
        self._rate_limit()
        
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
            search_query = f"{query} in {location}"
            
            params = {
                "query": search_query,
                "radius": radius,
                "key": self.google_api_key,
                "type": "establishment"
            }
            
            logging.info(f"Searching Google Places for: {search_query}")
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            businesses = []
            for place in data.get("results", [])[:max_results]:
                business = {
                    "name": place.get("name", ""),
                    "address": place.get("formatted_address", ""),
                    "phone": place.get("formatted_phone_number", ""),
                    "website": place.get("website", ""),
                    "business_status": place.get("business_status", ""),
                    "types": ", ".join(place.get("types", [])),
                    "place_id": place.get("place_id", ""),
                    "rating": place.get("rating", ""),
                    "user_ratings_total": place.get("user_ratings_total", ""),
                    "price_level": place.get("price_level", ""),
                    "source": "Google Places API",
                    "collected_date": datetime.now().isoformat()
                }
                businesses.append(business)
            
            logging.info(f"Found {len(businesses)} businesses via Google Places API")
            return businesses
            
        except Exception as e:
            logging.error(f"Google Places API error: {e}")
            return []

    def get_yellow_pages_businesses(self, location: str, category: str, max_results: int = 10) -> List[Dict]:
        """Get businesses from Yellow Pages (ethical scraping)"""
        self._rate_limit()
        
        try:
            # Format location for URL
            location_formatted = location.replace(' ', '-').replace(',', '').lower()
            url = f"https://www.yellowpages.com/{location_formatted}/{category}"
            
            logging.info(f"Searching Yellow Pages: {url}")
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find business listings
                businesses = soup.find_all('div', class_='result')
                logging.info(f"Found {len(businesses)} businesses on Yellow Pages")
                
                business_data = []
                for business in businesses[:max_results]:
                    try:
                        # Extract business name
                        name_elem = business.find('a', class_='business-name')
                        name = name_elem.text.strip() if name_elem else "N/A"
                        
                        # Extract phone number
                        phone_elem = business.find('div', class_='phones')
                        phone = phone_elem.text.strip() if phone_elem else "N/A"
                        
                        # Extract address
                        address_elem = business.find('div', class_='street-address')
                        address = address_elem.text.strip() if address_elem else "N/A"
                        
                        # Check for website
                        website_elem = business.find('a', class_='track-visit-website')
                        website = website_elem.get('href', '') if website_elem else ""
                        
                        business_info = {
                            "name": name,
                            "phone": phone,
                            "address": address,
                            "website": website,
                            "business_status": "OPERATIONAL",
                            "types": category,
                            "place_id": "",
                            "rating": "",
                            "user_ratings_total": "",
                            "price_level": "",
                            "source": "Yellow Pages",
                            "collected_date": datetime.now().isoformat()
                        }
                        
                        business_data.append(business_info)
                        
                    except Exception as e:
                        logging.warning(f"Error parsing business: {e}")
                        continue
                
                return business_data
            else:
                logging.warning(f"Yellow Pages returned status code: {response.status_code}")
                return []
                
        except Exception as e:
            logging.error(f"Yellow Pages error: {e}")
            return []

    def enrich_business_data(self, business: Dict) -> Dict:
        """Enrich business data with additional information"""
        if not business.get("website"):
            return business
        
        self._rate_limit()
        
        try:
            # Try to get additional info from company website
            response = self.session.get(business["website"], timeout=10)
            if response.status_code == 200:
                # Basic web scraping for contact info (ethical)
                content = response.text.lower()
                
                # Look for email patterns
                import re
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails = re.findall(email_pattern, content)
                if emails:
                    business["email"] = emails[0]
                
                # Look for phone patterns
                phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                phones = re.findall(phone_pattern, content)
                if phones and not business.get("phone"):
                    business["phone"] = phones[0]
                
                logging.info(f"Enriched data for {business['name']}")
                
        except Exception as e:
            logging.warning(f"Could not enrich data for {business['name']}: {e}")
        
        return business

    def collect_business_data(self, queries: List[str], locations: List[str], 
                            categories: List[str] = None) -> List[Dict]:
        """Collect business data from multiple sources"""
        all_businesses = []
        
        # Collect from Google Places API
        if self.google_api_key:
            for query in queries:
                for location in locations:
                    logging.info(f"Collecting Google Places data for: {query} in {location}")
                    businesses = self.get_google_businesses(query, location)
                    all_businesses.extend(businesses)
                    time.sleep(2)  # Respectful delay between searches
        
        # Collect from Yellow Pages
        if categories:
            for category in categories:
                for location in locations:
                    logging.info(f"Collecting Yellow Pages data for: {category} in {location}")
                    businesses = self.get_yellow_pages_businesses(location, category)
                    all_businesses.extend(businesses)
                    time.sleep(2)  # Respectful delay between searches
        
        # Remove duplicates based on name and address
        unique_businesses = {}
        for business in all_businesses:
            key = f"{business['name']}_{business['address']}"
            if key not in unique_businesses:
                unique_businesses[key] = business
        
        # Enrich the data
        enriched_businesses = []
        for business in unique_businesses.values():
            enriched = self.enrich_business_data(business)
            enriched_businesses.append(enriched)
        
        logging.info(f"Collected {len(enriched_businesses)} unique businesses")
        return enriched_businesses

    def save_to_csv(self, businesses: List[Dict], filename: str = None) -> str:
        """Save business data to CSV file"""
        if not businesses:
            logging.warning("No businesses to save")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_data_{timestamp}.csv"
        
        # Define fieldnames based on available data
        fieldnames = [
            'name', 'phone', 'email', 'address', 'website', 
            'business_status', 'types', 'rating', 'user_ratings_total',
            'price_level', 'source', 'collected_date'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for business in businesses:
                # Ensure all fields exist
                row = {field: business.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        logging.info(f"Data saved to {filename}")
        return filename

    def save_to_json(self, businesses: List[Dict], filename: str = None) -> str:
        """Save business data to JSON file"""
        if not businesses:
            logging.warning("No businesses to save")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_data_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, indent=2, ensure_ascii=False)
        
        logging.info(f"Data saved to {filename}")
        return filename

def load_config() -> Dict:
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning("config.json not found. Using default settings.")
        return {}
    except json.JSONDecodeError:
        logging.error("Invalid JSON in config.json")
        return {}

def main():
    """Main function to demonstrate the business data collector"""
    
    # Load configuration
    config = load_config()
    google_api_key = config.get('GOOGLE_API_KEY')
    
    # Initialize collector
    collector = BusinessDataCollector(google_api_key=google_api_key)
    
    # Example search parameters
    queries = [
        "plumber",
        "electrician", 
        "HVAC contractor",
        "roofing contractor"
    ]
    
    locations = [
        "Buffalo, NY",
        "Rochester, NY",
        "Syracuse, NY"
    ]
    
    categories = [
        "plumbers",
        "electricians",
        "heating-air-conditioning-hvac",
        "roofing"
    ]
    
    print("🏢 Business Data Collector - Personal Use")
    print("=" * 50)
    print("Collecting business data using ethical methods...")
    print()
    
    # Collect data
    businesses = collector.collect_business_data(queries, locations, categories)
    
    if businesses:
        # Save to CSV
        csv_file = collector.save_to_csv(businesses)
        
        # Save to JSON
        json_file = collector.save_to_json(businesses)
        
        print(f"✅ Successfully collected data for {len(businesses)} businesses")
        print(f"📊 CSV file: {csv_file}")
        print(f"📄 JSON file: {json_file}")
        
        # Display sample data
        print("\n📋 Sample Data:")
        print("-" * 30)
        for i, business in enumerate(businesses[:5]):
            print(f"{i+1}. {business['name']}")
            print(f"   Phone: {business.get('phone', 'N/A')}")
            print(f"   Address: {business.get('address', 'N/A')}")
            print(f"   Source: {business.get('source', 'N/A')}")
            print()
    else:
        print("❌ No business data collected. Check your API keys and search parameters.")

if __name__ == "__main__":
    main()
