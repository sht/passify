"""Form components for user input"""
from passify.components.base import Component, ContainerComponent
from passify.components.inputs import TextInput, NumberInput, RangeInput, Checkbox, CharacterTypeInput
from passify.components.display import Alert


class Form(Component):
    """Form container component"""
    
    def __init__(self, action="", method="post", **kwargs):
        """Initialize form"""
        super().__init__(**kwargs)
        self.action = action
        self.method = method
        self.children = kwargs.get('children', [])
        self.autocomplete = kwargs.get('autocomplete', 'on')
        self.id = kwargs.get('id', 'form')
        self.classes = kwargs.get('classes', '')
        
    def add_field(self, component):
        """Add a field component to the form"""
        self.children.append(component)
        return self
        
    def render(self):
        """Render the form"""
        children_html = ''.join(child.render() for child in self.children)
        return self._render_template(
            '''
            <form action="{{ action }}" method="{{ method }}" id="{{ id }}" 
                  class="{{ classes }}" autocomplete="{{ autocomplete }}">
                {{ children_html|safe }}
            </form>
            ''',
            children_html=children_html
        )


class SubmitButton(Component):
    """Submit button component"""
    
    def __init__(self, text, **kwargs):
        """Initialize button"""
        super().__init__(**kwargs)
        self.text = text
        self.type = kwargs.get('type', 'submit')
        self.classes = kwargs.get('classes', 'btn btn-primary')
        self.icon_class = kwargs.get('icon_class', '')
        self.id = kwargs.get('id', '')
        
    def render(self):
        """Render the button"""
        return self._render_template(
            '''
            <button type="{{ type }}" class="{{ classes }}" {% if id %}id="{{ id }}"{% endif %}>
                {% if icon_class %}
                <i class="{{ icon_class }} me-2"></i>
                {% endif %}
                {{ text }}
            </button>
            '''
        )


class PasswordForm(Component):
    """Complete password generation form"""
    
    def __init__(self, settings, **kwargs):
        """Initialize password form"""
        super().__init__(**kwargs)
        self.settings = settings
        self.error = kwargs.get('error', None)
        
    def render(self):
        """Render the password generation form"""
        # Create form container
        form = Form(method="post", autocomplete="off")
        
        # Add error alert if present
        if self.error:
            form.add_field(Alert(self.error, type_='danger'))
            
        # Add length slider and input
        length_container = ContainerComponent(classes="mb-4")
        length_container.add_child(Component()._render_template(
            '''
            <label for="length" class="form-label fw-bold">
                <i class="fas fa-ruler me-2"></i>Password Length
            </label>
            <div class="input-group">
                <input type="range" class="form-range w-75" id="lengthRange" min="4" max="64"
                       value="{{ settings.length }}" oninput="updateLengthValue(this.value)">
                <input type="number" class="form-control ms-2" id="length" name="length" min="4" max="64"
                       value="{{ settings.length }}" required oninput="updateRangeValue(this.value)">
            </div>
            <small class="text-muted">Move the slider to adjust password length</small>
            ''',
            settings=self.settings
        ))
        form.add_field(length_container)
        
        # Add character types section
        char_types_container = ContainerComponent(classes="mb-4")
        char_types_container.add_child(Component()._render_template(
            '''
            <label class="form-label fw-bold">
                <i class="fas fa-font me-2"></i>Character Types
            </label>
            '''
        ))
        
        # Character types card
        char_types_card = ContainerComponent(classes="card border-light mb-2")
        char_types_body = ContainerComponent(classes="card-body py-2")
        
        # Add character type options
        upper_type = CharacterTypeInput(
            'use_upper', 'Uppercase (A-Z)', 
            icon_class='fas fa-uppercase', 
            checked=self.settings.get('use_upper', True),
            min_value=self.settings.get('min_upper', 1)
        )
        char_types_body.add_child(upper_type)
        
        lower_type = CharacterTypeInput(
            'use_lower', 'Lowercase (a-z)', 
            icon_class='fas fa-lowercase', 
            checked=self.settings.get('use_lower', True),
            min_value=self.settings.get('min_lower', 1)
        )
        char_types_body.add_child(lower_type)
        
        digits_type = CharacterTypeInput(
            'use_digits', 'Numbers (0-9)', 
            icon_class='fas', 
            checked=self.settings.get('use_digits', True),
            min_value=self.settings.get('min_digits', 1)
        )
        char_types_body.add_child(digits_type)
        
        special_checkbox = Checkbox(
            'use_special', 'Special Characters (e.g. !@#$...)',
            checked=self.settings.get('use_special', False)
        )
        char_types_body.add_child(special_checkbox)
        
        char_types_card.add_child(char_types_body)
        char_types_container.add_child(char_types_card)
        form.add_field(char_types_container)
        
        # Add submit button
        submit_btn = SubmitButton(
            'Generate Secure Password',
            classes='btn btn-primary w-100 py-2 mt-2',
            icon_class='fas fa-key'
        )
        form.add_field(submit_btn)
        
        # Add JavaScript for slider
        form.add_field(Component()._render_template(
            '''
            <script>
                // Range and number input synchronization
                function updateLengthValue(val) {
                    document.getElementById('length').value = val;
                }

                function updateRangeValue(val) {
                    document.getElementById('lengthRange').value = val;
                }

                // Initialize sliders and form fields with session values
                document.addEventListener('DOMContentLoaded', function() {
                    // Ensure range slider and number input are in sync on page load
                    const lengthInput = document.getElementById('length');
                    const lengthRange = document.getElementById('lengthRange');
                    if (lengthInput && lengthRange) {
                        lengthRange.value = lengthInput.value;
                    }
                });
            </script>
            '''
        ))
        
        # Render the complete form
        return form.render()