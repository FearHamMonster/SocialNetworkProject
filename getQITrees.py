from Node import Node


def get_workclass_tree():
    root = Node("*")
    root.add_children([Node("Private"), Node("Self-emp-not-inc"), Node("Self-emp-inc"), Node("Federal-gov"), Node("Local-gov"), Node("State-gov"), Node("Without-pay"), Node("Never-worked")])
    return root

def get_maritalstatus_tree():
    root = Node("*")
    married = Node("Married")
    notmarried = Node("Not-Married")
    root.add_children([married, notmarried])
    married.add_children([Node("Married-civ-spouse"), Node("Married-spouse-absent"), Node("Married-AF-spouse")])
    notmarried.add_children([Node("Divorced"), Node("Never-married"), Node("Separated"), Node("Widowed")])
    return root

def get_race_tree():
    root = Node("*")
    root.add_children([Node("White"), Node("Asian-Pac-Islander"), Node("Amer-Indian-Eskimo"), Node("Other"), Node("Black")])
    return root


def get_sex_tree():
    root = Node("*")
    root.add_children([Node("Male"), Node("Female")])
    return root

def get_nativecountry_tree():
    root = Node("*")
    america = Node("America")
    europe = Node("Europe")
    asia = Node("Asia")
    africa = Node("Africa")
    
    north_a = Node("North-America")
    central_a = Node("Central-America")
    south_a = Node("South-America")
    
    west_europe = Node("West-Europe")
    east_europe = Node("East-Europe")

    west_asia = Node("West-Asia")
    east_asia = Node("East-Asia")
    
    north_africa = Node("North-Africa")
    south_africa = Node("South-Africa")
    
    
    root.add_children([america, europe, asia, africa])
    america.add_children([north_a, central_a, south_a])
    europe.add_children([west_europe, east_europe])
    asia.add_children([west_asia, east_asia])
    africa.add_children([north_africa, south_africa])
    
    north_a.add_children([Node("United-States"), Node("Canada"), Node("Outlying-US(Guam-USVI-etc)")])
    south_a.add_children([Node("Ecuador"), Node("Columbia"), Node("Peru")])
    central_a.add_children([Node("Puerto-Rico"), Node("Cuba"), Node("Honduras"), Node("Jamaica"), Node("Mexico"), Node("Dominican-Republic"), Node("Haiti"), Node("Guatemala"), Node("Nicaragua"), Node("El-Salvador"), Node("Trinadad&Tobago")])
    north_africa.add_children([])
    south_africa.add_children([Node("South")])
    west_asia.add_children([Node("India"), Node("Iran")]), 
    east_asia.add_children([Node("Cambodia"), Node("Japan"), Node("China"), Node("Philippines"), Node("Vietnam"), Node("Laos"), Node("Taiwan"), Node("Thailand"), Node("Hong")])
    west_europe.add_children([Node("England"), Node("Germany"), Node("Italy"), Node("Portugal"), Node("Ireland"), Node("France"), Node("Scotland"),Node("Holand-Netherlands")])
    east_europe.add_children([Node("Greece"), Node("Poland"), Node("Hungary"), Node("Yugoslavia")])
    
    return root
    