from pathlib import Path

import pandas as pd


RAW_FILES = [
    Path("data/raw/bicing_2018_08.csv"),
    Path("data/raw/bicing_2019_01.csv"),
]

CURATED_PATH = Path("data/curated/bicing_clean.parquet")


def load_and_concat(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def run_etl():
    df = load_and_concat(RAW_FILES)

    # Rinomino id per chiarezza
    df = df.rename(columns={"id": "station_id"})

    # Converto la data/ora: es. "01/08/18 17:43:08"
    df["timestamp"] = pd.to_datetime(
        df["updateTime"], format="%d/%m/%y %H:%M:%S", errors="coerce"
    )

    # Rimuovo eventuali righe senza timestamp valido
    df = df.dropna(subset=["timestamp"])

    # Cast a tipi numerici
    df["bikes"] = pd.to_numeric(df["bikes"], errors="coerce")
    df["slots"] = pd.to_numeric(df["slots"], errors="coerce")
    df["altitude"] = pd.to_numeric(df["altitude"], errors="coerce")

    # Di nuovo, tolgo righe proprio rotte
    df = df.dropna(subset=["bikes", "slots"])

    # Feature temporali
    df["hour"] = df["timestamp"].dt.hour
    df["weekday"] = df["timestamp"].dt.weekday  # 0=Lunedì, 6=Domenica
    df["is_weekend"] = df["weekday"].isin([5, 6]).astype(int)

    # Flag stazione vuota
    df["is_empty"] = (df["bikes"] == 0).astype(int)

    # Creo cartella curated se non esiste
    CURATED_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Salvo in Parquet
    df.to_parquet(CURATED_PATH, index=False)

    print(f"Righe finali: {len(df)}")
    print(f"Salvato in: {CURATED_PATH}")


if __name__ == "__main__":
    run_etl()
