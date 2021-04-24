from .SelectableComponent import SelectableComponent

class RegisterFile(SelectableComponent):
    def __init__(self, root, path, parent, rio):
        SelectableComponent.__init__(self, root, path, parent, rio)
        