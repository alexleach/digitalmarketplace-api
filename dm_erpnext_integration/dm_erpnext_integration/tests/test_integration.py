# -*- coding: utf-8 -*-
# Copyright (c) 2023, CCS Digital Marketplace and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


class TestDMIntegration(unittest.TestCase):
	"""Base test class for DM ERPNext Integration"""
	
	def setUp(self):
		"""Set up test fixtures"""
		frappe.set_user("Administrator")
	
	def tearDown(self):
		"""Clean up after tests"""
		frappe.set_user("Administrator")


if __name__ == '__main__':
	unittest.main()
