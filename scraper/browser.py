from playwright.sync_api import (
    Browser,
    BrowserContext,
    Locator,
    Page,
    Playwright,
)

def create_browser(
    p: Playwright,
) -> tuple[Browser, BrowserContext, Page]:

    """
    Se conecta a una instancia existente de Chromium y devuelve el navegador, 
    el contexto y la página que utilizará el scraper.     
    """  

    browser = p.chromium.connect_over_cdp(
        "http://localhost:9222"
    )

    context = browser.contexts[0]

    page = context.pages[0]

    return browser, context, page


def scroll_page(page: Page) -> None:

    """
    Realiza varios desplazamientos hacia abajo para forzar la carga
    de nuevos tweets en la página.
    """

    for _ in range(4):
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(400)
        
    page.wait_for_timeout(500)


def get_visible_tweets(
    page: Page,
) -> tuple[Locator, int]:

    """
    Obtiene los tweets visibles en la página y devuelve tanto el
    Locator como la cantidad de elementos encontrados.
    """
    
    articles = page.locator("article")

    n = articles.count()

    return articles, n