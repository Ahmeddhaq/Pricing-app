# Specification: Security and Code Quality Fixes

This specification details the implementation criteria for resolving the security, performance, and code cleanliness issues identified in the [Security Audit Report](file:///home/ahmedhaq/Work/Pricing-app-master/specs/audit/report.md).

---

## 1. User Stories

* **US-1 (Password Complexity)**: As an Admin, I want the system to enforce password complexity checks during user registration so that accounts are protected from simple dictionary attacks.
* **US-2 (Performance Optimization)**: As a User, I want search queries and dashboard loads to be as fast as possible, requiring the backend to avoid querying unnecessary database records and use indexing for quick lookups.
* **US-3 (Code Cleanliness)**: As a Developer, I want the codebase to be free of dead views, URLs, and template files so that maintenance is straightforward.

---

## 2. Functional Requirements

### 2.1 Security Hardening (`pricing_app/settings.py`)
* **FR-1 (Password Validation)**: Enable standard Django complexity validators (similarity, length, common, numeric) when not in local `DEBUG` mode.
* **FR-2 (Host Verification)**: Restrict `ALLOWED_HOSTS` in production to specific subdomains (`.onrender.com` and `.render.com`).
* **FR-3 (Strict Secret Key)**: Ensure `SECRET_KEY` raises a `KeyError` if the environment variable `DJANGO_SECRET_KEY` is missing in production (no unsafe fallback string).
* **FR-4 (Secure Cookies)**: Enable `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, and `SESSION_COOKIE_SAMESITE = 'Lax'` in production environments.

### 2.2 Performance Optimizations
* **FR-5 (Unused Query Removal)**: Remove the redundant query calling `Product.objects.all().order_by('sku')` from the `sales_dashboard` view in [views.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/views.py).
* **FR-6 (Database Indexing)**: Add `db_index=True` configuration to:
  * `MasterProduct.code` in [models.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/models.py)
  * `Product.sku` in [models.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/models.py)
  * Generate and execute the resulting database migrations.

### 2.3 Dead Code & Workspace Cleanup
* **FR-7 (Template Removal)**: Delete the unused template file [product_form.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/product_form.html).
* **FR-8 (View & URL Clean-up)**: Remove view functions `product_create`, `product_edit`, and `price_update` from [views.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/views.py) and their corresponding URLs from [urls.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/urls.py).
* **FR-9 (Outdated Comment Clean-up)**: Correct the outdated comment on the `import_apply` view function.
* **FR-10 (Requirements Alignment)**: Update [requirements.txt](file:///home/ahmedhaq/Work/Pricing-app-master/requirements.txt) to specify `Django>=6.0.6` to reflect the active virtual environment version.

---

## 3. Non-Functional Requirements

* **NFR-1 (Compatibility)**: All functional logic in other modules (dashboard, imports, permissions) must remain untouched and fully operational.
* **NFR-2 (Testing)**: The existing test suite must be updated if any URLs are removed, and all tests must pass with zero failures.
