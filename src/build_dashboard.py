from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/curated/station_bike_means.csv")
OUTPUT_HTML = Path("dashboard.html")


def main():
    # Leggi la tabella con le medie e le percentuali
    df = pd.read_csv(DATA_PATH)

    # Converte il DataFrame in HTML (solo tabella)
    table_html = df.to_html(
        index=False,
        classes="data-table",
        border=0,
        justify="center"
    )

    # Template HTML molto semplice
    html_page = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Bicing – Dashboard stazioni</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            text-align: center;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }}
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        table.data-table thead {{
            background-color: #1976d2;
            color: white;
        }}
        table.data-table th, table.data-table td {{
            padding: 8px 10px;
            border-bottom: 1px solid #ddd;
            text-align: center;
        }}
        table.data-table tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        table.data-table tr:hover {{
            background-color: #e3f2fd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Bicing – Stazioni e disponibilità media</h1>
        <p>
            Per ogni stazione: nome, bici medie a gennaio 2019, bici medie ad agosto 2018,
            numero di volte in cui era vuota e percentuale di vuoto.
        </p>
        {table_html}
    </div>
</body>
</html>
"""

    # Scrive il file HTML
    OUTPUT_HTML.write_text(html_page, encoding="utf-8")
    print(f"Dashboard generata: {OUTPUT_HTML.resolve()}")


if __name__ == "__main__":
    main()
