# SAnGreeA

## Requisites
- Python 3.12

## Installation
```bash
git clone https://github.com/FearHamMonster/SocialNetworkProject.git
cd SocialNetworkProject

python -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate    # Windows

pip install -r requirements.txt  
```

## Usage
# Single Use Test
Each of the files in analysis_files analyse different aspects of the algorithm
    - time_analysis: measures how much the algorithm takes to execute (calculated on an avarage)
    - utility_analysis: measures how much information was lost after the anonyimization of the dataset
    - horizontalTimeAnalysis: measures how much time the algorithms takes (number of QI attributes customizable)
    - queryAnalysis: measures the percentage of wrong queries on the anonymized dataset

Each of these files takes a list of parameters, they can be viewed with:
```python 
python -m analysis_files.some_file_inside --help 
```
This is true for the file Sangreea.py as well, which shows the input graph, the anonymized graph, and 
prints the various metadata about the anonymized graph in the standard output 

# Multiple Tests
To automatically execute tests in batch with predefined values, simply execute the batch files in batch/tests,
(they each will take several minutes unless parameters are manually changed inside)
These batch tests will automtically save the results as plots, saved in the plots directory.

The already existing plots in plots are the results of executing each of the batch tests.


