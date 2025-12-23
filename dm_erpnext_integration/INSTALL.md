# Digital Marketplace ERPNext Integration - Installation Guide

## Quick Start

### 1. Prerequisites

- Frappe Bench installed
- ERPNext (optional, but recommended)
- Python 3.9+

### 2. Installation Steps

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app (from this repository)
bench get-app /path/to/digitalmarketplace-api/dm_erpnext_integration

# Or if installing from GitHub (once pushed):
# bench get-app https://github.com/alexleach/digitalmarketplace-api.git --branch copilot/create-frappe-app-for-tenders

# Install the app on your site
bench --site your-site-name install-app dm_erpnext_integration

# Run migrations
bench --site your-site-name migrate

# Clear cache and build
bench --site your-site-name clear-cache
bench build
```

### 3. Configuration

1. Login to your ERPNext instance
2. Go to: **Home > Digital Marketplace > DM API Settings**
3. Configure:
   - API URL: `https://www.digitalmarketplace.service.gov.uk/api`
   - Auth Token: Your Digital Marketplace API token
   - Enable the integration
   - Set sync frequency

### 4. Initial Data Sync

Run the following commands to populate initial data:

```bash
# Sync frameworks and lots
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_frameworks.sync_frameworks_from_api

# Sync briefs/tenders
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_briefs.sync_briefs_from_api

# Sync suppliers (optional, can take time)
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_suppliers.sync_suppliers_from_api
```

### 5. Verify Installation

1. Navigate to **Home > Digital Marketplace > Briefs/Tenders**
2. You should see synchronized tenders from the Digital Marketplace

### 6. Enable Scheduler (if not already enabled)

```bash
bench --site your-site-name enable-scheduler
```

## Troubleshooting

### Issue: "App not found"
- Make sure you're in the correct bench directory
- Verify the app is in the `apps` folder

### Issue: "No module named 'dm_erpnext_integration'"
- Run: `bench build`
- Restart bench: `bench restart`

### Issue: "API connection error"
- Verify API URL and token in DM API Settings
- Check network connectivity
- Ensure firewall allows outbound HTTPS connections

### Issue: "Scheduler not running"
- Enable scheduler: `bench --site your-site-name enable-scheduler`
- Check scheduler status: `bench --site your-site-name doctor`

## Uninstallation

```bash
bench --site your-site-name uninstall-app dm_erpnext_integration
```

## Development Mode

For development, you can link the app:

```bash
# From the bench directory
bench get-app /path/to/dm_erpnext_integration --skip-assets
bench --site development.localhost install-app dm_erpnext_integration
```

## Next Steps

- Review the main README.md for usage instructions
- Configure sync frequency in DM API Settings
- Set up user permissions for Purchase User role
- Integrate with your procurement workflow
