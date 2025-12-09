Bicing analysis and critical maps
---------------------------------

Requirements
- Python 3
- pandas, folium
- Parquet dataset: data/curated/bicing_clean.parquet

Workflow
1) Generate the monthly analyses (frequency of empty/full stations)
   python src/eda_bicing.py
   - Output: data/curated/analysis_ago2018.csv and data/curated/analysis_jan_2019.csv

2) Classify stations and save critical CSVs (including balanced)
   python src/analyze_stations.py
   - Reads the analysis CSVs.
   - Assigns category: empty_problem, full_problem, both_problem, balanced (20% thresholds).
   - Sorts by severity and saves:
     data/curated/critical_stations_ago2018.csv
     data/curated/critical_stations_jan2019.csv

3) Generate interactive maps
   python src/map_bicing.py
   - Reads the critical CSVs.
   - Colors: red=empty_problem, blue=full_problem, purple=both_problem, green=balanced.
   - Popup: station name, ID, total slots, mean_bikes, pct_empty, pct_full, category.
   - Output: mappa_combined_ago2018.html, mappa_combined_jan2019.html

Quick notes
- The critical CSVs also include balanced stations, sorted by severity.
- To change the criticality thresholds, update empty_THRESHOLD and full_THRESHOLD in src/analyze_stations.py.
