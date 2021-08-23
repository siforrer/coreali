from .SelectableComponent import SelectableComponent
from .Field import Field
from .Memory import Memory
from .Register import Register
from .RegisterFile import RegisterFile
from systemrdl.node import FieldNode,MemNode,RegfileNode

class RegisterModel(SelectableComponent):
    """ Register model creation class that contains all blocks and registers in a hierarchical structure

    """



    def __init__(self, root, rio):
        """Construct the register model

        Args:
            root (systemrdl.node.RootNode): Hierarchical register model from the systemrdl-compiler
            rio (coreali.registerio.RegIo): Register IO that allows the access of hardware registers
        """
        SelectableComponent.__init__(self, root, root.top, None, rio)
        RegisterModel._construct(self, root.top, rio)

    @staticmethod
    def _construct(rgm, node, rio):
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