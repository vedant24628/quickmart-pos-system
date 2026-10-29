# Quick Mart — Feature Specifications & Verification

This document catalogs all verified capabilities and functional modules implemented in the **Quick Mart Retail Store Management & Point of Sale System**.

---

## 1. Authentication & Role-Based Access Control (RBAC)

- **Session Authentication**: Native Django session management with secure session cookies and middleware-driven route guards.
- **Role Hierarchy**:
  - **Admin**: Full read, write, update, and delete access across Inventory, Suppliers, POS Terminal, Billing Logs, and Analytics.
  - **Cashier**: Access focused on checkout billing, receipt generation, invoice history, and catalog search.
- **Cryptographic Password Security**:
  - PBKDF2 with SHA-256 password hashing for newly registered staff accounts.
  - Backward compatibility with standard scrypt hashes (`hashlib.scrypt`).
- **Unauthenticated Protection**: Protected routes automatically redirect unauthenticated traffic to `/auth/login?next=<path>`.

---

## 2. Interactive Point of Sale (POS) Terminal

- **Two-Panel Layout**:
  - *Left Catalog Panel*: Displays products in a responsive grid with category tabs, live search input, stock chips, and quick-add actions.
  - *Right Cart Panel*: Persistent sticky order panel showing item rows, unit price, quantity increment/decrement controls, subtotal, and tax summaries.
- **Dynamic Tax Computation**:
  - Automatic split into statutory **State GST (SGST 9%)** and **Central GST (CGST 9%)**.
  - Dynamic rounding ensuring financial balancing down to two decimal places.
- **Tender Methods**:
  - Support for **Cash**, **UPI** (Unified Payments Interface), and **Card**.
- **Atomic Stock Validation**:
  - Instant client-side and server-side stock availability checks.
  - Prevents ordering quantities exceeding shelf inventory.
  - Atomic decrementing of stock levels executed in a single transaction block (`transaction.atomic()`).

---

## 3. Digital Invoicing & PDF Generation

- **Unique Invoice Serials**: Sequential formatting using chronological prefixes (`QM-YYYYMM-XXXX`).
- **Thermal Browser Printing**: Responsive receipt layout styled with `@media print` rules for thermal roll printers and letterhead output.
- **Server-Side Vector PDF Engine**:
  - Programmatic generation using **ReportLab 5.0**.
  - Renders corporate header badges, store address, customer details, itemized transaction table, and GST breakdowns.
  - Dynamically streamed directly to the client browser as an attachment.

---

## 4. Multi-Category Inventory Management

- **7 Retail Departments**:
  - Vegetables, Fruits, Grocery, Electronics, Toiletries, Decor, and Kitchen.
- **Visual Three-Tier Stock Health Status**:
  - **Critical Stock** ($< 10$ units): Highlighted in high-visibility orange chips for urgent reordering.
  - **Low Stock** ($10–30$ units): Marked with amber warning tags for upcoming replenishment.
  - **In Stock** ($> 30$ units): Displayed in clean green indicators representing healthy inventory.
- **Search & Filter Suite**:
  - Instant substring search by product name.
  - Category dropdown filter.
  - Stock health status filter (`critical`, `low`, `good`).
  - Column sorting by Name, Price, Stock Quantity, and Department.

---

## 5. Wholesale Supplier Directory

- **Vendor Records**: Maintain corporate company names, account representatives, telephone numbers, emails, and physical warehouse addresses.
- **Relational Integrity**:
  - Displays dynamic product counts supplied by each vendor.
  - Deleting a vendor safely unlinks catalog products by setting `supplier_id = NULL` without causing cascading product loss.

---

## 6. Executive Business Intelligence & Sales Analytics

- **KPI Metric Tiles**:
  - Today's Gross Revenue (auto-resetting daily).
  - Weekly Revenue (last 7 days rolling aggregation).
  - Monthly Revenue (last 30 days rolling turnover).
  - Total Lifetime Bills Count.
  - Total Active Catalog Products.
  - Critical Stock Alert Count with direct-link shortcuts.
- **Interactive Chart.js Visualizations**:
  - **Multi-Horizon Gross Turnover Bar Chart**: Switchable between Daily (14-day history), Weekly (8-week rolling), and Monthly (12-month trend).
  - **Category Turnover Distribution Doughnut Chart**: Visualizes sales share across the 7 product categories.
  - **Top Performing Revenue Generators**: Lists top revenue-driving SKUs.
