"""Debug script to identify correct Cognito page selectors"""
import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_cognito_page():
    """Navigate to app and capture Cognito page structure"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})
        
        try:
            # Navigate to app
            logger.info("Navigating to http://localhost:8080...")
            page.goto("http://localhost:8080", wait_until="domcontentloaded", timeout=30000)
            
            # Wait for potential redirect to Cognito
            logger.info("Waiting for page to load...")
            page.wait_for_timeout(5000)
            
            # Get current URL
            current_url = page.url
            logger.info(f"Current URL: {current_url}")
            
            # Get page title
            title = page.title()
            logger.info(f"Page title: {title}")
            
            # Take screenshot
            page.screenshot(path="debug_cognito_page.png")
            logger.info("Screenshot saved: debug_cognito_page.png")
            
            # Try to find all input fields
            logger.info("\n=== INPUT FIELDS FOUND ===")
            inputs = page.query_selector_all("input")
            for i, inp in enumerate(inputs):
                name = inp.get_attribute("name") or "N/A"
                id_val = inp.get_attribute("id") or "N/A"
                type_val = inp.get_attribute("type") or "N/A"
                placeholder = inp.get_attribute("placeholder") or "N/A"
                logger.info(f"\nInput {i}:")
                logger.info(f"  name: {name}")
                logger.info(f"  id: {id_val}")
                logger.info(f"  type: {type_val}")
                logger.info(f"  placeholder: {placeholder}")
            
            # Try to find all buttons
            logger.info("\n=== BUTTONS FOUND ===")
            buttons = page.query_selector_all("button")
            for i, btn in enumerate(buttons):
                text = btn.text_content().strip() or "N/A"
                name = btn.get_attribute("name") or "N/A"
                id_val = btn.get_attribute("id") or "N/A"
                logger.info(f"\nButton {i}:")
                logger.info(f"  text: {text}")
                logger.info(f"  name: {name}")
                logger.info(f"  id: {id_val}")
            
            # Get all text on page (to see if login page loaded)
            logger.info("\n=== PAGE TEXT CONTENT (first 30 lines) ===")
            all_text = page.locator("body").text_content()
            if all_text:
                lines = all_text.split('\n')
                for line in lines[:30]:  # First 30 lines
                    if line.strip():
                        logger.info(line.strip())
            
            # Get page HTML (first 2000 chars)
            logger.info("\n=== PAGE HTML (first 2000 chars) ===")
            html = page.content()
            logger.info(html[:2000])
            
            logger.info("\n" + "="*60)
            logger.info("Debug complete! Check debug_cognito_page.png for screenshot")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Error during debug: {e}")
            page.screenshot(path="debug_error.png")
            logger.error("Error screenshot saved: debug_error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    debug_cognito_page()
