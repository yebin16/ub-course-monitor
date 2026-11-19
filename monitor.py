import asyncio
from playwright.async_api import async_playwright

HUB_URL = (
    "https://www.pub.hub.buffalo.edu/psc/"
    "csprdpub_3/EMPLOYEE/SA/c/"
    "SSR_STUDENT_FL.SSR_MD_SP_FL.GBL"
)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            print("Opening UB HUB Public Class Schedule...")
            response = await page.goto(
                HUB_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.wait_for_timeout(8000)

            print("HTTP status:", response.status if response else "N/A")
            print("Current URL:", page.url)
            print("Page title:", await page.title())

            body = await page.locator("body").inner_text()
            print("Page preview:", body[:2000])

            await page.screenshot(
                path="hub-test.png",
                full_page=True
            )

        finally:
            await browser.close()

asyncio.run(main())
