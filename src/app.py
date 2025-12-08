import streamlit as st
import pandas as pd
from pathlib import Path
import folium
from streamlit_folium import st_folium

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "curated"

AUG_CSV = DATA_DIR / "critical_stations_ago2018.csv"
JAN_CSV = DATA_DIR / "critical_stations_jan2019.csv"

COLOR_MAP = {
    "empty_problem": "red",
    "full_problem": "blue",
    "both_problem": "purple",
    "balanced": "green",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    df_aug = pd.read_csv(AUG_CSV)
    df_jan = pd.read_csv(JAN_CSV)
    df_aug["month"] = "Agosto 2018"
    df_jan["month"] = "Gennaio 2019"
    combined = pd.concat([df_aug, df_jan], ignore_index=True)
    return combined


def color_for_category(category: str) -> str:
    return COLOR_MAP.get(category, "gray")


def make_map(df: pd.DataFrame) -> folium.Map:
    m = folium.Map(location=[41.3851, 2.1734], zoom_start=13)
    for _, row in df.iterrows():
        color = color_for_category(row["category"])
        popup_html = (
            f"<b>{row['streetName']}</b><br>"
            f"ID: {row['station_id']}<br>"
            f"Slot totali: {row['tot_slots']}<br>"
            f"mean_bikes: {row['mean_bikes']}<br>"
            f"pct_empty: {row['pct_empty']}%<br>"
            f"pct_full: {row['pct_full']}%<br>"
            f"Categoria: {row['category']}"
        )
        folium.CircleMarker(
            location=[row["lat"], row["long"]],
            radius=6,
            color=color,
            fill=True,
            fill_opacity=0.85,
            popup=popup_html,
        ).add_to(m)
    return m


def main():
    st.set_page_config(page_title="Bicing Critical Stations", layout="wide")
    st.title("Bicing Critical Stations")
    st.caption("Dashboard interattiva su stazioni critiche (Agosto 2018 vs Gennaio 2019)")

    df = load_data()

    with st.sidebar:
        st.header("Filtri")
        month = st.selectbox("Mese", sorted(df["month"].unique()))
        categories = st.multiselect(
            "Categoria",
            options=list(COLOR_MAP.keys()),
            default=list(COLOR_MAP.keys()),
        )
        severity_min, severity_max = int(df["severity"].min()), int(df["severity"].max())
        severity_range = st.slider(
            "Severita",
            min_value=severity_min,
            max_value=severity_max,
            value=(severity_min, severity_max),
        )
        mean_min, mean_max = float(df["mean_bikes"].min()), float(df["mean_bikes"].max())
        mean_range = st.slider(
            "mean_bikes range",
            min_value=mean_min,
            max_value=mean_max,
            value=(mean_min, mean_max),
        )

    filtered = df[
        (df["month"] == month)
        & (df["category"].isin(categories))
        & (df["severity"].between(severity_range[0], severity_range[1]))
        & (df["mean_bikes"].between(mean_range[0], mean_range[1]))
    ]

    col1, col2, col3 = st.columns(3)
    col1.metric("Stazioni filtrate", len(filtered))
    col2.metric(
        "mean_bikes medio",
        round(filtered["mean_bikes"].mean(), 1) if not filtered.empty else "-",
    )
    col3.metric(
        "% empty medio",
        f"{filtered['pct_empty'].mean():.1f}%" if not filtered.empty else "-",
    )

    st.subheader("Distribuzione slot per categoria")
    if filtered.empty:
        st.warning("Nessuna stazione con i filtri selezionati.")
        return

    st.bar_chart(filtered.groupby("category")["tot_slots"].sum())

    st.subheader("Mappa")
    st_folium(make_map(filtered), height=550, width=1100)

    st.subheader("Dettaglio dati")
    st.dataframe(
        filtered.sort_values(
            ["severity", "pct_empty", "pct_full"], ascending=[False, False, False]
        )[
            [
                "station_id",
                "streetName",
                "tot_slots",
                "mean_bikes",
                "pct_empty",
                "pct_full",
                "category",
                "severity",
            ]
        ]
    )


if __name__ == "__main__":
    main()
