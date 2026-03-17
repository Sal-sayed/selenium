from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Open Google News directly (no captcha)
        page.goto("https://news.google.com/search?q=South%20Africa%20vs%20Australia")

        page.wait_for_selector("article")

        # Get top 5 news headlines
        articles = page.query_selector_all("article h3")

        print("\nTop News Headlines:\n")
        for i, article in enumerate(articles[:5]):
            print(f"{i+1}. {article.inner_text()}")

        page.wait_for_timeout(5000)
        browser.close()

run()