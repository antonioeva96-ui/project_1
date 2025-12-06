import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Percorso al file generato dall'ETL
CURATED_PATH = Path("data/curated/bicing_clean.parquet")


def load_data():
    """Carica il dataset pulito dal parquet."""
    return pd.read_parquet(CURATED_PATH)


def bikes_zero_stats(df):
    """Mostra le stazioni che risultano vuote più spesso."""
    empty_counts = (
        df[df["bikes"] == 0]
        .groupby("station_id")
        .size()
        .sort_values(ascending=False)
    )

    print("\n🔻 Top 10 stazioni più spesso vuote:")
    print(empty_counts.head(10))


def mean_bikes_by_hour(df):
    """Grafico: bici medie per ora della giornata."""
    mean_hour = df.groupby("hour")["bikes"].mean()

    plt.figure(figsize=(10, 4))
    mean_hour.plot(title="Media biciclette per ora")
    plt.xlabel("Ora del giorno")
    plt.ylabel("Bici medie")
    plt.grid(True)
    plt.show()


def mean_bikes_by_weekday(df):
    """Grafico: bici medie per giorno della settimana."""
    weekday_map = {
        0: "Lun",
        1: "Mar",
        2: "Mer",
        3: "Gio",
        4: "Ven",
        5: "Sab",
        6: "Dom",
    }
    df["weekday_name"] = df["weekday"].map(weekday_map)

    mean_week = (
        df.groupby("weekday_name")["bikes"]
        .mean()
        .reindex(["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"])
    )

    plt.figure(figsize=(8, 4))
    mean_week.plot(kind="bar", title="Media biciclette per giorno della settimana")
    plt.ylabel("Bici medie")
    plt.show()


def slots_vs_bikes(df):
    """Grafico: relazione tra capacità (slots) e biciclette presenti."""
    plt.figure(figsize=(6, 6))
    df.plot(kind="scatter", x="slots", y="bikes", alpha=0.3, title="Slots vs Bikes")
    plt.xlabel("Slots totali della stazione")
    plt.ylabel("Biciclette presenti")
    plt.show()


def main():
    print("Caricamento dataset...")
    df = load_data()

    print("\n📊 Info dataset:")
    print("Totale righe:", len(df))
    print("Totale stazioni:", df["station_id"].nunique())

    # Analisi
    bikes_zero_stats(df)
    mean_bikes_by_hour(df)
    mean_bikes_by_weekday(df)
    slots_vs_bikes(df)


if __name__ == "__main__":
    main()
