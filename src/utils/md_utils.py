from src.ast_node import ASTNode, Constant,Variable

def create_md_tree(node):
    def dfs(node):
        md = ""
        if node.children:
            for child in node.children:
                md += f"\n    {id(node)}[{get_md_string(node)}]-->{id(child)}[{get_md_string(child)}];"
                md += dfs(child)
        return md
    md = f"```mermaid\ngraph TD;" + dfs(node)
    with open("tree.md", "w") as file:
        file.write(md)

def get_md_string(node):
    if isinstance(node, Constant):
        return node.value[0][0]
    elif isinstance(node, Variable):
        return f"$$X_{node.index_of_value}$$"
    elif isinstance(node, ASTNode):
        return node.operation
    else:
        raise ValueError("Node must be Constant, Variable or ASTTreeNode")
