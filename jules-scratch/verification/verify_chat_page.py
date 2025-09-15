import re
from playwright.sync_api import sync_playwright, Page, expect
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"Current working directory: {os.getcwd()}")

    page.goto("http://localhost:3002/login")

    try:
        os.makedirs("/app/jules-scratch/verification", exist_ok=True)
        page.screenshot(path="/app/jules-scratch/verification/before_login.png")
        print("Successfully took before_login.png screenshot")
    except Exception as e:
        print(f"Error taking before_login.png screenshot: {e}")


    # Login
    page.get_by_placeholder("Enter your email").fill("test@test.com")
    page.get_by_placeholder("Enter your password").fill("password")
    page.get_by_role("button", name="🚀 Login to StudentMedia").click()

    # Wait for navigation to the main page
    page.wait_for_timeout(5000) # wait for 5 seconds
    print(f"URL after login attempt: {page.url}")

    try:
        page.screenshot(path="/app/jules-scratch/verification/after_login.png")
        print("Successfully took after_login.png screenshot")
    except Exception as e:
        print(f"Error taking after_login.png screenshot: {e}")


    # Navigate to chat page
    page.get_by_role("link", name="PChat").click()
    expect(page).to_have_url(re.compile(r"\/chat"))

    # Take screenshot
    page.screenshot(path="/app/jules-scratch/verification/chat_page.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
