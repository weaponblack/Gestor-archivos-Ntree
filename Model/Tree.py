from Model.Node import *


class BTree:

    def __init__(self, data):
        self.root = Node(data)  # Nodo*
        self.list = []
        self.total = 0