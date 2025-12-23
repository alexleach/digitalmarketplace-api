# Quick Start Guide - Digital Marketplace ERPNext Integration

Get up and running in 5 minutes!

## Prerequisites

✅ Frappe Bench installed  
✅ ERPNext site running  
✅ Digital Marketplace API access token  

## Step 1: Install the App (2 minutes)

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app from the repository
bench get-app /path/to/digitalmarketplace-api/dm_erpnext_integration

# Install on your site
bench --site your-site-name install-app dm_erpnext_integration

# Migrate database
bench --site your-site-name migrate
```

## Step 2: Configure API (1 minute)

1. Login to ERPNext
2. Go to: **Search Bar → Type "DM API"**
3. Click **DM API Settings**
4. Fill in:
   - **API URL**: `https://www.digitalmarketplace.service.gov.uk/api`
   - **Auth Token**: Your API token (get from Digital Marketplace)
   - **Enabled**: ✓ Check this box
   - **Sync Frequency**: Choose "Hourly"
5. Click **Save**

## Step 3: Initial Sync (2 minutes)

```bash
# Sync frameworks and lots (fast)
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_frameworks.sync_frameworks_from_api

# Sync tenders/briefs (may take 1-2 minutes)
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_briefs.sync_briefs_from_api
```

## Step 4: View Your Tenders! (30 seconds)

1. In ERPNext, click the **Awesome Bar** (search)
2. Type **"DM Brief"** or **"Briefs"**
3. Click **DM Brief** list
4. 🎉 See your synchronized tenders!

## What's Next?

### View Different Types of Data

- **Briefs/Tenders**: Active procurement opportunities
- **Frameworks**: G-Cloud, DOS, etc.
- **Lots**: Service categories
- **Suppliers**: Registered suppliers

### Filter and Search

Use filters to find:
- Live tenders (status = "live")
- Specific frameworks
- Tenders by date range
- By organization

### Enable Automatic Sync

If scheduler isn't running:
```bash
bench --site your-site-name enable-scheduler
```

Now briefs sync automatically every hour!

## Troubleshooting

### "No tenders showing up?"

1. Check API Settings are saved and enabled
2. Verify your API token is correct
3. Run sync command again
4. Check Error Log: **Home → System → Error Log**

### "Scheduler not running?"

```bash
bench --site your-site-name enable-scheduler
bench restart
```

### "Permission denied?"

Make sure you have **Purchase User** or **System Manager** role.

## Common Commands

```bash
# Re-sync everything
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_frameworks.sync_frameworks_from_api
bench --site your-site-name execute dm_erpnext_integration.dm_erpnext_integration.api.sync_briefs.sync_briefs_from_api

# Check sync status
# Go to DM API Settings → See "Last Sync Time" and "Last Sync Status"

# View logs
bench --site your-site-name console
# Then: frappe.get_list("Error Log", limit=5)

# Clear cache
bench --site your-site-name clear-cache
```

## Getting an API Token

### Option 1: Use Existing Digital Marketplace Account
Contact Digital Marketplace support to request API access.

### Option 2: Running Your Own API Instance
If you're running the digitalmarketplace-api locally:

```bash
export DM_API_AUTH_TOKENS=mySecretToken123
# Use "mySecretToken123" as your auth token in DM API Settings
```

## Success Checklist

- [ ] App installed and migrated
- [ ] API Settings configured with token
- [ ] Sync enabled
- [ ] Initial sync completed
- [ ] Can view briefs in ERPNext
- [ ] Scheduler enabled for automatic updates

## Need Help?

- 📖 See **README.md** for detailed documentation
- 📋 See **INSTALL.md** for troubleshooting
- 🐛 Report issues on GitHub
- 💬 Ask on Frappe Forum

---

**That's it! You're now automatically tracking Digital Marketplace tenders in ERPNext!** 🚀
