# Business Data Collector

A personal tool for ethically collecting business data using legitimate APIs and sources.

## 🚨 Important: Personal Use Only

This tool is designed for **personal use only**. It follows ethical guidelines and uses legitimate APIs to collect business information for sales lead generation.

## 🔧 Setup

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Configure API Keys
Edit `config.json` and add your Google API key:
```json
{
    "GOOGLE_API_KEY": "YOUR_ACTUAL_API_KEY_HERE"
}
```

### 3. Get a Google API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable the **Places API**
4. Create credentials (API Key)
5. Add the key to `config.json`

## 🚀 Usage

### Basic Usage
```bash
python3 business_collector.py
```

### Customize Search Parameters
Edit the `main()` function in `business_collector.py`:

```python
queries = [
    "plumber",
    "electrician", 
    "HVAC contractor"
]

locations = [
    "Buffalo, NY",
    "Rochester, NY"
]
```

## 📊 Output

The script generates:
- `business_data_YYYYMMDD_HHMMSS.csv` - CSV file for sales calls
- `business_data_YYYYMMDD_HHMMSS.json` - JSON data
- `business_collector.log` - Detailed logs

## 🔒 Security

- `config.json` is in `.gitignore` - your API keys stay private
- Uses official APIs only - no scraping of prohibited sites
- Respects rate limits and terms of service

## 📋 Data Collected

- Business name
- Phone number
- Address
- Website
- Business status
- Industry type
- Rating (if available)
- Source (Google Places API, Yellow Pages)

## ⚖️ Ethical Guidelines

- ✅ Uses official APIs only
- ✅ Respects rate limits
- ✅ Follows terms of service
- ✅ Personal use only
- ❌ No scraping of Google Search
- ❌ No violation of robots.txt

## 🛠️ Customization

### Add More Data Sources
The `BusinessDataCollector` class is designed to be extensible. You can add:
- Yelp Fusion API
- Local business registries
- Industry-specific databases

### Modify Search Parameters
- Change `queries` for different business types
- Adjust `locations` for different areas
- Modify `max_results` for different data volumes

## 📞 Support

For personal use questions or ethical guidance, refer to the ethical guidelines in the code comments.

## ⚠️ Disclaimer

This tool is for personal use only. Users are responsible for:
- Following all applicable laws and regulations
- Respecting website terms of service
- Using data ethically and responsibly
- Not violating any privacy or data protection laws

## 🔄 Updates

To update your local repository:
```bash
git pull origin main
```

## 📝 License

Personal use only. Not for commercial distribution.

## 🌐 Web Interface

This repository includes an interactive web interface for lead generation:

### Access the Web Interface
Once GitHub Pages is enabled, you can access the interactive lead generation tool at:
`https://musketeerdevelopment.github.io/business_data_collector/`

### Features
- **Interactive Quiz**: Answer questions about your target businesses
- **Quality Filters**: Filter by rating, reviews, website presence, and more
- **Revenue Indicators**: Target businesses by price level and status
- **Instant Results**: Get high-quality leads immediately
- **CSV/JSON Download**: Export results for your sales process

### Web Interface Parameters
- **Business Type**: Plumbing, electrical, HVAC, legal, accounting, etc.
- **Locations**: Target specific cities and states
- **Quality Filters**: Minimum rating, review count, website requirements
- **Business Size**: Price level indicators for established companies
- **Search Radius**: How far to search from target locations

### How to Use the Web Interface
1. Go to the GitHub Pages URL
2. Fill out the interactive quiz
3. Submit to generate leads
4. Download CSV or JSON files
5. Use the data for your sales calls

## 🚀 Quick Start with Web Interface

1. **Enable GitHub Pages**:
   - Go to your repository settings
   - Scroll to "Pages" section
   - Select "GitHub Actions" as source
   - The web interface will deploy automatically

2. **Configure API Key**:
   - Add your Google API key to `config.json`
   - The web interface will use this for real data

3. **Access the Tool**:
   - Visit your GitHub Pages URL
   - Start generating high-quality leads!

## 📊 Quality Scoring System

The web interface uses an intelligent scoring system to identify the best prospects:

- **Rating Bonus**: 4.5+ stars = +2 points, 4.0+ stars = +1 point
- **Review Count**: 50+ reviews = +2 points, 25+ reviews = +1 point  
- **Website Presence**: Has website = +1 point
- **Price Level**: Higher price levels = more established businesses
- **Business Status**: Operational businesses = +1 point

**Total Quality Score**: 0-10 scale, with 8+ being premium prospects.

