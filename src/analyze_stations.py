import pandas as pd
from pathlib import Path

AUG = Path("data/curated/analysis_ago2018.csv")
JAN = Path("data/curated/analysis_jan_2019.csv")

OUT_AUG = Path("data/curated/critical_stations_ago2018.csv")
OUT_JAN = Path("data/curated/critical_stations_jan2019.csv")

# soglie

empty_THRESHOLD = 20    # %
full_THRESHOLD = 20  # %


def classify_station(row):
    """
    Classificazione qualitativa:
    - empty_problem
    - full_problem
    - both_problem
    - balanced
    """
    empty = row["pct_empty"]
    full = row["pct_full"]

    if empty > empty_THRESHOLD and full > full_THRESHOLD:
        return "both_problem"
    elif empty > empty_THRESHOLD:
        return "empty_problem"
    elif full > full_THRESHOLD:
        return "full_problem"
    else:
        return "balanced"


def analyze_month(df: pd.DataFrame, label: str, output_path: Path):
    """
    Analisi delle stazioni critiche per un mese specifico.
    Ritorna e salva un CSV con solo le stazioni problematiche.
    """
    print(f"\n🔍 Analisi stazioni critiche – {label}")

    df = df.copy()
    df["category"] = df.apply(classify_station, axis=1)

    # ordiniamo per criticità: prima quelle molto problematiche
    category_priority = {
        "both_problem": 1,
        "empty_problem": 2,
        "full_problem": 3,
        "balanced": 4,
    }

    critical = df.copy()
    critical["severity"] = critical["category"].map(category_priority).fillna(5)
    critical = critical.sort_values(["severity", "pct_empty", "pct_full"], ascending=[True, False, False])

    # salvataggio
    output_path.parent.mkdir(parents=True, exist_ok=True)
    critical.to_csv(output_path, index=False)

    print(f"➡️  Salvate stazioni critiche ({label}) in: {output_path}")
    print("\nPrime righe:")
    print(critical[["station_id", "streetName", "pct_empty", "pct_full", "category"]].head(10))

    return critical


def main():
    df_aug = pd.read_csv(AUG)
    df_jan = pd.read_csv(JAN)

    analyze_month(df_aug, "Agosto 2018", OUT_AUG)
    analyze_month(df_jan, "Gennaio 2019", OUT_JAN)


if __name__ == "__main__":
    main()
