# common/views/auth.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from django.db.utils import OperationalError, DatabaseError
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def login_view(request):
    """
    Handle user login
    Authenticates against the 'itemgroups' table in main database
    """
    
    # If already logged in, redirect to home
    if request.session.get('is_authenticated'):
        return redirect('common:home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return render(request, 'common/auth/login.html')
        
        # Try to authenticate
        try:
            # Authenticate user
            success, user_data = authenticate_user(username, password)
            
            if success:
                # Set session variables
                request.session['is_authenticated'] = True
                request.session['username'] = user_data.get('username')
                request.session['custid'] = user_data.get('custid')
                request.session['company_name'] = user_data.get('company_name')
                request.session['company_expiry'] = user_data.get('company_expiry')
                
                # Customer database credentials (from softwares table)
                request.session['db_host'] = user_data.get('customer_db_host')
                request.session['db_name'] = user_data.get('customer_db_name')
                request.session['db_user'] = user_data.get('customer_db_user')
                request.session['db_password'] = user_data.get('customer_db_password')
                
                logger.info(f"Login successful for user: {username}")
                logger.info(f"Customer DB: {user_data.get('customer_db_host')}/{user_data.get('customer_db_name')}")
                messages.success(request, f'Welcome back, {username}!')
                
                # Redirect to next URL if it exists
                next_url = request.session.pop('next_url', None)
                if next_url:
                    return redirect(next_url)
                
                return redirect('common:home')
            else:
                logger.warning(f"Login failed for user: {username}")
                messages.error(request, 'Invalid username or password.')
                return render(request, 'common/auth/login.html')
                
        except OperationalError as e:
            error_msg = str(e).lower()
            logger.error(f"Database connection error during login: {str(e)}")
            
            if 'timeout' in error_msg or 'timed out' in error_msg:
                messages.error(request, 
                    'Connection to database server timed out. '
                    'Please check your network connection or contact administrator.')
            elif 'could not connect' in error_msg or 'connection refused' in error_msg:
                messages.error(request, 
                    'Cannot reach database server. '
                    'Please verify server address and firewall settings.')
            elif 'authentication failed' in error_msg or 'password authentication failed' in error_msg:
                messages.error(request, 
                    'Database authentication failed. '
                    'Please contact administrator to verify database credentials.')
            elif 'does not exist' in error_msg or 'no such table' in error_msg:
                messages.error(request, 
                    'Database or table does not exist. '
                    'Please contact administrator.')
            else:
                messages.error(request, 
                    'Database connection failed. Please contact administrator.')
            
            return render(request, 'common/auth/login.html')
            
        except DatabaseError as e:
            logger.error(f"Database error during login: {str(e)}")
            messages.error(request, 
                'Database query error. Please contact administrator.')
            return render(request, 'common/auth/login.html')
            
        except Exception as e:
            logger.error(f"Unexpected login error: {str(e)}", exc_info=True)
            messages.error(request, 
                'An unexpected error occurred. Please try again or contact administrator.')
            return render(request, 'common/auth/login.html')
    
    # GET request - show login form
    return render(request, 'common/auth/login.html')


def get_table_columns(cursor, table_name, query_placeholder):
    """
    Get column names for a table
    Returns dict mapping lowercase column name to actual column name
    """
    if query_placeholder == '%s':
        # PostgreSQL
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, [table_name])
        columns = [row[0] for row in cursor.fetchall()]
        # Create mapping of lowercase -> actual name
        return {col.lower(): col for col in columns}
    else:
        # SQLite - get pragma table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        return {col.lower(): col for col in columns}


def authenticate_user(username, password):
    """
    Authenticate user against the 'itemgroups' table in MAIN database
    
    PostgreSQL Note: Column names are lowercase in PostgreSQL:
    - description (username)
    - narration (password)
    - custid (customer ID)
    
    Flow:
    1. Connect to MAIN database (from .env)
    2. Authenticate user from itemgroups table
    3. Get custid from itemgroups
    4. Fetch company info from customers table
    5. Fetch customer database credentials from softwares table
    
    Args:
        username: User's username (from description field)
        password: User's password (from narration field)
        
    Returns:
        tuple: (success: bool, user_data: dict)
    """
    
    conn = None
    cursor = None
    
    try:
        # Load environment variables from .env file (MAIN database)
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
        load_dotenv(env_path)
        
        # Get MAIN database credentials from .env
        main_db_host = os.getenv('DB_HOST', '')
        main_db_port = os.getenv('PORT', '5432')
        main_db_name = os.getenv('DB_NAME', '')
        main_db_user = os.getenv('DB_USER', '')
        main_db_password = os.getenv('DB_PASSWORD', '')
        
        print("\n" + "="*80)
        print("AUTHENTICATION - MAIN DATABASE")
        print("="*80)
        print(f"Host:     {main_db_host if main_db_host else 'Not configured'}")
        print(f"Port:     {main_db_port if main_db_port else 'Not configured'}")
        print(f"Database: {main_db_name if main_db_name else 'Not configured'}")
        print(f"User:     {main_db_user if main_db_user else 'Not configured'}")
        print("="*80 + "\n")
        
        # Create connection to MAIN database
        if not main_db_host or main_db_host.strip() == '':
            # SQLite fallback for testing
            import sqlite3
            print(f"Connecting to SQLite database: {main_db_name}")
            conn = sqlite3.connect(main_db_name)
            cursor = conn.cursor()
            query_placeholder = '?'
        else:
            # PostgreSQL connection to MAIN database
            print(f"Connecting to PostgreSQL MAIN database...")
            import psycopg2
            conn = psycopg2.connect(
                host=main_db_host,
                port=main_db_port,
                database=main_db_name,
                user=main_db_user,
                password=main_db_password
            )
            conn.autocommit = False  # Explicitly manage transactions
            cursor = conn.cursor()
            query_placeholder = '%s'
        
        print(f"✓ Connected to MAIN database")
        print(f"Authenticating user: {username}\n")
        
        # Step 1: Authenticate user from itemgroups table
        # PostgreSQL: Use lowercase column names (description, narration, custid)
        auth_query = f"""
            SELECT 
                description,
                narration,
                custid
            FROM itemgroups
            WHERE description = {query_placeholder}
            AND narration = {query_placeholder}
        """
        
        logger.debug(f"Executing authentication query for user: {username}")
        cursor.execute(auth_query, [username, password])
        
        user = cursor.fetchone()
        
        if not user:
            logger.warning(f"Authentication failed - invalid credentials for user: {username}")
            cursor.close()
            conn.close()
            return False, {}
        
        # User found - extract data
        db_username = user[0]
        db_password = user[1]
        custid = user[2] if len(user) > 2 else None
        
        print(f"✓ User authenticated: {db_username}")
        print(f"  custid: {custid}")
        
        if not custid:
            logger.error(f"No custid found for user: {username}")
            cursor.close()
            conn.close()
            return False, {}
        
        # Step 2: Fetch company name from customers table
        company_name = None
        company_query = f'SELECT custname FROM customers WHERE custid = {query_placeholder}'
        cursor.execute(company_query, [custid])
        company_result = cursor.fetchone()
        
        if company_result:
            company_name = company_result[0]
            print(f"  Company: {company_name}")
        else:
            print(f"  No company name found for custid: {custid}")
        
        # Step 3: Fetch company expiry from softwares table
        company_expiry = None
        expiry_query = f'SELECT expiry FROM softwares WHERE custid = {query_placeholder}'
        cursor.execute(expiry_query, [custid])
        expiry_result = cursor.fetchone()
        
        if expiry_result:
            company_expiry = expiry_result[0]
            # Convert date to string for session storage
            if company_expiry:
                try:
                    company_expiry = company_expiry.strftime('%Y-%m-%d')
                except:
                    company_expiry = str(company_expiry)
            print(f"  Expiry: {company_expiry}")
        
        # Step 4: Fetch CUSTOMER database credentials from softwares table
        # Get actual column names from the table
        print("  Detecting softwares table structure...")
        column_map = get_table_columns(cursor, 'softwares', query_placeholder)
        print(f"  Available columns (lowercase): {list(column_map.keys())}")
        
        # Find the correct column names
        host_col = column_map.get('host', 'host')
        db_col = column_map.get('db', column_map.get('database', 'DB'))
        username_col = column_map.get('username', column_map.get('user', 'username'))
        pwd_col = column_map.get('pwd', column_map.get('password', 'pwd'))
        dbpass_col = column_map.get('dbpass', pwd_col)
        
        print(f"  Using columns: host={host_col}, db={db_col}, username={username_col}, pwd={pwd_col}, dbpass={dbpass_col}")
        
        # Build query with actual column names
        customer_db_query = f"""
            SELECT 
                {host_col},
                {db_col},
                {username_col},
                {pwd_col},
                {dbpass_col}
            FROM softwares
            WHERE custid = {query_placeholder}
        """
        
        cursor.execute(customer_db_query, [custid])
        customer_db_result = cursor.fetchone()
        
        if not customer_db_result:
            logger.error(f"No customer database credentials found for custid: {custid}")
            cursor.close()
            conn.close()
            return False, {}
        
        # Extract customer database credentials
        customer_db_host = customer_db_result[0]
        customer_db_name = customer_db_result[1]
        customer_db_user = customer_db_result[2]
        # Use dbpass if available, otherwise pwd
        customer_db_password = customer_db_result[4] if customer_db_result[4] else customer_db_result[3]
        
        print("\n" + "="*80)
        print("CUSTOMER DATABASE CREDENTIALS (from softwares table)")
        print("="*80)
        print(f"Host:     {customer_db_host}")
        print(f"Database: {customer_db_name}")
        print(f"User:     {customer_db_user}")
        print(f"Password: {'*' * len(str(customer_db_password)) if customer_db_password else 'Not set'}")
        print("="*80 + "\n")
        
        # Commit transaction
        if query_placeholder == '%s':
            conn.commit()
        
        # Prepare user data
        user_data = {
            'username': db_username,
            'custid': custid,
            'company_name': company_name,
            'company_expiry': company_expiry,
            
            # Customer database credentials (for middleware)
            'customer_db_host': customer_db_host,
            'customer_db_name': customer_db_name,
            'customer_db_user': customer_db_user,
            'customer_db_password': customer_db_password,
        }
        
        logger.info(f"User authenticated successfully: {username}")
        logger.info(f"Company: {company_name}, Expiry: {company_expiry}")
        logger.info(f"Customer DB: {customer_db_host}/{customer_db_name}")
        
        # Close connection
        cursor.close()
        conn.close()
        
        return True, user_data
                
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}", exc_info=True)
        
        # Rollback transaction on error
        try:
            if conn and query_placeholder == '%s':
                conn.rollback()
        except:
            pass
        
        # Close connection on error
        try:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        except:
            pass
        
        return False, {}


def logout_view(request):
    """Handle user logout"""
    
    username = request.session.get('username', 'User')
    
    # Clear session
    request.session.flush()
    
    logger.info(f"User logged out: {username}")
    messages.info(request, 'You have been logged out successfully.')
    return redirect('common:login')