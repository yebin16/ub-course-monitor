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
            print("Opening HUB homepage...", flush=True)
            await page.goto(
                HUB_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.wait_for_timeout(10000)

            print("Current URL:", page.url, flush=True)
            print(
                "Page preview:",
                (await page.locator("body").inner_text())[:3000],
                flush=True
            )

            await page.screenshot(
                path="hub-test.png",
                full_page=True
            )

            print("Searching for COURSE SCHEDULE...", flush=True)

            for frame in page.frames:
                print("Frame:", frame.url, flush=True)
                print(
                    "Matches:",
                    await frame.get_by_text(
                        "COURSE SCHEDULE", exact=True
                    ).count(),
                    flush=True
                )

            button = page.get_by_text(
                "COURSE SCHEDULE", exact=False
            )

            if await button.count() > 0:
                print("Clicking COURSE SCHEDULE...", flush=True)
                await button.first.click(timeout=15000)
                await page.wait_for_timeout(5000)
                print("After click URL:", page.url, flush=True)
                print(
                "After click page content:",
                (await page.locator("body").inner_text())[:5000],
                flush=True
            )
            spring = page.get_by_text("Spring 2027", exact=True)

            print("Spring 2027 matches:", await spring.count(), flush=True)

            if await spring.count() > 0:
                await spring.first.click(timeout=15000)
                await page.wait_for_timeout(5000)

                print("After Spring 2027 URL:", page.url, flush=True)
                print(
                    "After Spring 2027 content:",
                    (await page.locator("body").inner_text())[:5000],
                    flush=True
                )
            await page.screenshot(
                path="hub-test.png",
                full_page=True
            )

            else:
                print(
                    "COURSE SCHEDULE not found in main frame.",
                    flush=True
                )

            print("Final URL:", page.url, flush=True)

        finally:
            await browser.close()


asyncio.run(main())
