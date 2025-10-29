# Corpaxe Web Scraper

A Python-based web scraper for automating login and company searches on app.corpaxe.com.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Search for a specific ticker
python scraper.py "AAPL US"
python scraper.py "MSFT US"
python scraper.py "GOOGL"

# Run with default ticker (ABBV US)
python scraper.py
```

## Features

- ✅ Automated login to Corpaxe
- ✅ Search for any company ticker
- ✅ Smart suggestion matching:
  - Finds exact matches first
  - Defaults to US listings when no country specified
  - Falls back to best partial match
- ✅ Human-like interaction with random delays
- ✅ Handles modern React/Ant Design components
- ✅ Screenshots at every step for debugging
- ✅ Headless browser operation (no GUI needed)

## Output

Each run creates:

**Log File**: `logs/YYYYMMDD_HHMMSS_TICKER.log`
- Complete execution log with timestamps
- All important events and errors

**Screenshots**: `runs/YYYYMMDD_HHMMSS/`
- Login process (7 screenshots)
- Search process (5 screenshots)
- Final navigation to company page

## Requirements

- Ubuntu/Linux with Google Chrome installed
- Python 3.12+
- All dependencies in `requirements.txt`

## Files

- `scraper.py` - Main scraper script
- `requirements.txt` - Python dependencies
- `setup.md` - Detailed setup instructions
- `runs/` - Screenshot outputs

## Usage Examples

```bash
# US stocks with explicit country code
python scraper.py "AAPL US"
python scraper.py "TSLA US"
python scraper.py "JPM US"

# Just ticker symbols (defaults to US)
python scraper.py "GOOGL"  # → Selects GOOGL US
python scraper.py "MSFT"   # → Selects MSFT US
python scraper.py "LLY"    # → Selects LLY US (not ALLY US)

# International stocks (specify country)
python scraper.py "BP LN"   # London
python scraper.py "TTE FP"  # Paris
python scraper.py "7203 JP" # Tokyo
```

The scraper will:
1. Log into Corpaxe
2. Navigate to the Calendar page
3. Search for your ticker
4. Click the first suggestion
5. Navigate to the company page

## Troubleshooting

If the scraper fails, check:
- Screenshots in the latest `runs/` folder
- Error messages in the console
- `error_page_source.html` if created

For detailed setup instructions, see `setup.md`.
For backend integration, see `INTEGRATION.md`.
