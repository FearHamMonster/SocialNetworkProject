#/bin/sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

CSV_FILE="csv/utility_results.csv" 
k_LIST="2 3 5 10 50"
alpha_LIST="0 0.5 1"
> "$CSV_FILE" #clear file

# Realistic dataset and graph
for k in $k_LIST; do
 for alpha in $alpha_LIST; do
  python -m "analysis_files.utilityAnalysis" --n 500 --k $k --csv $CSV_FILE --real-dataset True --graph-type 0  --p 0.4 --alpha $alpha --seed 42
 done
done

python -m "plotting_files.plotUtilityResults" --csv $CSV_FILE --title "p=0.4"

> "$CSV_FILE" #clear file

# Realistic dataset and graph
for k in $k_LIST; do
 for alpha in $alpha_LIST; do
  python -m "analysis_files.utilityAnalysis" --n 500 --k $k --csv $CSV_FILE --real-dataset True --graph-type 0 --p 0.95 --alpha $alpha --seed 42
 done
done

python -m "plotting_files.plotUtilityResults" --csv $CSV_FILE --title "p=0.95"