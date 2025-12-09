import pandas as pd
import folium
from pathlib import Path

AUG_CSV = Path("data/curated/critical_stations_ago2018.csv")
JAN_CSV = Path("data/curated/critical_stations_jan2019.csv")


def color_for_category(category: str) -> str:
    """
    Convert the category already present in the critical CSVs into a color.
    """
    color_map = {
        "empty_problem": "red",
        "full_problem": "blue",
        "both_problem": "purple",
        "balanced": "green",
    }
    return color_map.get(category, "gray")


def generate_combined_map(df: pd.DataFrame, month_label: str, output_name: str):
    # Center map on Barcelona
    m = folium.Map(location=[41.3851, 2.1734], zoom_start=13)

    for _, row in df.iterrows():
        lat = row["lat"]
        lon = row["long"]
        cat = row["category"]
        color = color_for_category(cat)

        popup_html = (
            f"<b>{row['streetName']}</b><br>"
            f"ID: {row['station_id']}<br>"
            f"Slots: {row['tot_slots']}<br>"
            f"mean_bikes: {row['mean_bikes']}<br>"
            f"pct_empty: {row['pct_empty']}%<br>"
            f"pct_full: {row['pct_full']}%<br>"
            f"Category: {cat}"
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.8,
            popup=popup_html,
        ).add_to(m)

    m.save(output_name)
    print(f"Combined map generated ({month_label}): {output_name}")


def main():
    df_aug = pd.read_csv(AUG_CSV)
    df_jan = pd.read_csv(JAN_CSV)

    generate_combined_map(df_aug, "August 2018", "map_ago2018.html")
    generate_combined_map(df_jan, "January 2019", "map_jan2019.html")


if __name__ == "__main__":
    main()
