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
