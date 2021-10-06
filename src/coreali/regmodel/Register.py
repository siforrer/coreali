from .SelectableComponent import SelectableComponent

class Register(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)
        
    def _read_has_side_effect(self):
        for child in self.node.children():
            if "onread" in child.list_properties():
                return True
        return False