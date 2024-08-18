BOT_NAME = "quotes"
SPIDER_MODULES = ["quotes.spiders"]
NEWSPIDER_MODULE = "quotes.spiders"

ROBOTSTXT_OBEY = True

# Download handlers
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

# Twisted reactor
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Playwright settings
PLAYWRIGHT = {
    'browser': 'chromium',  # Use 'chromium', 'firefox', or 'webkit'
    'headless': False,  # Run in non-headless mode for debugging
    'slow_mo': 1000,    # Slow down operations for debugging
}

# Playwright specific settings
PLAYWRIGHT_BROWSER_TYPE = 'chromium'  # Set to 'firefox' or 'webkit' as needed
PLAYWRIGHT_DEFAULT_ARGS = ['--headless']  # Remove if running in non-headless mode
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 100000  # Timeout for navigation
PLAYWRIGHT_CONTEXT_ARGS = {
    'viewport': {'width': 1280, 'height': 800},  # Optional: Set viewport size
}