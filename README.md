# Django Multi-Business ERP System

A scalable Django-based ERP system supporting multiple business types (Laundry, Restaurant, and more).

## Features

- 🏢 Multi-business architecture (Laundry, Restaurant, future: Logistics, Trading)
- 📊 Comprehensive inventory management
- 💰 Financial accounting and reporting
- 👥 Customer and supplier management
- 🎨 Dynamic theming and business-specific UI
- 📱 Responsive design
- 🔐 Role-based access control
- 📈 Advanced reporting and analytics

## Project Structure

```
erp_project/
├── core/              # Core functionality and utilities
├── common/            # Shared models and components
├── inventory/         # Inventory management
├── financial/         # Financial accounting
├── reports/           # Reporting system
├── laundry/           # Laundry business module
├── restaurant/        # Restaurant business module
└── api/               # REST API
```

## Setup Instructions

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

## Adding New Business Module

To add a new business type (e.g., logistics, trading):

1. Create new app:
```bash
python manage.py startapp [business_name]
```

2. Follow the structure of existing business modules (laundry/restaurant)
3. Update business_config.json
4. Create business-specific templates and static files

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and development process.

## License

This project is licensed under the MIT License.
