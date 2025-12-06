import pandas as pd
from pathlib import Path

# Input: parquet pulito generato dall'ETL
CURATED_PATH = Path("data/curated/bicing_clean.parquet")

# Output CSV
OUT_AUG = Path("data/curated/analysis_ago2018.csv")
OUT_JAN = Path("data/curated/analysis_jan_2019.csv")


def build_month_analysis(df_month: pd.DataFrame) -> pd.DataFrame:
    """
    Crea la tabella di analisi per un singolo mese.

    Colonne finali:
      station_id,
      streetName,
      long,
      lat,
      tot_slots,
      mean_bikes,
      mean_free_slots,
      total_observations,
      times_total_empty,
      times_total_full,
      pct_empty,
      pct_full
    """

    df_month = df_month.copy()

    # Flag per stazione vuota e stazione piena
    df_month["is_empty"] = (df_month["bikes"] == 0).astype(int)
    df_month["is_full"] = (df_month["slots"] == 0).astype(int)

    group_cols = ["station_id", "streetName", "longitude", "latitude"]

    agg = (
        df_month
        .groupby(group_cols)
        .agg(
            tot_slots=("slots", "max"),              # capacità totale stazione
            mean_bikes=("bikes", "mean"),            # bici medie
            total_observations=("bikes", "size"),    # numero rilevazioni
            times_total_empty=("is_empty", "sum"),   # volte bikes == 0
            times_total_full=("is_full", "sum"),     # volte slots == 0
        )
        .reset_index()
    )

    # Arrotonda mean_bikes prima di usarla
    agg["mean_bikes"] = agg["mean_bikes"].round(1)

    # 🚀 NUOVA COLONNA: mean_free_slots = tot_slots - mean_bikes
    agg["mean_free_slots"] = (agg["tot_slots"] - agg["mean_bikes"]).round(1)

    # Percentuali di volte vuota/piena
    agg["pct_empty"] = (
        agg["times_total_empty"] / agg["total_observations"] * 100
    ).round(2)

    agg["pct_full"] = (
        agg["times_total_full"] / agg["total_observations"] * 100
    ).round(2)

    # Rinomina coordinate
    agg = agg.rename(columns={
        "longitude": "long",
        "latitude": "lat",
    })

    # Ordine delle colonne (come richiesto)
    agg = agg[
        [
            "station_id",
            "streetName",
            "long",
            "lat",
            "tot_slots",
            "mean_bikes",
            "mean_free_slots",     # <-- nuova colonna al posto giusto
            "total_observations",
            "times_total_empty",
            "times_total_full",
            "pct_empty",
            "pct_full",
        ]
    ]

    # Ordina per ID stazione
    agg = agg.sort_values("station_id")

    return agg


def main():
    print("Caricamento dataset completo...")
    df = pd.read_parquet(CURATED_PATH)

    # Colonne temporali
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month

    # Agosto 2018
    df_aug_2018 = df[(df["year"] == 2018) & (df["month"] == 8)]
    print(f"Righe agosto 2018: {len(df_aug_2018)}")
    aug_analysis = build_month_analysis(df_aug_2018)
    OUT_AUG.parent.mkdir(parents=True, exist_ok=True)
    aug_analysis.to_csv(OUT_AUG, index=False)
    print(f"Salvato: {OUT_AUG}")

    # Gennaio 2019
    df_jan_2019 = df[(df["year"] == 2019) & (df["month"] == 1)]
    print(f"Righe gennaio 2019: {len(df_jan_2019)}")
    jan_analysis = build_month_analysis(df_jan_2019)
    jan_analysis.to_csv(OUT_JAN, index=False)
    print(f"Salvato: {OUT_JAN}")


if __name__ == "__main__":
    main()
