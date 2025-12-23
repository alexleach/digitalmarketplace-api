# Digital Marketplace ERPNext Integration - User Guide

## What You'll See in ERPNext

After installing this app, you'll have a new "Digital Marketplace" module in ERPNext with the following sections:

### 1. Briefs/Tenders (Main View)

This is where you'll spend most of your time. Each brief/tender shows:

**List View:**
```
┌─────────────────────────────────────────────────────────────┐
│ DM Brief List                                    [+ New]     │
├─────────────────────────────────────────────────────────────┤
│ Filters: Status: [Live ▼] Framework: [All ▼]               │
├──────┬──────────────────────────┬─────────┬────────────────┤
│ ID   │ Title                    │ Status  │ Published      │
├──────┼──────────────────────────┼─────────┼────────────────┤
│ 1234 │ Digital Developer Ne...  │ live    │ 2023-12-20     │
│ 1235 │ Cloud Infrastructure...  │ live    │ 2023-12-19     │
│ 1236 │ User Research Speci...   │ closed  │ 2023-12-15     │
│ 1237 │ Agile Delivery Mana...   │ live    │ 2023-12-18     │
└──────┴──────────────────────────┴─────────┴────────────────┘
```

**Detail View (when you click a brief):**
```
┌─────────────────────────────────────────────────────────────┐
│ DM Brief: 1234                                    [Edit]     │
├─────────────────────────────────────────────────────────────┤
│ Title: Digital Developer Needed                             │
│ Status: Live                                                │
│ Organisation: Department for Education                       │
│ Framework: digital-outcomes-and-specialists-5               │
│ Lot: digital-specialists                                    │
│                                                              │
│ ┌─ Dates ─────────────────────────────────────────────────┐│
│ │ Published: 2023-12-20 10:00                             ││
│ │ Applications Close: 2023-12-27 23:59                    ││
│ │ Clarifications Close: 2023-12-23 17:00                  ││
│ └─────────────────────────────────────────────────────────┘│
│                                                              │
│ ┌─ Requirements ──────────────────────────────────────────┐│
│ │ Summary:                                                 ││
│ │ We need an experienced Python developer to work on...   ││
│ │                                                          ││
│ │ Essential Requirements:                                  ││
│ │ - 5+ years Python experience                            ││
│ │ - Experience with Django                                ││
│ │ - UK Security Clearance SC                              ││
│ │                                                          ││
│ │ Nice to Have:                                            ││
│ │ - AWS experience                                         ││
│ │ - Docker/Kubernetes knowledge                            ││
│ └─────────────────────────────────────────────────────────┘│
│                                                              │
│ ┌─ Budget & Contract ─────────────────────────────────────┐│
│ │ Budget: £80,000 - £95,000                               ││
│ │ Contract Length: 6 months                               ││
│ │ Work Place: London or Remote                            ││
│ │ Security Clearance: SC                                  ││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### 2. Frameworks

View all available procurement frameworks:

```
┌─────────────────────────────────────────────────────────────┐
│ DM Framework List                                           │
├─────────────────────────────┬─────────┬─────────────────────┤
│ Name                        │ Status  │ Family              │
├─────────────────────────────┼─────────┼─────────────────────┤
│ G-Cloud 13                  │ live    │ g-cloud             │
│ Digital Outcomes & Sp... 5  │ live    │ digital-outcomes... │
│ G-Cloud 12                  │ expired │ g-cloud             │
└─────────────────────────────┴─────────┴─────────────────────┘
```

### 3. Lots (Service Categories)

Browse different service types:

```
┌─────────────────────────────────────────────────────────────┐
│ DM Lot List                                                 │
├─────────────────────────────────────────────────────────────┤
│ Cloud hosting (SaaS)                                        │
│ Cloud hosting (PaaS)                                        │
│ Cloud hosting (IaaS)                                        │
│ Digital specialists                                         │
│ Digital outcomes                                            │
│ User research studios                                       │
└─────────────────────────────────────────────────────────────┘
```

### 4. Suppliers

View registered suppliers:

```
┌─────────────────────────────────────────────────────────────┐
│ DM Supplier List                                            │
├─────┬──────────────────────────┬──────────────────────────┬─┤
│ ID  │ Name                     │ Contact Email            │ │
├─────┼──────────────────────────┼──────────────────────────┼─┤
│ 101 │ Digital Services Ltd     │ info@digitalservices.uk  │ │
│ 102 │ Cloud Solutions Inc      │ sales@cloudsolutions.com │ │
│ 103 │ Agile Consultancy        │ hello@agileconsult.uk    │ │
└─────┴──────────────────────────┴──────────────────────────┴─┘
```

### 5. API Settings (Admin Only)

Configuration page for administrators:

```
┌─────────────────────────────────────────────────────────────┐
│ DM API Settings                                   [Save]     │
├─────────────────────────────────────────────────────────────┤
│ API URL: [https://digitalmarketplace.service.gov.uk/api  ] │
│ Auth Token: [••••••••••••••••••••••••]                     │
│ Enabled: [✓]                                                │
│ Sync Frequency: [Hourly ▼]                                 │
│                                                              │
│ ─── Status ───────────────────────────────────────────────  │
│ Last Sync: 2023-12-23 14:30:00                             │
│ Last Status: Briefs: 45 synced, 0 errors                   │
└─────────────────────────────────────────────────────────────┘
```

## Common Workflows

### 1. Finding Active Tenders

**Steps:**
1. Click **Home** → Search "DM Brief"
2. Click **DM Brief** list
3. Filter: **Status = Live**
4. Sort by **Published Date** (newest first)
5. Click any brief to see details

### 2. Monitoring Deadlines

**Steps:**
1. Go to **DM Brief** list
2. Filter: **Status = Live**
3. Add column: **Applications Closed At**
4. Sort by closing date (soonest first)
5. See briefs closing soon

### 3. Finding Briefs by Type

**Steps:**
1. Go to **DM Brief** list
2. Filter by **Framework**: "digital-outcomes-and-specialists-5"
3. Filter by **Lot**: "digital-specialists"
4. See only Digital Specialist opportunities

### 4. Exporting Data

**Steps:**
1. Open **DM Brief** list
2. Apply any filters you want
3. Click menu (three dots)
4. Select **Export**
5. Choose format (Excel/CSV)
6. Download file

### 5. Setting Up Email Alerts

**Steps:**
1. Go to **Settings** → **Email Alerts**
2. Create new alert
3. Document Type: **DM Brief**
4. Condition: `doc.status == "live"`
5. Recipients: Your email
6. Save
7. Get notified of new tenders!

## Integration Examples

### Link Brief to Project

```
1. Open a DM Brief
2. Click "Create" → "Project"
3. Project auto-fills with brief title
4. Add team members
5. Track bid preparation
```

### Create Quotation from Brief

```
1. Open a DM Brief
2. Note requirements and budget
3. Create new Quotation
4. Reference brief ID in description
5. Build your proposal
```

### Track Multiple Briefs

```
1. Create custom DocType "Bid Tracker"
2. Link to DM Brief
3. Add fields: Bid Status, Team, Probability
4. Track all active bids in one place
```

## Tips & Tricks

### 💡 Quick Filters

Save common filters:
- "Live Tenders This Week"
- "High Budget Opportunities"
- "Remote Work Available"

### 📊 Custom Reports

Create reports for:
- Tenders by department
- Average budget by lot type
- Closing deadlines this month
- Framework comparison

### 🔔 Stay Updated

Set up alerts for:
- New tenders in your area
- Tenders closing soon
- Framework updates

### 📱 Mobile Access

Access from mobile:
- Use ERPNext mobile app
- View briefs on the go
- Get push notifications

### 🔍 Advanced Search

Use global search bar:
- Type "Python developer" to find relevant briefs
- Search by organization name
- Find briefs with specific budgets

## Dashboard Widgets

Add widgets to your dashboard:

1. **Active Tenders Count**: See total live briefs
2. **Closing This Week**: List urgent opportunities
3. **Recent Updates**: New or modified briefs
4. **By Framework Chart**: Pie chart of tender distribution

## Keyboard Shortcuts

- **Ctrl+K** or **Cmd+K**: Quick search
- **Ctrl+G**: Go to list
- **N**: New document
- **S**: Save
- **Ctrl+H**: Help

## Mobile View

The app works great on mobile:

```
┌─────────────────────┐
│ 📱 ERPNext         │
├─────────────────────┤
│ 🏠 Home            │
│ 📋 DM Brief        │
│   → Live (45)      │
│   → Closed (123)   │
│ 🏢 DM Framework    │
│ 📦 DM Lot          │
│ 👥 DM Supplier     │
└─────────────────────┘
```

Tap any brief to see full details, swipe to go back.

## Troubleshooting UI Issues

### "Can't see Digital Marketplace module"
- Check you have Purchase User or System Manager role
- Ask admin to assign role

### "No data showing"
- Wait for initial sync (can take 2-3 minutes)
- Check DM API Settings → Last Sync Status
- Run manual sync if needed

### "Slow loading"
- Add filters to reduce data
- Clear cache: Settings → Clear Cache
- Contact admin if persistent

## Next Steps

1. **Explore the data** - Browse different views
2. **Set up filters** - Save your common searches
3. **Create reports** - Analyze tender patterns
4. **Integrate workflows** - Link to projects/tasks
5. **Train your team** - Share this guide!

---

**Questions?** See README.md for more details or ask your system administrator.
