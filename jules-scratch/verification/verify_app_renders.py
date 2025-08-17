import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Listen for console messages
        page.on("console", lambda msg: print(f"CONSOLE: {msg.type}: {msg.text}"))

        try:
            # Go to the local http server on port 8001
            page.goto('http://localhost:8001/index.html', wait_until='networkidle')

            # Wait for the main heading to be visible to ensure the app has rendered
            heading = page.get_by_role("heading", name="Your Financial Future")
            expect(heading).to_be_visible(timeout=15000)

            # Also check if the dashboard content is there
            net_worth_label = page.get_by_text("Current Net Worth")
            expect(net_worth_label).to_be_visible()

            # Take a screenshot
            page.screenshot(path="jules-scratch/verification/verification.png")
            print("Verification successful, screenshot taken.")

        except Exception as e:
            print(f"An error occurred: {e}")
            # Save a screenshot on failure to see what's on the page
            page.screenshot(path="jules-scratch/verification/error_screenshot.png")
            print("Error screenshot taken.")
            # Print page content
            print("\nPAGE HTML:\n")
            print(page.content())

        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
