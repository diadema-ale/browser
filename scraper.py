#!/usr/bin/env python3
"""
Simple web scraper for logging into https://app.corpaxe.com/Account/Login
"""

# Standard library imports
import time
import sys
import random
import logging
from pathlib import Path
from datetime import datetime

# Third-party imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Local imports
# None


class CorpaxeScraper:
    def __init__(self, headless=True, logger=None):
        """Initialize the scraper with Chrome options"""
        self.headless = headless
        self.driver = None
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.screenshot_dir = Path(f"runs/{self.timestamp}")
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.screenshot_counter = 0
        self.logger = logger or logging.getLogger(__name__)
        
    def setup_driver(self):
        """Set up Chrome driver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
        # Additional options for better compatibility
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to appear more like a regular browser
        chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        try:
            # Use webdriver-manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ Chrome driver initialized successfully")
            print(f"✓ Screenshots will be saved to: {self.screenshot_dir}")
            self.logger.info(f"Chrome driver initialized. Screenshots directory: {self.screenshot_dir}")
            return True
        except Exception as e:
            print(f"✗ Failed to initialize Chrome driver: {str(e)}")
            print("\nPlease make sure Google Chrome is installed on your system.")
            print("Run: sudo apt-get update && sudo apt-get install -y google-chrome-stable")
            self.logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            return False
    
    def save_screenshot(self, name):
        """Save a screenshot with a descriptive name"""
        self.screenshot_counter += 1
        filename = f"{self.screenshot_counter:02d}_{name}.png"
        filepath = self.screenshot_dir / filename
        self.driver.save_screenshot(str(filepath))
        print(f"  📸 Screenshot saved: {filepath}")
        self.logger.debug(f"Screenshot saved: {filepath}")
        return filepath
    
    def random_wait(self, min_seconds=0.25, max_seconds=1.5):
        """Wait for a random time between min and max seconds"""
        wait_time = random.uniform(min_seconds, max_seconds)
        print(f"  ⏳ Waiting {wait_time:.2f}s...")
        time.sleep(wait_time)
    
    def login(self, url, username, password):
        """Login to the website"""
        if not self.driver:
            print("✗ Driver not initialized")
            return False
            
        try:
            print(f"\n→ Navigating to {url}")
            self.logger.info(f"Navigating to {url}")
            self.driver.get(url)
            self.save_screenshot("initial_page_load")
            
            # Wait for the page to load and email field to be present
            wait = WebDriverWait(self.driver, 10)
            
            # Wait for and find the email field (ID: Email)
            print("→ Waiting for login form to load...")
            email_field = wait.until(
                EC.presence_of_element_located((By.ID, "Email"))
            )
            self.save_screenshot("login_form_loaded")
            
            # Clear and enter email
            print("→ Entering email...")
            email_field.clear()
            self.random_wait()
            email_field.send_keys(username)
            self.save_screenshot("email_entered")
            print("✓ Email entered")
            
            # Find and fill password field (ID: Password)
            print("→ Entering password...")
            self.random_wait()
            password_field = self.driver.find_element(By.ID, "Password")
            password_field.clear()
            self.random_wait()
            password_field.send_keys(password)
            self.save_screenshot("password_entered")
            print("✓ Password entered")
            
            # Find and click login button
            print("→ Looking for login button...")
            self.random_wait()
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            
            # Scroll to button if needed
            self.driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
            self.random_wait(0.3, 0.8)  # Brief pause after scrolling
            
            self.save_screenshot("before_login_click")
            
            print("→ Clicking login button...")
            login_button.click()
            print("✓ Login button clicked")
            
            # Wait for page to process login
            print("→ Waiting for login to process...")
            time.sleep(5)  # Give login time to process
            
            self.save_screenshot("after_login_click")
            
            # Check if login was successful
            current_url = self.driver.current_url
            page_title = self.driver.title
            
            print(f"  Current URL: {current_url}")
            print(f"  Page title: {page_title}")
            
            if current_url != url:
                print(f"✓ Login appears successful - redirected to: {current_url}")
                self.save_screenshot("login_successful")
                self.logger.info(f"Login successful - redirected to: {current_url}")
                return True
            else:
                # Check for error messages
                print("→ Checking for error messages...")
                error_selectors = [
                    ".error", 
                    ".alert-danger", 
                    ".validation-summary-errors",
                    ".text-danger",
                    "[role='alert']"
                ]
                
                error_found = False
                for selector in error_selectors:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for error in error_elements:
                        if error.is_displayed() and error.text.strip():
                            print(f"✗ Error found: {error.text}")
                            self.logger.error(f"Login error found: {error.text}")
                            error_found = True
                
                if not error_found:
                    print("? Login status unclear - no redirect detected but no errors found")
                    
                self.save_screenshot("login_result_unclear")
                return False
                
        except Exception as e:
            print(f"✗ Error during login: {str(e)}")
            self.logger.error(f"Error during login: {str(e)}")
            self.save_screenshot("error_occurred")
            # Save page source for debugging
            error_html_path = self.screenshot_dir / "error_page_source.html"
            with open(error_html_path, 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            print(f"  Page source saved: {error_html_path}")
            self.logger.info(f"Error page source saved: {error_html_path}")
            return False
    
    def search_on_calendar(self, search_term):
        """Search for a term on the Calendar page"""
        try:
            print(f"\n→ Searching for: {search_term}")
            self.logger.info(f"Starting search for: {search_term}")
            
            # Wait for the calendar page to fully load (wait for table or content)
            print("→ Waiting for Calendar page to load...")
            wait = WebDriverWait(self.driver, 20)
            try:
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                print("  ✓ Page DOM ready")
            except:
                print("  ? Page readyState wait timed out")
            
            # Wait for any loading indicator to disappear
            for _ in range(10):
                loading_texts = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Loading')]")
                visible_loading = [el for el in loading_texts if el.is_displayed()]
                if not visible_loading:
                    break
                print("  ⏳ Page still loading...")
                time.sleep(1)
            
            self.random_wait(2, 3)
            self.save_screenshot("calendar_page_loaded")
            
            # Look for search input box
            print("→ Looking for search input box...")
            search_selectors = [
                "input[type='search']",
                "input[placeholder*='Search']",
                "input[placeholder*='search']", 
                "#search",
                ".search-input",
                "input.form-control",
                "input[type='text']"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            location = element.location
                            if location['y'] < 300:
                                search_input = element
                                print(f"  ✓ Found search input using selector: {selector}")
                                break
                    if search_input:
                        break
                except:
                    continue
            
            if not search_input:
                print("✗ Could not find search input box")
                self.save_screenshot("search_input_not_found")
                return False
            
            # Click on search input
            print("→ Clicking on search input...")
            self.random_wait()
            search_input.click()
            self.save_screenshot("search_input_clicked")
            
            # Clear and type search term
            print(f"→ Typing search term: {search_term}")
            search_input.clear()
            self.random_wait()
            
            for char in search_term:
                search_input.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            self.save_screenshot("search_term_typed")
            print("✓ Search term entered")
            
            # Wait for dropdown with actual suggestion items (not just the container)
            print("→ Waiting for dropdown suggestions to load...")
            suggestion_selector = ".ant-select-dropdown .rc-virtual-list-holder-inner > div"
            
            visible_suggestions = []
            max_wait_attempts = 12
            for attempt in range(max_wait_attempts):
                time.sleep(1)
                try:
                    suggestions = self.driver.find_elements(By.CSS_SELECTOR, suggestion_selector)
                    visible_suggestions = []
                    for suggestion in suggestions:
                        if suggestion.is_displayed() and suggestion.text and suggestion.text.strip():
                            visible_suggestions.append({
                                'element': suggestion,
                                'text': suggestion.text.strip()
                            })
                    if visible_suggestions:
                        print(f"  ✓ Found {len(visible_suggestions)} suggestions after {attempt + 1}s")
                        break
                except:
                    pass
                if attempt < max_wait_attempts - 1:
                    print(f"  ⏳ Waiting for suggestions... ({attempt + 1}/{max_wait_attempts})")
            
            self.save_screenshot("dropdown_suggestions_visible")
            
            if not visible_suggestions:
                print("✗ No visible suggestions found after waiting")
                self.save_screenshot("no_suggestions_found")
                return False
            
            print(f"  Found {len(visible_suggestions)} suggestions:")
            for i, sug in enumerate(visible_suggestions):
                print(f"    {i+1}. {sug['text']}")
            
            # Look for exact match first
            exact_match = None
            search_upper = search_term.upper().strip()
            
            for sug in visible_suggestions:
                sug_text_upper = sug['text'].upper()
                if sug_text_upper.startswith(search_upper + ":") or sug_text_upper == search_upper:
                    exact_match = sug
                    print(f"\n  ✓ Found exact match: {sug['text']}")
                    break
            
            if not exact_match:
                if not any(search_upper.endswith(f" {country}") for country in ["US", "LN", "CN", "JP", "FP", "GR", "MK", "VN"]):
                    print("\n  ? No country specified, looking for US listing...")
                    us_search = search_upper + " US"
                    
                    for sug in visible_suggestions:
                        sug_text_upper = sug['text'].upper()
                        if sug_text_upper.startswith(us_search + ":"):
                            exact_match = sug
                            print(f"  ✓ Found US listing: {sug['text']}")
                            break
            
            if not exact_match:
                print("\n  ? No exact match found, looking for best partial match...")
                best_match = None
                
                for sug in visible_suggestions:
                    sug_text_upper = sug['text'].upper()
                    if sug_text_upper.startswith(search_upper):
                        best_match = sug
                        print(f"  ✓ Found partial match: {sug['text']}")
                        break
                
                if not best_match and visible_suggestions:
                    best_match = visible_suggestions[0]
                    print(f"  ! Using first suggestion as fallback: {best_match['text']}")
                
                selected_suggestion = best_match
            else:
                selected_suggestion = exact_match
            
            if not selected_suggestion:
                print("✗ No suitable suggestion found")
                self.save_screenshot("no_suitable_suggestion")
                return False
            
            # Click the selected suggestion
            print(f"\n→ Clicking on: {selected_suggestion['text']}")
            self.random_wait()
            selected_suggestion['element'].click()
            print("✓ Suggestion clicked")
            
            # Wait for page to load
            print("→ Waiting for new page to load...")
            self.random_wait(2, 3)
            
            self.save_screenshot("after_suggestion_clicked")
            
            current_url = self.driver.current_url
            print(f"✓ Navigated to: {current_url}")
            self.logger.info(f"Search successful - navigated to: {current_url}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error during search: {str(e)}")
            self.logger.error(f"Error during search: {str(e)}")
            self.save_screenshot("search_error")
            return False
    
    def get_last_screenshot(self):
        """Get the path of the last screenshot taken"""
        if self.screenshot_counter > 0:
            filename = f"{self.screenshot_counter:02d}_after_suggestion_clicked.png"
            filepath = self.screenshot_dir / filename
            if filepath.exists():
                return str(filepath.absolute())
        return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("✓ Browser closed")


def setup_logging(search_term):
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create log filename with timestamp and ticker
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_search_term = search_term.replace(" ", "_").replace("/", "_")
    log_filename = log_dir / f"{timestamp}_{safe_search_term}.log"
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)  # Also output to console
        ]
    )
    
    return logging.getLogger(__name__)


def main():
    """Main function to run the scraper"""
    # Configuration
    URL = "https://app.corpaxe.com/Account/Login"
    USERNAME = "ale@diademapartnerslp.com"
    PASSWORD = "Copyright2024!"
    
    # Default search term or get from command line
    if len(sys.argv) > 1:
        SEARCH_TERM = " ".join(sys.argv[1:])
    else:
        SEARCH_TERM = "ABBV US"  # Default search term
    
    # Set up logging
    logger = setup_logging(SEARCH_TERM)
    
    logger.info("=== Corpaxe Login Scraper ===")
    logger.info(f"Search term: {SEARCH_TERM}\n")
    
    # Create scraper instance
    scraper = CorpaxeScraper(headless=True, logger=logger)
    
    # Setup driver
    if not scraper.setup_driver():
        logger.error("Failed to setup Chrome driver")
        sys.exit(1)
    
    exit_code = 1  # Default to failure
    
    try:
        # Attempt login
        success = scraper.login(URL, USERNAME, PASSWORD)
        
        if success:
            print("\n✓ Login completed successfully!")
            
            # Perform search on calendar page
            search_success = scraper.search_on_calendar(SEARCH_TERM)
            
            if search_success:
                print("\n✓ Search completed successfully!")
                exit_code = 0  # Success
                
                # Get last screenshot path
                last_screenshot = scraper.get_last_screenshot()
                if last_screenshot:
                    print(f"\n=== RESULT ===")
                    print(f"LAST_SCREENSHOT={last_screenshot}")
                    logger.info(f"Last screenshot: {last_screenshot}")
            else:
                print("\n✗ Search failed!")
        else:
            print("\n✗ Login failed!")
            
    finally:
        # Always close the browser
        scraper.close()
        print(f"\n📁 All screenshots saved to: {scraper.screenshot_dir}")
        print("✓ Run completed")
        
        logger.info(f"Run completed with exit code: {exit_code}")
        logger.info(f"Screenshots saved to: {scraper.screenshot_dir}")
        
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
