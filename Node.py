
#Tree structure for labels
class Node:
    def __init__(self, label):
        self.label = label
        self.children = []  
        self.father = None
        
    def get_label(self):
        return self.label

    def add_children(self, labels):
        self.children = labels.copy()
        for child in self.children:
            child.father = self
    
    def get_children_number(self):
        return len(self.children)

    def are_labels_descendent(self, label1, label2):
        node1 = self.get_node_by_label(label1)
        return node1.is_label_descendent(label2)
        
    def is_label_descendent(self, label):
        for child in self.children:
            if child.get_label() == label:
                return True
            if(child.is_label_descendent(label)):
                return True
        return False
    
    def generalizes(self, other):
        if self.get_label() == other.get_label():
            return False
        return self.is_label_descendent(other.get_label())
    
    def get_root(self):
        if self.father == None:
            return self
        return self.father.get_root()
    
    def count_all_leaves(self):
        root = self.get_root()
        return root.count_leaves_from_node()
            
    
    def lowest_common_ancestor(self, label1, label2):
        node1 = self.get_node_by_label(label1)
        node2 = self.get_node_by_label(label2)
        try:
            while(node1.depth() > node2.depth()):
                node1 = node1.father
        except Exception as e:
            print(e, label1, label2)
        while(node2.depth() > node1.depth()):
            node2 = node2.father
        
        while node1 != node2:
            node1 = node1.father
            node2 = node2.father

        return node1.get_label()
    
    def depth(self):
        if(self.is_root()):
            return 0
        return 1 + self.father.depth()
    
    def height_of_label(self, label):
        node = self.get_node_by_label(label)
        return node.height()

    def height(self):
        if self.is_leaf():
            return 0
        max_height = 0
        for child in self.children:
            child_height = child.height()
            if child_height > max_height:
                max_height = child_height
        return max_height + 1
    
    def cost_of_generalization(self, label1, label2):
        label_generalization = self.lowest_common_ancestor(label1, label2)
        generalization_cost = label_generalization.NCP()
        total_cost = 0
        if label_generalization.is_label_descendent(label1):
                total_cost += generalization_cost
        if label_generalization.is_label_descendent(label2):
                total_cost += generalization_cost
        return total_cost

     
    #Normalized Certainty Penalty
    def NCP(self):
        if self.is_leaf():
            return 0
        else:
            return self.count_leaves_from_node() / self.count_all_leaves()
    
    def count_leaves_from_node(self):
        if self.is_leaf():
            return 1
        else: 
            result = 0
            for child in self.children:
                result += child.count_leaves_from_node()
            return result
    
    def is_leaf(self):
        return self.children == []

    def is_root(self):
        return self.father == None
    
    def get_node_by_label(self, label):
        if self.get_label() == label:
            return self
        for child in self.children:
            result = child.get_node_by_label(label)
            if result is not None:
                return result
        return None
                
    def print_label(self):
        print(self.label)

    def print_with_DFS(self):
        self.print_label()
        
        for child in self.children:
            child.print_with_DFS()
            
@staticmethod
def getSampleTree():
    l1 = Node("l1")
    l2 = Node("l2")
    l3 = Node("l3")
    l4 = Node("l4")
    l5 = Node("l5")
    l6 = Node("l6")
    l7 = Node("l7")
    root = Node("*")
    
    root.add_children([l6,l7])
    l6.add_children([l1,l2,l3])
    l7.add_children([l4,l5])
    
    return root
    