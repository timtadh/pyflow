header_string =     "digraph %s {\n    node [shape=box];\n"
subgraph_prefix =   "    {\n        rank=same; \n"
node_string =       "        %s [label=%s];\n"
subgraph_postfix =  "    }\n"
edge_string =       "    %s -> %s;\n"
footer_string =     "}\n"

class Node(object):
    """Example node with the proper attributes."""
    def __init__(self, string, children=[]):
        super(Node, self).__init__()
        self.graph_id = ""
        self.string = string
        self.children = children
    
    def __str__(self):
        return self.string

node_count = 0

def ast_walk_tree(node, rank, subgraph_list=[]):
    global node_count
    node_count += 1
    node.graph_id = str(node_count)
    
    if len(subgraph_list)-1 < rank:
        subgraph_list.append([])
        
    subgraph_list[rank].append(node)
    
    for child in node.children:
        ast_walk_tree(child, rank+1, subgraph_list)
        
    return subgraph_list

def ast_dot(root, path, name="AST"):    

    
    f = open(path, 'w')
    f.write(header_string % name)
    
    global node_count
    node_count = 0
    
    subgraph_list = ast_walk_tree(root, 0, [])
    for subgraph in subgraph_list:
        f.write(subgraph_prefix)
        for node in subgraph:
            f.write(node_string % (node.graph_id, str(node)))
        f.write(subgraph_postfix)
    
    for subgraph in subgraph_list:
        for node in subgraph:
            for child in node.children:
                f.write(edge_string % (node.graph_id, child.graph_id))
    f.write(footer_string)

if __name__ == "__main__":
    n1 = Node("1", [])
    n2 = Node("2", [])
    n3 = Node("3", [n1,n2])
    n4 = Node("4", [])
    n5 = Node("5", [Node("8",[])])
    n6 = Node("6", [])
    n7 = Node("7", [n4, n5, n6])
    root = Node("root", [n3, n7])
    ast_dot(root,"AST.dot")