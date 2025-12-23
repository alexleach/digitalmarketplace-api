# -*- coding: utf-8 -*-
# Copyright (c) 2023, CCS Digital Marketplace and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from dm_erpnext_integration.dm_erpnext_integration.api.dm_client import get_dm_client


def sync_briefs_from_api():
    """
    Sync briefs (tenders) from Digital Marketplace API to ERPNext
    This is called by the scheduler
    """
    # Check if sync is enabled
    settings = frappe.get_single("DM API Settings")
    if not settings.enabled:
        frappe.log_error("Digital Marketplace sync is disabled", "DM Sync")
        return
    
    try:
        client = get_dm_client()
        
        # Sync live briefs (active tenders)
        sync_briefs_by_status(client, "live")
        
        # Also sync closed briefs for completeness
        sync_briefs_by_status(client, "closed")
        
        # Update sync status
        settings.last_sync_time = frappe.utils.now()
        settings.last_sync_status = "Briefs synced successfully"
        settings.save(ignore_permissions=True)
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(
            message=f"Error in sync_briefs_from_api: {str(e)}",
            title="DM Brief Sync Error"
        )


def sync_briefs_by_status(client, status: str):
    """
    Sync briefs for a specific status with pagination
    
    Args:
        client: DigitalMarketplaceClient instance
        status: Brief status to sync
    """
    page = 1
    synced_count = 0
    error_count = 0
    
    while True:
        response = client.get_briefs(status=status, page=page)
        
        if not response or "briefs" not in response:
            break
        
        briefs = response.get("briefs", [])
        if not briefs:
            break
        
        for brief_data in briefs:
            try:
                sync_brief(brief_data)
                synced_count += 1
            except Exception as e:
                error_count += 1
                frappe.log_error(
                    message=f"Error syncing brief {brief_data.get('id', 'unknown')}: {str(e)}",
                    title="DM Brief Sync Error"
                )
        
        # Check if there are more pages
        links = response.get("links", {})
        if not links.get("next"):
            break
        
        page += 1
    
    frappe.logger().info(f"Synced {synced_count} briefs with status '{status}', {error_count} errors")


def sync_brief(brief_data: dict):
    """
    Sync a single brief
    
    Args:
        brief_data: Brief data from API
    """
    brief_id = str(brief_data.get("id"))
    if not brief_id:
        return
    
    # Check if brief already exists
    if frappe.db.exists("DM Brief", brief_id):
        doc = frappe.get_doc("DM Brief", brief_id)
    else:
        doc = frappe.new_doc("DM Brief")
        doc.brief_id = brief_id
    
    # Update basic fields
    doc.title = brief_data.get("title")
    doc.status = brief_data.get("status")
    doc.organisation = brief_data.get("organisation")
    doc.location = brief_data.get("location")
    doc.is_a_copy = brief_data.get("isACopy", False)
    
    # Link to framework and lot
    framework_slug = brief_data.get("frameworkSlug")
    if framework_slug and frappe.db.exists("DM Framework", framework_slug):
        doc.framework = framework_slug
    
    lot_slug = brief_data.get("lotSlug") or brief_data.get("lot")
    if lot_slug and frappe.db.exists("DM Lot", lot_slug):
        doc.lot = lot_slug
    
    # Update dates
    doc.created_at = brief_data.get("createdAt")
    doc.updated_at = brief_data.get("updatedAt")
    doc.published_at = brief_data.get("publishedAt")
    doc.applications_closed_at = brief_data.get("applicationsClosedAt")
    doc.clarification_questions_closed_at = brief_data.get("clarificationQuestionsClosedAt")
    doc.withdrawn_at = brief_data.get("withdrawnAt")
    
    # Update requirements
    doc.summary_of_requirements = brief_data.get("summaryOfRequirements") or brief_data.get("summary")
    doc.organisation_requirements = brief_data.get("organisationRequirements") or brief_data.get("organisation")
    
    # Handle essential requirements (could be list or string)
    essential_reqs = brief_data.get("essentialRequirements")
    if essential_reqs:
        if isinstance(essential_reqs, list):
            doc.essential_requirements = "\n".join([f"- {req}" for req in essential_reqs])
        else:
            doc.essential_requirements = essential_reqs
    
    # Handle nice to have requirements
    nice_to_have = brief_data.get("niceToHaveRequirements")
    if nice_to_have:
        if isinstance(nice_to_have, list):
            doc.nice_to_have_requirements = "\n".join([f"- {req}" for req in nice_to_have])
        else:
            doc.nice_to_have_requirements = nice_to_have
    
    # Budget and contract details
    doc.budget_range = brief_data.get("budgetRange")
    doc.work_place = brief_data.get("workplaceAddress") or brief_data.get("workPlace")
    doc.work_arrangement = brief_data.get("workingArrangements") or brief_data.get("workArrangement")
    doc.contract_length = brief_data.get("contractLength")
    doc.security_clearance_required = brief_data.get("securityClearanceRequired")
    
    # Evaluation criteria
    technical_criteria = brief_data.get("technicalCompetenceCriteria") or brief_data.get("technicalCompetence")
    if technical_criteria:
        if isinstance(technical_criteria, list):
            doc.technical_competence_criteria = "\n".join([f"- {crit}" for crit in technical_criteria])
        else:
            doc.technical_competence_criteria = technical_criteria
    
    cultural_criteria = brief_data.get("culturalFitCriteria") or brief_data.get("culturalFit")
    if cultural_criteria:
        if isinstance(cultural_criteria, list):
            doc.cultural_fit_criteria = "\n".join([f"- {crit}" for crit in cultural_criteria])
        else:
            doc.cultural_fit_criteria = cultural_criteria
    
    doc.evaluation_type = brief_data.get("evaluationType")
    
    # Store raw JSON data for reference
    doc.raw_data = json.dumps(brief_data, indent=2)
    
    doc.save(ignore_permissions=True)
