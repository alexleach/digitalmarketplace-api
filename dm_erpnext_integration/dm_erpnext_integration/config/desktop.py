# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _


def get_data():
	return [
		{
			"label": _("Digital Marketplace"),
			"icon": "fa fa-shopping-cart",
			"items": [
				{
					"type": "doctype",
					"name": "DM Brief",
					"label": _("Briefs/Tenders"),
					"description": _("Digital Marketplace procurement opportunities")
				},
				{
					"type": "doctype",
					"name": "DM Framework",
					"label": _("Frameworks"),
					"description": _("G-Cloud, DOS and other frameworks")
				},
				{
					"type": "doctype",
					"name": "DM Lot",
					"label": _("Lots"),
					"description": _("Service categories and lots")
				},
				{
					"type": "doctype",
					"name": "DM Supplier",
					"label": _("Suppliers"),
					"description": _("Digital Marketplace suppliers")
				},
				{
					"type": "doctype",
					"name": "DM Service",
					"label": _("Services"),
					"description": _("Published services")
				}
			]
		},
		{
			"label": _("Settings"),
			"icon": "fa fa-cog",
			"items": [
				{
					"type": "doctype",
					"name": "DM API Settings",
					"label": _("API Settings"),
					"description": _("Configure Digital Marketplace API connection")
				}
			]
		}
	]
