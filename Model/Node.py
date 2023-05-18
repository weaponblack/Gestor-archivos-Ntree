class Node:

    def __init__(self, data):
        self.data = data
        self.left_node = None
        self.right_node = None

    def getList(self):
        return list

    def setList(self, list):
        self.list = list

    # Insertar nodo forma recursiva
    def insertNode(self, data):
        self.__auxInsertNode(data, self.root)

    def __auxInsertNode(self, data, root):
        if data < root.data:
            if root.left_node is None:
                root.left_node = Node(data)
            else:
                self.__auxInsertNode(data, root.left_node)
        if data > root.data:
            if root.right_node is None:
                root.right_node = Node(data)
            else:
                self.__auxInsertNode(data, root.right_node)

    def inOrden(self, Temp):
        if Temp is not None:
            self.inOrden(Temp.getIzq())
            self.list.append(Temp.getDato())
            self.inOrden(Temp.getDer())
        else:
            self.total += 1

    def preOrden(self, Temp):
        if Temp is not None:
            self.list.append(Temp.getDato())
            self.preOrden(Temp.getIzq())
            self.preOrden(Temp.getDer())

    def postOrden(self, Temp):
        if Temp is not None:
            self.postOrden(Temp.getIzq())
            self.postOrden(Temp.getDer())
            self.list.append(Temp.getDato())