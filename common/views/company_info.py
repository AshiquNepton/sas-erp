# common/views/company.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from datetime import datetime
import traceback
import logging

from common.models.company_information import Organization
from common.middleware.database_middleware import get_customer_db
from common.utils.form_helpers import (
    fetch_record_by_field_view, 
    search_records_view
)

logger = logging.getLogger(__name__)

# Field mapping for Company form
COMPANY_FIELD_MAPPING = {
    # Database field -> Frontend field
    'CompanyId': 'company_code',
    'CompanyName': 'company_name',
    'ArabicName': 'arabic_name',
    'Subtitle': 'subtitle',
    'Address1': 'address1',
    'Address2': 'address2',
    'Address3': 'address3',
    'Phone': 'phone',
    'Mobile': 'mobile',
    'Url': 'website',
    'Email': 'email',
    'TinNo': 'tinno',
    'CrNo': 'crno',
    'LicenseNo': 'licenseno',
    'BuildingNo': 'building_no',
    'StreetName': 'street_name',
    'Zone': 'zone',
    'Area': 'area',
    'City': 'city',
    'State': 'state',
    'District': 'district',
    'PoBox': 'po_box',
    'PlotIdentification': 'plot_identification',
    'AccountNumber': 'account_number',
    'AccountName': 'account_name',
    'Branch': 'branch',
    'Ifsc': 'ifsc',
    'PayerId': 'payer_id',
    'PayerBank': 'payer_bank',
    'PayerIban': 'payer_iban',
    'PeriodFrom': 'period_from',
    'PeriodTo': 'period_to',
    'BusinessType': 'business_type',
    'DefaultDb': 'default_db',
}

# Reverse mapping
FRONTEND_TO_DB_MAPPING = {v: k for k, v in COMPANY_FIELD_MAPPING.items()}


def company_form(request):
    """Company form view"""
    
    # Check if user is authenticated
    if not request.session.get('is_authenticated'):
        from django.shortcuts import redirect
        return redirect('common:login')
    
    # Get current year for default period dates
    current_year = datetime.now().year
    
    # Company form configuration
    form_config = {
        'form_id': 'company-form',
        'title': 'Company Information',
        'icon': '🏢',
        'action': reverse('common:save_company'),
        'footer_status': 'Ready',
        'background': 'white',
        
        # Buttons configuration
        'buttons': [
            {
                'label': 'New',
                'icon': '➕',
                'type': 'primary',
                'onclick': "newCompany()"
            },
            {
                'label': 'Save',
                'icon': '💾',
                'type': 'success',
                'onclick': "saveCompany()"
            },
            {
                'label': 'Delete',
                'icon': '🗑️',
                'type': 'danger',
                'onclick': "deleteCompany()"
            },
        ],
        
        # Menu items
        'menu_items': [
            {'label': 'Print', 'icon': '🖨️', 'onclick': "printCompany()"},
            {'label': 'Export', 'icon': '📤', 'onclick': "exportCompany()"},
            {'label': 'Settings', 'icon': '⚙️', 'onclick': "companySettings()"},
        ],
        
        # Field groups
        'groups': [
            {
                'id': 'address',
                'title': 'General',
                'icon': '📍',
            },
            {
                'id': 'contact',
                'title': 'Contact Information',
                'icon': '📞',
            },
            {
                'id': 'financial',
                'title': 'Financial Information',
                'icon': '💰',
            },
            {
                'id': 'options',
                'title': 'Options',
                'icon': '🔗',
            },
        ],
        
        # Fields configuration
        'fields': [
            # Basic Information Fields
            {
                'name': 'company_code',
                'label': 'Company Code',
                'type': 'text',
                'required': True,
                'width': '50%',
                'placeholder': 'Enter Company code',
                'group': None,
                'db_field': 'CompanyId',
                'lookup': True,  # Enable exact lookup
            },
            {
                'name': 'company_name',
                'label': 'Company Name',
                'type': 'text',
                'required': True,
                'width': '50%',
                'placeholder': 'Start typing to search...',
                'group': None,
                'db_field': 'CompanyName',
                'autocomplete': True,  # Enable autocomplete dropdown
            },
            {
                'name': 'arabic_name',
                'label': 'Arabic Name',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter Arabic name',
                'group': None,
                'db_field': 'ArabicName'
            },
            {
                'name': 'subtitle',
                'label': 'Subtitle',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter subtitle',
                'group': None,
                'db_field': 'Subtitle'
            },
            {
                'name': 'business_type',
                'label': 'Business Type',
                'type': 'select',
                'required': True,
                'width': '33.33%',
                'placeholder': 'Select business type',
                'group': None,
                'db_field': 'BusinessType',
                'options': [
                    {'value': '1', 'label': 'Laundry'},
                    {'value': '2', 'label': 'Restaurant'},
                ]
            },
            {
                'name': 'period_from',
                'label': 'Period From',
                'type': 'date',
                'required': True,
                'width': '50%',
                'group': None,
                'db_field': 'PeriodFrom',
                'default': f'{current_year}-01-01'
            },
            {
                'name': 'period_to',
                'label': 'Period To',
                'type': 'date',
                'required': True,
                'width': '50%',
                'group': None,
                'db_field': 'PeriodTo',
                'default': f'{current_year}-12-31'
            },

            # Address Group
            {
                'name': 'crno',
                'label': 'CR No',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'CR No',
                'group': 'address',
                'db_field': 'CrNo'
            },
            {
                'name': 'licenseno',
                'label': 'License No',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'License No',
                'group': 'address',
                'db_field': 'LicenseNo'
            },
            {
                'name': 'address1',
                'label': 'Address 1',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter address 1',
                'group': 'address',
                'db_field': 'Address1'
            },
            {
                'name': 'address2',
                'label': 'Address 2',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter address 2',
                'group': 'address',
                'db_field': 'Address2'
            },
            {
                'name': 'address3',
                'label': 'Address 3',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter address 3',
                'group': 'address',
                'db_field': 'Address3'
            },
            {
                'name': 'building_no',
                'label': 'Building No',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter building number',
                'group': 'address',
                'db_field': 'BuildingNo'
            },
            {
                'name': 'street_name',
                'label': 'Street Name',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter street name',
                'group': 'address',
                'db_field': 'StreetName'
            },
            {
                'name': 'zone',
                'label': 'Zone',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter zone',
                'group': 'address',
                'db_field': 'Zone'
            },
            {
                'name': 'area',
                'label': 'Area',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter area',
                'group': 'address',
                'db_field': 'Area'
            },
            {
                'name': 'city',
                'label': 'City',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter city',
                'group': 'address',
                'db_field': 'City'
            },
            {
                'name': 'state',
                'label': 'State/Province',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter state',
                'group': 'address',
                'db_field': 'State'
            },
            {
                'name': 'district',
                'label': 'District',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter district',
                'group': 'address',
                'db_field': 'District'
            },
            {
                'name': 'po_box',
                'label': 'PO Box',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter PO Box',
                'group': 'address',
                'db_field': 'PoBox'
            },
            {
                'name': 'plot_identification',
                'label': 'Plot Identification',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter plot identification',
                'group': 'address',
                'db_field': 'PlotIdentification'
            },
            
            # Contact Information Group
            {
                'name': 'phone',
                'label': 'Phone',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter phone number',
                'group': 'contact',
                'db_field': 'Phone'
            },
            {
                'name': 'mobile',
                'label': 'Mobile',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter mobile number',
                'group': 'contact',
                'db_field': 'Mobile'
            },
            {
                'name': 'email',
                'label': 'Email',
                'type': 'email',
                'required': False,
                'width': '50%',
                'placeholder': 'Start typing email...',
                'group': 'contact',
                'db_field': 'Email',
                'autocomplete': True,  # Enable autocomplete
            },
            {
                'name': 'website',
                'label': 'Website',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter website URL',
                'group': 'contact',
                'db_field': 'Url'
            },
            
            # Financial Information Group
            {
                'name': 'tinno',
                'label': 'TIN No',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter TIN No',
                'group': 'financial',
                'db_field': 'TinNo'
            },
            {
                'name': 'account_number',
                'label': 'Account Number',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter Account Number',
                'group': 'financial',
                'db_field': 'AccountNumber'
            },
            {
                'name': 'account_name',
                'label': 'Account Name',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter Account Name',
                'group': 'financial',
                'db_field': 'AccountName'
            },
            {
                'name': 'branch',
                'label': 'Branch',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter Branch Name',
                'group': 'financial',
                'db_field': 'Branch'
            },
            {
                'name': 'ifsc',
                'label': 'IFSC',
                'type': 'text',
                'required': False,
                'width': '50%',
                'placeholder': 'Enter IFSC',
                'group': 'financial',
                'db_field': 'Ifsc'
            },
            {
                'name': 'payer_id',
                'label': 'Payer ID',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter Payer ID',
                'group': 'financial',
                'db_field': 'PayerId'
            },
            {
                'name': 'payer_bank',
                'label': 'Payer Bank',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter Payer Bank',
                'group': 'financial',
                'db_field': 'PayerBank'
            },
            {
                'name': 'payer_iban',
                'label': 'Payer IBAN',
                'type': 'text',
                'required': False,
                'width': '33.33%',
                'placeholder': 'Enter Payer IBAN',
                'group': 'financial',
                'db_field': 'PayerIban'
            },
            
            # Options Group
            {
                'name': 'default_db',
                'label': 'Set as Default Database',
                'type': 'checkbox',
                'required': False,
                'width': '100%',
                'group': 'options',
                'db_field': 'DefaultDb'
            },
        ]
    }
    
    # Create context with form_config
    context = {
        'form_config': form_config,
        'page_title': 'Company Information',
    }
    
    return render(request, 'common/masters/company_form.html', context)


@require_http_methods(["GET"])
def lookup_company(request):
    """
    AJAX endpoint to lookup company by exact field value
    GET /company/lookup/?field=CompanyId&value=1
    """
    return fetch_record_by_field_view(request, Organization, COMPANY_FIELD_MAPPING)


@require_http_methods(["GET"])
def search_company_by_name(request):
    """
    AJAX endpoint for autocomplete search by company name
    GET /company/search/name/?q=Nep&limit=10
    """
    display_fields = ['company_code', 'company_name', 'city']
    return search_records_view(
        request, 
        Organization, 
        'CompanyName', 
        COMPANY_FIELD_MAPPING,
        display_fields
    )


@require_http_methods(["GET"])
def search_company_by_email(request):
    """
    AJAX endpoint for autocomplete search by email
    GET /company/search/email/?q=test&limit=10
    """
    display_fields = ['company_code', 'company_name', 'email']
    return search_records_view(
        request, 
        Organization, 
        'Email', 
        COMPANY_FIELD_MAPPING,
        display_fields
    )


@require_http_methods(["POST"])
def save_company(request):
    """Save company data - Optimized version"""
    
    try:
        customer_db = get_customer_db()
        company_id = request.POST.get('company_code')
        
        if not company_id:
            return JsonResponse({
                'success': False,
                'error': 'Company code is required'
            })
        
        # Prepare data
        company_data = {}
        
        for form_field, db_field in FRONTEND_TO_DB_MAPPING.items():
            value = request.POST.get(form_field)
            
            if db_field == 'CompanyId':
                try:
                    company_data[db_field] = int(value)
                except (ValueError, TypeError):
                    return JsonResponse({
                        'success': False,
                        'error': f'Invalid Company Code "{value}"'
                    })
            
            elif db_field == 'BusinessType':
                if value:
                    try:
                        company_data[db_field] = int(value)
                    except (ValueError, TypeError):
                        company_data[db_field] = 1
                else:
                    company_data[db_field] = 1
            
            elif db_field == 'DefaultDb':
                company_data[db_field] = 1 if value == 'on' or value == '1' else 0
            
            elif db_field in ['PeriodFrom', 'PeriodTo']:
                if value:
                    try:
                        company_data[db_field] = datetime.strptime(value, '%Y-%m-%d').date()
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'error': f'Invalid date format for {form_field}'
                        })
                else:
                    current_year = datetime.now().year
                    if db_field == 'PeriodFrom':
                        company_data[db_field] = datetime(current_year, 1, 1).date()
                    else:
                        company_data[db_field] = datetime(current_year, 12, 31).date()
            
            else:
                if value and value.strip():
                    company_data[db_field] = value.strip()
                else:
                    company_data[db_field] = None
        
        # Save or update
        try:
            company = Organization.objects.using(customer_db).get(CompanyId=company_data['CompanyId'])
            for field, value in company_data.items():
                if field != 'CompanyId':
                    setattr(company, field, value)
            company.save(using=customer_db)
            action = 'updated'
            
        except Organization.DoesNotExist:
            company = Organization(**company_data)
            company.save(using=customer_db)
            action = 'created'
        
        logger.info(f"Company {action}: {company.CompanyId} - {company.CompanyName}")
        
        return JsonResponse({
            'success': True,
            'message': f'Company {action} successfully',
            'company_id': company.CompanyId,
            'company_name': company.CompanyName
        })
        
    except Exception as e:
        logger.error(f"Error saving company: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["GET"])
def get_company(request, company_id):
    """Get company data by ID"""
    try:
        customer_db = get_customer_db()
        company = get_object_or_404(Organization.objects.using(customer_db), CompanyId=company_id)
        
        data = {}
        for db_field, form_field in COMPANY_FIELD_MAPPING.items():
            value = getattr(company, db_field, None)
            
            if value is None:
                data[form_field] = None
            elif hasattr(value, 'strftime'):
                data[form_field] = value.strftime('%Y-%m-%d')
            elif isinstance(value, bool) or db_field == 'DefaultDb':
                data[form_field] = value == 1 if isinstance(value, int) else value
            else:
                data[form_field] = str(value)
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error getting company: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_http_methods(["POST"])
def delete_company(request, company_id):
    """Delete company by ID"""
    try:
        customer_db = get_customer_db()
        company = get_object_or_404(Organization.objects.using(customer_db), CompanyId=company_id)
        company_name = company.CompanyName
        company.delete(using=customer_db)
        
        logger.info(f"Company deleted: {company_id} - {company_name}")
        
        return JsonResponse({
            'success': True,
            'message': f'Company "{company_name}" deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting company: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': str(e)
        })