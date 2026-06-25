# Technical Implementation Plan: Lubricant Pricing Studio

This document maps the architectural decisions, database models, view configurations, and template permissions implementing the **Lubricant Pricing Studio** application.

---

## 1. Tech Stack & Infrastructure

* **Language/Framework**: Python + Django.
* **Database**:
  * Local: SQLite (`db.sqlite3`).
  * Production: PostgreSQL (connected via Render database environment strings).
* **WSGI Server**: Gunicorn.
* **Static Files**: Whitenoise for serving static files efficiently in production.
* **Templates**: Django Template Engine with context processors for role-checking.

---

## 2. Database Models (Relational Schema)

Below are the core models defined in [core/models.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/models.py):

### 2.1 Catalog & Pricing Tables
* **`MasterProduct`**: Definitions of product categories.
  * Fields: `code` (char), `description` (char), `viscosity` (char), `specification` (text), `approval` (text), `packaging` (char), `liters_per_case` (decimal).
* **`Product`**: Price-tracked entries.
  * Fields: `sku` (char), `name` (char), `master` (FK to `MasterProduct`), `quantity` (decimal), `production_price` (decimal), `profit_percent` (decimal), `selling_price` (decimal - automatically calculated via model save override), `updated_by` (FK to User), `effective_date` (date).
* **`Pricing`**: Pack pricing rule inputs.
  * Fields: `product` (FK to `MasterProduct`), `packaging` (char), `production_cost_per_liter` (decimal), `quantity` (decimal), `discount` (decimal), `final_cost` (decimal), `selling_price` (decimal), `price` (decimal), `created_at` (datetime).

### 2.2 CRM & Documents Tables
* **`Lead`**: Sales pipeline entries.
  * Fields: `opportunity_name` (char), `contact_name` (char), `contact_email` (char), `contact_phone` (char), `revenue` (decimal), `stage` (choice: `New`, `Qualified`, `Proposition`, `Won`), `salesperson` (FK to User), `created_at` (datetime).
* **`Quotation`**: Sales quotation tracker.
  * Fields: `product` (FK to `Product`), `salesperson` (FK to User), `customer_name` (char), `quantity` (decimal), `discount_percent` (decimal), `created_at` (datetime).

### 2.3 Operations & Audit Logs
* **`ProductChange`**: Tracks audit logs of pricing updates.
  * Fields: `product` (FK to `Product`), `changed_by` (FK to User), `field_name` (char), `old_value` (char), `new_value` (char), `created_at` (datetime).
* **`ImportFile` / `ExportFile`**: Tracking spreadsheet uploads/downloads.
* **`Notification`**: System alerts.

---

## 3. URLs & Routing Structure

Django routes are defined in `pricing_app/urls.py` and `core/urls.py`:

* `/` ── maps to `views.dashboard`
  * Automatically inspects requests: redirects users belonging to the `Sales` group (or Admin) to `sales_dashboard` and users belonging to the `Production` group to `production_dashboard`.
* `/products/` ── maps to `views.products_list` (Catalog database, read-only for Sales, write-access for Production/Admin).
* `/pricing/` ── maps to `views.pricing_list` (Price calculations, restricted to Production/Admin).
* `/crm/` ── maps to `views.crm_dashboard` (Kanban board, restricted to Sales/Admin).
* `/invite/` ── maps to `views.invite_people` (Admin-only page to create users and assign roles).
* `/import/` / `/export/` ── maps to `views.import_upload` and `views.export_dashboard` (Spreadsheet operations, restricted to Production/Admin).

---

## 4. UI Permissions & Security

### 4.1 Custom Context Processor
* We use a context processor `core.context_processors.role_check` to inject role flags (`is_admin`, `is_sales`, `is_production`) into every rendered context.
* This is used in [templates/base.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/base.html) to hide or expose navigation tabs.

### 4.2 View Level Decorators & Redirects
* Views are wrapped with `@login_required`.
* Operations views execute checks at startup:
  ```python
  if not is_production(request.user):
      return redirect('dashboard')
  ```
  This prevents brute-force URL manipulation.
