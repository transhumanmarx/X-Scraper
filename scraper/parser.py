from numpy import rint
import pandas as pd
from playwright.sync_api import Locator, Page

def complete_missing_data(
    df: pd.DataFrame,
    page: Page,
) -> pd.DataFrame:
    
    """
    Completa la información que no pudo obtenerse durante el scraping inicial visitando individualmente cada tweet.
    Actualmente recupera la fecha de publicación y el nombre visible del usuario cuando esos datos están ausentes.
    """

    print()
    print("Iniciando segunda pasada...")

    for idx, row in df.iterrows():

        if pd.isna(row["timestamp"]) or pd.isna(row["display_name"]):

            url = row["url"]

            print("Completando:", url)
            
            try:

                page.goto(
                    url,
                    wait_until="domcontentloaded"
                )

                page.wait_for_timeout(3000)

                # ----------------------
                # Timestamp y fecha_simple
                # ----------------------

                if pd.isna(row["timestamp"]):

                    try:

                        time_locator = page.locator("time")

                        if time_locator.count() > 0:

                            timestamp = (
                                time_locator
                                .first
                                .get_attribute("datetime")
                            )

                            df.at[idx, "timestamp"] = timestamp

                            if timestamp:
                                df.at[idx, "fecha_simple"] = timestamp[:10]

                    except Exception as e:
                        print("Error al recuperar timestamp:", e)

                # ----------------------
                # DISPLAY NAME
                # ----------------------

                if pd.isna(row["display_name"]):

                    try:

                        user_locator = page.locator(
                            '[data-testid="User-Name"] span'
                        )

                        if user_locator.count() > 0:

                            df.at[idx, "display_name"] = (
                                user_locator
                                .first
                                .inner_text()
                            )

                    except:
                        pass

            except Exception as e:
                print(
                    "Error al completar tweet:",
                    url,
                    "|",
                    e
                )

    return df

def parse_tweet(
    tweet: Locator,
    seen_urls: set[str],
) -> dict | None:

    """
    Extrae la información relevante de un tweet visible en la página.
    Además de obtener el contenido del tweet, evita procesar URLs
    duplicadas y organiza toda la información en un diccionario listo
    para su posterior almacenamiento.
    """

    links = tweet.locator(
        'a[href*="/status/"]'
    )

    if links.count() == 0:
        return None

    tweet_url = links.first.get_attribute("href")

    if tweet_url is None:
        return None

    tweet_url = (
        "https://x.com"
        + tweet_url
    )

    if tweet_url in seen_urls:
        return None

    seen_urls.add(tweet_url)

    # ======================
    # NOMBRE VISIBLE
    # ======================

    display_name = None

    try:

        display_name = (
            tweet.locator(
                '[data-testid="User-Name"]'
            )
            .first
            .inner_text()
            .split("\n")[0]
        )

    except Exception as e:

        print(
            "Error al obtener display_name:",
            e
        )
        

    # ======================
    # USERNAME
    # ======================

    username = ""

    try:

        username = (
            tweet_url
            .split("/")[3]
        )

    except Exception as e:
        print("Error al obtener username:", e)

    # ======================
    # LIKES
    # ======================

    likes = ""

    try:

        likes = tweet.locator(
            '[data-testid="like"]'
        ).inner_text()

    except Exception as e:
        print("Error al obtener likes:", e)


    # ======================
    # RETWEETS
    # ======================

    retweets = ""

    try:

        retweets = tweet.locator(
            '[data-testid="retweet"]'
        ).inner_text()

    except Exception as e:
        print("Error al obtener retweets:", e)


    # ======================
    # REPLIES
    # ======================

    replies = ""

    try:

        replies = tweet.locator(
            '[data-testid="reply"]'
        ).inner_text()

    except Exception as e:
        print("Error al obtener replies:", e)


    # ======================
    # IMAGEN
    # ======================

    has_image = False

    try:

        if tweet.locator(
            '[data-testid="tweetPhoto"]'
        ).count() > 0:

            has_image = True

    except Exception as e:
        print("Error al detectar imagen:", e)


    # ======================
    # VIDEO
    # ======================

    has_video = False

    try:

        if tweet.locator(
            '[data-testid="videoPlayer"]'
        ).count() > 0:

            has_video = True

    except Exception as e:
        print("Error al detectar video:", e)


    # TEXTO

    text = ""

    try:

        text_locator = tweet.locator(
            '[data-testid="tweetText"]'
        )

        if text_locator.count() > 0:
            text = text_locator.first.inner_text()

    except Exception as e:
        print(
            "Error al obtener texto:",
            e
        )

    # ======================
    # TWEET CITADO
    # ======================

    has_quote = False
    quoted_tweet = ""

    try:

        text_locators = tweet.locator(
            '[data-testid="tweetText"]'
        )

        if text_locators.count() > 1:

            has_quote = True

            # USERNAME DEL TWEET CITADO

            quoted_username = ""

            user_locators = tweet.locator(
                '[data-testid="User-Name"]'
            )

            if user_locators.count() > 1:

                quoted_user_text = (
                    user_locators
                    .nth(1)
                    .inner_text()
                )

                for line in quoted_user_text.split("\n"):

                    if line.startswith("@"):
                        quoted_username = line
                        break

            # FECHA DEL TWEET CITADO

            quoted_date = ""

            time_locators = tweet.locator("time")

            if time_locators.count() > 1:

                quoted_date_raw = (
                    time_locators
                    .nth(1)
                    .get_attribute("datetime")
                )

                if quoted_date_raw:
                    quoted_date = quoted_date_raw[:10]

            # TEXTO DEL TWEET CITADO

            quoted_text = (
                text_locators
                .nth(1)
                .inner_text()
            )

            # UNIR LA INFORMACIÓN

            quoted_tweet = (
                f"{quoted_username} | "
                f"{quoted_date} | "
                f"{quoted_text}"
            )

    except Exception as e:

        print(
            "Error al obtener tweet citado:",
            e
        )

    # ======================
    # HASHTAGS
    # ======================

    hashtags = []

    try:

        words = text.split()

        hashtags = [
            x
            for x in words
            if x.startswith("#")
        ]

    except Exception as e:
        print("Error al obtener hashtags:", e)


    # ======================
    # MENCIONES
    # ======================

    mentions = []

    try:

        words = text.split()

        mentions = [
            x
            for x in words
            if x.startswith("@")
        ]

    except Exception as e:
        print("Error al obtener menciones:", e)


    # FECHA

    try:

        date = (
            tweet.locator("time")
            .first
            .get_attribute("datetime")
        )

        fecha_simple = date[:10] if date else None

    except:

        date = None
        fecha_simple = None

        try:

            date = (
                tweet.locator("time")
                .first
                .get_attribute("datetime")
            )

            fecha_simple = date[:10] if date else None

        except Exception as e:
            print("Error al obtener timestamp:", e)


    return {
    "timestamp": date,
    "fecha_simple": fecha_simple,
    "username": username,
    "display_name": display_name,
    "texto": text,
    "url": tweet_url,
    "likes": likes,
    "retweets": retweets,
    "replies": replies,
    "hashtags": ", ".join(hashtags),
    "mentions": ", ".join(mentions),
    "has_image": has_image,
    "has_video": has_video,
    "has_quote": has_quote,
    "quoted_tweet": quoted_tweet
}