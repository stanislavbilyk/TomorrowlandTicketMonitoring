import asyncio
from playwright.async_api import async_playwright
import re
from notifier.telegram_bot import (
    send_telegram_message
)

from config import (
    BOT_TOKEN,
    CHAT_ID
)

URL = "https://www.viagogo.com/cz/Festival-Tickets/International-Festivals/Tomorrowland-Festival-Tickets/E-160250858?quantity=1"

TARGET_PRICE = 23000
TARGET_TICKET = "Magnificent Greens"





async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False,
            slow_mo=1000
        )

        page = await browser.new_page()

        await page.goto(URL)

        await page.wait_for_selector(
            '[data-testid="quantity-modal"]'
        )

        await page.evaluate("""
        document.querySelector('.sc-h3lopm-5')?.remove()
        """)

        modal = page.locator(
            '[data-testid="quantity-modal"]'
        )

        await modal.get_by_role(
            "button"
        ).click(force=True)

        await page.wait_for_selector(
            '[data-listing-id]'
        )

        print("Listings loaded")

        cards = page.locator(
            '[data-listing-id]'
        )

        count = await cards.count()

        print(count)

        parsed = []

        for i in range(count):

            card = cards.nth(i)

            title = await card.locator("h3").text_content()

            print(f"Title: {title}")

            if not title:
                continue

            if TARGET_TICKET not in title:
                continue

            price = await card.get_attribute(
                "data-price"
            )

            print(f"Raw price: {price}")

            if not price:
                continue

            digits = re.sub(r"[^\d]", "", price)

            value = int(digits)

            parsed.append(value)

        print(parsed)

        if not parsed:
            print("No prices found")

            input("Press Enter to exit...")
            return

        cheapest = min(parsed)

        print(f"Lowest price: {cheapest}")

        if cheapest <= TARGET_PRICE:
            send_telegram_message(
                BOT_TOKEN,
                CHAT_ID,
                f"Ticket found: {cheapest} Kč"
            )

        input("Press Enter to exit...")


asyncio.run(main())