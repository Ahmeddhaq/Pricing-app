# Project Context

## What This Project Does
The Lubricant Pricing Studio is a Django-based collaborative platform designed to coordinate product pricing and sales workflows. It acts as a central control center where the Production team maintains the master product database and updates manufacturing costs/margins, while the Sales team utilizes the pricing matrix to manage customer pipelines, track leads via a CRM Kanban board, and generate official quotation and proforma invoice PDFs.

## Key Features
- **Role-Based Workspaces**: Segregated dashboards and access levels tailored for Sales (CRM pipeline, client lookups) and Production (cost updates, bulk catalog imports) with Admin control.
- **Dynamic Price Worksheet**: Automatically calculates packaged product selling prices using formulas mapped to production base costs per liter, packaging multipliers, and profit margins.
- **CRM & Document Generation**: Built-in lead tracking system with draggable Kanban pipeline and automated PDF generation for Sales Quotations and Proforma Invoices.
- **Data Import/Export**: Bulk product updates using Excel spreadsheet uploads (.xlsx) with verification logs.

## Tech Stack
- Frontend: HTML5, CSS3 (Vanilla), Vanilla JavaScript
- Backend: Python + Django
- Database: SQLite (local development) / PostgreSQL (production deployment)
