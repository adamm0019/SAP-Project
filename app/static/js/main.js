document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

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
        document.getElementById('search-results').innerHTML = `
            <div class="alert alert-info">
                Dynamic search results for: ${q}
            </div>
        `;
    }

    const searchTermElement = document.getElementById('search-term');
    if (searchTermElement && searchTermElement.textContent) {
        searchTermElement.innerHTML = searchTermElement.textContent;
    }
});