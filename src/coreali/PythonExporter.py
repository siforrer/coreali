# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 09:50:05 2021

@author: FSIL
"""
import os

import jinja2 as jj
from systemrdl.node import RootNode, Node, RegNode, AddrmapNode, RegfileNode
from systemrdl.node import FieldNode, MemNode, AddressableNode

class PythonExporter:
    def __init__(self):

        loader = jj.ChoiceLoader([
            jj.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
            jj.PrefixLoader({
                'base': jj.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))
            }, delimiter=":")
        ])

        self.jj_env = jj.Environment(
            loader=loader,
            undefined=jj.StrictUndefined
        )

        self.top = None
        self.namespace_db = {}
        self.source_files = []

    def export(self, node: Node, path: str):
        if isinstance(node, RootNode):
            node = node.top
        self.top = node

        context = {
            'top_node': node,
            'RegNode': RegNode,
            'FieldNode': FieldNode,
            'RegfileNode': RegfileNode,
            'AddrmapNode': AddrmapNode,
            'MemNode': MemNode,
            'AddressableNode': AddressableNode,
            'isinstance': isinstance,
            'class_needs_definition': self._class_needs_definition,
            'get_class_name': self._get_class_name,
            'source_files': self.source_files
        }


        template = self.jj_env.get_template("regmodel.py")
        stream = template.stream(context)
        stream.dump(path)
        
    def _get_class_name(self, node: Node) -> str:
        class_name = node.get_rel_path(
            self.top.parent,
            hier_separator="_", array_suffix="", empty_array_suffix=""
        )

        return class_name

    def _class_needs_definition(self, node: Node) -> bool:
        type_name = self._get_class_name(node)

        if type_name in self.namespace_db:
            obj = self.namespace_db[type_name]

            if (obj is None) or (obj is not node.inst.original_def):
                raise RuntimeError("Namespace collision! Type-name generation is not robust enough to create unique names!")

            return False

        self.namespace_db[type_name] = node.inst.original_def
        return True

