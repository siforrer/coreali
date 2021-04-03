from coreali.regmodel import AccessableNode,AccessableFieldNode,AccessableMemNode, AccessableTopNode


{% macro class_definition(node) -%}
{%- if class_needs_definition(node) %}
class {{get_class_name(node)}}(AccessableNode):
    def __init__(self, root, path, parent, rio):
        AccessableNode.__init__(self,root, path, parent, rio)
        {{child_insts(node)|indent|indent}}
{% endif -%}
{%- endmacro -%}

{% macro class_definition_top_node(node) -%}
{%- if class_needs_definition(node) %}
class {{get_class_name(node)}}(AccessableTopNode):
    def __init__(self, rio):
        AccessableTopNode.__init__(self, {{source_files}}, rio)
        {{child_insts(node)|indent|indent}}
{% endif -%}
{%- endmacro -%}

{%- macro child_insts(node) -%}
{%- for child in node.children() -%}
    {%- if isinstance(child, (FieldNode)) -%}
self.{{child.inst_name}} = AccessableFieldNode(self._root, self.node.get_path(empty_array_suffix="") + ".{{child.inst_name}}", self)
    {%- elif isinstance(child, (MemNode)) -%}
self.{{child.inst_name}} = AccessableMemNode(self._root, self.node.get_path(empty_array_suffix="") + ".{{child.inst_name}}", self, rio)
    {%- else -%}
self.{{child.inst_name}} = {{get_class_name(child)}}(self._root, self.node.get_path(empty_array_suffix="") + ".{{child.inst_name}}", self, rio)
    {%- endif %}
{% endfor -%}
{%- endmacro %}


{% macro top() -%}
    {%- for node in top_node.descendants(in_post_order=True) -%}
        {{child_def(node)}}
    {%- endfor -%}
    {{class_definition_top_node(top_node)}}
{%- endmacro -%}

{%- macro child_def(node) -%}
    {%- if isinstance(node, (FieldNode, RegNode, RegfileNode, AddrmapNode)) -%}
		{{class_definition(node)}}
    {%- endif -%}
{%- endmacro -%}


{{top()}}