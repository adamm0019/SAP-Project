document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }

    const messageTextarea = document.querySelector('textarea[name="message"]');
    if (messageTextarea) {
        const maxLength = 500;

        const counterDiv = document.createElement('div');
        counterDiv.className = 'form-text text-muted';
        counterDiv.id = 'char-counter';
        counterDiv.textContent = `${messageTextarea.value.length}/${maxLength} characters`;

        messageTextarea.parentNode.insertBefore(counterDiv, messageTextarea.nextSibling);

        messageTextarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            counterDiv.textContent = `${currentLength}/${maxLength} characters`;

            if (currentLength > maxLength * 0.9) {
                counterDiv.classList.add('text-danger');
            } else {
                counterDiv.classList.remove('text-danger');
            }
        });
    }

    const urlParams = new URLSearchParams(window.location.search);
    const q = urlParams.get('q');

    if (q && document.getElementById('search-results')) {
        const resultDiv = document.createElement('div');
        resultDiv.className = 'alert alert-info';
        resultDiv.textContent = `Dynamic search results for: ${q}`;
        document.getElementById('search-results').appendChild(resultDiv);
    }

    const passwordField = document.querySelector('input[name="password"]');
    if (passwordField && passwordField.type === 'password' && document.querySelector('form').action.includes('register')) {
        const strengthMeter = document.createElement('div');
        strengthMeter.className = 'progress mt-2';
        strengthMeter.style.height = '5px';

        const strengthBar = document.createElement('div');
        strengthBar.className = 'progress-bar';
        strengthBar.style.width = '0%';
        strengthBar.setAttribute('role', 'progressbar');
        strengthBar.setAttribute('aria-valuenow', '0');
        strengthBar.setAttribute('aria-valuemin', '0');
        strengthBar.setAttribute('aria-valuemax', '100');

        strengthMeter.appendChild(strengthBar);
        passwordField.parentNode.appendChild(strengthMeter);

        passwordField.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;

            if (password.length >= 8) strength += 25;
            if (/[A-Z]/.test(password)) strength += 25;
            if (/[a-z]/.test(password)) strength += 25;
            if (/[0-9]/.test(password)) strength += 25;

            strengthBar.style.width = `${strength}%`;
            strengthBar.setAttribute('aria-valuenow', strength);

            if (strength < 50) {
                strengthBar.className = 'progress-bar bg-danger';
            } else if (strength < 75) {
                strengthBar.className = 'progress-bar bg-warning';
            } else {
                strengthBar.className = 'progress-bar bg-success';
            }
        });
    }
});