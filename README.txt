Bicing analysis e mappe critiche
---------------------------------

Requisiti
- Python 3
- pandas, folium
- Dataset parquet: data/curated/bicing_clean.parquet

Workflow
1) Genera le analisi mensili (frequenza stazioni vuote/piene)
   python src/eda_bicing.py
   - Output: data/curated/analysis_ago2018.csv e data/curated/analysis_jan_2019.csv
   - Calcoli: pct_empty = (times_total_empty / total_observations) * 100; pct_full analogo.

2) Classifica stazioni e salva CSV critici (inclusi balanced)
   python src/analyze_stations.py
   - Legge i CSV di analisi.
   - Assegna category: empty_problem, full_problem, both_problem, balanced (soglie 20%).
   - Ordina per severity e salva:
     data/curated/critical_stations_ago2018.csv
     data/curated/critical_stations_jan2019.csv

3) Genera le mappe interattive
   python src/map_bicing.py
   - Legge i CSV critici.
   - Colori: red=empty_problem, blue=full_problem, purple=both_problem, green=balanced.
   - Popup: nome stazione, ID, slot totali, mean_bikes, pct_empty, pct_full, categoria.
   - Output: mappa_combined_ago2018.html, mappa_combined_jan2019.html   

Note rapide
- I CSV critici includono anche le stazioni balanced, ordinate per severità.
- Se vuoi cambiare le soglie di criticità, modifica empty_THRESHOLD e full_THRESHOLD in src/analyze_stations.py.
