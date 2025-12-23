# -*- coding: utf-8 -*-
# Copyright (c) 2023, CCS Digital Marketplace and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from unittest.mock import Mock, patch
from dm_erpnext_integration.dm_erpnext_integration.api.dm_client import DigitalMarketplaceClient


class TestDMClient(unittest.TestCase):
	"""Test cases for Digital Marketplace API client"""
	
	def setUp(self):
		"""Set up test fixtures"""
		self.api_url = "https://api.example.com"
		self.auth_token = "test_token_123"
		self.client = DigitalMarketplaceClient(
			api_url=self.api_url,
			auth_token=self.auth_token
		)
	
	def test_client_initialization(self):
		"""Test that client initializes with correct values"""
		self.assertEqual(self.client.api_url, self.api_url)
		self.assertEqual(self.client.auth_token, self.auth_token)
		self.assertIn("Authorization", self.client.headers)
		self.assertEqual(
			self.client.headers["Authorization"],
			f"Bearer {self.auth_token}"
		)
	
	@patch('requests.request')
	def test_get_frameworks(self, mock_request):
		"""Test getting frameworks from API"""
		# Mock response
		mock_response = Mock()
		mock_response.json.return_value = {
			"frameworks": [
				{"slug": "g-cloud-13", "name": "G-Cloud 13"},
				{"slug": "dos-5", "name": "Digital Outcomes and Specialists 5"}
			]
		}
		mock_response.raise_for_status = Mock()
		mock_request.return_value = mock_response
		
		# Call method
		frameworks = self.client.get_frameworks()
		
		# Assertions
		self.assertIsNotNone(frameworks)
		self.assertEqual(len(frameworks), 2)
		self.assertEqual(frameworks[0]["slug"], "g-cloud-13")
		
		# Verify request was made correctly
		mock_request.assert_called_once()
		call_args = mock_request.call_args
		self.assertEqual(call_args[1]["method"], "GET")
		self.assertIn("/frameworks", call_args[1]["url"])
	
	@patch('requests.request')
	def test_get_briefs(self, mock_request):
		"""Test getting briefs from API"""
		# Mock response
		mock_response = Mock()
		mock_response.json.return_value = {
			"briefs": [
				{"id": 1, "title": "Test Brief", "status": "live"}
			],
			"links": {}
		}
		mock_response.raise_for_status = Mock()
		mock_request.return_value = mock_response
		
		# Call method
		response = self.client.get_briefs(status="live", page=1)
		
		# Assertions
		self.assertIsNotNone(response)
		self.assertIn("briefs", response)
		self.assertEqual(len(response["briefs"]), 1)
		
		# Verify request parameters
		call_args = mock_request.call_args
		self.assertIn("params", call_args[1])
		self.assertEqual(call_args[1]["params"]["status"], "live")
		self.assertEqual(call_args[1]["params"]["page"], 1)


if __name__ == '__main__':
	unittest.main()
