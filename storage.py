"""
Smart Inventory & Expiry Manager - Storage & Persistence Module
Course: Introduction to Algorithms | Instructor: Dr. Fatma Talaat | Team: Axiom

This module manages SQLite database operations for persistent inventory storage,
input validation, transaction integrity, and sample dataset seeding.
"""

import contextlib
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, Generator, List, Optional

# Default database path in the project data/ directory
DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "inventory.db")


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Creates a database connection with row factory configured to return dict-like objects."""
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


@contextlib.contextmanager
def db_session(db_path: str = DEFAULT_DB_PATH) -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager providing safe transaction management and guaranteed connection closure.
    Prevents file lock issues on Windows platforms.
    """
    conn = get_connection(db_path)
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initializes the SQLite schema and ensures necessary indexes exist."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0),
                min_threshold INTEGER NOT NULL CHECK (min_threshold >= 0),
                expiration_date TEXT,
                unit_price REAL DEFAULT 0.0 CHECK (unit_price >= 0),
                supplier TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_expiry ON products(expiration_date);")


def get_all_products(db_path: str = DEFAULT_DB_PATH) -> List[Dict[str, Any]]:
    """Retrieves all products from the database ordered by product id."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY id ASC;")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_product_by_id(db_path: str, product_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a single product by primary key."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?;", (str(product_id).strip(),))
        row = cursor.fetchone()
        return dict(row) if row else None


def add_product(db_path: str, product: Dict[str, Any]) -> None:
    """
    Inserts a new product record into the database.
    Validates required fields, non-negative quantities, and ID uniqueness.
    """
    prod_id = str(product.get("id", "")).strip().upper()
    name = str(product.get("name", "")).strip()
    category = str(product.get("category", "General")).strip()
    
    if not prod_id:
        raise ValueError("Product ID (SKU) cannot be empty.")
    if not name:
        raise ValueError("Product Name cannot be empty.")

    try:
        quantity = int(product.get("quantity", 0))
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid quantity: must be a non-negative integer.") from err

    try:
        min_threshold = int(product.get("min_threshold", 0))
        if min_threshold < 0:
            raise ValueError("Minimum threshold cannot be negative.")
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid minimum threshold: must be a non-negative integer.") from err

    try:
        unit_price = float(product.get("unit_price", 0.0))
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid unit price: must be a non-negative number.") from err

    raw_expiry = product.get("expiration_date")
    expiration_date = str(raw_expiry).strip() if raw_expiry else None
    if expiration_date in ("", "None", "null"):
        expiration_date = None

    supplier = str(product.get("supplier", "")).strip()
    now_iso = datetime.now().isoformat()

    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?;", (prod_id,))
        if cursor.fetchone():
            raise ValueError(f"Product ID '{prod_id}' already exists. SKU must be unique.")

        cursor.execute("""
            INSERT INTO products (id, name, category, quantity, min_threshold, expiration_date, unit_price, supplier, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (prod_id, name, category, quantity, min_threshold, expiration_date, unit_price, supplier, now_iso, now_iso))


def update_product(db_path: str, product_id: str, updates: Dict[str, Any]) -> None:
    """Updates an existing product record."""
    prod_id = str(product_id).strip()
    existing = get_product_by_id(db_path, prod_id)
    if not existing:
        raise ValueError(f"Product with ID '{prod_id}' does not exist.")

    name = str(updates.get("name", existing["name"])).strip()
    category = str(updates.get("category", existing["category"])).strip()
    
    try:
        quantity = int(updates.get("quantity", existing["quantity"]))
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid quantity.") from err

    try:
        min_threshold = int(updates.get("min_threshold", existing["min_threshold"]))
        if min_threshold < 0:
            raise ValueError("Minimum threshold cannot be negative.")
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid minimum threshold.") from err

    try:
        unit_price = float(updates.get("unit_price", existing["unit_price"]))
        if unit_price < 0:
            raise ValueError("Unit price cannot be negative.")
    except (TypeError, ValueError) as err:
        raise ValueError("Invalid unit price.") from err

    raw_expiry = updates.get("expiration_date", existing["expiration_date"])
    expiration_date = str(raw_expiry).strip() if raw_expiry else None
    if expiration_date in ("", "None", "null"):
        expiration_date = None

    supplier = str(updates.get("supplier", existing["supplier"])).strip()
    now_iso = datetime.now().isoformat()

    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE products
            SET name = ?, category = ?, quantity = ?, min_threshold = ?, expiration_date = ?, unit_price = ?, supplier = ?, updated_at = ?
            WHERE id = ?;
        """, (name, category, quantity, min_threshold, expiration_date, unit_price, supplier, now_iso, prod_id))


def delete_product(db_path: str, product_id: str) -> bool:
    """Deletes a product by ID. Returns True if deleted, False if not found."""
    prod_id = str(product_id).strip()
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?;", (prod_id,))
        return cursor.rowcount > 0


def clear_all_products(db_path: str = DEFAULT_DB_PATH) -> None:
    """Empties the products table."""
    with db_session(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products;")
