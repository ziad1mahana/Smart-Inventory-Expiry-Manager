"""
Smart Inventory & Expiry Manager - Algorithms Unit Tests
Course: Introduction to Algorithms | Instructor: Dr. Fatma Talaat | Team: Axiom
"""

import unittest
from algorithms import (
    ChainedHashTable,
    calculate_priority_score,
    linear_search,
    linear_search_by_id,
    merge_sort,
    merge_sort_with_trace,
)


class TestMergeSort(unittest.TestCase):
    def test_empty_and_single_element(self):
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(merge_sort([42]), [42])

    def test_standard_numbers(self):
        data = [38, 27, 43, 3, 9, 82, 10]
        sorted_data = merge_sort(data)
        self.assertEqual(sorted_data, [3, 9, 10, 27, 38, 43, 82])

    def test_reverse_order(self):
        data = [5, 1, 9, 3, 7]
        sorted_desc = merge_sort(data, reverse=True)
        self.assertEqual(sorted_desc, [9, 7, 5, 3, 1])

    def test_dict_sorting_by_key(self):
        items = [
            {"name": "Milk", "quantity": 4},
            {"name": "Bread", "quantity": 1},
            {"name": "Eggs", "quantity": 25},
            {"name": "Yogurt", "quantity": 14},
        ]
        sorted_items = merge_sort(items, key_func=lambda x: x["quantity"])
        quantities = [x["quantity"] for x in sorted_items]
        self.assertEqual(quantities, [1, 4, 14, 25])

    def test_handling_none_values_missing_last(self):
        """Ensure products with missing expiration dates are ordered after dated products."""
        items = [
            {"id": "A", "expiry": "2026-10-20"},
            {"id": "B", "expiry": None},
            {"id": "C", "expiry": "2026-10-15"},
            {"id": "D", "expiry": None},
        ]
        sorted_asc = merge_sort(items, key_func=lambda x: x["expiry"], missing_last=True)
        expiries = [x["expiry"] for x in sorted_asc]
        self.assertEqual(expiries, ["2026-10-15", "2026-10-20", None, None])

    def test_stability(self):
        """Merge sort must preserve original relative order of equal keys."""
        items = [
            {"id": 1, "val": 10},
            {"id": 2, "val": 5},
            {"id": 3, "val": 10},
            {"id": 4, "val": 5},
        ]
        sorted_items = merge_sort(items, key_func=lambda x: x["val"])
        ids = [x["id"] for x in sorted_items]
        self.assertEqual(ids, [2, 4, 1, 3])

    def test_merge_sort_trace(self):
        data = ["Banana", "Apple", "Orange", "Grape"]
        sorted_res, trace = merge_sort_with_trace(data)
        self.assertEqual(sorted_res, ["Apple", "Banana", "Grape", "Orange"])
        self.assertGreater(len(trace), 0)
        actions = [t["action"] for t in trace]
        self.assertIn("DIVIDE", actions)
        self.assertIn("MERGE", actions)


class TestChainedHashTable(unittest.TestCase):
    def test_basic_crud(self):
        ht = ChainedHashTable(initial_capacity=8)
        ht.put("SKU-101", {"name": "Milk", "price": 1.5})
        ht.put("SKU-102", {"name": "Bread", "price": 1.0})

        self.assertEqual(len(ht), 2)
        self.assertTrue(ht.contains("SKU-101"))
        self.assertTrue(ht.contains("SKU-102"))
        self.assertFalse(ht.contains("SKU-999"))

        # Test retrieval
        val = ht.get("SKU-101")
        self.assertEqual(val["name"], "Milk")

        # Test update existing
        ht.put("SKU-101", {"name": "Fresh Milk", "price": 1.75})
        self.assertEqual(len(ht), 2)
        self.assertEqual(ht.get("SKU-101")["name"], "Fresh Milk")

        # Test deletion
        deleted = ht.delete("SKU-101")
        self.assertTrue(deleted)
        self.assertEqual(len(ht), 1)
        self.assertFalse(ht.contains("SKU-101"))
        self.assertIsNone(ht.get("SKU-101"))

        # Deleting non-existent key
        self.assertFalse(ht.delete("NON_EXISTENT"))

    def test_dynamic_rehashing_and_collisions(self):
        """Inserting items beyond max_load_factor triggers automatic capacity doubling."""
        ht = ChainedHashTable(initial_capacity=4, max_load_factor=0.75)
        self.assertEqual(ht.capacity, 4)

        keys = [f"ITEM-{i:03d}" for i in range(15)]
        for k in keys:
            ht.put(k, f"Value_{k}")

        self.assertEqual(len(ht), 15)
        self.assertGreater(ht.capacity, 4)
        for k in keys:
            self.assertEqual(ht.get(k), f"Value_{k}")

        stats = ht.get_stats()
        self.assertLessEqual(stats["load_factor"], 0.75)
        self.assertGreater(stats["occupied_buckets"], 0)

    def test_get_with_comparisons(self):
        ht = ChainedHashTable(initial_capacity=8)
        ht.put("KEY-A", 100)
        val, comps = ht.get_with_comparisons("KEY-A")
        self.assertEqual(val, 100)
        self.assertGreaterEqual(comps, 1)

        val_missing, comps_missing = ht.get_with_comparisons("NOT_FOUND")
        self.assertIsNone(val_missing)


class TestLinearSearch(unittest.TestCase):
    def test_linear_search_by_id_found(self):
        items = [
            {"id": "SKU-001", "name": "Apple"},
            {"id": "SKU-002", "name": "Banana"},
            {"id": "SKU-003", "name": "Cherry"},
        ]
        item, comps = linear_search_by_id(items, "SKU-002")
        self.assertIsNotNone(item)
        self.assertEqual(item["name"], "Banana")
        self.assertEqual(comps, 2)

    def test_linear_search_not_found(self):
        items = [
            {"id": "SKU-001", "name": "Apple"},
            {"id": "SKU-002", "name": "Banana"},
        ]
        item, comps = linear_search_by_id(items, "SKU-999")
        self.assertIsNone(item)
        self.assertEqual(comps, 2)  # Worst case: scanned all elements

    def test_linear_search_predicate(self):
        nums = [10, 25, 30, 45, 50]
        matches, comps = linear_search(nums, lambda x: x > 25)
        self.assertEqual(matches, [30, 45, 50])
        self.assertEqual(comps, 5)


class TestPriorityScorer(unittest.TestCase):
    def test_expired_and_low_stock_critical(self):
        # Expired 3 days ago, 0 units in stock
        score, urgency, reason, breakdown = calculate_priority_score(
            days_until_expiry=-3,
            quantity=0,
            min_threshold=10,
            unit_price=5.0
        )
        self.assertGreaterEqual(score, 70)
        self.assertEqual(urgency, "CRITICAL")
        self.assertIn("EXPIRED", reason)
        self.assertIn("OUT OF STOCK", reason)

    def test_safe_product_low_priority(self):
        # Expires in 60 days, ample stock
        score, urgency, reason, breakdown = calculate_priority_score(
            days_until_expiry=60,
            quantity=50,
            min_threshold=10,
            unit_price=2.0
        )
        self.assertLess(score, 20)
        self.assertEqual(urgency, "LOW")


if __name__ == "__main__":
    unittest.main()
