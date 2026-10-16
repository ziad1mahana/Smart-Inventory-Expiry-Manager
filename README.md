# Smart Inventory & Expiry Manager 📦

**Course:** Introduction to Algorithms  
**Instructor:** Dr. Fatma Talaat  
**Team Name:** Axiom  
**Project Title:** Smart Inventory & Expiry Manager  

---

## 1. Project Overview & Problem Statement

Small grocery stores, convenience marts, and retail shops face significant financial losses and operational friction from:
1. **Perishable inventory spoilage:** Unsold products expiring unnoticed on shelves.
2. **Stockouts:** Depleted high-demand items that lead to lost revenue.
3. **Inefficient prioritization:** Managers lacking actionable guidance on which products require urgent markdown, disposal, or reordering.

**Smart Inventory & Expiry Manager** is a modern, responsive web application engineered to solve these challenges through algorithmic automation. It combines persistent SQLite inventory tracking with pure, hand-crafted Python algorithms (Merge Sort, Chained Hash Tables, Linear Search, and Multi-Factor Priority Ranking) to optimize store operations, reduce waste, and provide real-time decision support.

---

## 2. Key Features

- **Executive KPI Dashboard:** Real-time metrics for total SKUs, units in stock, inventory valuation, expired items, items nearing expiration, and low-stock alerts. Interactive Plotly charts visualize stock health, category valuation, and expiration timelines.
- **Full Inventory CRUD Management:** Add, edit, and delete products with strict validation (positive quantities, non-negative thresholds and prices, unique SKUs, safe date formatting).
- **Manual Merge Sort:** Pure divide-and-conquer implementation sorting items by expiration date, stock quantity, unit price, SKU, or priority score. Non-perishables (missing dates) are handled gracefully and consistently placed at the end.
- **Expiration Alert Center:** Configurable expiration threshold slider (default: 7 days) classifying products into *Expired*, *Expiring Today*, *Expiring Soon*, *Safe*, and *Non-Perishable*.
- **Low-Stock & Intelligent Reorder Station:** Identifies items at or below threshold and calculates suggested replenishment units:
  $$\text{Reorder Units} = \max(0, (2 \times \text{min\_threshold}) - \text{quantity})$$
  Includes an inline stock receiving form to instantly update quantities.
- **Deterministic Priority Action Matrix:** Ranks all inventory items using an explainable mathematical scoring engine combining spoilage urgency, stock depletion ratio, and capital at risk.
- **Academic Algorithm Lab:** Interactive side-by-side comparison of Linear Search ($O(n)$) vs Hash Table ($O(1)$), live bucket inspection of separate chaining collisions, step-by-step Merge Sort divide-and-conquer visualization, and an empirical scaling benchmark harness.
- **Inventory Reports & CSV Export:** One-click export of sanitized CSV reports for full inventory, disposal audits, reorder sheets, and category summaries.
- **Dynamic Relative Demo Data:** Restoring demo data seeds 20 realistic grocery products dynamically calculated relative to today's date (`datetime.date.today()`), guaranteeing that the live demonstration is always fresh.

---

## 3. Technology Stack

- **Core Language:** Python 3.10+ (Tested on Python 3.14)
- **Web Interface:** Streamlit
- **Persistence:** SQLite (`data/inventory.db`) with transactional session context management
- **Data Manipulation:** Pandas (tabular conversions and CSV generation)
- **Visualizations:** Plotly Express & Plotly Graph Objects
- **Algorithms & Structures:** Pure Python standard libraries (`math`, `time`, `typing`, `datetime`)

---

## 4. Algorithmic Implementations & Big-O Analysis

### A. Merge Sort (Divide & Conquer)
- **Concept:** Recursively splits the array into two halves at the midpoint until single-element subarrays are reached, recursively sorts them, and merges them using two pointers while preserving stability.
- **Recurrence Relation:**
  $$T(n) = 2T(n/2) + \Theta(n)$$
  By the Master Theorem (Case 2: $a=2, b=2, f(n) = \Theta(n) \implies n^{\log_2 2} = n^1$), the time complexity is $\Theta(n \log n)$.
- **Time Complexity:**
  - Best Case: $O(n \log n)$
  - Average Case: $O(n \log n)$
  - Worst Case: $O(n \log n)$
- **Auxiliary Space Complexity:** $O(n)$ required for allocating temporary subarrays during the merge phase.
- **Missing Date Handling:** A custom safe comparison function ensures that items with `expiration_date = None` are sorted consistently to the end of the list without raising type comparison exceptions.

### B. Custom Chained Hash Table
- **Concept:** A hash table implemented with **Separate Chaining** (linked list of `HashNode` items in each bucket) and dynamic rehashing.
- **Hash Function:** Polynomial rolling hash:
  $$h(s) = \left(\sum_{i=0}^{m-1} \text{ord}(s[i]) \times 31^i\right) \pmod{\text{capacity}}$$
- **Dynamic Resizing:** When the load factor $\alpha = \frac{n}{m} > 0.75$, the table automatically doubles its bucket array ($m \leftarrow 2m$) and rehashes all elements.
- **Time Complexity:**
  - Average Case (under Simple Uniform Hashing Assumption): $O(1 + \alpha) = O(1)$
  - Worst Case: $O(n)$ (when all keys hash to the identical bucket)
- **Space Complexity:** $O(m + n)$ where $m$ is the number of buckets and $n$ is the number of stored keys.

### C. Linear Search
- **Concept:** Sequentially inspects each element in the list from index $0$ to $n-1$ until a matching product ID or keyword is found.
- **Time Complexity:**
  - Best Case: $O(1)$ (target located at index 0)
  - Average Case: $O(n/2) = O(n)$
  - Worst Case: $O(n)$ (target at index $n-1$ or absent)
- **Space Complexity:** $O(1)$ auxiliary memory.

### D. Multi-Factor Priority Ranking
- **Concept:** A deterministic, explainable mathematical score (0–100+ points) evaluated per item:
  - **Spoilage Urgency:** Already expired ($50\text{ pts} + 3\times\text{overdue days}$), expires today ($45\text{ pts}$), expires $\le 3\text{d}$ ($30\text{ pts}$), expires $\le 7\text{d}$ ($15\text{ pts}$).
  - **Stock Deficit:** Out of stock ($35\text{ pts}$), below minimum threshold ($\text{round}(35 \times \frac{\text{threshold} - \text{qty}}{\text{threshold}})$).
  - **Capital at Stake:** Up to 15 bonus points for perishable products with high inventory value at risk.
- **Computational Complexity:** $O(n)$ to compute scores for $n$ items, plus $O(n \log n)$ to order them via Merge Sort $\implies O(n \log n)$ total.

---

## 5. Big-O Complexity Comparison Table

| Algorithm / Data Structure | Best Case (Time) | Average Case (Time) | Worst Case (Time) | Space Complexity | Practical Purpose in Project |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Linear Search** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | Keyword search across product names & suppliers |
| **Chained Hash Table Lookup** | $O(1)$ | $O(1)$ | $O(n)$ | $O(m + n)$ | Instant $O(1)$ SKU lookup by product ID |
| **Chained Hash Table Insertion** | $O(1)$ | $O(1)^*$ | $O(n)$ | $O(1)$ | Fast SKU indexing with dynamic doubling |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Stable sorting by date, quantity, price, priority |
| **Priority Ranking** | $O(n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Multi-factor operational urgency scoring |

*\*Amortized average time accounting for occasional table doubling.*

---

## 6. Project Directory Structure

```text
Smart Inventory & Expiry Manager/
├── app.py                  # Main Streamlit web application & modern SaaS UI
├── algorithms.py           # Pure Python implementations: Merge Sort, Hash Table, Linear Search
├── inventory.py            # Business logic: classifications, reorder formula, dynamic demo seed
├── storage.py              # SQLite database persistence layer & transactional session manager
├── requirements.txt        # Minimal pinned project dependencies
├── README.md               # Comprehensive project documentation & demo presentation script
├── .gitignore              # Ignored cache, virtual environments, and SQLite database files
├── data/                   # SQLite database directory (inventory.db)
└── tests/                  # Automated test suite
    ├── test_algorithms.py  # Unit tests for Merge Sort, Hash Table, Linear Search, Priority
    └── test_inventory.py   # Unit tests for SQLite CRUD, reorder formulas, date classifications
```

---

## 7. Installation and Run Instructions

### Prerequisites
Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your machine.

### Installation
1. Open a terminal in the project directory:
   ```bash
   cd "Smart Inventory & Expiry Manager"
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
Launch the application using Streamlit:
```bash
streamlit run app.py
```
The application will open automatically in your browser at `http://localhost:8501`.

### Running Automated Tests
Run the complete unit test suite to verify all algorithms, edge cases, and persistence:
```bash
python -m unittest discover -s tests -v
```

---

## 8. Step-by-Step Live Demo Script for Dr. Fatma Talaat (3–5 Minutes)

When presenting this project to **Dr. Fatma Talaat**, follow this concise, high-impact demonstration flow:

1. **Introduction & Motivation (30 seconds):**
   - *"Good morning Dr. Fatma. We are Team Axiom, presenting the Smart Inventory & Expiry Manager. Our goal was to solve two critical grocery store challenges—food spoilage and stockouts—using the fundamental algorithms taught in our course."*
   - Point out that all algorithms are manually implemented in pure Python in `algorithms.py` rather than delegating to library shortcuts.

2. **Executive Dashboard (45 seconds):**
   - Show the KPI cards: Total SKUs, units, valuation, expired products, and low stock items.
   - Explain how all metrics are calculated live from our persistent SQLite database (`data/inventory.db`).
   - Mention that sample data dates are dynamically computed relative to *today's date*, ensuring realistic expiration states at any time.

3. **Product Catalog & Manual Merge Sort (60 seconds):**
   - Navigate to **Product Catalog**.
   - Select **Sort By: Expiration Date (Earliest First)**.
   - Highlight: *"Here we demonstrate our Divide-and-Conquer Merge Sort ($O(n \log n)$). Notice how expired and imminent products appear first, while non-perishables like Salt and Rice with no expiry date are placed cleanly at the end without throwing errors."*
   - Show that sorting by **Quantity** or **Priority Score** instantly re-orders using the same stable algorithm.

4. **Algorithm Lab & Academic Showcase (90 seconds - Most Important!):**
   - Navigate to **Algorithm Lab**.
   - **Tab 1 (Search Comparison):** Select a SKU (e.g. `SKU-1016`) and click *Run Search Comparison*.
     - Show Dr. Fatma the difference: Linear Search scanned 16 items sequentially ($O(n)$), while our Custom Chained Hash Table found it in 1 comparison ($O(1)$).
   - **Tab 2 (Hash Table Inspection):** Show the live bucket distribution table. Point out the load factor $\alpha = n/m$, collision count, and chained linked nodes in each bucket. Explain the polynomial rolling hash function.
   - **Tab 3 (Merge Sort Visualizer):** Walk through the recursive divide steps and merge steps showing how subarrays are combined. Mention recurrence $T(n) = 2T(n/2) + \Theta(n)$ and auxiliary space $O(n)$.
   - **Tab 4 (Empirical Scaling Benchmark):** Click *Run Synthetic Scaling Benchmark* to display the Plotly curves demonstrating $O(1)$ vs $O(n)$ scaling across 100 to 5,000 items.

5. **Operational Stations & CSV Export (45 seconds):**
   - Visit **Low-Stock & Reorder Station**: Explain the deterministic formula $\max(0, 2 \times \text{threshold} - \text{qty})$. Use the *Receive Stock* button to add units to an out-of-stock item and watch the state update immediately.
   - Visit **Inventory Reports**: Download a CSV report to show real-world export capability.
   - Conclude: *"Thank you, Dr. Fatma. The system is fully tested with 19 automated unit tests and is ready for small grocery deployment."*

---

## 9. Known Limitations

- **Single-Node SQLite:** Designed for single-store local deployments. Multi-location enterprise chains would benefit from PostgreSQL.
- **Barcode Scanner Integration:** Currently inputs SKUs via text and forms; hardware barcode reader integration can be added via USB HID emulation in future iterations.
- **Empirical Benchmark Variance:** Microsecond timings at small $N$ ($N \le 100$) reflect operating system task scheduling and Python bytecode interpretation rather than theoretical complexity deviations.
