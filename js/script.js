document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const typeButtons = document.querySelectorAll('.type-btn');
    const lengthSlider = document.getElementById('length');
    const lengthValue = document.getElementById('length-value');
    const numbersCheckbox = document.getElementById('numbers');
    const symbolsCheckbox = document.getElementById('symbols');
    const passwordOutput = document.getElementById('password');
    const copyButton = document.getElementById('copy');
    const refreshButton = document.getElementById('refresh');

    // Current password configuration
    const config = {
        type: 'random',
        length: 16,
        numbers: true,
        symbols: false
    };

    // Initialize the app
    generatePassword();

    // Event listeners
    typeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons
            typeButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            this.classList.add('active');
            // Update config
            config.type = this.getAttribute('data-type');
            
            // Update UI based on password type
            updateUIForType(config.type);
            
            // Generate new password
            generatePassword();
        });
    });

    lengthSlider.addEventListener('input', function() {
        config.length = this.value;
        lengthValue.value = this.value;
        updateSliderBackground();
        generatePassword();
    });

    lengthValue.addEventListener('input', function() {
        let value = parseInt(this.value);
        if (isNaN(value)) {
            value = config.length;
        }
        
        // Constrain value between min and max
        value = Math.max(4, Math.min(32, value));
        
        config.length = value;
        lengthSlider.value = value;
        this.value = value;
        updateSliderBackground();
        generatePassword();
    });

    numbersCheckbox.addEventListener('change', function() {
        config.numbers = this.checked;
        generatePassword();
    });

    symbolsCheckbox.addEventListener('change', function() {
        config.symbols = this.checked;
        generatePassword();
    });

    copyButton.addEventListener('click', function() {
        copyToClipboard(passwordOutput.value);
    });

    refreshButton.addEventListener('click', function() {
        generatePassword();
    });

    // Functions
    function generatePassword() {
        let password = '';
        
        switch(config.type) {
            case 'random':
                password = generateRandomPassword();
                break;
            case 'memorable':
                password = generateMemorablePassword();
                break;
            case 'pin':
                password = generatePinPassword();
                break;
        }
        
        passwordOutput.value = password;
    }

    function generateRandomPassword() {
        const lowercaseChars = 'abcdefghijklmnopqrstuvwxyz';
        const uppercaseChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const numberChars = '0123456789';
        const symbolChars = '!@#$%^&*()_-+=<>?/[]{}|';
        
        let availableChars = lowercaseChars + uppercaseChars;
        if (config.numbers) availableChars += numberChars;
        if (config.symbols) availableChars += symbolChars;
        
        let password = '';
        
        // Ensure at least one character from each selected category
        password += getRandomChar(lowercaseChars);
        password += getRandomChar(uppercaseChars);
        if (config.numbers) password += getRandomChar(numberChars);
        if (config.symbols) password += getRandomChar(symbolChars);
        
        // Fill the rest of the password
        while (password.length < config.length) {
            password += getRandomChar(availableChars);
        }
        
        // Shuffle the password
        return shuffleString(password);
    }

    function generateMemorablePassword() {
        const words = [
            'apple', 'beach', 'cloud', 'dream', 'earth', 'fruit', 'glass',
            'happy', 'juice', 'kite', 'light', 'music', 'night', 'ocean',
            'paper', 'queen', 'river', 'storm', 'tiger', 'unity', 'voice',
            'water', 'xylophone', 'yellow', 'zebra', 'bread', 'chair', 'dance',
            'eagle', 'flute', 'grape', 'honey', 'igloo', 'jewel', 'koala',
            'mountain', 'forest', 'window', 'garden', 'flower', 'planet', 'rocket',
            'school', 'pencil', 'orange', 'banana', 'monkey', 'puzzle', 'castle',
            'bridge', 'camera', 'dragon', 'energy', 'family', 'giant', 'helmet',
            'island', 'jungle', 'kitten', 'lemon', 'mirror', 'notebook', 'octopus',
            'pillow', 'quartz', 'rainbow', 'sunset', 'train', 'umbrella', 'violin',
            'whale', 'yogurt', 'zucchini', 'anchor', 'button', 'circle', 'desert',
            'engine', 'feather', 'guitar', 'helmet', 'insect', 'jacket', 'ladder',
            'magnet', 'needle', 'ostrich', 'panda', 'quiver', 'robot', 'saddle',
            'teapot', 'unicorn', 'village', 'wallet', 'yawn', 'zipper', 'artist',
            'bottle', 'candle', 'donkey', 'envelope', 'forest', 'glove', 'hammer',
            'icicle', 'jungle', 'kangaroo', 'lantern', 'meadow', 'napkin', 'orchid',
            'parrot', 'quokka', 'rocket', 'scooter', 'ticket', 'utensil', 'vulture',
            'window', 'yacht', 'zeppelin'
        ];
        
        // Select random words and capitalize first letter
        let password = '';
        while (password.length < config.length) {
            const word = words[Math.floor(Math.random() * words.length)];
            const capitalizedWord = word.charAt(0).toUpperCase() + word.slice(1);
            password += capitalizedWord;
        }
        
        // Trim password to the specified length
        password = password.slice(0, config.length);
        
        // Add number and symbol if needed
        if (config.numbers || config.symbols) {
            let extras = '';
            if (config.numbers) extras += Math.floor(Math.random() * 100);
            if (config.symbols) extras += getRandomChar('!@#$%^&*');
            
            // Replace end of password with extras
            password = password.slice(0, config.length - extras.length) + extras;
        }
        
        return password;
    }

    function generatePinPassword() {
        const digits = '0123456789';
        let pin = '';
        
        for (let i = 0; i < config.length; i++) {
            pin += getRandomChar(digits);
        }
        
        return pin;
    }

    function getRandomChar(characters) {
        return characters.charAt(Math.floor(Math.random() * characters.length));
    }

    function shuffleString(string) {
        const array = string.split('');
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array.join('');
    }

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text)
            .then(() => {
                // Visual feedback for copy success
                copyButton.textContent = 'Copied!';
                copyButton.style.backgroundColor = 'var(--success-color)';
                
                setTimeout(() => {
                    copyButton.textContent = 'Copy password';
                    copyButton.style.backgroundColor = '';
                }, 2000);
            })
            .catch(err => {
                console.error('Could not copy text: ', err);
            });
    }

    function updateUIForType(type) {
        const toggleContainer = document.querySelector('.toggle-container');
        
        if (type === 'pin') {
            // Set PIN length to 6 by default
            config.length = 6;
            lengthSlider.value = 6;
            lengthValue.value = 6;
            updateSliderBackground();
            
            numbersCheckbox.checked = true;
            symbolsCheckbox.checked = false;
            
            // Hide toggle options for PIN
            toggleContainer.style.display = 'none';
        } else if (type === 'memorable') {
            // Set memorable password length to 16 by default
            config.length = 16;
            lengthSlider.value = 16;
            lengthValue.value = 16;
            updateSliderBackground();
            
            // Show toggle options for memorable
            toggleContainer.style.display = 'block';
            
            // Enable checkboxes for memorable
            numbersCheckbox.disabled = false;
            symbolsCheckbox.disabled = false;
        } else {
            // For random password
            // Show toggle options for random
            toggleContainer.style.display = 'block';
            
            // Enable checkboxes for random
            numbersCheckbox.disabled = false;
            symbolsCheckbox.disabled = false;
        }
    }

    function updateSliderBackground() {
        const min = parseInt(lengthSlider.min);
        const max = parseInt(lengthSlider.max);
        const val = parseInt(lengthSlider.value);
        const percentage = ((val - min) * 100) / (max - min);
        
        lengthSlider.style.background = `linear-gradient(to right, var(--primary-color) 0%, var(--primary-color) ${percentage}%, #d1d5db ${percentage}%, #d1d5db 100%)`;
    }

    // Initialize slider background
    updateSliderBackground();
});
