"""Base component class for UI elements"""
from flask import render_template_string
import re


class Component:
    """Base component class for rendering UI elements"""
    
    def __init__(self, **kwargs):
        """Initialize component with attributes"""
        self.attributes = kwargs
        
    def render(self):
        """Render the component as HTML"""
        raise NotImplementedError("Subclasses must implement render()")
        
    def _render_template(self, template_str, **context):
        """Render a template with component attributes and context"""
        # Combine attributes and context
        template_context = {**self.attributes, **context}
        return render_template_string(template_str, **template_context)


class InputComponent(Component):
    """Base class for input components"""
    
    def __init__(self, name, label, **kwargs):
        """Initialize with name and label"""
        super().__init__(**kwargs)
        self.name = name
        self.label = label
        self.id = kwargs.get('id', name)
        self.value = kwargs.get('value', '')
        self.required = kwargs.get('required', False)
        self.help_text = kwargs.get('help_text', None)
        self.classes = kwargs.get('classes', '')
        
    def render(self):
        """Render the input component"""
        raise NotImplementedError("Subclasses must implement render()")


class ContainerComponent(Component):
    """Container for child components"""
    
    def __init__(self, children=None, **kwargs):
        """Initialize with child components"""
        super().__init__(**kwargs)
        self.children = children or []
        
    def add_child(self, component):
        """Add a child component"""
        self.children.append(component)
        return self
        
    def render(self):
        """Render the container with its children"""
        children_html = ''.join(child.render() for child in self.children)
        return self._render_template(
            '''
            <div class="{{ classes }}">
                {{ children_html|safe }}
            </div>
            ''',
            children_html=children_html,
            classes=self.attributes.get('classes', '')
        )