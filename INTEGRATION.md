# Corpaxe Scraper - Backend Integration Guide

## Quick Command

To run the scraper from another script, use this exact command:

```bash
/home/ale/browser/venv/bin/python /home/ale/browser/scraper.py "TICKER_SYMBOL"
```

## Examples

```bash
# Search for Apple
/home/ale/browser/venv/bin/python /home/ale/browser/scraper.py "AAPL"

# Search for Microsoft US
/home/ale/browser/venv/bin/python /home/ale/browser/scraper.py "MSFT US"

# Search for Eli Lilly
/home/ale/browser/venv/bin/python /home/ale/browser/scraper.py "LLY"
```

## Exit Codes

- **0**: Success - search completed successfully
- **1**: Failure - login failed or search failed

## Output Format

On success, the script outputs a line with the last screenshot path:

```
LAST_SCREENSHOT=/home/ale/browser/runs/20251029_115436/12_after_suggestion_clicked.png
```

## Parsing Output

### Bash Example
```bash
#!/bin/bash
OUTPUT=$(/home/ale/browser/venv/bin/python /home/ale/browser/scraper.py "AAPL" 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    # Extract last screenshot path
    SCREENSHOT=$(echo "$OUTPUT" | grep "^LAST_SCREENSHOT=" | cut -d'=' -f2)
    echo "Success! Screenshot: $SCREENSHOT"
else
    echo "Failed with exit code: $EXIT_CODE"
fi
```

### Python Example
```python
import subprocess
import re

def run_corpaxe_scraper(ticker):
    cmd = ['/home/ale/browser/venv/bin/python', '/home/ale/browser/scraper.py', ticker]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extract screenshot path
        match = re.search(r'^LAST_SCREENSHOT=(.+)$', result.stdout, re.MULTILINE)
        if match:
            screenshot_path = match.group(1)
            return True, screenshot_path
    
    return False, None

# Usage
success, screenshot = run_corpaxe_scraper("AAPL")
if success:
    print(f"Screenshot saved at: {screenshot}")
```

## Requirements

- Script must be run on the same machine
- Google Chrome must be installed
- Network access to https://app.corpaxe.com
- Write access to /home/ale/browser/runs/ directory

## Logs

Each run creates:
- Log file: `/home/ale/browser/logs/YYYYMMDD_HHMMSS_TICKER.log`
- Timestamped screenshot folder: `/home/ale/browser/runs/YYYYMMDD_HHMMSS/`
- 12 screenshots documenting the entire process
- Error screenshots and HTML if failures occur

All output is sent to both stdout/stderr and the log file.

## Ticker Format

- US stocks: Can use just ticker (e.g., "AAPL") or with country ("AAPL US")
- International: Must include country code (e.g., "BP LN", "TTE FP")
- Default: When no country specified, defaults to US listing

## Timeout

The script typically completes in 20-30 seconds. Set your timeout accordingly.
