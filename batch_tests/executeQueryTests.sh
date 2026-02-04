#/bin/sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

CSV_FILE="csv/query_results.csv" 
n_LIST="200 500 1000 2000"
alpha_LIST="0 0.5 1"
> "$CSV_FILE" #clear file

# Realistic dataset and graph
for n in $n_LIST; do
 for alpha in $alpha_LIST; do
  python -m "analysis_files.queryAnalysis" --n $n --k 3 --csv $CSV_FILE --real-dataset True --graph-type 0 --alpha $alpha --repetitions 100
 done
done

python -m "plotting_files.plotQueryResults" --csv $CSV_FILE --title "Realistic "

> "$CSV_FILE" #clear file

# Unrealistic dataset and graph
for n in $n_LIST; do
 for alpha in $alpha_LIST; do
  python -m "analysis_files.queryAnalysis" --n $n --k 3 --csv $CSV_FILE --real-dataset False --random-values True --graph-type 0 --alpha $alpha --repetitions 100
 done
done

python -m "plotting_files.plotQueryResults" --csv $CSV_FILE --title "Unrealistic "
