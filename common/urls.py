from django.urls import path
from common.views import company_info, customers, settings
from common.views import auth  # Import auth views

app_name = 'common'

urlpatterns = [
    # Authentication URLs
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    
    # Home page
    path('', settings.home, name='home'),
    
    # Customer URLs
    path('customer/', customers.customer_form, name='customer'),
    
    # Company URLs
    path('company/', company_info.company_form, name='company_form'),
    
    # Lookup & Search endpoints
    path('company/lookup/', company_info.lookup_company, name='lookup_company'),  # Exact lookup
    path('company/search/name/', company_info.search_company_by_name, name='search_company_name'),  # Autocomplete
    path('company/search/email/', company_info.search_company_by_email, name='search_company_email'),  # Autocomplete
    
    # CRUD operations
    path('company/save/', company_info.save_company, name='save_company'),
    path('company/get/<int:company_id>/', company_info.get_company, name='get_company'),
    path('company/delete/<int:company_id>/', company_info.delete_company, name='delete_company'),


    # Settings URLs
    path('settings/database/', settings.database_config, name='database_config'),
]