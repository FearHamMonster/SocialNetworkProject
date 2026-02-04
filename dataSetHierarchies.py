import getQITrees as trees 

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
