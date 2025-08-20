"""Input components for forms"""
from passify.components.base import InputComponent


class TextInput(InputComponent):
    """Text input component"""
    
    def __init__(self, name, label, type_="text", **kwargs):
        """Initialize text input"""
        super().__init__(name, label, **kwargs)
        self.type = type_
        self.placeholder = kwargs.get('placeholder', '')
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        
    def render(self):
        """Render the text input"""
        return self._render_template(
            '''
            <div class="mb-3">
                <label for="{{ id }}" class="form-label">{{ label }}</label>
                <input type="{{ type }}" class="form-control {{ classes }}" id="{{ id }}" name="{{ name }}"
                       value="{{ value }}" placeholder="{{ placeholder }}"
                       {% if min is not none %}min="{{ min }}"{% endif %}
                       {% if max is not none %}max="{{ max }}"{% endif %}
                       {% if required %}required{% endif %}>
                {% if help_text %}
                <div class="form-text">{{ help_text }}</div>
                {% endif %}
            </div>
            '''
        )


class NumberInput(TextInput):
    """Number input component"""
    
    def __init__(self, name, label, **kwargs):
        """Initialize number input"""
        super().__init__(name, label, type_="number", **kwargs)


class RangeInput(InputComponent):
    """Range slider input component"""
    
    def __init__(self, name, label, **kwargs):
        """Initialize range input"""
        super().__init__(name, label, **kwargs)
        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 100)
        self.step = kwargs.get('step', 1)
        self.value_id = kwargs.get('value_id', f"{name}_value")
        
    def render(self):
        """Render the range input"""
        return self._render_template(
            '''
            <div class="mb-3">
                <label for="{{ id }}" class="form-label">{{ label }} 
                    <span class="badge bg-secondary" id="{{ value_id }}">{{ value }}</span>
                </label>
                <input type="range" class="form-range {{ classes }}" id="{{ id }}" name="{{ name }}"
                       min="{{ min }}" max="{{ max }}" value="{{ value }}" step="{{ step }}"
                       oninput="document.getElementById('{{ value_id }}').textContent = this.value">
                {% if help_text %}
                <div class="form-text">{{ help_text }}</div>
                {% endif %}
            </div>
            '''
        )


class Checkbox(InputComponent):
    """Checkbox input component"""
    
    def __init__(self, name, label, **kwargs):
        """Initialize checkbox"""
        super().__init__(name, label, **kwargs)
        self.checked = kwargs.get('checked', False)
        
    def render(self):
        """Render the checkbox"""
        return self._render_template(
            '''
            <div class="form-check mb-2 {{ classes }}">
                <input class="form-check-input" type="checkbox" id="{{ id }}" name="{{ name }}"
                       {% if checked %}checked{% endif %}>
                <label class="form-check-label" for="{{ id }}">{{ label }}</label>
                {% if help_text %}
                <div class="form-text">{{ help_text }}</div>
                {% endif %}
            </div>
            '''
        )


class CharacterTypeInput(InputComponent):
    """Combined checkbox with minimum number input"""
    
    def __init__(self, name, label, icon_class='', **kwargs):
        """Initialize character type input"""
        super().__init__(name, label, **kwargs)
        self.checked = kwargs.get('checked', False)
        self.icon_class = icon_class
        self.min_value = kwargs.get('min_value', 1)
        self.min_name = f"min_{name}"
        self.min_id = f"min_{self.id}"
        
    def render(self):
        """Render the character type input"""
        return self._render_template(
            '''
            <div class="form-check d-flex align-items-center mb-2 {{ classes }}">
                <input class="form-check-input" type="checkbox" id="{{ id }}" name="{{ name }}"
                       {% if checked %}checked{% endif %}>
                <label class="form-check-label me-auto" for="{{ id }}">
                    {% if icon_class %}
                    <i class="{{ icon_class }} me-1"></i>
                    {% endif %}
                    {{ label }}
                </label>
                <div class="d-flex align-items-center">
                    <span class="me-2 small">Min:</span>
                    <input type="number" class="form-control form-control-sm" style="width: 60px;"
                           name="{{ min_name }}" id="{{ min_id }}" min="0" max="64" value="{{ min_value }}"
                           data-bs-toggle="tooltip" title="Minimum {{ label }} characters">
                </div>
            </div>
            '''
        )