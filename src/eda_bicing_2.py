import pandas as pd
from pathlib import Path

CURATED_PATH = Path("data/curated/bicing_clean.parquet")
OUTPUT_PATH = Path("data/curated/station_bike_means.csv")


def main():
    print("Caricamento dataset...")
    df = pd.read_parquet(CURATED_PATH)

    # Colonne temporali
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month

    # Filtri periodi disponibili
    df_jan_2019 = df[(df["year"] == 2019) & (df["month"] == 1)]
    df_aug_2018 = df[(df["year"] == 2018) & (df["month"] == 8)]

    # Media bici per stazione in gennaio 2019
    jan_mean = (
        df_jan_2019
        .groupby(["station_id", "streetName"])["bikes"]
        .mean()
        .round()
        .reset_index(name="mean_bikes_jan_2019")
    )

    # Media bici per stazione in agosto 2018
    aug_mean = (
        df_aug_2018
        .groupby(["station_id", "streetName"])["bikes"]
        .mean()
        .round()
        .reset_index(name="mean_bikes_aug_2018")
    )

    # Numero volte vuota in tutto il dataset
    empty_counts = (
        df.groupby(["station_id", "streetName"])["is_empty"]
        .sum()
        .reset_index(name="times_empty")
    )

    # Numero totale osservazioni per station_id (per calcolo percentuale)
    total_counts = (
        df.groupby(["station_id", "streetName"])["is_empty"]
        .count()
        .reset_index(name="total_observations")
    )

    # Merge
    result = (
        jan_mean
        .merge(aug_mean, on=["station_id", "streetName"], how="outer")
        .merge(empty_counts, on=["station_id", "streetName"], how="left")
        .merge(total_counts, on=["station_id", "streetName"], how="left")
    )

    # Calcolo percentuale volte vuota
    result["pct_empty"] = (
        result["times_empty"] / result["total_observations"] * 100
    ).round(2)

    # Ordina per ID stazione
    result = result.sort_values("station_id")

    print("\nPrime 10 righe del risultato:")
    print(result.head(10))

    # Salvataggio CSV
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)
    print(f"\nTabella salvata in: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
