# Digital Marketplace ERPNext Integration

A Frappe app that integrates the UK Government's Digital Marketplace tenders/briefs with ERPNext, automating the process of loading procurement opportunities into your ERP system.

## Overview

This app enables automatic synchronization of:
- **Briefs/Tenders**: Digital Marketplace procurement opportunities (live, closed, etc.)
- **Frameworks**: G-Cloud, Digital Outcomes and Specialists frameworks
- **Lots**: Service categories (SaaS, PaaS, IaaS, Digital Specialists, etc.)
- **Suppliers**: Registered suppliers on the Digital Marketplace
- **Services**: Published services from suppliers

## Features

- 🔄 **Automated Sync**: Scheduled jobs to automatically fetch and update tenders
- 📊 **Complete Data Model**: DocTypes for all major Digital Marketplace entities
- 🔐 **Secure API Integration**: Token-based authentication with the Digital Marketplace API
- 📝 **Full Tender Details**: Captures requirements, budgets, timelines, and evaluation criteria
- 🔗 **Linked Data**: Maintains relationships between briefs, frameworks, lots, and suppliers
- 📅 **Configurable Sync**: Choose sync frequency (hourly, daily, weekly)

## Installation

### Prerequisites

- Frappe/ERPNext installed and running
- Python 3.9 or higher
- Access to Digital Marketplace API (auth token required)

### Install via bench

```bash
# Get the app from the repository
bench get-app https://github.com/alexleach/digitalmarketplace-api.git --branch copilot/create-frappe-app-for-tenders

# Install the app on your site
bench --site [your-site-name] install-app dm_erpnext_integration

# Migrate the database
bench --site [your-site-name] migrate
```

### Manual Installation

1. Clone the repository:
```bash
cd ~/frappe-bench/apps
git clone https://github.com/alexleach/digitalmarketplace-api.git
cd digitalmarketplace-api
git checkout copilot/create-frappe-app-for-tenders
```

2. Install dependencies:
```bash
cd dm_erpnext_integration
pip install -e .
```

3. Install the app on your site:
```bash
bench --site [your-site-name] install-app dm_erpnext_integration
bench --site [your-site-name] migrate
```

## Configuration

### 1. Set up API credentials

1. Navigate to: **Home > Digital Marketplace > DM API Settings**
2. Configure the following:
   - **API URL**: The Digital Marketplace API base URL (default: `https://www.digitalmarketplace.service.gov.uk/api`)
   - **Auth Token**: Your Digital Marketplace API authentication token
   - **Enabled**: Check to enable synchronization
   - **Sync Frequency**: Choose how often to sync (Hourly, Every 6 Hours, Daily, Weekly)

### 2. Getting an API Token

To obtain an API token for the Digital Marketplace:

1. Contact the Digital Marketplace support team
2. Or, if you're running your own instance of the digitalmarketplace-api (this repository):
   ```bash
   # Set the auth token in environment variable
   export DM_API_AUTH_TOKENS=mySecretToken123:anotherToken456
   ```

### 3. Run Initial Sync

After configuration, you can trigger an initial sync manually:

```bash
# Sync frameworks and lots
bench --site [your-site-name] execute dm_erpnext_integration.dm_erpnext_integration.api.sync_frameworks.sync_frameworks_from_api

# Sync briefs/tenders
bench --site [your-site-name] execute dm_erpnext_integration.dm_erpnext_integration.api.sync_briefs.sync_briefs_from_api

# Sync suppliers
bench --site [your-site-name] execute dm_erpnext_integration.dm_erpnext_integration.api.sync_suppliers.sync_suppliers_from_api
```

## Usage

### Viewing Tenders

1. Navigate to: **Home > Digital Marketplace > DM Brief**
2. View all synchronized tenders with filters for:
   - Status (live, closed, withdrawn, etc.)
   - Framework (G-Cloud, DOS, etc.)
   - Published date

### Tender Details

Each brief/tender includes:
- **Basic Information**: Title, organization, location, status
- **Timeline**: Created, published, and closing dates
- **Requirements**: Summary, essential and nice-to-have requirements
- **Budget & Contract**: Budget range, contract length, work arrangement
- **Evaluation**: Technical competence and cultural fit criteria
- **Raw Data**: Complete JSON response from the API for reference

### Working with Frameworks and Lots

- **DM Framework**: View all available frameworks (G-Cloud 13, DOS 5, etc.)
- **DM Lot**: Browse service categories and understand which allow briefs

### Supplier Information

- **DM Supplier**: Access supplier details including contact information and company registration details

## Architecture

### DocTypes

The app creates the following DocTypes in ERPNext:

1. **DM API Settings** (Single): Configuration for API connection
2. **DM Framework**: Digital Marketplace frameworks
3. **DM Lot**: Service lots/categories
4. **DM Brief**: Tenders/procurement opportunities
5. **DM Supplier**: Registered suppliers
6. **DM Service**: Published services

### API Client

The `dm_client.py` module provides a Python client for the Digital Marketplace API with methods for:
- Fetching frameworks, briefs, suppliers, and services
- Pagination support
- Error handling and logging

### Sync Jobs

Scheduled tasks run automatically:
- **Hourly**: Sync briefs/tenders (configurable)
- **Daily**: Sync frameworks, lots, and suppliers

## Development

### Running Tests

```bash
bench --site [your-site-name] run-tests --app dm_erpnext_integration
```

### Project Structure

```
dm_erpnext_integration/
├── dm_erpnext_integration/
│   ├── doctype/           # DocType definitions
│   │   ├── dm_api_settings/
│   │   ├── dm_framework/
│   │   ├── dm_lot/
│   │   ├── dm_brief/
│   │   ├── dm_supplier/
│   │   └── dm_service/
│   └── api/               # API integration modules
│       ├── dm_client.py         # API client
│       ├── sync_frameworks.py   # Framework sync
│       ├── sync_briefs.py       # Brief sync
│       └── sync_suppliers.py    # Supplier sync
├── hooks.py               # Frappe hooks
├── pyproject.toml        # Python project config
└── README.md             # This file
```

## API Reference

### Digital Marketplace API Endpoints Used

- `GET /frameworks` - List all frameworks
- `GET /frameworks/{slug}` - Get framework details
- `GET /briefs` - List briefs with filters
- `GET /briefs/{id}` - Get brief details
- `GET /suppliers` - List suppliers
- `GET /suppliers/{id}` - Get supplier details
- `GET /services` - List services
- `GET /services/{id}` - Get service details

## Troubleshooting

### Sync Not Running

1. Check that the app is enabled in DM API Settings
2. Verify auth token is correct
3. Check scheduler is enabled: `bench --site [your-site-name] enable-scheduler`
4. Review error logs: **Home > System > Error Log**

### Missing Data

1. Run manual sync commands (see Configuration section)
2. Check API connectivity and authentication
3. Review sync status in DM API Settings

### API Connection Issues

1. Verify the API URL is correct
2. Check firewall/network settings
3. Ensure the API token has necessary permissions

## Contributing

This is an open-source project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues related to:
- **This app**: Open an issue on GitHub
- **Digital Marketplace API**: Contact the Crown Commercial Service
- **ERPNext/Frappe**: Visit the Frappe Forum

## About the Digital Marketplace

The Digital Marketplace is the UK government's platform for buying and selling digital services. Learn more at: https://www.digitalmarketplace.service.gov.uk/

## Credits

Developed for integration with the Crown Commercial Service Digital Marketplace.

Based on the [digitalmarketplace-api](https://github.com/alphagov/digitalmarketplace-api) project.
