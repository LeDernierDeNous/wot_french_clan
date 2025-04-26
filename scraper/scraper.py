from fastapi import FastAPI
from playwright.async_api import async_playwright
import asyncio
import time  # Import the time module to measure elapsed time

app = FastAPI()

# Async function for scraping the page
async def get_languages(id: int):
    url = f"https://eu.wargaming.net/clans/wot/{id}/"

    async with async_playwright() as playwright:
        # Launch browser
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Navigate to the URL
            await page.goto(url)

            css_selector = ".language-list"

            # Wait for the page to load
            await page.wait_for_selector(css_selector)  # Wait for 10 seconds (you can adjust this)

            # Locate the '.language-list' element and its children
            language_list = await page.query_selector(css_selector)
            items = await language_list.query_selector_all("*")  # Find all child elements

            # Extract and return the unique text content
            languages = set()  # Use a set to deduplicate
            for item in items:
                text = await item.inner_text()
                if text.strip():  # Avoid adding empty text
                    languages.add(text.strip())

        finally:
            await browser.close()

        return list(languages)  # Return a list of deduplicated text

# FastAPI endpoint
@app.get("/get_language_by_scraping/{id}")
async def get_language_by_scraping(id: int):
    start_time = time.time()  # Record the start time of the request

    # Call the scraping function
    languages = await get_languages(id)
    
    elapsed_time = time.time() - start_time  # Calculate the elapsed time

    # Return the list of languages and elapsed time
    return {"languages": languages, "elapsed_time": elapsed_time}
