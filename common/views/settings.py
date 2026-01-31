from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from core.dbhelper import DatabaseHelper
from datetime import datetime, timedelta

def get_common_context():
    """Get common context data for all views"""
    return {
        'company_info': {
            'name': 'Nepton Business System',
            'short_name': 'Nepton',
            'tagline': 'Business System',
            'expiry_date': (datetime.now() + timedelta(days=365)).strftime('%d %b %Y'),
        },
        'user_info': {
            'name': 'Muhammed Ashiqu',
            'id': 'ASHIQU',
            'account': 'AQWE#'
        },
        'navbar_config': {
            'sections': [
                {
                    'id': 'pending',
                    'label': 'Pending',
                    'icon': '📋',
                    'items': [
                        {'label': 'Pending Transactions', 'url': '#', 'count': 3},
                        {'label': 'Pending Approvals', 'url': '#', 'count': 5},
                    ]
                },
                {
                    'id': 'admin',
                    'label': 'Admin',
                    'icon': '⚙️',
                    'items': [
                        {'label': 'User Management', 'url': '#'},
                        {'label': 'Workflow Management', 'url': '#'},
                        {'label': 'Database Configuration', 'url': 'common:database_config'},
                    ]
                },
                {
                    'id': 'transactions',
                    'label': 'Transactions',
                    'icon': '💳',
                    'items': [
                        {'label': 'Debit and Deposit Card', 'url': '#', 'status': 'Draft'},
                        {'label': 'All Transactions', 'url': '#'},
                    ]
                },
                {
                    'id': 'accounts',
                    'label': 'Accounts',
                    'icon': '🏦',
                    'items': [
                        {'label': 'Account Summary', 'url': '#'},
                        {'label': 'View All Accounts', 'url': '#'},
                    ]
                },
                {
                    'id': 'settings',
                    'label': 'Settings',
                    'icon': '🔧',
                    'items': [
                        {'label': 'Company Information', 'url': 'common:company_form'},
                        {'label': 'Customer Management', 'url': 'common:customer'},
                        {'label': 'System Settings', 'url': '#'},
                    ]
                },
            ]
        }
    }

def home(request):
    """
    Home view - Updated to include user session info and company info from database
    """
    
    # Check authentication
    if not request.session.get('is_authenticated'):
        return redirect('common:login')
    
    # Get user info from session
    user_info = {
        'name': request.session.get('username', 'User'),
        'id': request.session.get('custid', 'N/A'),
        'software_id': request.session.get('software_id'),
        'customer_id': request.session.get('customer_id'),
    }
    
    # Get company info from session (fetched from database during login)
    company_name = request.session.get('company_name', 'Your Company')
    company_expiry = request.session.get('company_expiry', 'N/A')
    
    # Format expiry date if it's a date object
    if company_expiry and company_expiry != 'N/A':
        try:
            # If it's already a string, use it
            if isinstance(company_expiry, str):
                formatted_expiry = company_expiry
            else:
                # If it's a datetime object, format it
                formatted_expiry = company_expiry.strftime('%d %b %Y')
        except:
            formatted_expiry = str(company_expiry)
    else:
        formatted_expiry = '31 Dec 2025'
    
    company_info = {
        'name': company_name,
        'short_name': company_name[:10] if company_name else 'Company',  # First 10 chars
        'tagline': 'Business System',
        'expiry_date': formatted_expiry,
    }
    
    # Navbar configuration based on software_id
    software_id = request.session.get('software_id')
    
    if software_id == 4:
        # Laundry menu
        navbar_config = {
            'sections': [
                {
                    'id': 'orders',
                    'label': 'Orders',
                    'icon': '📋',
                    'active': True,
                    'items': [
                        {'label': 'New Order', 'url': 'laundry:new_order', 'active': False},
                        {'label': 'Pending Orders', 'url': 'laundry:pending_orders', 'count': 5},
                        {'label': 'Completed Orders', 'url': 'laundry:completed_orders'},
                    ]
                },
                {
                    'id': 'customers',
                    'label': 'Customers',
                    'icon': '👥',
                    'items': [
                        {'label': 'All Customers', 'url': 'laundry:customers'},
                        {'label': 'Add Customer', 'url': 'laundry:add_customer'},
                    ]
                },
                {
                    'id': 'services',
                    'label': 'Services',
                    'icon': '🧺',
                    'items': [
                        {'label': 'Service List', 'url': 'laundry:services'},
                        {'label': 'Pricing', 'url': 'laundry:pricing'},
                    ]
                },
            ]
        }
    elif software_id == 5:
        # Restaurant menu
        navbar_config = {
            'sections': [
                {
                    'id': 'orders',
                    'label': 'Orders',
                    'icon': '🍽️',
                    'active': True,
                    'items': [
                        {'label': 'New Order', 'url': 'restaurant:new_order', 'active': False},
                        {'label': 'Pending Orders', 'url': 'restaurant:pending_orders', 'count': 3},
                        {'label': 'Completed Orders', 'url': 'restaurant:completed_orders'},
                    ]
                },
                {
                    'id': 'menu',
                    'label': 'Menu',
                    'icon': '📖',
                    'items': [
                        {'label': 'All Items', 'url': 'restaurant:menu_items'},
                        {'label': 'Add Item', 'url': 'restaurant:add_item'},
                        {'label': 'Categories', 'url': 'restaurant:categories'},
                    ]
                },
                {
                    'id': 'tables',
                    'label': 'Tables',
                    'icon': '🪑',
                    'items': [
                        {'label': 'All Tables', 'url': 'restaurant:tables'},
                        {'label': 'Reservations', 'url': 'restaurant:reservations'},
                    ]
                },
            ]
        }
    else:
        # Default/common menu
        navbar_config = {
            'sections': [
                {
                    'id': 'masters',
                    'label': 'Masters',
                    'icon': '📊',
                    'active': True,
                    'items': [
                        {'label': 'Company Info', 'url': 'common:company_form', 'active': False},
                        {'label': 'Customers', 'url': 'common:customer'},
                    ]
                },
                {
                    'id': 'settings',
                    'label': 'Settings',
                    'icon': '⚙️',
                    'items': [
                        {'label': 'Database Config', 'url': 'common:database_config'},
                        {'label': 'Logout', 'url': 'common:logout'},
                    ]
                },
            ]
        }
    
    context = {
        'page_title': 'Dashboard',
        'user_info': user_info,
        'company_info': company_info,
        'navbar_config': navbar_config,
        'show_form': False,
    }
    
    return render(request, 'common/home.html', context)


def database_config(request):
    """Show database configuration form"""
    
    print("=" * 60)
    print("DATABASE CONFIG VIEW - DEBUG")
    print("=" * 60)
    
    db_configured = DatabaseHelper.is_configured()
    
    # Default config
    db_config = {
        'HOST': '',
        'PORT': '5432',
        'NAME': '',
        'USER': '',
        'PASSWORD': ''
    }
    
    if db_configured:
        loaded_config = DatabaseHelper.load_credentials()
        if loaded_config:
            db_config.update(loaded_config)
            db_config['PASSWORD'] = '********'
    
    # Configure the form using universal form system
    db_form_config = {
        'form_id': 'database-config-form',
        'title': 'PostgreSQL Database Connection',
        'icon': '🗄️',
        'action': '/settings/save-database/',
        'footer_status': 'Ready',
        'background': 'soft-pink',
        
        # Buttons configuration
        'buttons': [
            {
                'label': 'Test Connection',
                'icon': '🔌',
                'type': 'primary',
                'onclick': "testConnection()"
            },
            {
                'label': 'Save',
                'icon': '💾',
                'type': 'success',
                'onclick': "saveDatabase()"
            },
        ],
        
        # Menu items (optional)
        'menu_items': [],
        
        # No groups - all fields in main area
        'groups': [],
        
        # Fields configuration
        'fields': [
            {
                'name': 'db_host',
                'label': 'Database Host',
                'type': 'text',
                'required': True,
                'width': '50%',
                'placeholder': 'e.g., localhost or 192.168.1.100',
                'group': None
            },
            {
                'name': 'db_port',
                'label': 'Port',
                'type': 'number',
                'required': True,
                'width': '50%',
                'placeholder': '5432',
                'group': None
            },
            {
                'name': 'db_name',
                'label': 'Database Name',
                'type': 'text',
                'required': True,
                'width': '100%',
                'placeholder': 'Enter database name',
                'group': None
            },
            {
                'name': 'db_user',
                'label': 'Username',
                'type': 'text',
                'required': True,
                'width': '50%',
                'placeholder': 'postgres',
                'group': None
            },
            {
                'name': 'db_password',
                'label': 'Password',
                'type': 'password',
                'required': True,
                'width': '50%',
                'placeholder': 'Enter password',
                'group': None
            },
        ]
    }
    
    # Add default values if config exists
    if db_configured:
        for field in db_form_config['fields']:
            field_name = field['name'].replace('db_', '').upper()
            if field_name in db_config:
                # We don't have a 'value' key in the template, so we'll use placeholder
                # or you can modify the template to support initial values
                pass
    
    context = {
        'db_form_config': db_form_config,
        'db_configured': db_configured,
        'page_title': 'Database Configuration',
    }
    
    print(f"Context keys: {context.keys()}")
    print(f"Form config keys: {db_form_config.keys()}")
    print(f"Number of fields: {len(db_form_config['fields'])}")
    print(f"Template: common/database_config.html")
    print("=" * 60)
    
    return render(request, 'common/settings/database_config.html', context)


def save_database_config(request):
    """Save database configuration"""
    
    if request.method == 'POST':
        
        db_config = {
            'engine': 'postgresql',
            'name': request.POST.get('db_name'),
            'user': request.POST.get('db_user'),
            'password': request.POST.get('db_password'),
            'host': request.POST.get('db_host'),
            'port': request.POST.get('db_port')
        }
        
        # Test connection first
        success, message = DatabaseHelper.test_connection(db_config)
        
        if success:
            # Save credentials
            DatabaseHelper.save_credentials(db_config)
            messages.success(request, 'Database configuration saved! Please restart the server.')
            return redirect('common:home')
        else:
            messages.error(request, f'Connection failed: {message}')
            return redirect('common:database_config')
    
    return redirect('common:home')


def test_database_connection(request):
    """Test database connection via AJAX"""
    
    if request.method == 'POST':
        
        db_config = {
            'engine': 'postgresql',
            'name': request.POST.get('db_name'),
            'user': request.POST.get('db_user'),
            'password': request.POST.get('db_password'),
            'host': request.POST.get('db_host'),
            'port': request.POST.get('db_port')
        }
        
        success, message = DatabaseHelper.test_connection(db_config)
        
        return JsonResponse({
            'success': success,
            'message': message if success else None,
            'error': message if not success else None
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})