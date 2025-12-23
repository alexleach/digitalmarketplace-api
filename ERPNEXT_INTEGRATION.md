# ERPNext Integration Available! 🎉

## New Frappe App for Automated Tender Management

This repository now includes a **complete Frappe application** that integrates the Digital Marketplace API with ERPNext, enabling automated synchronization of government procurement tenders.

### 📍 Location

The Frappe app is located in: **[`/dm_erpnext_integration/`](dm_erpnext_integration/)**

### 🚀 What It Does

Automatically syncs Digital Marketplace tenders (briefs) into your ERPNext system:
- ✅ Live procurement opportunities
- ✅ Framework and lot information
- ✅ Supplier details
- ✅ Complete tender requirements and budgets

### ⚡ Quick Start

```bash
# Install the app
bench get-app /path/to/digitalmarketplace-api/dm_erpnext_integration
bench --site yoursite install-app dm_erpnext_integration

# Configure and sync
# See documentation for details
```

### 📚 Documentation

Start here: **[dm_erpnext_integration/INDEX.md](dm_erpnext_integration/INDEX.md)**

Quick links:
- **[QUICKSTART.md](dm_erpnext_integration/QUICKSTART.md)** - 5-minute setup
- **[README.md](dm_erpnext_integration/README.md)** - Full documentation
- **[USER_GUIDE.md](dm_erpnext_integration/USER_GUIDE.md)** - Daily usage

### 💡 Features

- 🔄 Automated hourly sync of tenders
- 📊 Complete data models for all entities
- 👥 Role-based access control
- 📤 Export and reporting capabilities
- 🔗 Integration with ERPNext workflows
- 📱 Mobile-responsive UI

### 🎯 Perfect For

- Government contractors tracking opportunities
- Procurement teams managing bids
- Organizations automating tender discovery
- Anyone using ERPNext for procurement

### 📝 What's Included

- 6 DocTypes (data models)
- API client with authentication
- 3 scheduled sync jobs
- 50+ files of code and tests
- 56KB of comprehensive documentation

### 🏗️ Repository Structure

```
digitalmarketplace-api/
├── app/                      # Original Flask API (unchanged)
├── migrations/              # Database migrations (unchanged)
├── tests/                   # API tests (unchanged)
└── dm_erpnext_integration/  # 🆕 NEW Frappe App!
    ├── INDEX.md             # Start here
    ├── QUICKSTART.md        # 5-minute guide
    ├── README.md            # Full docs
    └── dm_erpnext_integration/
        ├── api/             # API integration
        ├── doctype/         # Data models
        └── tests/           # Tests
```

### 🔗 Learn More

- **Documentation Hub**: [dm_erpnext_integration/INDEX.md](dm_erpnext_integration/INDEX.md)
- **Digital Marketplace**: https://digitalmarketplace.service.gov.uk
- **Frappe Framework**: https://frappeframework.com

---

**Ready to automate your tender management? Check out [`/dm_erpnext_integration/`](dm_erpnext_integration/)!** 🚀
