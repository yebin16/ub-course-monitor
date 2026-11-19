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
        page = await browser.new_page(
            viewport={"width": 1440, "height": 900}
        )

        try:
            print("Opening HUB Public Class Schedule...")
            await page.goto(
                HUB_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.get_by_text(
                "COURSE SCHEDULE", exact=True
            ).wait_for(timeout=30000)

            print("Clicking COURSE SCHEDULE...")
            await page.get_by_text(
                "COURSE SCHEDULE", exact=True
            ).click()

            await page.wait_for_timeout(5000)

            print("Current URL:", page.url)
            print("Page title:", await page.title())
            print(
                "Page preview:",
                (await page.locator("body").inner_text())[:3000]
            )

            await page.screenshot(
                path="hub-test.png",
                full_page=True
            )

        finally:
            await browser.close()


asyncio.run(main())
