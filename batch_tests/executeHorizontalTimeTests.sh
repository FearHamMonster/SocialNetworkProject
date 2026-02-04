#/bin/sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

CSV_FILE="csv/horizontal_time_results.csv" 
ATTR_NUM_LIST="1 2 3 4 5 6"
> "$CSV_FILE" #clear file

# Realistic dataset and graph
 for ATTR_NUM in $ATTR_NUM_LIST; do
  python -m "analysis_files.horizontalTimeAnalysis" --n 500 --k 3 --csv $CSV_FILE --real-dataset False --graph-type 0 --seed 42 --QI-attr $ATTR_NUM
 done

python -m "plotting_files.plotHorizontalTimeResults" --csv $CSV_FILE --title "Horizontal Time Tests"

