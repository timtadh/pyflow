import subprocess
import sys
import main

header_string =         "digraph %s {\n    node [shape=box];\n"
subgraph_prefix =       "    {\n        rank=same; \n"
node_string_nocolor =   "        %s [label=%s];\n"
node_string_color =     "        %s [label=%s, style=filled, fillcolor=\"%s\"];\n"
subgraph_postfix =      "    }\n"
edge_string =           "    %s -> %s;\n"
footer_string =         "}\n"

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
            if hasattr(node,"graph_color"):
                f.write(node_string_color % (node.graph_id, str(node), node.graph_color))
            else:
                f.write(node_string_nocolor % (node.graph_id, str(node)))
        f.write(subgraph_postfix)
    
    for subgraph in subgraph_list:
        for node in subgraph:
            for child in node.children:
                f.write(edge_string % (node.graph_id, child.graph_id))
    f.write(footer_string)

if __name__ == "__main__":
    import ast
    if len(sys.argv) > 1 and sys.argv[1] == 'v': 
        print 'verbose mode'
        ast.debug = 1
    else: ast.debug = 0
    c_parser = main.construct_parser()
    top = c_parser.parse(sys.stdin.read())
    ast_dot(top, "AST.dot")
    print "Running dot..."
    popen_obj = subprocess.Popen(["dot", "-Tpng",  "AST.dot",  "-o",  "AST.png"])
    print c_parser.symbol_table
    print sys.argv, sys.argv[1]
