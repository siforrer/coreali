from .SelectableComponent import SelectableComponent
class RegisterModel(SelectableComponent):
    def __init__(self, root, rio):
        SelectableComponent.__init__(self, root, root.top.get_path(), None, rio)
