"""
Smart Inventory & Expiry Manager - Inventory Business Logic Module
Course: Introduction to Algorithms | Instructor: Dr. Fatma Talaat | Team: Axiom

This module handles inventory business rules:
- Expiration date analysis & classification relative to current date
- Stock depletion tracking & intelligent reorder recommendations
- Dynamic sample dataset generation with relative dates
"""

from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import storage
from algorithms import calculate_priority_score


# Standard grocery categories
CATEGORIES = [
    "Dairy & Eggs",
    "Bakery & Bread",
    "Fresh Produce",
    "Meat & Poultry",
    "Beverages",
    "Snacks & Sweets",
    "Canned & Dry Goods",
    "Condiments & Sauces",
]


def parse_date(date_str: Optional[str]) -> Optional[date]:
    """Safely parses a YYYY-MM-DD string into a datetime.date object."""
    if not date_str:
        return None
    try:
        return datetime.strptime(str(date_str).strip(), "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def calculate_days_until_expiry(expiration_date_str: Optional[str], current_date: Optional[date] = None) -> Optional[int]:
    """
    Calculates remaining days until expiration.
    Returns negative integer if expired, 0 if expires today, positive if future, or None if no date.
    """
    if current_date is None:
        current_date = date.today()
    exp_date = parse_date(expiration_date_str)
    if exp_date is None:
        return None
    return (exp_date - current_date).days


def classify_expiry_status(days_left: Optional[int], warning_days: int = 7) -> Tuple[str, str]:
    """
    Classifies expiration status into standardized badge labels and visual severity.
    
    Returns:
        (status_key, display_label)
    """
    if days_left is None:
        return "NO_EXPIRY", "Non-Perishable"
    if days_left < 0:
        return "EXPIRED", f"Expired ({abs(days_left)}d ago)"
    if days_left == 0:
        return "EXPIRING_TODAY", "Expires Today!"
    if days_left <= warning_days:
        return "EXPIRING_SOON", f"Expires Soon ({days_left}d)"
    return "SAFE", f"Safe ({days_left}d)"


def classify_stock_status(quantity: int, min_threshold: int) -> Tuple[str, str]:
    """
    Classifies stock level into health status.
    
    Returns:
        (status_key, display_label)
    """
    if quantity <= 0:
        return "OUT_OF_STOCK", "Out of Stock"
    if min_threshold > 0 and quantity <= min_threshold:
        return "LOW_STOCK", "Low Stock"
    if min_threshold > 0 and quantity >= (3 * min_threshold):
        return "OVERSTOCKED", "Overstocked"
    return "HEALTHY", "Optimal Stock"


def calculate_reorder_recommendation(quantity: int, min_threshold: int, unit_price: float = 0.0) -> Dict[str, Any]:
    """
    Applies inventory reordering policy:
    - Target stock level: 2 * min_threshold
    - Suggested units: max(0, (2 * min_threshold) - quantity)
    - Reorder cost: suggested_units * unit_price
    """
    target_stock = max(0, 2 * min_threshold)
    suggested_units = max(0, target_stock - quantity)
    est_cost = suggested_units * max(0.0, unit_price)

    return {
        "needs_reorder": quantity <= min_threshold,
        "target_stock": target_stock,
        "suggested_units": suggested_units,
        "estimated_cost": round(est_cost, 2),
    }


def enrich_product_data(product: Dict[str, Any], warning_days: int = 7, current_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Enriches a raw database product record with computed expiration metrics,
    stock classifications, reorder recommendations, and algorithmic priority scores.
    """
    if current_date is None:
        current_date = date.today()

    p = dict(product)
    qty = int(p.get("quantity", 0))
    threshold = int(p.get("min_threshold", 0))
    unit_price = float(p.get("unit_price", 0.0))
    exp_str = p.get("expiration_date")

    days_left = calculate_days_until_expiry(exp_str, current_date=current_date)
    expiry_key, expiry_label = classify_expiry_status(days_left, warning_days=warning_days)
    stock_key, stock_label = classify_stock_status(qty, threshold)
    reorder_info = calculate_reorder_recommendation(qty, threshold, unit_price)

    # Calculate algorithmic priority score
    score, urgency, reason, breakdown = calculate_priority_score(
        days_until_expiry=days_left,
        quantity=qty,
        min_threshold=threshold,
        unit_price=unit_price
    )

    p["days_until_expiry"] = days_left
    p["expiry_status_key"] = expiry_key
    p["expiry_status_label"] = expiry_label
    p["stock_status_key"] = stock_key
    p["stock_status_label"] = stock_label
    p["reorder"] = reorder_info
    p["total_stock_value"] = round(qty * unit_price, 2)
    p["priority_score"] = score
    p["priority_urgency"] = urgency
    p["priority_reason"] = reason
    p["priority_breakdown"] = breakdown

    return p


def get_enriched_inventory(db_path: str = storage.DEFAULT_DB_PATH, warning_days: int = 7) -> List[Dict[str, Any]]:
    """Loads all products from SQLite and enriches each with computed analytical metrics."""
    raw_products = storage.get_all_products(db_path)
    today = date.today()
    return [enrich_product_data(p, warning_days=warning_days, current_date=today) for p in raw_products]


def generate_sample_products(current_date: Optional[date] = None) -> List[Dict[str, Any]]:
    """
    Generates 20 realistic grocery products with dates computed dynamically
    relative to current_date. This guarantees the demo is always live and meaningful!
    """
    if current_date is None:
        current_date = date.today()

    def d_offset(days: int) -> str:
        return (current_date + timedelta(days=days)).isoformat()

    sample_items = [
        # --- EXPIRED PRODUCTS ---
        {
            "id": "SKU-1001",
            "name": "Almarai Full Fat Milk 1L",
            "category": "Dairy & Eggs",
            "quantity": 4,
            "min_threshold": 12,
            "expiration_date": d_offset(-3),  # Expired 3 days ago
            "unit_price": 1.75,
            "supplier": "Almarai Co."
        },
        {
            "id": "SKU-1002",
            "name": "Fresh Gourmet Strawberries 250g",
            "category": "Fresh Produce",
            "quantity": 8,
            "min_threshold": 10,
            "expiration_date": d_offset(-1),  # Expired yesterday
            "unit_price": 3.20,
            "supplier": "Greenfield Farms"
        },
        {
            "id": "SKU-1003",
            "name": "Artisan French Baguette",
            "category": "Bakery & Bread",
            "quantity": 3,
            "min_threshold": 15,
            "expiration_date": d_offset(-2),  # Expired 2 days ago
            "unit_price": 1.20,
            "supplier": "Parisian Bakery"
        },

        # --- EXPIRING TODAY ---
        {
            "id": "SKU-1004",
            "name": "Greek Natural Yogurt 500g",
            "category": "Dairy & Eggs",
            "quantity": 14,
            "min_threshold": 10,
            "expiration_date": d_offset(0),   # Today!
            "unit_price": 2.50,
            "supplier": "Olympus Dairy"
        },
        {
            "id": "SKU-1005",
            "name": "Fresh Chicken Breast Fillet 500g",
            "category": "Meat & Poultry",
            "quantity": 6,
            "min_threshold": 8,
            "expiration_date": d_offset(0),   # Today!
            "unit_price": 5.80,
            "supplier": "Al-Wataniya Poultry"
        },

        # --- EXPIRING SOON (1 to 7 days) ---
        {
            "id": "SKU-1006",
            "name": "Organic Baby Spinach 200g",
            "category": "Fresh Produce",
            "quantity": 5,
            "min_threshold": 8,
            "expiration_date": d_offset(1),   # Tomorrow!
            "unit_price": 2.10,
            "supplier": "Greenfield Farms"
        },
        {
            "id": "SKU-1007",
            "name": "Fresh Orange Juice 1L",
            "category": "Beverages",
            "quantity": 11,
            "min_threshold": 10,
            "expiration_date": d_offset(2),   # 2 days
            "unit_price": 2.80,
            "supplier": "SunRays Beverages"
        },
        {
            "id": "SKU-1008",
            "name": "White Sandwich Toast Bread",
            "category": "Bakery & Bread",
            "quantity": 2,                    # Low stock + expiring soon
            "min_threshold": 14,
            "expiration_date": d_offset(3),   # 3 days
            "unit_price": 1.50,
            "supplier": "Golden Harvest"
        },
        {
            "id": "SKU-1009",
            "name": "Cheddar Cheese Block 250g",
            "category": "Dairy & Eggs",
            "quantity": 16,
            "min_threshold": 8,
            "expiration_date": d_offset(5),   # 5 days
            "unit_price": 4.10,
            "supplier": "Kraft Foods"
        },
        {
            "id": "SKU-1010",
            "name": "Lean Minced Beef 500g",
            "category": "Meat & Poultry",
            "quantity": 0,                    # Out of stock + upcoming expiry batch
            "min_threshold": 10,
            "expiration_date": d_offset(4),
            "unit_price": 6.50,
            "supplier": "Al-Wataniya Poultry"
        },

        # --- SAFE / FRESH PERISHABLES (14 to 60 days) ---
        {
            "id": "SKU-1011",
            "name": "Free-Range Large Brown Eggs 30pk",
            "category": "Dairy & Eggs",
            "quantity": 25,
            "min_threshold": 12,
            "expiration_date": d_offset(18),
            "unit_price": 4.80,
            "supplier": "FarmFresh Organics"
        },
        {
            "id": "SKU-1012",
            "name": "Pure Butter Unsalted 200g",
            "category": "Dairy & Eggs",
            "quantity": 22,
            "min_threshold": 15,
            "expiration_date": d_offset(28),
            "unit_price": 3.40,
            "supplier": "Lurpak Foods"
        },
        {
            "id": "SKU-1013",
            "name": "Organic Honey Honeycomb 400g",
            "category": "Condiments & Sauces",
            "quantity": 12,
            "min_threshold": 6,
            "expiration_date": d_offset(120),
            "unit_price": 8.90,
            "supplier": "Apiary Valley"
        },
        {
            "id": "SKU-1014",
            "name": "Italian Roasted Espresso Beans 500g",
            "category": "Beverages",
            "quantity": 30,
            "min_threshold": 10,
            "expiration_date": d_offset(90),
            "unit_price": 7.50,
            "supplier": "Lavazza Import"
        },

        # --- LOW-STOCK BUT SAFE EXPIRY ---
        {
            "id": "SKU-1015",
            "name": "Extra Virgin Olive Oil 750ml",
            "category": "Condiments & Sauces",
            "quantity": 2,                    # Low stock!
            "min_threshold": 10,
            "expiration_date": d_offset(240),
            "unit_price": 9.50,
            "supplier": "Mediterranean Harvest"
        },
        {
            "id": "SKU-1016",
            "name": "Belgian Dark Chocolate 100g",
            "category": "Snacks & Sweets",
            "quantity": 1,                    # Low stock!
            "min_threshold": 15,
            "expiration_date": d_offset(150),
            "unit_price": 2.90,
            "supplier": "Godiva Confections"
        },
        {
            "id": "SKU-1017",
            "name": "Whole Rolled Oats 1kg",
            "category": "Canned & Dry Goods",
            "quantity": 0,                    # Out of stock!
            "min_threshold": 8,
            "expiration_date": d_offset(180),
            "unit_price": 3.10,
            "supplier": "Quaker Oats"
        },

        # --- NON-PERISHABLE / MISSING EXPIRATION DATES ---
        {
            "id": "SKU-1018",
            "name": "Basmati White Rice 5kg",
            "category": "Canned & Dry Goods",
            "quantity": 40,
            "min_threshold": 15,
            "expiration_date": None,          # Non-perishable / no expiry
            "unit_price": 11.20,
            "supplier": "Indus Valley"
        },
        {
            "id": "SKU-1019",
            "name": "Pure Refined Table Salt 1kg",
            "category": "Condiments & Sauces",
            "quantity": 55,
            "min_threshold": 20,
            "expiration_date": None,          # No expiry date
            "unit_price": 0.60,
            "supplier": "Salsal Salt Co."
        },
        {
            "id": "SKU-1020",
            "name": "Sparkling Mineral Water 6x500ml",
            "category": "Beverages",
            "quantity": 18,
            "min_threshold": 12,
            "expiration_date": d_offset(300),
            "unit_price": 4.25,
            "supplier": "San Pellegrino"
        },
    ]

    return sample_items


def seed_or_reset_demo_data(db_path: str = storage.DEFAULT_DB_PATH) -> int:
    """Clears existing data and populates SQLite with 20 realistic sample products."""
    storage.init_db(db_path)
    storage.clear_all_products(db_path)
    sample_items = generate_sample_products()
    for item in sample_items:
        storage.add_product(db_path, item)
    return len(sample_items)
