# Specification: Lubricant Pricing Studio

This document defines the features, specifications, and architecture of the **Lubricant Pricing Studio** codebase. The app serves as a real-time price calculator, CRM pipeline tracker, and coordination tool between Production and Sales teams.

---

## 1. User Stories

### Administrator
* **US-1 (User Management)**: As an Admin, I want to invite users by creating accounts and assigning them to either the "Sales" or "Production" role group, so that their access permissions are correct.
* **US-2 (Account Termination)**: As an Admin, I want to remove user accounts from the workspace.

### Production Team
* **US-3 (Master Catalog CRUD)**: As a Production member, I want to add, edit, and delete products in the master catalog (including SKU code, sub-brand name, viscosity, specification, and approvals).
* **US-4 (Cost Management)**: As a Production member, I want to search for a product and update its base production cost and profit margin, so that the customer-facing selling price updates automatically.
* **US-5 (Bulk Import)**: As a Production member, I want to upload an Excel spreadsheet (.xlsx/csv) to bulk import master product listings and price configurations.
* **US-6 (Audit Trail)**: As a Production member, I want to view a history log of all catalog adjustments and price changes (including who made the change, the field modified, the old value, and the new value).

### Sales Team
* **US-7 (Product Lookup)**: As a Sales member, I want to search the catalog in real-time by code or specification to check active costs and selling prices.
* **US-8 (CRM Pipeline)**: As a Sales member, I want to track customer leads using a visual Kanban board and drag opportunities through the lifecycle stages (New, Qualified, Proposition, Won).
* **US-9 (Document Generation)**: As a Sales member, I want to generate clean, professional Sales Quotations and Proforma Invoice PDFs directly from my leads to send to customers.
* **US-10 (Inquiry Dispatch)**: As a Sales member, I want to send inquires (requests for new product codes or specifications) directly to the Production team from the dashboard.

---

## 2. Functional Requirements

### 2.1 Role-Based Access Control (RBAC)
* **FR-1**: Only logged-in users can access the application (enforced via `@login_required`).
* **FR-2**: Role segregation must restrict views:
  * **Production Pages** (`/products/`, `/pricing/`, `/import/`, `/history/`, `/export/`) are accessible only to the Admin and users in the `Production` group.
  * **Sales Pages** (`/crm/`, `/documents/...`, `/quotation/create/`) are accessible only to the Admin and users in the `Sales` group.
* **FR-3**: Unauthorized page requests must gracefully redirect the user to the landing URL (`/`), which dynamically routes them to their corresponding role dashboard.

### 2.2 Cost & Selling Price Calculation Logic
* **FR-4**: Calculated product pricing formulas must compute:
  * **Pack Capacity Multiplier**: The capacity is derived from the packaging description (e.g. `12x1` = 12L, `4x4` = 16L, `4x5` = 20L, `20` = 20L, `208` = 208L).
  * **Final Cost** = `(Base Production Cost per Liter * Pack Capacity Multiplier) + Packaging Value`.
  * **Selling Price** = `Final Cost * 1.20` (reflecting a standard 20% markup).

### 2.3 CRM Kanban Board & Document Generation
* **FR-5**: Leads in the CRM dashboard must track Opportunity Name, Client Contact Details, and Target Revenue.
* **FR-6**: The Kanban board must support draggable columns mapping stages: `New`, `Qualified`, `Proposition`, and `Won`. Moving cards updates the database stage fields via async requests.
* **FR-7**: PDF documents (Sales Quotation and Proforma Invoice) must render company branding, client specifications, item pricing details, and date validations.

### 2.4 Excel Parser & Importer
* **FR-8**: The Excel importer must parse rows containing columns: `sku`, `name`, `quantity`, `production_price`, and `profit_percent`.
* **FR-9**: The parser must log detailed data validation summaries (indicating missing fields or corrupt numeric cells) and skip rows that are exact duplicates.

---

## 3. Non-Functional Requirements

### 3.1 Technology Stack & Performance
* **Backend**: Python + Django (v5+), utilizing Django ORM for relational queries.
* **Database**: SQLite (for local development and testing) / PostgreSQL (for production/Render deployments).
* **Frontend**: Responsive, modern user interface utilizing Vanilla HTML5, CSS3 styling variables, and lightweight JavaScript interactions.
* **Security**: CSRF tokens enabled on all form operations, Django session authentication, and parameterized query execution to block SQL injection.
