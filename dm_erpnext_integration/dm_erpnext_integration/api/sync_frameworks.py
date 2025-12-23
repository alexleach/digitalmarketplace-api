# -*- coding: utf-8 -*-
# Copyright (c) 2023, CCS Digital Marketplace and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from dm_erpnext_integration.dm_erpnext_integration.api.dm_client import get_dm_client


def sync_frameworks_from_api():
    """
    Sync frameworks from Digital Marketplace API to ERPNext
    This is called by the scheduler
    """
    # Check if sync is enabled
    settings = frappe.get_single("DM API Settings")
    if not settings.enabled:
        frappe.log_error("Digital Marketplace sync is disabled", "DM Sync")
        return
    
    try:
        client = get_dm_client()
        frameworks = client.get_frameworks()
        
        if not frameworks:
            frappe.log_error("No frameworks returned from API", "DM Framework Sync")
            return
        
        synced_count = 0
        error_count = 0
        
        for framework_data in frameworks:
            try:
                sync_framework(framework_data)
                synced_count += 1
            except Exception as e:
                error_count += 1
                frappe.log_error(
                    message=f"Error syncing framework {framework_data.get('slug', 'unknown')}: {str(e)}",
                    title="DM Framework Sync Error"
                )
        
        # Update sync status
        settings.last_sync_time = frappe.utils.now()
        settings.last_sync_status = f"Frameworks: {synced_count} synced, {error_count} errors"
        settings.save(ignore_permissions=True)
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(
            message=f"Error in sync_frameworks_from_api: {str(e)}",
            title="DM Framework Sync Error"
        )


def sync_framework(framework_data: dict):
    """
    Sync a single framework
    
    Args:
        framework_data: Framework data from API
    """
    slug = framework_data.get("slug")
    if not slug:
        return
    
    # Check if framework already exists
    if frappe.db.exists("DM Framework", slug):
        doc = frappe.get_doc("DM Framework", slug)
    else:
        doc = frappe.new_doc("DM Framework")
        doc.slug = slug
    
    # Update fields
    doc.name1 = framework_data.get("name")
    doc.framework_family = framework_data.get("family") or framework_data.get("framework")
    doc.status = framework_data.get("status")
    doc.framework_id = framework_data.get("id")
    doc.has_direct_award = framework_data.get("hasDirectAward", False)
    doc.has_further_competition = framework_data.get("hasFurtherCompetition", False)
    doc.framework_agreement_version = framework_data.get("frameworkAgreementVersion")
    doc.clarification_questions_open = framework_data.get("clarificationQuestionsOpen", False)
    doc.allow_declaration_reuse = framework_data.get("allowDeclarationReuse", False)
    
    # Store variations as JSON string if present
    if "variations" in framework_data:
        doc.variations = json.dumps(framework_data.get("variations"))
    
    doc.save(ignore_permissions=True)
    
    # Sync lots for this framework
    lots = framework_data.get("lots", [])
    for lot_data in lots:
        sync_lot(lot_data)


def sync_lot(lot_data: dict):
    """
    Sync a single lot
    
    Args:
        lot_data: Lot data from API
    """
    slug = lot_data.get("slug")
    if not slug:
        return
    
    # Check if lot already exists
    if frappe.db.exists("DM Lot", slug):
        doc = frappe.get_doc("DM Lot", slug)
    else:
        doc = frappe.new_doc("DM Lot")
        doc.slug = slug
    
    # Update fields
    doc.lot_name = lot_data.get("name")
    doc.lot_id = lot_data.get("id")
    doc.one_service_limit = lot_data.get("oneServiceLimit", False)
    doc.allows_brief = lot_data.get("allowsBrief", False)
    
    doc.save(ignore_permissions=True)
