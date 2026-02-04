#/bin/sh
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

CSV_FILE="csv/time_results.csv" 
k_LIST="2 5 10 50"
n_LIST=" 50 100 200 300 400 500 1000"
> "$CSV_FILE" #clear file

# Realistic dataset and graph
for k in $k_LIST; do
 for n in $n_LIST; do
  python -m "analysis_files.timeAnalysis" --n $n --k $k --csv $CSV_FILE --real-dataset False --graph-type 0 --seed 42
 done
done

python -m "plotting_files.plotTimeResults" --csv $CSV_FILE --title "Realistic dataset and graph"

> "$CSV_FILE" #clear file

# Realistic dataset and graph with different dataset/graph each repetition
for k in $k_LIST; do
 for n in $n_LIST; do
  python -m "analysis_files.timeAnalysis" --n $n --k $k --csv $CSV_FILE --real-dataset False --graph-type 0 --seed 42 --same-dataset False
 done
done

python -m "plotting_files.plotTimeResults" --csv $CSV_FILE --title "Realistic dataset and graph (different each rep)"


> "$CSV_FILE" #clear file

# Unrealistic dataset and graph 
for k in $k_LIST; do
 for n in $n_LIST; do
  python -m "analysis_files.timeAnalysis" --n $n --k $k --csv $CSV_FILE --real-dataset False --random-values True --graph-type 1 --avarage-degree 10 --seed 42
 done
done

python -m "plotting_files.plotTimeResults" --csv $CSV_FILE --title "Unrealistic dataset and graph"


