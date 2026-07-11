"""Canonical OpenAlex node module.

The connector keeps one implementation module per published entity so the
flattening code remains readable. `subsets_utils.load_nodes()` discovers those
modules directly; this file exists for the factory scaffold's canonical path
check.
"""
