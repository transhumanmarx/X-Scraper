import pandas as pd


def create_dataframe(
    tweets_data: list[dict],
) -> pd.DataFrame:
    
    """
    Convierte la lista de tweets en un DataFrame  de pandas
    para facilitar su procesamiento y exportación.
    """
    return pd.DataFrame(tweets_data)

def export_to_excel(
    df: pd.DataFrame,
    output_path: str,
) -> None:
    """
    Exporta el DataFrame a un archivo Excel utilizando OpenPyXL.
    """
    df.to_excel(
        output_path,
        index=False,
        engine="openpyxl"
    )