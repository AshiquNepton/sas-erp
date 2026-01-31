# common/middleware/database_middleware.py

from django.db import connections
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.utils import OperationalError, ProgrammingError
import threading
import os
from dotenv import load_dotenv

# Thread-local storage for customer database alias
_thread_locals = threading.local()


def get_customer_db():
    """
    Get the current customer database alias from thread-local storage
    Returns 'customer_db' by default
    """
    return getattr(_thread_locals, 'customer_db', 'customer_db')


def set_customer_db(db_alias):
    """
    Set the customer database alias in thread-local storage
    """
    _thread_locals.customer_db = db_alias


def get_complete_db_config(host, port, name, user, password):
    """
    Get a complete database configuration dict with ALL required Django settings
    This prevents KeyError for CONN_HEALTH_CHECKS, TIME_ZONE, etc.
    """
    return {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,  # Don't persist connections
        'CONN_HEALTH_CHECKS': False,  # Required by Django 4.1+
        'OPTIONS': {
            'connect_timeout': 10,
        },
        'TIME_ZONE': getattr(settings, 'TIME_ZONE', 'UTC'),
        'TEST': {
            'CHARSET': None,
            'COLLATION': None,
            'NAME': None,
            'MIRROR': None,
        },
    }


def get_default_customer_db_config():
    """
    Get default customer database configuration from environment
    This is used as a fallback when user is not logged in
    """
    # Load environment variables
    env_path = os.path.join(settings.BASE_DIR, '.env')
    load_dotenv(env_path)
    
    # Use main database credentials as default for customer_db
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('PORT', '5432')
    db_name = os.getenv('DB_NAME', 'postgres')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', '')
    
    return get_complete_db_config(db_host, db_port, db_name, db_user, db_password)


class DynamicDatabaseMiddleware:
    """
    Middleware to dynamically configure customer database based on session data
    
    CRITICAL ORDER: This middleware MUST run BEFORE AuthenticationMiddleware
    to ensure customer database is configured before sessions are accessed
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Paths that should use default database (no session required)
        self.no_session_paths = [
            '/login/',
            '/static/',
            '/media/',
            '/favicon.ico',
            '/admin/',
        ]
    
    def __call__(self, request):
        path = request.path
        
        # Check if this path requires session access
        needs_session = True
        for no_session_path in self.no_session_paths:
            if path.startswith(no_session_path):
                needs_session = False
                break
        
        # Configure default database first
        default_config = get_default_customer_db_config()
        
        # If path doesn't need session, use default database config
        if not needs_session:
            settings.DATABASES['customer_db'] = default_config
            
            # Close existing connection
            if 'customer_db' in connections:
                try:
                    connections['customer_db'].close()
                except Exception:
                    pass
            
            set_customer_db('customer_db')
            request._customer_db_configured = True
            print(f"[MIDDLEWARE] Using default database for: {path}")
        
        else:
            # Try to get customer database credentials from session
            try:
                db_host = request.session.get('db_host')
                db_name = request.session.get('db_name')
                db_user = request.session.get('db_user')
                db_password = request.session.get('db_password')
                
                # If we have customer database credentials in session
                if all([db_host, db_name, db_user, db_password]):
                    # Configure the customer_db connection with complete settings
                    customer_db_config = get_complete_db_config(
                        db_host, '5432', db_name, db_user, db_password
                    )
                    
                    # Update the database configuration
                    settings.DATABASES['customer_db'] = customer_db_config
                    
                    # Close existing connection
                    if 'customer_db' in connections:
                        try:
                            connections['customer_db'].close()
                        except Exception:
                            pass
                    
                    set_customer_db('customer_db')
                    request._customer_db_configured = True
                    print(f"[MIDDLEWARE] Configured customer_db: {db_host}/{db_name}")
                
                else:
                    # No customer credentials in session - use default
                    settings.DATABASES['customer_db'] = default_config
                    
                    # Close existing connection
                    if 'customer_db' in connections:
                        try:
                            connections['customer_db'].close()
                        except Exception:
                            pass
                    
                    set_customer_db('customer_db')
                    request._customer_db_configured = True
                    print("[MIDDLEWARE] No customer credentials - using default database")
                    
            except (ProgrammingError, OperationalError) as e:
                # If we can't access session (table doesn't exist), use default
                print(f"[MIDDLEWARE] Database not migrated, using default database")
                print(f"[MIDDLEWARE] Please run: python manage.py migrate --database=customer_db")
                
                settings.DATABASES['customer_db'] = default_config
                
                # Close existing connection
                if 'customer_db' in connections:
                    try:
                        connections['customer_db'].close()
                    except Exception:
                        pass
                
                set_customer_db('customer_db')
                request._customer_db_configured = True
                
            except KeyError as e:
                # Handle settings KeyError
                print(f"[MIDDLEWARE] Settings error: {e}, using default database")
                settings.DATABASES['customer_db'] = default_config
                
                # Close existing connection
                if 'customer_db' in connections:
                    try:
                        connections['customer_db'].close()
                    except Exception:
                        pass
                
                set_customer_db('customer_db')
                request._customer_db_configured = True
                
            except Exception as e:
                # If we can't access session for any other reason, use default
                print(f"[MIDDLEWARE] Session access error: {e}, using default database")
                settings.DATABASES['customer_db'] = default_config
                
                # Close existing connection
                if 'customer_db' in connections:
                    try:
                        connections['customer_db'].close()
                    except Exception:
                        pass
                
                set_customer_db('customer_db')
                request._customer_db_configured = True
        
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """
        Handle database connection exceptions
        """
        from django.db.utils import OperationalError, DatabaseError
        
        if isinstance(exception, (OperationalError, DatabaseError, ProgrammingError, KeyError)):
            print(f"[MIDDLEWARE] Database error: {str(exception)}")
            
            # If it's a connection error, try to close the connection
            if 'customer_db' in connections:
                try:
                    connections['customer_db'].close()
                except Exception:
                    pass
        
        return None