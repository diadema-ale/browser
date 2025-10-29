# Corpaxe Login Scraper Setup Guide

This guide will help you set up and run the Python scraper for logging into https://app.corpaxe.com/Account/Login.

## Prerequisites

- Ubuntu 22.04 or similar Linux distribution
- Python 3.12 or higher
- Internet connection for downloading dependencies

## Installation Steps

### 1. Install Google Chrome (Required)

Since this is a headless server without a browser, you need to install Google Chrome:

```bash
# Update package list
sudo apt-get update

# Install dependencies
sudo apt-get install -y wget gnupg

# Add Google Chrome's GPG key
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -

# Add Chrome repository
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list

# Update package list again
sudo apt-get update

# Install Google Chrome Stable
sudo apt-get install -y google-chrome-stable

# Verify installation
google-chrome --version
```

### 2. Set Up Python Environment

The virtual environment has already been created. To activate it:

```bash
cd /home/ale/browser
source venv/bin/activate
```

### 3. Install Python Dependencies

All required packages are listed in `requirements.txt`. If you need to reinstall them:

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

The main dependencies are:
- **selenium**: Web browser automation framework
- **webdriver-manager**: Automatically manages ChromeDriver downloads
- **requests**: HTTP library (for potential future enhancements)

### 4. Run the Scraper

To run the scraper:

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Run with default search term (ABBV US)
python scraper.py

# Run with custom search term
python scraper.py "MSFT US"
python scraper.py "AAPL US"
```

The scraper will:
1. Automatically download the appropriate ChromeDriver version
2. Open Chrome in headless mode (no GUI)
3. Navigate to the login page
4. Enter credentials and attempt to log in
5. Navigate to the Calendar page
6. Search for the specified ticker/company
7. Click on the first dropdown suggestion
8. Navigate to the company page
9. Take screenshots at every step for debugging

## Configuration

The login credentials are currently hardcoded in `scraper.py`:
- URL: https://app.corpaxe.com/Account/Login
- Username: ale@diademapartnerslp.com
- Password: Copyright2024!

To change these, edit the variables in the `main()` function of `scraper.py`.

## Troubleshooting

### Chrome Installation Issues

If you encounter issues installing Chrome, try:

```bash
# Alternative method using snap
sudo snap install chromium

# Or download the .deb package directly
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f  # Fix any dependency issues
```

### ChromeDriver Issues

The scraper uses `webdriver-manager` to automatically download and manage ChromeDriver. If you encounter issues:

1. Clear the webdriver cache:
   ```bash
   rm -rf ~/.wdm/
   ```

2. Manually specify Chrome binary location in the script if needed

### Headless Mode Issues

The scraper runs in headless mode by default. If you need to debug visually (requires GUI):

1. Modify `scraper.py` and change:
   ```python
   scraper = CorpaxeScraper(headless=False)
   ```

2. Make sure you have X11 forwarding enabled if running over SSH

### Login Failures

If login fails:
1. Check the screenshots in the `runs/{timestamp}/` folder
2. Check the `error_page_source.html` file if an error occurs
3. Verify the element IDs haven't changed on the website
4. Some websites detect automated browsers - the script includes measures to avoid detection

### Analyzing Issues

If you encounter issues, check the screenshots in the `runs/{timestamp}/` folder which capture every step of the process. The scraper also saves HTML page source when errors occur.

## Output

The scraper creates screenshots in timestamped folders under `runs/`:

**Login Process:**
- `01_initial_page_load.png`: Initial page load
- `02_login_form_loaded.png`: Login form ready
- `03_email_entered.png`: After entering email
- `04_password_entered.png`: After entering password
- `05_before_login_click.png`: Before clicking login
- `06_after_login_click.png`: After login attempt
- `07_login_successful.png`: After successful redirect

**Search Process:**
- `08_calendar_page_loaded.png`: Calendar page loaded
- `09_search_input_clicked.png`: Search input focused
- `10_search_term_typed.png`: After typing search term
- `11_dropdown_suggestions_visible.png`: Dropdown suggestions shown
- `12_after_suggestion_clicked.png`: After clicking first suggestion

Each run creates a new timestamped folder (format: YYYYMMDD_HHMMSS) for easy debugging and comparison.

## Features

- **Human-like Behavior**: Random wait times between 0.25-1.5 seconds for all interactions
- **Intelligent Search**: Types search terms character by character with realistic delays
- **Ant Design Support**: Handles modern React/Ant Design dropdown components
- **Comprehensive Screenshots**: Captures every step for easy debugging
- **Command Line Arguments**: Pass any search term as an argument

## Next Steps

You can extend the scraper to:
- Extract data from the company pages after navigation
- Search for multiple companies in one run
- Export data to CSV or JSON
- Schedule regular runs with different search terms
- Add email notifications for specific events

## Security Notes

1. **Credentials**: Currently hardcoded - consider using environment variables or a config file
2. **Screenshots**: May contain sensitive information - handle with care
3. **Logs**: Be careful not to log sensitive data

## Running as a Scheduled Job

To run the scraper periodically, you can use cron:

```bash
# Edit crontab
crontab -e

# Add a line like this to run every day at 2 AM:
0 2 * * * cd /home/ale/browser && /home/ale/browser/venv/bin/python /home/ale/browser/scraper.py >> /home/ale/browser/scraper.log 2>&1
```

## Maintenance

- Regularly update Chrome: `sudo apt-get update && sudo apt-get upgrade google-chrome-stable`
- Update Python packages: `pip install --upgrade -r requirements.txt`
- Monitor for website changes that might break the scraper
