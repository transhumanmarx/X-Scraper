import pandas as pd
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

from scraper.browser import (
    create_browser,
    scroll_page,
    get_visible_tweets
)

from scraper.utils import (
    create_daily_windows,
    build_search_url
)

from scraper.exporter import (
    create_dataframe,
    )

from scraper.parser import (
    complete_missing_data,
    parse_tweet
)


# =====================================================
# Funcion principal de scraping
# =====================================================

def scrape_x(
    account: str,
    start_date: str,
    end_date: str,
    progress_callback=None
) -> pd.DataFrame:

    """
    Realiza el proceso completo de scraping de publicaciones de una
    cuenta de X dentro de un intervalo de fechas. 
    El proceso incluye la construcción de las búsquedas diarias, la
    recolección de tweets, la recuperación de información faltante y
    la exportación de los resultados a un archivo Excel.
    """

    print ("Entrando a scrape_x")

    # =====================================================
    # VENTANAS DIARIAS
    # =====================================================

    windows = create_daily_windows(
        start_date,
        end_date
    )

    # =====================================================
    # SCRAPING
    # =====================================================

    tweets_data = []
    seen_urls = set()

    with sync_playwright() as p:

        browser, context, page = create_browser(p)

        for since_date, until_date in windows:

            url = build_search_url(
                account,
                since_date,
                until_date
            )

            print()
            print(url)

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(5000)


            if page.is_closed():
                print("La página se cerró")
                break

            sin_nuevos = 0
            n_urls_previas = len(seen_urls)

            while sin_nuevos < 3:

                print("Ciclos sin tweets nuevos:", sin_nuevos)
            
                articles, n = get_visible_tweets(page)

                print("Tweets visibles:", n)

                n_articles_previos = n

                for i in range(n):

                    try:

                        tweet = articles.nth(i)
                                                
                        tweet_data = parse_tweet(
                            tweet,
                            seen_urls
                        )

                        if tweet_data is None:
                            continue

                        tweets_data.append(tweet_data)

                        print(
                            len(tweets_data),
                            tweet_data["simplified_date"]
                            if tweet_data["simplified_date"] else ""
                        )

                        print(
                            "Texto:",
                            tweet_data["texto"][:50]
                        )
                
                    except Exception as e:

                        print(
                            "Error processing tweet:",
                            e
                        )

                scroll_page(page)   
                
                if len(seen_urls) == n_urls_previas:

                    sin_nuevos += 1

                else:

                    sin_nuevos = 0
                    n_urls_previas = len(seen_urls)


            print(
                "FIN DEL DÍA:",
                since_date,
                "| Total Acumulado:",
                len(tweets_data)
            )
            if progress_callback:
                progress_callback(
                since_date,
                len(tweets_data)
            )                       

        df = create_dataframe(tweets_data)

 
        # =====================================================
        # SEGUNDA PASADA PARA COMPLETAR DATOS FALTANTES
        # =====================================================

        df = complete_missing_data(
            df,
            page
        )
       

    print()
    print("Tweets encontrados:", len(df))
    
    return df