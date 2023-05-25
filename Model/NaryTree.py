from Model.NaryTreeNode import NaryTreeNode


class NaryTree:
    def __init__(self):
        self.root = None

    def add_node(self, data, parent=None):
        new_node = NaryTreeNode(data)
        if parent is None:
            self.root = new_node
        else:

            for node in self.__find_node(parent.name, self.root):

                node.children.append(new_node)

    def __find_node(self, data, current_node):
        nodes = []
        if current_node.data.name == data:
            nodes.append(current_node)
        for child in current_node.children:
            nodes += self.__find_node(data, child)
        return nodes

    def find_node(self, data):
        nodes = self.__find_node(data, self.root)
        if nodes:
            return nodes[0]
        return None
