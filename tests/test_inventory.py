"""
Smart Inventory & Expiry Manager - Storage & Inventory Unit Tests
Course: Introduction to Algorithms | Instructor: Dr. Fatma Talaat | Team: Axiom
"""

import os
import tempfile
import unittest
from datetime import date, timedelta

import inventory
import storage


class TestStorageAndInventory(unittest.TestCase):
    def setUp(self):
        # Create an isolated temporary SQLite database for unit tests
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = os.path.join(self.temp_dir.name, "test_inventory.db")
        storage.init_db(self.db_path)

    def tearDown(self):
        try:
            self.temp_dir.cleanup()
        except Exception:
            pass

    def test_database_crud(self):
        # 1. Add product
        product = {
            "id": "SKU-TEST-1",
            "name": "Organic Honey",
            "category": "Condiments & Sauces",
            "quantity": 10,
            "min_threshold": 5,
            "expiration_date": "2026-12-31",
            "unit_price": 7.50,
            "supplier": "Bee Farms"
        }
        storage.add_product(self.db_path, product)

        # 2. Get product
        fetched = storage.get_product_by_id(self.db_path, "SKU-TEST-1")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["name"], "Organic Honey")
        self.assertEqual(fetched["quantity"], 10)
        self.assertEqual(fetched["unit_price"], 7.50)

        # 3. Duplicate ID rejection
        with self.assertRaises(ValueError):
            storage.add_product(self.db_path, product)

        # 4. Update product
        storage.update_product(self.db_path, "SKU-TEST-1", {
            "name": "Organic Wildflower Honey",
            "category": "Condiments & Sauces",
            "quantity": 3,  # Changed quantity to 3 (low stock)
            "min_threshold": 5,
            "expiration_date": "2026-12-31",
            "unit_price": 8.00,
            "supplier": "Bee Farms"
        })
        updated = storage.get_product_by_id(self.db_path, "SKU-TEST-1")
        self.assertEqual(updated["name"], "Organic Wildflower Honey")
        self.assertEqual(updated["quantity"], 3)
        self.assertEqual(updated["unit_price"], 8.00)

        # 5. Delete product
        deleted = storage.delete_product(self.db_path, "SKU-TEST-1")
        self.assertTrue(deleted)
        self.assertIsNone(storage.get_product_by_id(self.db_path, "SKU-TEST-1"))

    def test_demo_data_seeding(self):
        count = inventory.seed_or_reset_demo_data(self.db_path)
        self.assertGreaterEqual(count, 18)
        all_items = storage.get_all_products(self.db_path)
        self.assertEqual(len(all_items), count)

    def test_reorder_calculation(self):
        # Quantity = 4, threshold = 10, unit_price = 2.0
        # Target = 2 * 10 = 20. Suggested = 20 - 4 = 16 units. Cost = 16 * 2.0 = $32.00
        rec = inventory.calculate_reorder_recommendation(quantity=4, min_threshold=10, unit_price=2.0)
        self.assertTrue(rec["needs_reorder"])
        self.assertEqual(rec["suggested_units"], 16)
        self.assertEqual(rec["estimated_cost"], 32.0)

        # Quantity = 25, threshold = 10
        rec2 = inventory.calculate_reorder_recommendation(quantity=25, min_threshold=10, unit_price=2.0)
        self.assertFalse(rec2["needs_reorder"])
        self.assertEqual(rec2["suggested_units"], 0)
        self.assertEqual(rec2["estimated_cost"], 0.0)

    def test_expiry_classification(self):
        # Expired
        status, label = inventory.classify_expiry_status(-2)
        self.assertEqual(status, "EXPIRED")

        # Today
        status, label = inventory.classify_expiry_status(0)
        self.assertEqual(status, "EXPIRING_TODAY")

        # Expiring soon
        status, label = inventory.classify_expiry_status(5, warning_days=7)
        self.assertEqual(status, "EXPIRING_SOON")

        # Safe
        status, label = inventory.classify_expiry_status(30, warning_days=7)
        self.assertEqual(status, "SAFE")

        # Non-perishable / missing date
        status, label = inventory.classify_expiry_status(None)
        self.assertEqual(status, "NO_EXPIRY")


if __name__ == "__main__":
    unittest.main()
