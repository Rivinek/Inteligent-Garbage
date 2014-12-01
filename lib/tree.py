import uuid


def sanitize_id(id):
    return id.strip().replace(" ", "")

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)


class Node:

    def __init__(self, name, identifier=None, condicional=None, expanded=True):
        self.__identifier = (
            str(uuid.uuid1()) if identifier is None else sanitize_id(
                str(identifier)
            )
        )
        self.name = name
        self.expanded = expanded
        self.__bpointer = None
        self.__fpointer = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def bpointer(self):
        return self.__bpointer

    @bpointer.setter
    def bpointer(self, value):
        if value is not None:
            self.__bpointer = sanitize_id(value)

    @property
    def fpointer(self):
        return self.__fpointer

    def update_fpointer(self, identifier, mode=_ADD):
        if mode is _ADD:
            self.__fpointer.append(sanitize_id(identifier))
        elif mode is _DELETE:
            self.__fpointer.remove(sanitize_id(identifier))
        elif mode is _INSERT:
            self.__fpointer = [sanitize_id(identifier)]


class Tree:

    def __init__(self):
        self.nodes = []

    def get_index(self, position):
        for index, node in enumerate(self.nodes):
            if node.identifier == position:
                break
        return index

    def create_node(self, name, identifier=None, parent=None):

        node = Node(name, identifier)
        self.nodes.append(node)
        self.__update_fpointer(parent, node.identifier, _ADD)
        node.bpointer = parent
        return node

    def show(self, position, level=_ROOT):
        queue = self[position].fpointer
        if level == _ROOT:
            print("{0} [{1}]".format(self[position].name,
                                     self[position].identifier))
        else:
            print("\t"*level, "{0} [{1}]".format(self[position].name,
                                                 self[position].identifier))
        if self[position].expanded:
            level += 1
            for element in queue:
                self.show(element, level)  # recursive call

    def show_from_root(self, level=_ROOT):
        position = self.nodes[0].identifier
        queue = self[position].fpointer
        if level == _ROOT:
            print("{0} [{1}]".format(self[position].name,
                                     self[position].identifier))
        else:
            print("\t"*level, "{0} [{1}]".format(self[position].name,
                                                 self[position].identifier))
        if self[position].expanded:
            level += 1
            for element in queue:
                self.show(element, level)

    def predict(
        self, position, trash, level=_ROOT, tmp=[]
    ):
        queue = self[position].fpointer
        join_names = lambda *args: ':'.join(args)
        toxicity = join_names('toxicity', trash.toxicity, 'True')
        time = join_names('time', trash.time, 'True')
        way = join_names('way', trash.way, 'True')
        if level == _ROOT:
            pass
        if self[position].identifier+':True' in [toxicity, time, way]:
            trash.level = level

        if self[position].expanded:
            level += 1
            for element in queue:
                self.predict(
                    element,
                    level=level,
                    trash=trash,
                    tmp=tmp
                )

    def expand_tree(self, position, mode=_DEPTH):
        yield position
        queue = self[position].fpointer
        while queue:
            yield queue[0]
            expansion = self[queue[0]].fpointer
            if mode is _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode is _WIDTH:
                queue = queue[1:] + expansion  # width-first

    def is_branch(self, position):
        return self[position].fpointer

    def __update_fpointer(self, position, identifier, mode):
        if position is None:
            return
        else:
            self[position].update_fpointer(identifier, mode)

    def __update_bpointer(self, position, identifier):
        self[position].bpointer = identifier

    def __getitem__(self, key):
        return self.nodes[self.get_index(key)]

    def __setitem__(self, key, item):
        self.nodes[self.get_index(key)] = item

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, identifier):
        return [node.identifier for node in self.nodes
                if node.identifier is identifier]