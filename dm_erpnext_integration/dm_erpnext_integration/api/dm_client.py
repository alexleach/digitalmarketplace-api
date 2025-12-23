# -*- coding: utf-8 -*-
# Copyright (c) 2023, CCS Digital Marketplace and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import requests
import json
from typing import Optional, Dict, List


class DigitalMarketplaceClient:
    """Client to interact with the Digital Marketplace API"""
    
    def __init__(self, api_url: str = None, auth_token: str = None):
        """
        Initialize the Digital Marketplace API client
        
        Args:
            api_url: Base URL for the Digital Marketplace API
            auth_token: Bearer token for authentication
        """
        if not api_url or not auth_token:
            settings = frappe.get_single("DM API Settings")
            self.api_url = api_url or settings.api_url
            self.auth_token = auth_token or settings.get_password("auth_token")
        else:
            self.api_url = api_url
            self.auth_token = auth_token
        
        self.headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, method: str = "GET", params: Dict = None) -> Optional[Dict]:
        """
        Make a request to the Digital Marketplace API
        
        Args:
            endpoint: API endpoint (e.g., '/briefs', '/frameworks')
            method: HTTP method (GET, POST, etc.)
            params: Query parameters
            
        Returns:
            Response data as dictionary or None on error
        """
        url = f"{self.api_url.rstrip('/')}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            frappe.log_error(
                message=f"Error making request to {url}: {str(e)}",
                title="Digital Marketplace API Error"
            )
            return None
    
    def get_frameworks(self) -> Optional[List[Dict]]:
        """
        Get all frameworks from the Digital Marketplace API
        
        Returns:
            List of framework dictionaries
        """
        response = self._make_request("/frameworks")
        if response and "frameworks" in response:
            return response["frameworks"]
        return []
    
    def get_framework(self, framework_slug: str) -> Optional[Dict]:
        """
        Get a specific framework by slug
        
        Args:
            framework_slug: Framework slug (e.g., 'g-cloud-13')
            
        Returns:
            Framework dictionary or None
        """
        response = self._make_request(f"/frameworks/{framework_slug}")
        if response and "frameworks" in response:
            return response["frameworks"]
        return None
    
    def get_briefs(self, status: str = None, framework: str = None, page: int = 1) -> Optional[Dict]:
        """
        Get briefs (tenders) from the Digital Marketplace API
        
        Args:
            status: Filter by status (e.g., 'live', 'closed', 'draft')
            framework: Filter by framework slug
            page: Page number for pagination
            
        Returns:
            Dictionary containing briefs and pagination info
        """
        params = {"page": page}
        if status:
            params["status"] = status
        if framework:
            params["framework"] = framework
        
        response = self._make_request("/briefs", params=params)
        return response
    
    def get_brief(self, brief_id: int) -> Optional[Dict]:
        """
        Get a specific brief by ID
        
        Args:
            brief_id: Brief ID
            
        Returns:
            Brief dictionary or None
        """
        response = self._make_request(f"/briefs/{brief_id}")
        if response and "briefs" in response:
            return response["briefs"]
        return None
    
    def get_suppliers(self, framework: str = None, page: int = 1) -> Optional[Dict]:
        """
        Get suppliers from the Digital Marketplace API
        
        Args:
            framework: Filter by framework slug
            page: Page number for pagination
            
        Returns:
            Dictionary containing suppliers and pagination info
        """
        params = {"page": page}
        if framework:
            params["framework"] = framework
        
        response = self._make_request("/suppliers", params=params)
        return response
    
    def get_supplier(self, supplier_id: int) -> Optional[Dict]:
        """
        Get a specific supplier by ID
        
        Args:
            supplier_id: Supplier ID
            
        Returns:
            Supplier dictionary or None
        """
        response = self._make_request(f"/suppliers/{supplier_id}")
        if response and "suppliers" in response:
            return response["suppliers"]
        return None
    
    def get_services(self, framework: str = None, status: str = "published", page: int = 1) -> Optional[Dict]:
        """
        Get services from the Digital Marketplace API
        
        Args:
            framework: Filter by framework slug
            status: Filter by status (default: 'published')
            page: Page number for pagination
            
        Returns:
            Dictionary containing services and pagination info
        """
        params = {"page": page, "status": status}
        if framework:
            params["framework"] = framework
        
        response = self._make_request("/services", params=params)
        return response
    
    def get_service(self, service_id: str) -> Optional[Dict]:
        """
        Get a specific service by ID
        
        Args:
            service_id: Service ID
            
        Returns:
            Service dictionary or None
        """
        response = self._make_request(f"/services/{service_id}")
        if response and "services" in response:
            return response["services"]
        return None


def get_dm_client() -> DigitalMarketplaceClient:
    """
    Get an instance of the Digital Marketplace client
    
    Returns:
        DigitalMarketplaceClient instance
    """
    return DigitalMarketplaceClient()
