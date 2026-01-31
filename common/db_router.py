# common/db_router.py

from common.middleware.database_middleware import get_customer_db

class CustomerDatabaseRouter:
    """
    Hybrid Database Router:
    
    MAIN Database ('default'):
    - Django sessions (django_session table)
    - Django auth (User, Group, Permission)
    - Django admin, contenttypes, messages
    - Authentication tables (itemgroups, customers, softwares)
    
    Customer Database ('customer_db'):
    - All customer-specific models:
      * common app (Organization, CompanyInformation)
      * laundry app models
      * restaurant app models
      * inventory app models
      * financial app models
      * reports app models
    """
    
    # Apps that should ALWAYS use MAIN database
    main_database_apps = {
        'admin',
        'auth',
        'contenttypes',
        'sessions',        # Sessions go to MAIN database
        'messages',
    }
    
    # Apps that should use CUSTOMER database
    customer_database_apps = {
        'common',
        'inventory',
        'financial',
        'laundry',
        'restaurant',
        'reports',
    }
    
    def db_for_read(self, model, **hints):
        """
        Route read operations to appropriate database
        """
        app_label = model._meta.app_label
        model_name = model.__name__
        
        # Django core apps -> MAIN database
        if app_label in self.main_database_apps:
            print(f"[ROUTER READ] App: {app_label}, Model: {model_name}, Using DB: default")
            return 'default'
        
        # Customer apps -> CUSTOMER database
        if app_label in self.customer_database_apps:
            db = get_customer_db()
            print(f"[ROUTER READ] App: {app_label}, Model: {model_name}, Using DB: {db}")
            return db
        
        # Default to MAIN database
        print(f"[ROUTER READ] App: {app_label}, Model: {model_name}, Using DB: default (fallback)")
        return 'default'
    
    def db_for_write(self, model, **hints):
        """
        Route write operations to appropriate database
        """
        app_label = model._meta.app_label
        model_name = model.__name__
        
        # Django core apps -> MAIN database
        if app_label in self.main_database_apps:
            print(f"[ROUTER WRITE] App: {app_label}, Model: {model_name}, Using DB: default")
            return 'default'
        
        # Customer apps -> CUSTOMER database
        if app_label in self.customer_database_apps:
            db = get_customer_db()
            print(f"[ROUTER WRITE] App: {app_label}, Model: {model_name}, Using DB: {db}")
            return db
        
        # Default to MAIN database
        print(f"[ROUTER WRITE] App: {app_label}, Model: {model_name}, Using DB: default (fallback)")
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both objects are in the same database
        """
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)
        
        # Allow relations if both in same database
        if db1 and db2:
            return db1 == db2
        
        # Allow all other relations
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure migrations only happen in the appropriate database
        """
        # Django core apps migrate to MAIN database
        if app_label in self.main_database_apps:
            return db == 'default'
        
        # Customer apps migrate to CUSTOMER database
        if app_label in self.customer_database_apps:
            return db == 'customer_db'
        
        # Default: allow migration to MAIN database
        return db == 'default'