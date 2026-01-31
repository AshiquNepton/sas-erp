from django.shortcuts import render
from django.http import JsonResponse

def customer_form(request):
    """Customer form view - DIAGNOSTIC VERSION"""
    
    # Print to console for debugging
    print("=" * 50)
    print("CUSTOMER FORM VIEW CALLED")
    print("=" * 50)
    
    # Customer form configuration
    form_config = {
        'form_id': 'customer-form',
        'title': 'Customer Information',
        'icon': '👤',
        'action': '/common/customer/save/',
        'footer_status': 'Ready',
        'background': 'blue',
        
        'buttons': [
            {
                'label': 'New',
                'icon': '➕',
                'type': 'primary',
                'onclick': "newCustomer()"
            },
            {
                'label': 'Save',
                'icon': '💾',
                'type': 'success',
                'onclick': "saveCustomer()"
            },
            {
                'label': 'Delete',
                'icon': '🗑️',
                'type': 'danger',
                'onclick': "deleteCustomer()"
            },
        ],
        
        'menu_items': [
            {'label': 'Print', 'icon': '🖨️', 'onclick': "printCustomer()"},
            {'label': 'Export', 'icon': '📤', 'onclick': "exportCustomer()"},
            {'label': 'Import', 'icon': '📥', 'onclick': "importCustomer()"},
            {'label': 'Settings', 'icon': '⚙️', 'onclick': "openSettings()"},
        ],
        
        'groups': [
            {'id': 'contact', 'title': 'Contact Information', 'icon': '📞'},
            {'id': 'shipping', 'title': 'Shipping Address', 'icon': '🚚'},
            {'id': 'billing', 'title': 'Billing Address', 'icon': '📄'},
            {'id': 'preferences', 'title': 'Customer Preferences', 'icon': '⚙️'},
        ],
        
        'fields': [
            # Basic fields (no group)
            {
                'name': 'customer_code',
                'label': 'Customer Code',
                'type': 'text',
                'required': True,
                'width': '32.5%',
                'placeholder': 'Auto-generated',
                'group': None
            },
            {
                'name': 'first_name',
                'label': 'First Name',
                'type': 'text',
                'required': True,
                'width': '32.5%',
                'placeholder': 'Enter first name',
                'group': None
            },
            {
                'name': 'last_name',
                'label': 'Last Name',
                'type': 'text',
                'required': True,
                'width': '32%',
                'placeholder': 'Enter last name',
                'group': None
            },
            {
                'name': 'company_name',
                'label': 'Company Name',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter company name',
                'group': None
            },
            {
                'name': 'customer_type',
                'label': 'Customer Type',
                'type': 'select',
                'required': True,
                'width': '50%',
                'group': None,
                'options': [
                    {'value': 'individual', 'label': 'Individual'},
                    {'value': 'business', 'label': 'Business'},
                    {'value': 'vip', 'label': 'VIP'},
                ]
            },
            
            # Contact group
            {
                'name': 'email',
                'label': 'Email',
                'type': 'email',
                'required': True,
                'width': '50%',
                'placeholder': 'customer@example.com',
                'group': 'contact'
            },
            {
                'name': 'phone',
                'label': 'Phone',
                'type': 'text',
                'required': True,
                'width': '50%',
                'placeholder': '+974 XXXX XXXX',
                'group': 'contact'
            },
            
            # Shipping group
            {
                'name': 'ship_address1',
                'label': 'Address Line 1',
                'type': 'text',
                'required': False,
                'width': '100%',
                'placeholder': 'Street address',
                'group': 'shipping'
            },
            {
                'name': 'ship_city',
                'label': 'City',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'City',
                'group': 'shipping'
            },
            
            # Billing group
            {
                'name': 'bill_address1',
                'label': 'Address Line 1',
                'type': 'text',
                'required': False,
                'width': '100%',
                'placeholder': 'Street address',
                'group': 'billing'
            },
            
            # Preferences group
            {
                'name': 'preferred_language',
                'label': 'Preferred Language',
                'type': 'select',
                'required': False,
                'width': '50%',
                'group': 'preferences',
                'options': [
                    {'value': 'en', 'label': 'English'},
                    {'value': 'ar', 'label': 'Arabic'},
                ]
            },
        ]
    }
    
    context = {
        'form_config': form_config,
        'page_title': 'Customer Management',
    }
    
    # Debug print
    print(f"Context keys: {context.keys()}")
    print(f"Form config keys: {form_config.keys()}")
    print(f"Number of fields: {len(form_config['fields'])}")
    print(f"Number of groups: {len(form_config['groups'])}")
    print(f"Template: common/masters/customer_form.html")
    print("=" * 50)
    
    return render(request, 'common/masters/customer_form.html', context)


def save_customer(request):
    """Save customer data"""
    if request.method == 'POST':
        # Process form data here
        return JsonResponse({'success': True, 'message': 'Customer saved'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})