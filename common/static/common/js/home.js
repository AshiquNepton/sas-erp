// ============================================
// Sidebar Navigation Functions
// ============================================

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('collapsed');
        
        // Save state to localStorage
        const isCollapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', isCollapsed);
    }
}

function toggleSection(sectionId) {
    const section = document.getElementById('section-' + sectionId);
    if (section) {
        section.classList.toggle('expanded');
        
        // Save expanded sections to localStorage
        const expandedSections = getExpandedSections();
        const index = expandedSections.indexOf(sectionId);
        
        if (section.classList.contains('expanded')) {
            if (index === -1) expandedSections.push(sectionId);
        } else {
            if (index > -1) expandedSections.splice(index, 1);
        }
        
        localStorage.setItem('expandedSections', JSON.stringify(expandedSections));
    }
}

function getExpandedSections() {
    try {
        return JSON.parse(localStorage.getItem('expandedSections') || '[]');
    } catch {
        return [];
    }
}

function handleSubitemClick(event, sectionId) {
    // Handle active state
    const allSubitems = document.querySelectorAll('.nav-subitem');
    allSubitems.forEach(item => item.classList.remove('active'));
    
    if (event.currentTarget) {
        event.currentTarget.classList.add('active');
    }
}

// Restore sidebar state on page load
document.addEventListener('DOMContentLoaded', function() {
    // Restore sidebar collapsed state
    const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    const sidebar = document.getElementById('sidebar');
    if (sidebar && sidebarCollapsed) {
        sidebar.classList.add('collapsed');
    }
    
    // Restore expanded sections
    const expandedSections = getExpandedSections();
    expandedSections.forEach(sectionId => {
        const section = document.getElementById('section-' + sectionId);
        if (section && !section.classList.contains('expanded')) {
            section.classList.add('expanded');
        }
    });
});

// ============================================
// Alert Auto-Dismiss
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.messages-container .alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000); // Auto-dismiss after 5 seconds
    });
});

// Add slideOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

// ============================================
// Progress Bar Functions
// ============================================

function showProgressBar(label = 'Processing...') {
    const progressLine = document.getElementById('footerProgressLine');
    const progressLabel = document.getElementById('progressLabel');
    
    if (progressLine) {
        progressLine.classList.add('active');
    }
    if (progressLabel) {
        progressLabel.textContent = label;
    }
    
    updateProgress(0);
}

function hideProgressBar() {
    const progressLine = document.getElementById('footerProgressLine');
    if (progressLine) {
        progressLine.classList.remove('active');
    }
}

function updateProgress(percentage) {
    const progressFill = document.getElementById('progressBarFill');
    const progressPercentage = document.getElementById('progressPercentage');
    
    if (progressFill) {
        progressFill.style.width = percentage + '%';
    }
    if (progressPercentage) {
        progressPercentage.textContent = Math.round(percentage) + '%';
    }
}

// Example usage:
// showProgressBar('Saving data...');
// updateProgress(50);
// hideProgressBar();

// ============================================
// Utility Functions
// ============================================

// Format date
function formatDate(date) {
    const options = { 
        weekday: 'short', 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    };
    return date.toLocaleDateString('en-US', options);
}

// Format time
function formatTime(date) {
    const options = { 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit',
        hour12: true 
    };
    return date.toLocaleTimeString('en-US', options);
}

// Debounce function for search/filter inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ============================================
// Form Validation Helper
// ============================================

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    if (form.checkValidity()) {
        return true;
    } else {
        form.reportValidity();
        return false;
    }
}

// ============================================
// AJAX Helper Functions
// ============================================

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function ajaxPost(url, data, successCallback, errorCallback) {
    const csrftoken = getCookie('csrftoken');
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (successCallback) successCallback(data);
    })
    .catch(error => {
        console.error('Error:', error);
        if (errorCallback) errorCallback(error);
    });
}

// ============================================
// Keyboard Shortcuts
// ============================================

document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + B: Toggle Sidebar
    if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
        e.preventDefault();
        toggleSidebar();
    }
    
    // ESC: Close any open overlays
    if (e.key === 'Escape') {
        // Close custom alerts/confirms if open
        const alertOverlay = document.getElementById('customAlertOverlay');
        const confirmOverlay = document.getElementById('customConfirmOverlay');
        
        if (alertOverlay && alertOverlay.classList.contains('show')) {
            closeAlert();
        }
        if (confirmOverlay && confirmOverlay.classList.contains('show')) {
            closeConfirm(false);
        }
    }
});

// ============================================
// Console Log Styling
// ============================================

console.log('%c🏠 Home Page Loaded', 'color: #667eea; font-size: 16px; font-weight: bold;');
console.log('%cSidebar navigation and footer ready', 'color: #10b981; font-size: 12px;');