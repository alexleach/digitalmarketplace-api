# Digital Marketplace ERPNext Integration - Architecture

## System Overview

This diagram shows how the Frappe app integrates with ERPNext to automate tender management:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Digital Marketplace API                       │
│            https://digitalmarketplace.service.gov.uk/api        │
│                                                                  │
│  Endpoints:  /briefs  /frameworks  /lots  /suppliers  /services │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTPS + Bearer Token Auth
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              dm_erpnext_integration (Frappe App)                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              API Client (dm_client.py)                  │    │
│  │  - Authentication handling                              │    │
│  │  - Request/response processing                          │    │
│  │  - Pagination support                                   │    │
│  │  - Error handling & logging                             │    │
│  └──────────────┬─────────────────────────────────────────┘    │
│                 │                                                │
│                 ▼                                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           Sync Modules (Scheduled Jobs)                 │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  sync_briefs.py        → Hourly sync of tenders        │    │
│  │  sync_frameworks.py    → Daily sync of frameworks      │    │
│  │  sync_suppliers.py     → Daily sync of suppliers       │    │
│  └──────────────┬─────────────────────────────────────────┘    │
│                 │                                                │
│                 ▼                                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              DocTypes (Data Models)                     │    │
│  ├────────────────────────────────────────────────────────┤    │
│  │  DM API Settings  → Configuration                       │    │
│  │  DM Framework     → G-Cloud, DOS frameworks            │    │
│  │  DM Lot          → Service categories                   │    │
│  │  DM Brief        → Tenders/procurement opportunities    │    │
│  │  DM Supplier     → Supplier information                 │    │
│  │  DM Service      → Published services                   │    │
│  └──────────────┬─────────────────────────────────────────┘    │
│                 │                                                │
└─────────────────┼────────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Frappe/ERPNext Database                       │
│                   (PostgreSQL/MySQL/MariaDB)                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ERPNext Web UI                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Users can:                                                      │
│  ✓ View synchronized tenders                                    │
│  ✓ Filter by status, framework, date                            │
│  ✓ See full tender details                                      │
│  ✓ Export data for reporting                                    │
│  ✓ Link to projects/quotations                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Configuration Phase
```
Administrator → DM API Settings → Store API URL & Token
```

### 2. Initial Sync
```
Manual Command → sync_frameworks → Fetch & Store Frameworks/Lots
Manual Command → sync_briefs → Fetch & Store Tenders
```

### 3. Automatic Sync (Scheduled)
```
Frappe Scheduler → Hourly → sync_briefs → Update Tenders
Frappe Scheduler → Daily → sync_frameworks → Update Frameworks
Frappe Scheduler → Daily → sync_suppliers → Update Suppliers
```

### 4. Data Access
```
Purchase User → ERPNext UI → Query DocTypes → View Tenders
```

## Component Details

### API Client Layer
**File**: `dm_client.py`

Responsibilities:
- HTTP request handling
- Authentication with Bearer tokens
- Response parsing
- Error handling and retry logic
- Pagination management

Key Methods:
- `get_briefs()` - Fetch tenders
- `get_frameworks()` - Fetch frameworks
- `get_suppliers()` - Fetch suppliers
- `get_services()` - Fetch services

### Sync Layer
**Files**: `sync_briefs.py`, `sync_frameworks.py`, `sync_suppliers.py`

Responsibilities:
- Data transformation (API → DocType)
- Deduplication (update existing records)
- Batch processing with pagination
- Error recovery and logging
- Status reporting

Process Flow:
```
1. Check if sync is enabled
2. Fetch data from API (with pagination)
3. For each record:
   a. Check if exists (by ID/slug)
   b. Create or update DocType
   c. Handle relationships (links)
4. Update sync status
5. Commit to database
```

### Data Layer (DocTypes)

**DM Brief** (Main Entity)
- Stores complete tender information
- Links to Framework and Lot
- Includes requirements, budget, timeline
- Preserves raw JSON for reference

**DM Framework**
- G-Cloud versions
- Digital Outcomes and Specialists
- Status tracking (live, expired, etc.)

**DM Lot**
- SaaS, PaaS, IaaS
- Digital Specialists, Outcomes, User Research
- Service categorization

**DM Supplier**
- Company information
- Contact details
- Registration numbers

**DM Service**
- Published offerings
- Pricing information
- Service descriptions

**DM API Settings**
- API URL and token
- Sync configuration
- Status monitoring

## Security Considerations

1. **Authentication**: Bearer token stored encrypted in database
2. **Access Control**: Role-based (Purchase User, System Manager)
3. **Audit Trail**: Frappe's built-in change tracking
4. **HTTPS**: All API communication encrypted
5. **Token Management**: Tokens stored as Password field type

## Scalability

### Current Limits
- Handles pagination automatically
- No hard limit on number of briefs
- Designed for UK Digital Marketplace scale (~1000s of briefs)

### Performance
- Sync time: ~1-2 minutes for full brief sync
- Database: Standard Frappe performance (MySQL/PostgreSQL)
- No special hardware requirements

### Optimization Options
- Filter syncs by framework
- Adjust sync frequency
- Implement incremental updates (track last_modified)
- Add caching layer

## Error Handling

### Levels of Error Handling

1. **API Level** (dm_client.py)
   - Connection errors
   - Timeout handling
   - Invalid responses
   - Rate limiting

2. **Sync Level** (sync_*.py)
   - Individual record failures
   - Partial batch completion
   - Status reporting

3. **System Level** (Frappe)
   - Error Log integration
   - Email notifications (configurable)
   - Scheduler monitoring

### Error Recovery
- Failed records logged but don't stop sync
- Next sync attempt retries
- Manual re-sync available
- Detailed error messages in Error Log

## Extension Points

### Custom Fields
Add organization-specific fields to DocTypes:
```python
# In hooks.py
custom_fields = {
    "DM Brief": [
        {
            "fieldname": "internal_reference",
            "label": "Internal Ref",
            "fieldtype": "Data"
        }
    ]
}
```

### Custom Reports
Create reports using Frappe Report Builder:
- Tenders by budget range
- Tenders closing this week
- Framework comparison
- Supplier analysis

### Workflow Integration
Link briefs to:
- Projects (track bid progress)
- Quotations (prepare proposals)
- Tasks (assign team members)
- Custom workflows

### Webhooks
Trigger actions on new briefs:
- Send notifications
- Create tasks
- Update external systems
- Generate reports

## Deployment

### Development
```bash
bench get-app /path/to/dm_erpnext_integration
bench --site dev.localhost install-app dm_erpnext_integration
```

### Production
```bash
bench get-app https://github.com/alexleach/digitalmarketplace-api.git
bench --site production.site install-app dm_erpnext_integration
bench --site production.site migrate
bench restart
```

### Docker
```dockerfile
# Add to your ERPNext Dockerfile
RUN bench get-app dm_erpnext_integration
RUN bench --site all install-app dm_erpnext_integration
```

## Monitoring

### Health Checks
- Check "Last Sync Time" in DM API Settings
- Review Error Log for failures
- Monitor scheduler status

### Metrics to Track
- Number of briefs synced per run
- Sync duration
- Error rate
- API response times

### Alerts
Configure email alerts for:
- Sync failures
- API connection issues
- Data inconsistencies

## Future Enhancements

Potential additions:
1. **Real-time sync** via webhooks (if DM API supports)
2. **Smart filtering** - only sync relevant briefs
3. **AI/ML features** - match briefs to services
4. **Bidding workflow** - integrated proposal generation
5. **Analytics dashboard** - tender trends and insights
6. **Mobile app** - tender notifications on the go

## Resources

- **Frappe Documentation**: https://frappeframework.com/docs
- **ERPNext Documentation**: https://docs.erpnext.com
- **Digital Marketplace**: https://digitalmarketplace.service.gov.uk
- **API Source**: https://github.com/alphagov/digitalmarketplace-api
