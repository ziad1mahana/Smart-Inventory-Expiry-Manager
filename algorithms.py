"""
Smart Inventory & Expiry Manager - Algorithms Module
Course: Introduction to Algorithms | Instructor: Dr. Fatma Talaat | Team: Axiom

This module contains explicit, manual Python implementations of core algorithms
and data structures required for inventory sorting, lookup, and prioritization:
1. Merge Sort (Divide & Conquer) - O(n log n)
2. Chained Hash Table with Collision Handling & Dynamic Resizing - O(1) avg, O(n) worst
3. Linear Search - O(n) worst
4. Multi-Factor Priority Ranking Algorithm
"""

import math
from typing import Any, Callable, Dict, List, Optional, Tuple


# ============================================================================
# 1. MERGE SORT (Divide & Conquer)
# ============================================================================

def _safe_compare(a_val: Any, b_val: Any, missing_last: bool = True) -> int:
    """
    Compares two values safely, gracefully handling None/missing values.
    
    Returns:
        -1 if a < b
         0 if a == b
         1 if a > b
    """
    if a_val is None and b_val is None:
        return 0
    if a_val is None:
        return 1 if missing_last else -1
    if b_val is None:
        return -1 if missing_last else 1
    
    # Direct comparison for standard comparable types (str, int, float, date)
    if a_val < b_val:
        return -1
    elif a_val > b_val:
        return 1
    return 0


def merge_sort(
    items: List[Any],
    key_func: Optional[Callable[[Any], Any]] = None,
    reverse: bool = False,
    missing_last: bool = True
) -> List[Any]:
    """
    Sorts a list using the classical Merge Sort divide-and-conquer algorithm.
    
    Recurrence Relation: T(n) = 2*T(n/2) + Theta(n)
    Time Complexity:
        - Best Case:    O(n log n)
        - Average Case: O(n log n)
        - Worst Case:   O(n log n)
    Auxiliary Space Complexity:
        - O(n) required for temporary subarrays during merging.
    Stability:
        - Stable (preserves original order of elements with equal keys).
    
    Args:
        items: List of elements to sort.
        key_func: Optional function to extract comparison key from element.
        reverse: If True, sort in descending order.
        missing_last: If True, elements with None key appear at the end.
    
    Returns:
        A new sorted list.
    """
    if len(items) <= 1:
        return list(items)
    
    if key_func is None:
        key_func = lambda x: x

    # Divide: split array into left and right halves around midpoint
    mid = len(items) // 2
    left_half = merge_sort(items[:mid], key_func=key_func, reverse=reverse, missing_last=missing_last)
    right_half = merge_sort(items[mid:], key_func=key_func, reverse=reverse, missing_last=missing_last)

    # Conquer & Combine: merge the two sorted halves
    return _merge(left_half, right_half, key_func, reverse, missing_last)


def _merge(
    left: List[Any],
    right: List[Any],
    key_func: Callable[[Any], Any],
    reverse: bool,
    missing_last: bool
) -> List[Any]:
    """Merges two sorted lists into a single sorted list."""
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        key_l = key_func(left[i])
        key_r = key_func(right[j])
        cmp = _safe_compare(key_l, key_r, missing_last=missing_last)

        # In ascending order, pick left if cmp <= 0 (maintaining stability)
        # In descending order, pick left if cmp >= 0
        should_pick_left = (cmp <= 0) if not reverse else (cmp >= 0)

        if should_pick_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append any remaining elements
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged


def merge_sort_with_trace(
    items: List[Any],
    key_func: Optional[Callable[[Any], Any]] = None,
    label_func: Optional[Callable[[Any], str]] = None
) -> Tuple[List[Any], List[Dict[str, Any]]]:
    """
    Executes Merge Sort and records each recursive split and merge operation
    to provide educational step-by-step trace visualization.
    
    Returns:
        (sorted_list, trace_steps)
    """
    if key_func is None:
        key_func = lambda x: x
    if label_func is None:
        label_func = lambda x: str(key_func(x))

    trace: List[Dict[str, Any]] = []
    step_counter = [0]

    def _sort_traced(arr: List[Any], depth: int) -> List[Any]:
        if len(arr) <= 1:
            return list(arr)

        mid = len(arr) // 2
        left_raw = arr[:mid]
        right_raw = arr[mid:]

        step_counter[0] += 1
        trace.append({
            "step": step_counter[0],
            "action": "DIVIDE",
            "depth": depth,
            "input": [label_func(x) for x in arr],
            "left": [label_func(x) for x in left_raw],
            "right": [label_func(x) for x in right_raw],
            "description": f"Depth {depth}: Split {len(arr)} items into [{len(left_raw)}] and [{len(right_raw)}]"
        })

        left_sorted = _sort_traced(left_raw, depth + 1)
        right_sorted = _sort_traced(right_raw, depth + 1)

        merged = _merge(left_sorted, right_sorted, key_func, reverse=False, missing_last=True)

        step_counter[0] += 1
        trace.append({
            "step": step_counter[0],
            "action": "MERGE",
            "depth": depth,
            "left": [label_func(x) for x in left_sorted],
            "right": [label_func(x) for x in right_sorted],
            "merged": [label_func(x) for x in merged],
            "description": f"Depth {depth}: Merged {len(left_sorted)} + {len(right_sorted)} items -> [{', '.join([label_func(x) for x in merged])}]"
        })

        return merged

    sorted_result = _sort_traced(items, depth=0)
    return sorted_result, trace


# ============================================================================
# 2. CUSTOM HASH TABLE (Separate Chaining Collision Resolution)
# ============================================================================

class HashNode:
    """Key-value entry node for hash table separate chaining."""
    __slots__ = ("key", "value", "next")

    def __init__(self, key: str, value: Any, next_node: Optional["HashNode"] = None):
        self.key: str = str(key)
        self.value: Any = value
        self.next: Optional["HashNode"] = next_node


class ChainedHashTable:
    """
    A custom Hash Table implementation utilizing separate chaining (linked nodes)
    for collision resolution and dynamic rehashing.
    
    Academic Complexity:
    - Time Complexity (Lookup, Insertion, Deletion):
        * Average Case: O(1 + alpha), where alpha = n / m is the load factor.
          Under the Simple Uniform Hashing Assumption (SUHA), average time is O(1).
        * Worst Case:   O(n), occurring when all n keys collide into the same bucket.
    - Space Complexity: O(m + n), where m is bucket capacity and n is stored items.
    
    Hash Function:
    - Polynomial rolling hash: h(s) = sum(ord(s[i]) * 31^i) mod capacity
    """

    def __init__(self, initial_capacity: int = 16, max_load_factor: float = 0.75):
        if initial_capacity < 4:
            initial_capacity = 4
        self.capacity: int = initial_capacity
        self.max_load_factor: float = max_load_factor
        self.size: int = 0
        self.buckets: List[Optional[HashNode]] = [None] * self.capacity

    def _hash(self, key: str) -> int:
        """Computes bucket index using a polynomial rolling hash function."""
        s = str(key)
        hash_val = 0
        prime = 31
        for i, char in enumerate(s):
            hash_val = (hash_val + ord(char) * (prime ** (i % 7)))
        return hash_val % self.capacity

    def put(self, key: str, value: Any) -> None:
        """
        Inserts or updates a key-value pair.
        Automatically rehashes if load factor exceeds threshold.
        """
        key_str = str(key)
        index = self._hash(key_str)
        curr = self.buckets[index]

        # Check if key already exists in bucket chain -> update value
        while curr is not None:
            if curr.key == key_str:
                curr.value = value
                return
            curr = curr.next

        # Insert new node at head of chain (O(1))
        new_node = HashNode(key_str, value, next_node=self.buckets[index])
        self.buckets[index] = new_node
        self.size += 1

        # Check load factor and resize if necessary
        if (self.size / self.capacity) > self.max_load_factor:
            self._resize(self.capacity * 2)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieves value associated with key. Returns default if not found."""
        key_str = str(key)
        index = self._hash(key_str)
        curr = self.buckets[index]

        while curr is not None:
            if curr.key == key_str:
                return curr.value
            curr = curr.next

        return default

    def get_with_comparisons(self, key: str) -> Tuple[Any, int]:
        """
        Retrieves value along with the number of key equality comparisons performed.
        Useful for comparing O(1) hash lookup vs O(n) linear search.
        """
        key_str = str(key)
        index = self._hash(key_str)
        curr = self.buckets[index]
        comparisons = 0

        while curr is not None:
            comparisons += 1
            if curr.key == key_str:
                return curr.value, comparisons
            curr = curr.next

        return None, comparisons

    def contains(self, key: str) -> bool:
        """Returns True if key is present in the hash table."""
        return self.get(key) is not None

    def delete(self, key: str) -> bool:
        """
        Deletes key-value pair. Returns True if deleted, False if key was not found.
        """
        key_str = str(key)
        index = self._hash(key_str)
        curr = self.buckets[index]
        prev: Optional[HashNode] = None

        while curr is not None:
            if curr.key == key_str:
                if prev is None:
                    self.buckets[index] = curr.next
                else:
                    prev.next = curr.next
                self.size -= 1
                return True
            prev = curr
            curr = curr.next

        return False

    def _resize(self, new_capacity: int) -> None:
        """Doubles bucket capacity and rehashes all elements."""
        old_buckets = self.buckets
        self.capacity = new_capacity
        self.buckets = [None] * self.capacity
        self.size = 0  # Re-incremented during put

        for head in old_buckets:
            curr = head
            while curr is not None:
                self.put(curr.key, curr.value)
                curr = curr.next

    def get_stats(self) -> Dict[str, Any]:
        """Returns diagnostic metrics about bucket distribution and collisions."""
        empty_buckets = 0
        collision_count = 0
        max_bucket_len = 0
        bucket_lengths = []

        for head in self.buckets:
            length = 0
            curr = head
            while curr is not None:
                length += 1
                curr = curr.next

            bucket_lengths.append(length)
            if length == 0:
                empty_buckets += 1
            elif length > 1:
                collision_count += (length - 1)
            if length > max_bucket_len:
                max_bucket_len = length

        load_factor = self.size / self.capacity if self.capacity > 0 else 0.0

        return {
            "capacity": self.capacity,
            "size": self.size,
            "load_factor": round(load_factor, 3),
            "empty_buckets": empty_buckets,
            "occupied_buckets": self.capacity - empty_buckets,
            "total_collisions": collision_count,
            "max_chain_length": max_bucket_len,
            "bucket_lengths": bucket_lengths,
        }

    def get_chain_inspection(self) -> List[Dict[str, Any]]:
        """Returns a human-readable representation of all buckets and keys."""
        inspection = []
        for idx, head in enumerate(self.buckets):
            keys_in_bucket = []
            curr = head
            while curr is not None:
                keys_in_bucket.append(curr.key)
                curr = curr.next
            inspection.append({
                "bucket_index": idx,
                "chain_length": len(keys_in_bucket),
                "keys": keys_in_bucket
            })
        return inspection

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, key: str) -> Any:
        val = self.get(key)
        if val is None:
            raise KeyError(f"Key '{key}' not found in ChainedHashTable")
        return val

    def __setitem__(self, key: str, value: Any) -> None:
        self.put(key, value)


# ============================================================================
# 3. LINEAR SEARCH
# ============================================================================

def linear_search(
    items: List[Any],
    predicate: Callable[[Any], bool]
) -> Tuple[List[Any], int]:
    """
    Performs a linear scan across items checking predicate(item).
    
    Time Complexity:
        - Best Case:    O(1) (target found at index 0)
        - Average Case: O(n) (target found mid-way)
        - Worst Case:   O(n) (target at end or not present)
    Space Complexity: O(1) auxiliary (excluding return container).
    
    Returns:
        (matching_items_list, comparisons_count)
    """
    matches = []
    comparisons = 0

    for item in items:
        comparisons += 1
        if predicate(item):
            matches.append(item)

    return matches, comparisons


def linear_search_by_id(
    items: List[Dict[str, Any]],
    target_id: str
) -> Tuple[Optional[Dict[str, Any]], int]:
    """
    Scans a list of product dictionaries sequentially by product 'id'.
    Terminates early on first match.
    
    Returns:
        (found_product_or_None, comparisons_count)
    """
    comparisons = 0
    target_norm = str(target_id).strip().upper()

    for item in items:
        comparisons += 1
        curr_id = str(item.get("id", "")).strip().upper()
        if curr_id == target_norm:
            return item, comparisons

    return None, comparisons


# ============================================================================
# 4. MULTI-FACTOR PRIORITY SCORING ALGORITHM
# ============================================================================

def calculate_priority_score(
    days_until_expiry: Optional[int],
    quantity: int,
    min_threshold: int,
    unit_price: float = 0.0
) -> Tuple[int, str, str, Dict[str, int]]:
    """
    Calculates a deterministic multi-factor priority score (0 to 100+ points)
    to order inventory items requiring urgent operational attention.
    
    The score balances:
    1. Expiration Urgency (Spoilage Risk):
       - Already Expired:      +50 base pts + min(30, abs(days)*3)
       - Expiring Today:       +45 pts
       - Expiring in 1-3 days: +30 pts
       - Expiring in 4-7 days: +15 pts
       - Safe / No Expiry:       0 pts
    2. Stock Depletion (Stockout Risk):
       - Out of stock (qty=0): +35 pts
       - Low stock (qty <= threshold): round(35 * (threshold - qty) / max(1, threshold))
       - Healthy stock:          0 pts
    3. Capital Risk at Stake:
       - Value of expiring stock (qty * price), up to 15 bonus points
    
    Returns:
        (total_score, urgency_level, explanation_text, breakdown_dict)
    """
    expiry_pts = 0
    stock_pts = 0
    capital_pts = 0
    reasons = []

    # Factor 1: Expiration Risk
    if days_until_expiry is not None:
        if days_until_expiry < 0:
            overdue_days = abs(days_until_expiry)
            expiry_pts = 50 + min(30, overdue_days * 3)
            reasons.append(f"EXPIRED ({overdue_days}d ago)")
        elif days_until_expiry == 0:
            expiry_pts = 45
            reasons.append("EXPIRES TODAY")
        elif days_until_expiry <= 3:
            expiry_pts = 30
            reasons.append(f"Critical Expiry ({days_until_expiry}d left)")
        elif days_until_expiry <= 7:
            expiry_pts = 15
            reasons.append(f"Upcoming Expiry ({days_until_expiry}d left)")

    # Factor 2: Low-Stock Risk
    if quantity <= 0:
        stock_pts = 35
        reasons.append("OUT OF STOCK")
    elif min_threshold > 0 and quantity <= min_threshold:
        deficit = min_threshold - quantity
        ratio = deficit / max(1, min_threshold)
        stock_pts = max(5, round(35 * ratio))
        reasons.append(f"Low Stock ({quantity}/{min_threshold} units)")

    # Factor 3: Capital Risk at Stake (if perishable item is nearing expiry)
    if days_until_expiry is not None and days_until_expiry <= 7 and quantity > 0:
        value_at_risk = quantity * max(0.0, unit_price)
        capital_pts = min(15, int(value_at_risk / 15.0))
        if capital_pts > 0:
            reasons.append(f"Value at risk: ${value_at_risk:.2f}")

    total_score = expiry_pts + stock_pts + capital_pts

    # Determine Urgency Tier
    if total_score >= 70:
        urgency_level = "CRITICAL"
    elif total_score >= 45:
        urgency_level = "HIGH"
    elif total_score >= 20:
        urgency_level = "MEDIUM"
    else:
        urgency_level = "LOW"

    explanation = " | ".join(reasons) if reasons else "Healthy stock & safe expiry"

    breakdown = {
        "expiry_points": expiry_pts,
        "stock_points": stock_pts,
        "capital_points": capital_pts,
        "total": total_score
    }

    return total_score, urgency_level, explanation, breakdown
