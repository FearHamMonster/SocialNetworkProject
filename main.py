import getQITrees as trees
import generateGraph as graphgen
import anon 
import random
import GraphUtilities as utils
attributes_type = {
                   "age" : "numerical",
                   "workclass" : "categorical",
                   "marital-status" : "categorical",
                   "race" : "categorical",
                   "sex" : "categorical",
                   "native-country" : "categorical"
}

gen_trees = {
    "workclass" : trees.get_workclass_tree(),
    "marital-status" : trees.get_maritalstatus_tree(),
    "race" : trees.get_race_tree(),
    "sex" : trees.get_sex_tree(),
    "native-country" : trees.get_nativecountry_tree()
}

G = graphgen.generate_powerlaw_graph(0.2, 4, 10, from_dataset=False)
anon.SaNGreeA(G, 3, attributes_type, gen_trees, show_masked=False)




