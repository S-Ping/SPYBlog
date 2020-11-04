class Tree:
    def __init__(self, tree_list: list, field: str, join_field: str):
        self.tree_list = tree_list
        self.field = field
        self.join_field = join_field

    def generate(self):
        for n1 in self.tree_list:
            n1.setdefault('children', [])
            for n2 in self.tree_list:
                assert self.join_field in n2
                if n2[self.join_field] == n1[self.field]:
                    n1['children'].append(n2)
        tree = []
        for node in self.tree_list:
            if not node[self.join_field]:
                tree.append(node)
        return tree
