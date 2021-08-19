from .SelectableComponent import SelectableComponent
from .Field import Field
from .Memory import Memory
from .Register import Register
from .RegisterFile import RegisterFile
from systemrdl.node import FieldNode,MemNode,RegfileNode

class RegisterModel(SelectableComponent):
    
    @staticmethod
    def construct(rgm, node, rio):
        for child in node.children():
            if isinstance(child, (FieldNode)):
                rgm.__dict__[child.inst_name] = Field(rgm._root, child , rgm, rio)
            elif isinstance(child, (MemNode)):
                rgm.__dict__[child.inst_name] = Memory(rgm._root, child , rgm, rio)
            elif isinstance(child, (RegfileNode)):
                rgm.__dict__[child.inst_name] = RegisterFile(rgm._root, child , rgm, rio)
            else:
                rgm.__dict__[child.inst_name] = Register(rgm._root, child , rgm, rio)
            RegisterModel.construct(rgm.__dict__[child.inst_name], child, rio)

    def __init__(self, root, rio):
        SelectableComponent.__init__(self, root, root.top, None, rio)
        RegisterModel.construct(self, root.top, rio)
