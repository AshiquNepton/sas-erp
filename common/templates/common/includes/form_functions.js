// // <!-- common/templates/common/includes/form_functions.js -->
// <script>
// /**
//  * Example Company Form Functions
//  * Add these functions to your company_form.html or include this script
//  */

// function saveCompany() {
//     // Get form data
//     const form = document.getElementById('company-form-form');
//     const formData = new FormData(form);
    
//     // Validate required fields
//     const companyName = formData.get('company_name');
//     const companyCode = formData.get('company_code');
//     const phone = formData.get('phone');
    
//     if (!companyName || !companyCode || !phone) {
//         showAlert('Please fill in all required fields', 'error', 'Validation Error');
//         return;
//     }
    
//     // Show loading toast
//     showToast('Saving company information...', 'info', 0, 'Processing');
    
//     // Make AJAX request (example)
//     fetch('/common/company/save/', {
//         method: 'POST',
//         body: formData,
//         headers: {
//             'X-Requested-With': 'XMLHttpRequest'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             showToast('Company information saved successfully!', 'success', 3000, 'Success');
//             // Optionally reload or update UI
//         } else {
//             showAlert(data.message || 'Failed to save company information', 'error', 'Error');
//         }
//     })
//     .catch(error => {
//         showAlert('An error occurred while saving. Please try again.', 'error', 'Error');
//         console.error('Error:', error);
//     });
// }

// function deleteCompany() {
//     showConfirm(
//         'Are you sure you want to delete this company? This action cannot be undone.',
//         function(confirmed) {
//             if (confirmed) {
//                 // Show processing
//                 showToast('Deleting company...', 'info', 0, 'Processing');
                
//                 // Make delete request
//                 fetch('/common/company/delete/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-Requested-With': 'XMLHttpRequest'
//                     },
//                     body: JSON.stringify({ id: getCurrentCompanyId() })
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         showToast('Company deleted successfully', 'success', 3000);
//                         // Redirect or clear form
//                         setTimeout(() => {
//                             window.location.href = '/common/company/';
//                         }, 2000);
//                     } else {
//                         showAlert(data.message || 'Failed to delete company', 'error');
//                     }
//                 })
//                 .catch(error => {
//                     showAlert('An error occurred while deleting. Please try again.', 'error');
//                     console.error('Error:', error);
//                 });
//             }
//         },
//         'danger',
//         'Delete Company',
//         'Delete',
//         'Cancel'
//     );
// }

// /**
//  * Example Customer Form Functions
//  * Add these functions to your customer_form.html or include this script
//  */

// function saveCustomer() {
//     // Get form data
//     const form = document.getElementById('customer-form-form');
//     const formData = new FormData(form);
    
//     // Validate required fields
//     const firstName = formData.get('first_name');
//     const lastName = formData.get('last_name');
//     const email = formData.get('email');
//     const phone = formData.get('phone');
//     const customerType = formData.get('customer_type');
    
//     if (!firstName || !lastName || !email || !phone || !customerType) {
//         showAlert('Please fill in all required fields', 'error', 'Validation Error');
//         return;
//     }
    
//     // Validate email format
//     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     if (!emailRegex.test(email)) {
//         showAlert('Please enter a valid email address', 'error', 'Invalid Email');
//         return;
//     }
    
//     // Show loading toast
//     showToast('Saving customer information...', 'info', 0, 'Processing');
    
//     // Make AJAX request (example)
//     fetch('/common/customer/save/', {
//         method: 'POST',
//         body: formData,
//         headers: {
//             'X-Requested-With': 'XMLHttpRequest'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             showToast('Customer information saved successfully!', 'success', 3000, 'Success');
//             // Update customer code if new customer
//             if (data.customer_code) {
//                 document.getElementById('customer_code').value = data.customer_code;
//             }
//         } else {
//             showAlert(data.message || 'Failed to save customer information', 'error', 'Error');
//         }
//     })
//     .catch(error => {
//         showAlert('An error occurred while saving. Please try again.', 'error', 'Error');
//         console.error('Error:', error);
//     });
// }

// function deleteCustomer() {
//     showConfirm(
//         'Are you sure you want to delete this customer? This action cannot be undone and will remove all associated data.',
//         function(confirmed) {
//             if (confirmed) {
//                 // Show processing
//                 showToast('Deleting customer...', 'info', 0, 'Processing');
                
//                 // Make delete request
//                 fetch('/common/customer/delete/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                         'X-Requested-With': 'XMLHttpRequest'
//                     },
//                     body: JSON.stringify({ id: getCurrentCustomerId() })
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.success) {
//                         showToast('Customer deleted successfully', 'success', 3000);
//                         // Redirect or clear form
//                         setTimeout(() => {
//                             window.location.href = '/common/customer/';
//                         }, 2000);
//                     } else {
//                         showAlert(data.message || 'Failed to delete customer', 'error');
//                     }
//                 })
//                 .catch(error => {
//                     showAlert('An error occurred while deleting. Please try again.', 'error');
//                     console.error('Error:', error);
//                 });
//             }
//         },
//         'danger',
//         'Delete Customer',
//         'Delete',
//         'Cancel'
//     );
// }

// /**
//  * Helper Functions
//  */

// function getCurrentCompanyId() {
//     // Implement logic to get current company ID
//     // This could be from URL, hidden field, or data attribute
//     return document.getElementById('company_id')?.value || null;
// }

// function getCurrentCustomerId() {
//     // Implement logic to get current customer ID
//     return document.getElementById('customer_id')?.value || null;
// }

// /**
//  * Form Validation Helper
//  */
// function validateForm(formId, requiredFields) {
//     const form = document.getElementById(formId);
//     const formData = new FormData(form);
//     const missing = [];
    
//     requiredFields.forEach(field => {
//         const value = formData.get(field.name);
//         if (!value || value.trim() === '') {
//             missing.push(field.label);
//         }
//     });
    
//     if (missing.length > 0) {
//         showAlert(
//             `Please fill in the following required fields:\n\n${missing.join('\n')}`,
//             'error',
//             'Validation Error'
//         );
//         return false;
//     }
    
//     return true;
// }

// /**
//  * Success/Error Handlers for AJAX
//  */
// function handleSaveSuccess(message = 'Data saved successfully!') {
//     showToast(message, 'success', 3000, 'Success');
// }

// function handleSaveError(error, defaultMessage = 'An error occurred while saving.') {
//     const message = error.message || defaultMessage;
//     showAlert(message, 'error', 'Error');
// }

// function handleDeleteSuccess(redirectUrl = null) {
//     showToast('Record deleted successfully', 'success', 3000);
//     if (redirectUrl) {
//         setTimeout(() => {
//             window.location.href = redirectUrl;
//         }, 2000);
//     }
// }

// function handleDeleteError(error) {
//     showAlert(
//         error.message || 'An error occurred while deleting. Please try again.',
//         'error',
//         'Delete Error'
//     );
// }
// </script>