"""Display components for showing output"""
from passify.components.base import Component


class Alert(Component):
    """Alert component for showing messages"""
    
    def __init__(self, message, type_='info', **kwargs):
        """Initialize alert"""
        super().__init__(**kwargs)
        self.message = message
        self.type = type_
        self.dismissible = kwargs.get('dismissible', True)
        self.icon_class = kwargs.get('icon_class', self._get_icon_for_type())
        
    def _get_icon_for_type(self):
        """Get appropriate icon for alert type"""
        icons = {
            'success': 'fas fa-check-circle',
            'danger': 'fas fa-exclamation-triangle',
            'warning': 'fas fa-exclamation-circle',
            'info': 'fas fa-info-circle'
        }
        return icons.get(self.type, 'fas fa-info-circle')
        
    def render(self):
        """Render the alert"""
        return self._render_template(
            '''
            <div class="alert alert-{{ type }} {% if dismissible %}alert-dismissible fade show{% endif %}" role="alert">
                {% if icon_class %}
                <i class="{{ icon_class }} me-2"></i>
                {% endif %}
                {{ message }}
                {% if dismissible %}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                {% endif %}
            </div>
            '''
        )


class PasswordDisplay(Component):
    """Component for displaying generated password"""
    
    def __init__(self, password, **kwargs):
        """Initialize password display"""
        super().__init__(**kwargs)
        self.password = password
        
    def render(self):
        """Render the password display"""
        return self._render_template(
            '''
            <div class="alert alert-success mt-4">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <strong><i class="fas fa-check-circle me-2"></i>Your Password:</strong>
                    <button class="btn btn-sm btn-outline-success" id="copyBtn" onclick="copyPassword()">
                        <i class="fas fa-copy me-1"></i>Copy
                    </button>
                </div>
                <div class="display-6 text-center py-2 font-monospace" id="passwordDisplay">{{ password }}</div>
                
                <!-- Password Strength Indicator -->
                <div class="mt-3">
                    <div class="d-flex justify-content-between mb-1">
                        <span>Password Strength:</span>
                        <span id="strengthLabel" class="fw-bold"></span>
                    </div>
                    <div class="progress">
                        <div id="strengthBar" class="progress-bar" role="progressbar"></div>
                    </div>
                </div>
            </div>
            
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    calculateStrength("{{ password }}");
                });
            
                function calculateStrength(password) {
                    // Base score
                    let strength = 0;
                    let label = "";
                    let color = "";
                
                    // Length check
                    if (password.length >= 12) strength += 25;
                    else if (password.length >= 8) strength += 15;
                    else strength += 5;
                
                    // Character type checks
                    if (/[A-Z]/.test(password)) strength += 15;
                    if (/[a-z]/.test(password)) strength += 15;
                    if (/[0-9]/.test(password)) strength += 15;
                    if (/[^A-Za-z0-9]/.test(password)) strength += 20;
                
                    // Variety check
                    const uniqueChars = new Set(password).size;
                    const uniqueRatio = uniqueChars / password.length;
                    strength += Math.floor(uniqueRatio * 10);
                
                    // Cap at 100%
                    strength = Math.min(100, strength);
                
                    // Set label and color based on strength
                    if (strength >= 80) {
                        label = "Very Strong";
                        color = "#28a745"; // green
                    } else if (strength >= 60) {
                        label = "Strong";
                        color = "#17a2b8"; // teal
                    } else if (strength >= 40) {
                        label = "Medium";
                        color = "#ffc107"; // yellow
                    } else if (strength >= 20) {
                        label = "Weak";
                        color = "#fd7e14"; // orange
                    } else {
                        label = "Very Weak";
                        color = "#dc3545"; // red
                    }
                
                    // Update UI
                    document.getElementById('strengthBar').style.width = strength + '%';
                    document.getElementById('strengthBar').style.backgroundColor = color;
                    document.getElementById('strengthLabel').textContent = label;
                    document.getElementById('strengthLabel').style.color = color;
                }
            
                function copyPassword() {
                    const passwordText = document.getElementById('passwordDisplay').textContent;
                    navigator.clipboard.writeText(passwordText).then(function() {
                        const copyBtn = document.getElementById('copyBtn');
                        const originalText = copyBtn.innerHTML;
                
                        copyBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
                        copyBtn.classList.remove('btn-outline-success');
                        copyBtn.classList.add('btn-success');
                
                        setTimeout(function() {
                            copyBtn.innerHTML = originalText;
                            copyBtn.classList.remove('btn-success');
                            copyBtn.classList.add('btn-outline-success');
                        }, 2000);
                    });
                }
            </script>
            '''
        )


class Card(Component):
    """Card container component"""
    
    def __init__(self, title=None, children=None, **kwargs):
        """Initialize card"""
        super().__init__(**kwargs)
        self.title = title
        self.children = children or []
        self.header_class = kwargs.get('header_class', '')
        self.body_class = kwargs.get('body_class', 'p-4')
        
    def add_child(self, component):
        """Add child component"""
        self.children.append(component)
        return self
        
    def render(self):
        """Render the card"""
        children_html = ''.join(child.render() for child in self.children)
        return self._render_template(
            '''
            <div class="card shadow-lg {{ classes }}">
                {% if title %}
                <div class="card-header {{ header_class }}">
                    <h2 class="mb-0">{{ title }}</h2>
                </div>
                {% endif %}
                <div class="card-body {{ body_class }}">
                    {{ children_html|safe }}
                </div>
            </div>
            ''',
            children_html=children_html
        )