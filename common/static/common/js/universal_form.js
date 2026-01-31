/* ========================================================
   UNIVERSAL FORM JAVASCRIPT - FIXED MINIMIZE TO FOOTER
   Properly minimizes forms to a footer bar with restore/close
   ======================================================== */

(function() {
    'use strict';
    
    // State management
    let designModeActive = false;
    let selectedField = null;
    let currentActiveGroup = null;
    let minimizedForms = [];
    
    // ==================== INITIALIZE FOOTER ====================
    
    function initializeMinimizedFooter() {
        // Check if footer already exists
        if (document.getElementById('minimizedFormsFooter')) {
            return;
        }
        
        // Create footer container
        const footer = document.createElement('div');
        footer.id = 'minimizedFormsFooter';
        footer.className = 'minimized-forms-footer';
        footer.innerHTML = '<div id="minimizedFormsContainer" class="minimized-forms-container"></div>';
        document.body.appendChild(footer);
        
        console.log('✓ Minimized forms footer initialized');
    }
    
    // ==================== FORM STATE MANAGEMENT ====================
    
    window.minimizeForm = function(formId) {
        console.log('🔽 Minimizing form:', formId);
        
        const form = document.getElementById(formId);
        const overlay = document.getElementById('modal-overlay-' + formId);
        
        if (!form) {
            console.error('❌ Form not found:', formId);
            return;
        }
        
        // Get form info
        const formTitle = form.querySelector('.form-title h3')?.textContent || 'Form';
        const formIcon = form.querySelector('.form-icon')?.textContent || '📝';
        
        // Add to minimized forms array (avoid duplicates)
        const existingIndex = minimizedForms.findIndex(f => f.id === formId);
        if (existingIndex === -1) {
            minimizedForms.push({
                id: formId,
                title: formTitle,
                icon: formIcon
            });
            console.log('✓ Added to minimized array:', formTitle);
        }
        
        // Hide form and overlay
        if (form) {
            form.classList.remove('active');
            setTimeout(() => {
                form.style.display = 'none';
            }, 300);
        }
        
        if (overlay) {
            overlay.classList.remove('active');
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
        }
        
        // Update footer
        updateMinimizedFormsFooter();
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        console.log('✓ Form minimized successfully');
    };
    
    window.maximizeForm = function(formId) {
        console.log('⬜ Toggle maximize for:', formId);
        const form = document.getElementById(formId);
        if (form) {
            const currentState = form.getAttribute('data-state');
            const newState = currentState === 'maximized' ? 'normal' : 'maximized';
            form.setAttribute('data-state', newState);
            console.log('✓ Form state changed to:', newState);
        }
    };
    
    window.closeForm = function(formId) {
        closeFormOverlay(formId);
    };
    
    window.closeFormOverlay = function(formId) {
        console.log('✕ Closing form:', formId);
        
        const form = document.getElementById(formId);
        const overlay = document.getElementById('modal-overlay-' + formId);
        
        // Remove from minimized forms
        minimizedForms = minimizedForms.filter(f => f.id !== formId);
        updateMinimizedFormsFooter();
        
        // Hide with animation
        if (form) {
            form.classList.remove('active');
            setTimeout(() => {
                form.style.display = 'none';
                form.setAttribute('data-state', 'closed');
            }, 300);
        }
        if (overlay) {
            overlay.classList.remove('active');
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
        }
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        // Call custom handler if exists
        setTimeout(() => {
            if (typeof window.customCloseFormOverlay === 'function') {
                window.customCloseFormOverlay(formId);
            }
        }, 350);
        
        console.log('✓ Form closed');
    };
    
    window.openForm = function(formId) {
        console.log('=== 📂 OPENING FORM ===');
        console.log('Form ID:', formId);
        
        const form = document.getElementById(formId);
        const overlay = document.getElementById('modal-overlay-' + formId);
        
        if (!form) {
            console.error('❌ Form element not found:', formId);
            return;
        }
        
        if (!overlay) {
            console.error('❌ Overlay element not found:', 'modal-overlay-' + formId);
        }
        
        // Remove from minimized list if present
        minimizedForms = minimizedForms.filter(f => f.id !== formId);
        updateMinimizedFormsFooter();
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        // Set initial state
        form.setAttribute('data-state', 'normal');
        
        // Force display
        if (overlay) {
            overlay.style.display = 'block';
        }
        form.style.display = 'flex';
        
        // Trigger animation on next frame
        requestAnimationFrame(() => {
            if (overlay) {
                overlay.classList.add('active');
            }
            form.classList.add('active');
            console.log('✓ Active classes added');
        });
        
        // Auto-select first group tab if exists
        setTimeout(() => {
            const firstTab = form.querySelector('.group-tab');
            if (firstTab) {
                const groupId = firstTab.id.replace('tab-', '');
                selectGroup(groupId);
            }
        }, 100);
        
        console.log('=== ✓ FORM OPENED ===');
    };
    
    window.restoreForm = function(formId) {
        console.log('⬆️ Restoring form from footer:', formId);
        openForm(formId);
    };
    
    window.closeFormFromFooter = function(formId) {
        console.log('✕ Closing form from footer:', formId);
        closeFormOverlay(formId);
    };
    
    // ==================== MINIMIZED FORMS FOOTER ====================
    
    function updateMinimizedFormsFooter() {
        const footer = document.getElementById('minimizedFormsFooter');
        const container = document.getElementById('minimizedFormsContainer');
        
        if (!container) {
            console.warn('⚠️ Minimized forms container not found, initializing...');
            initializeMinimizedFooter();
            return;
        }
        
        console.log('🔄 Updating footer with', minimizedForms.length, 'forms');
        
        if (minimizedForms.length === 0) {
            container.innerHTML = '';
            if (footer) {
                footer.style.display = 'none';
            }
            return;
        }
        
        // Show footer
        if (footer) {
            footer.style.display = 'block';
        }
        
        // Build minimized items
        container.innerHTML = minimizedForms.map(form => `
            <div class="minimized-form-item">
                <span class="minimized-form-icon">${form.icon}</span>
                <span class="minimized-form-title">${form.title}</span>
                <div class="minimized-form-actions">
                    <button class="minimized-form-btn expand" 
                            onclick="restoreForm('${form.id}')" 
                            title="Restore">
                        ⬆️
                    </button>
                    <button class="minimized-form-btn close" 
                            onclick="closeFormFromFooter('${form.id}')" 
                            title="Close">
                        ✕
                    </button>
                </div>
            </div>
        `).join('');
        
        console.log('✓ Footer updated successfully');
    }
    
    // ==================== GROUP TABS ====================
    
    window.selectGroup = function(groupId) {
        console.log('📑 Selecting group:', groupId);
        
        // Hide all group contents
        const allContents = document.querySelectorAll('.form-group-content-area');
        allContents.forEach(content => {
            content.style.display = 'none';
        });
        
        // Show ungrouped fields
        const ungroupedFields = document.getElementById('ungrouped-fields');
        if (ungroupedFields) {
            ungroupedFields.style.display = 'block';
        }
        
        // Remove active class from all tabs
        const allTabs = document.querySelectorAll('.group-tab');
        allTabs.forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Show selected group content
        const selectedContent = document.getElementById('group-content-' + groupId);
        if (selectedContent) {
            selectedContent.style.display = 'block';
        }
        
        // Add active class to selected tab
        const selectedTab = document.getElementById('tab-' + groupId);
        if (selectedTab) {
            selectedTab.classList.add('active');
        }
        
        currentActiveGroup = groupId;
        localStorage.setItem('activeGroup', groupId);
    };
    
    // ==================== MENU ====================
    
    window.toggleMenu = function() {
        const menu = document.getElementById('menuDropdown');
        if (menu) {
            menu.classList.toggle('show');
        }
    };
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const menu = document.getElementById('menuDropdown');
        const button = event.target.closest('.dropdown-wrapper');
        if (!button && menu && menu.classList.contains('show')) {
            menu.classList.remove('show');
        }
    });
    
    // ==================== DESIGN MODE ====================
    
    window.openDesignMode = function() {
        designModeActive = true;
        const sidebar = document.getElementById('designSidebar');
        if (sidebar) {
            sidebar.classList.add('open');
        }
        
        const fields = document.querySelectorAll('.form-field-wrapper');
        fields.forEach(field => {
            field.classList.add('design-mode-active');
            field.addEventListener('click', selectField);
        });
        
        toggleMenu();
    };
    
    window.closeDesignMode = function() {
        designModeActive = false;
        const sidebar = document.getElementById('designSidebar');
        if (sidebar) {
            sidebar.classList.remove('open');
        }
        
        const fields = document.querySelectorAll('.form-field-wrapper');
        fields.forEach(field => {
            field.classList.remove('design-mode-active', 'selected');
            field.removeEventListener('click', selectField);
        });
        
        selectedField = null;
    };
    
    function selectField(event) {
        event.stopPropagation();
        
        document.querySelectorAll('.form-field-wrapper').forEach(f => {
            f.classList.remove('selected');
        });
        
        this.classList.add('selected');
        selectedField = this;
        
        const fieldName = this.getAttribute('data-field-name');
        const label = this.querySelector('label');
        const labelText = label ? label.textContent.replace('✏️', '').replace('*', '').trim() : '';
        const currentWidth = this.style.width || '100%';
        const isRequired = label ? label.classList.contains('required') : false;
        
        document.getElementById('selectedFieldName').textContent = fieldName;
        document.getElementById('editLabel').value = labelText;
        document.getElementById('editWidth').value = currentWidth;
        document.getElementById('editRequired').checked = isRequired;
        
        const widthSelect = document.getElementById('editWidth');
        const customWidthInput = document.getElementById('customWidth');
        const standardWidths = ['25%', '33.33%', '50%', '66.66%', '75%', '100%'];
        if (!standardWidths.includes(currentWidth)) {
            widthSelect.value = 'custom';
            customWidthInput.style.display = 'block';
            customWidthInput.value = currentWidth;
        } else {
            customWidthInput.style.display = 'none';
        }
    }
    
    window.applyFieldChanges = function() {
        if (!selectedField) {
            alert('Please select a field first');
            return;
        }
        
        const label = selectedField.querySelector('label');
        const newLabel = document.getElementById('editLabel').value;
        const widthSelect = document.getElementById('editWidth');
        const customWidth = document.getElementById('customWidth');
        const newWidth = widthSelect.value === 'custom' ? customWidth.value : widthSelect.value;
        const isRequired = document.getElementById('editRequired').checked;
        
        if (label) {
            label.textContent = newLabel;
            if (isRequired) {
                label.classList.add('required');
            } else {
                label.classList.remove('required');
            }
        }
        
        selectedField.style.width = newWidth;
        selectedField.style.flex = `0 0 ${newWidth}`;
        
        alert('Changes applied successfully!');
    };
    
    window.cancelFieldEdit = function() {
        document.querySelectorAll('.form-field-wrapper').forEach(f => {
            f.classList.remove('selected');
        });
        selectedField = null;
        document.getElementById('selectedFieldName').textContent = 'None';
    };
    
    window.moveFieldUp = function() {
        if (!selectedField) {
            alert('Please select a field first');
            return;
        }
        
        const container = selectedField.parentElement;
        const prev = selectedField.previousElementSibling;
        if (prev && prev.classList.contains('form-field-wrapper')) {
            container.insertBefore(selectedField, prev);
        }
    };
    
    window.moveFieldDown = function() {
        if (!selectedField) {
            alert('Please select a field first');
            return;
        }
        
        const container = selectedField.parentElement;
        const next = selectedField.nextElementSibling;
        if (next && next.classList.contains('form-field-wrapper')) {
            container.insertBefore(next, selectedField);
        }
    };
    
    window.saveFormLayout = function() {
        const fields = document.querySelectorAll('.form-field-wrapper');
        const layout = {};
        
        fields.forEach((field, index) => {
            const fieldName = field.getAttribute('data-field-name');
            const label = field.querySelector('label');
            layout[fieldName] = {
                order: index,
                width: field.style.width,
                label: label ? label.textContent.replace('*', '').trim() : '',
                required: label ? label.classList.contains('required') : false
            };
        });
        
        localStorage.setItem('formLayout', JSON.stringify(layout));
        alert('Form layout saved successfully!');
    };
    
    window.resetFormLayout = function() {
        if (confirm('Are you sure you want to reset the form layout to default?')) {
            localStorage.removeItem('formLayout');
            localStorage.removeItem('activeGroup');
            alert('Form layout reset. Page will reload...');
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
    };
    
    // ==================== INITIALIZATION ====================
    
    window.addEventListener('DOMContentLoaded', function() {
        console.log('🚀 Universal Form System Initialized');
        
        // Initialize minimized footer
        initializeMinimizedFooter();
        
        // Setup width selector
        const editWidthEl = document.getElementById('editWidth');
        if (editWidthEl) {
            editWidthEl.addEventListener('change', function() {
                const customWidthInput = document.getElementById('customWidth');
                if (this.value === 'custom') {
                    customWidthInput.style.display = 'block';
                    customWidthInput.focus();
                } else {
                    customWidthInput.style.display = 'none';
                }
            });
        }
        
        // Load saved layout
        const savedLayout = localStorage.getItem('formLayout');
        if (savedLayout) {
            try {
                const layout = JSON.parse(savedLayout);
                Object.keys(layout).forEach(fieldName => {
                    const field = document.querySelector(`[data-field-name="${fieldName}"]`);
                    if (field) {
                        const config = layout[fieldName];
                        field.style.width = config.width;
                        field.style.flex = `0 0 ${config.width}`;
                        
                        const label = field.querySelector('label');
                        if (label && config.label) {
                            label.textContent = config.label;
                            if (config.required) {
                                label.classList.add('required');
                            } else {
                                label.classList.remove('required');
                            }
                        }
                    }
                });
            } catch (e) {
                console.error('Error loading saved layout:', e);
            }
        }
        
        // Activate saved group or first group
        const savedActiveGroup = localStorage.getItem('activeGroup');
        const firstTab = document.querySelector('.group-tab');
        
        if (savedActiveGroup && document.getElementById('tab-' + savedActiveGroup)) {
            selectGroup(savedActiveGroup);
        } else if (firstTab) {
            const firstGroupId = firstTab.id.replace('tab-', '');
            selectGroup(firstGroupId);
        }
    });
    
})();