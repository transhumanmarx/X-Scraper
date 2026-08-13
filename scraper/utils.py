from datetime import datetime, timedelta
from urllib.parse import quote

def create_daily_windows(
        start_date: str,
        end_date: str
) -> list[tuple[str, str]]:


    
    """
    Genera una lista de consultas diarias entre dos fechas. 
    Cada elemento contiene la fecha que se utilizará tanto en
    los parámetros `since` como `until` de la búsqueda en X.
    """

    windows = []

    current = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    while current <= end:

        windows.append(
            (
                current.strftime("%Y-%m-%d"),
                current.strftime("%Y-%m-%d")
            )
        )

        current += timedelta(days=1)

    return windows


def build_search_url(
    account: str,
    start_day: str,
    end_day: str
) -> str:

    """
    Construye la URL de búsqueda avanzada de X para una cuenta y un
    intervalo de fechas determinado.
    """
    
    query = f"(from:{account}) since:{start_day} until:{end_day}"

    return (
        "https://x.com/search?q="
        + quote(query)
        + "&src=typed_query&f=live"
    )