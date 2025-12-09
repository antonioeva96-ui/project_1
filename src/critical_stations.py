import pandas as pd
from pathlib import Path

AUG = Path("data/curated/station_metrics_2018_08.csv")
JAN = Path("data/curated/station_metrics_2019_01.csv")

OUT_AUG = Path("data/curated/critical_stations_ago2018.csv")
OUT_JAN = Path("data/curated/critical_stations_jan2019.csv")

# thresholds
empty_THRESHOLD = 20    # %
full_THRESHOLD = 20     # %


def classify_station(row):
    """
    Qualitative classification:
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
    Analyze critical stations for a specific month.
    Returns and saves a CSV with the stations ordered by severity.
    """
    print(f"\nAnalyzing critical stations - {label}")

    df = df.copy()
    df["category"] = df.apply(classify_station, axis=1)

    # Sort by severity: the most problematic first
    category_priority = {
        "both_problem": 1,
        "empty_problem": 2,
        "full_problem": 3,
        "balanced": 4,
    }

    critical = df.copy()
    critical["severity"] = critical["category"].map(category_priority).fillna(5)
    critical = critical.sort_values(["severity", "pct_empty", "pct_full"], ascending=[True, False, False])

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    critical.to_csv(output_path, index=False)

    print(f"Saved critical stations ({label}) to: {output_path}")
    print("\nTop rows:")
    print(critical[["station_id", "streetName", "pct_empty", "pct_full", "category"]].head(10))

    return critical


def main():
    df_aug = pd.read_csv(AUG)
    df_jan = pd.read_csv(JAN)

    analyze_month(df_aug, "August 2018", OUT_AUG)
    analyze_month(df_jan, "January 2019", OUT_JAN)


if __name__ == "__main__":
    main()
