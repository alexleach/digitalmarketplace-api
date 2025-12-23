# -*- coding: utf-8 -*-
# Copyright (c) 2023, CCS Digital Marketplace and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from dm_erpnext_integration.dm_erpnext_integration.api.dm_client import get_dm_client


def sync_suppliers_from_api():
    """
    Sync suppliers from Digital Marketplace API to ERPNext
    This is called by the scheduler
    """
    # Check if sync is enabled
    settings = frappe.get_single("DM API Settings")
    if not settings.enabled:
        frappe.log_error("Digital Marketplace sync is disabled", "DM Sync")
        return
    
    try:
        client = get_dm_client()
        
        page = 1
        synced_count = 0
        error_count = 0
        
        while True:
            response = client.get_suppliers(page=page)
            
            if not response or "suppliers" not in response:
                break
            
            suppliers = response.get("suppliers", [])
            if not suppliers:
                break
            
            for supplier_data in suppliers:
                try:
                    sync_supplier(supplier_data)
                    synced_count += 1
                except Exception as e:
                    error_count += 1
                    frappe.log_error(
                        message=f"Error syncing supplier {supplier_data.get('id', 'unknown')}: {str(e)}",
                        title="DM Supplier Sync Error"
                    )
            
            # Check if there are more pages
            links = response.get("links", {})
            if not links.get("next"):
                break
            
            page += 1
        
        # Update sync status
        settings.last_sync_time = frappe.utils.now()
        settings.last_sync_status = f"Suppliers: {synced_count} synced, {error_count} errors"
        settings.save(ignore_permissions=True)
        
        frappe.db.commit()
        
        frappe.logger().info(f"Synced {synced_count} suppliers, {error_count} errors")
        
    except Exception as e:
        frappe.log_error(
            message=f"Error in sync_suppliers_from_api: {str(e)}",
            title="DM Supplier Sync Error"
        )


def sync_supplier(supplier_data: dict):
    """
    Sync a single supplier
    
    Args:
        supplier_data: Supplier data from API
    """
    supplier_id = str(supplier_data.get("id"))
    if not supplier_id:
        return
    
    # Check if supplier already exists
    if frappe.db.exists("DM Supplier", supplier_id):
        doc = frappe.get_doc("DM Supplier", supplier_id)
    else:
        doc = frappe.new_doc("DM Supplier")
        doc.supplier_id = supplier_id
    
    # Update fields
    doc.supplier_name = supplier_data.get("name")
    doc.description = supplier_data.get("description")
    doc.duns_number = supplier_data.get("dunsNumber")
    doc.companies_house_number = supplier_data.get("companiesHouseNumber") or supplier_data.get("companiesHouseId")
    
    # Contact information
    contact_info = supplier_data.get("contactInformation", {})
    if contact_info:
        doc.contact_email = contact_info.get("email")
        doc.contact_phone = contact_info.get("phoneNumber") or contact_info.get("phone")
        doc.contact_website = contact_info.get("website")
        
        # Build address string
        address_parts = []
        if contact_info.get("address1"):
            address_parts.append(contact_info.get("address1"))
        if contact_info.get("address2"):
            address_parts.append(contact_info.get("address2"))
        if contact_info.get("city"):
            address_parts.append(contact_info.get("city"))
        if contact_info.get("postcode"):
            address_parts.append(contact_info.get("postcode"))
        if contact_info.get("country"):
            address_parts.append(contact_info.get("country"))
        
        if address_parts:
            doc.contact_address = ", ".join(address_parts)
    
    doc.save(ignore_permissions=True)
