# Technical Implementation Plan: Security & Quality Fixes

This plan outlines the changes to resolve the identified security risks, remove dead code, and optimize database lookup queries.

---

## 1. Database Schema Changes

We will add indexing to the heavily queried lookup columns `code` and `sku`:

#### [MODIFY] [models.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/models.py)
* Add `db_index=True` to `MasterProduct.code`
* Add `db_index=True` to `Product.sku`

#### [NEW] [Migration file](file:///home/ahmedhaq/Work/Pricing-app-master/core/migrations/)
* Run `python manage.py makemigrations core` to generate the migration file adding the database indexes.
* Run `python manage.py migrate` to apply the index modifications.

---

## 2. API & View Clean-up

We will remove the dead views, URLs, and correct query performance:

#### [MODIFY] [urls.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/urls.py)
* Remove the following URL paths:
  * `products/new/`
  * `products/<int:pk>/edit/`
  * `products/<int:pk>/price/`

#### [MODIFY] [views.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/views.py)
* Remove functions:
  * `product_create(request)`
  * `product_edit(request, pk)`
  * `price_update(request, pk)`
* Under `sales_dashboard` view:
  * Delete line 138: `products = Product.objects.all().order_by('sku')` and remove it from the returned context.
* Under `import_apply` view:
  * Update the comment `Allow anonymous application; updated_by set to None if anonymous` to accurately state that authorization is required.

#### [DELETE] [product_form.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/product_form.html)
* Delete the template file completely.

---

## 3. Settings Hardening

#### [MODIFY] [settings.py](file:///home/ahmedhaq/Work/Pricing-app-master/pricing_app/settings.py)
* **Secret Key**: Check if `DJANGO_SECRET_KEY` is set. In production (`not DEBUG`), raise a `KeyError` if it is missing.
* **Hosts Security**: If `not DEBUG`, limit `ALLOWED_HOSTS` to specific Render domains: `['.onrender.com', '.render.com']`.
* **Password Validation**: Restore default password checkers if `not DEBUG`.
* **Cookie Flags**: If `not DEBUG`, add the following security properties:
  * `SESSION_COOKIE_SECURE = True`
  * `CSRF_COOKIE_SECURE = True`
  * `SESSION_COOKIE_HTTPONLY = True`
  * `SESSION_COOKIE_SAMESITE = 'Lax'`

---

## 4. Requirements update

#### [MODIFY] [requirements.txt](file:///home/ahmedhaq/Work/Pricing-app-master/requirements.txt)
* Change `Django>=4.2,<5.0` to `Django>=6.0.6` to keep package constraints aligned with the environment.

---

## 5. Verification Plan

### Automated Tests
* Run `python manage.py test` to verify.
