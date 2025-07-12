#!/usr/bin/env python3
"""
Web Backend for Business Data Collector
Handles lead generation requests from the web interface
"""

import json
import csv
import os
from datetime import datetime
from business_collector import BusinessDataCollector, load_config

def generate_high_quality_leads(params):
    """Generate leads based on web interface parameters"""
    
    # Load configuration
    config = load_config()
    google_api_key = config.get('GOOGLE_API_KEY')
    
    if not google_api_key or google_api_key == "YOUR_GOOGLE_API_KEY_HERE":
        return {
            "error": "Google API key not configured. Please add your API key to config.json"
        }
    
    # Initialize collector
    collector = BusinessDataCollector(google_api_key=google_api_key)
    
    # Extract parameters
    business_type = params.get('businessType', '')
    locations = params.get('locations', [])
    min_rating = params.get('minRating', 0)
    min_reviews = params.get('minReviews', 0)
    has_website = params.get('hasWebsite', 'any')
    business_status = params.get('businessStatus', 'any')
    price_level = params.get('priceLevel', 'any')
    max_results = params.get('maxResults', 25)
    search_radius = params.get('searchRadius', 10) * 1609  # Convert miles to meters
    
    # Generate search queries
    queries = [business_type]
    
    # Collect data
    businesses = collector.collect_business_data(queries, locations)
    
    # Apply quality filters
    filtered_businesses = []
    for business in businesses:
        # Rating filter
        if min_rating > 0:
            rating = float(business.get('rating', 0))
            if rating < min_rating:
                continue
        
        # Reviews filter
        if min_reviews > 0:
            reviews = int(business.get('user_ratings_total', 0))
            if reviews < min_reviews:
                continue
        
        # Website filter
        if has_website == 'has_website' and not business.get('website'):
            continue
        elif has_website == 'no_website' and business.get('website'):
            continue
        
        # Business status filter
        if business_status != 'any' and business.get('business_status') != business_status:
            continue
        
        # Price level filter
        if price_level != 'any':
            business_price = business.get('price_level', '')
            if business_price and int(business_price) < int(price_level):
                continue
        
        # Calculate quality score
        quality_score = calculate_quality_score(business, params)
        business['quality_score'] = quality_score
        
        filtered_businesses.append(business)
    
    # Sort by quality score (highest first)
    filtered_businesses.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
    
    # Limit results
    filtered_businesses = filtered_businesses[:max_results]
    
    # Generate output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save CSV
    csv_filename = f"high_quality_leads_{timestamp}.csv"
    save_to_csv(filtered_businesses, csv_filename)
    
    # Save JSON
    json_filename = f"high_quality_leads_{timestamp}.json"
    save_to_json(filtered_businesses, json_filename)
    
    return {
        "success": True,
        "businesses": filtered_businesses,
        "total_found": len(filtered_businesses),
        "csv_file": csv_filename,
        "json_file": json_filename,
        "timestamp": timestamp
    }

def calculate_quality_score(business, params):
    """Calculate quality score for a business"""
    score = 5  # Base score
    
    # Rating bonus
    rating = float(business.get('rating', 0))
    if rating >= 4.5:
        score += 2
    elif rating >= 4.0:
        score += 1
    
    # Reviews bonus
    reviews = int(business.get('user_ratings_total', 0))
    if reviews >= 50:
        score += 2
    elif reviews >= 25:
        score += 1
    
    # Website bonus
    if business.get('website'):
        score += 1
    
    # Price level bonus (higher = more established)
    price_level = business.get('price_level', 0)
    if price_level and int(price_level) >= 3:
        score += 1
    
    # Business status bonus
    if business.get('business_status') == 'OPERATIONAL':
        score += 1
    
    return min(score, 10)

def save_to_csv(businesses, filename):
    """Save businesses to CSV file"""
    if not businesses:
        return
    
    fieldnames = [
        'name', 'address', 'phone', 'website', 'rating', 
        'user_ratings_total', 'price_level', 'business_status', 
        'types', 'quality_score', 'source', 'collected_date'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for business in businesses:
            row = {field: business.get(field, '') for field in fieldnames}
            writer.writerow(row)

def save_to_json(businesses, filename):
    """Save businesses to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(businesses, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Test function
    test_params = {
        "businessType": "plumber",
        "locations": ["Buffalo, NY"],
        "minRating": 4.0,
        "minReviews": 10,
        "hasWebsite": "has_website",
        "businessStatus": "OPERATIONAL",
        "priceLevel": "3",
        "maxResults": 10,
        "searchRadius": 10
    }
    
    result = generate_high_quality_leads(test_params)
    print(json.dumps(result, indent=2))
