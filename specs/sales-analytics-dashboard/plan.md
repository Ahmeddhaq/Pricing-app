# Technical Implementation Plan: Sales Analytics Dashboard

This plan outlines the model updates, backend calculations, URL routing, and Chart.js integration to build the new Sales Analytics Dashboard page ([templates/crm_analytics.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/crm_analytics.html)).

---

## 1. Architecture Overview & Tech Stack Decisions

To support dynamic charts with high performance and visual fidelity:
* **Frontend Chart Rendering**: Use **Chart.js** (loaded via CDN) inside the browser. Chart.js is lightweight, highly customizable, responsive, and fits within the Orange & White design system.
* **Backend Computations**: All aggregation, grouping, and arithmetic will be executed on the backend in a Django view using Django ORM aggregation functions (`Sum`, `Avg`, `Count`) and timezone-aware dates.
* **Data Transfer**: The dashboard view will render the HTML template, embedding the computed metrics and historical arrays as a JSON payload inside a script tag (`id="analytics-data"`). This eliminates the need for a separate API roundtrip, loading the page and charts in a single render.

---

## 2. Database Schema & Migration Plan

We will add three fields to the `Lead` model in [core/models.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/models.py):
* `product` (ForeignKey to Product, nullable)
* `quantity` (DecimalField, default=0.00)
* `won_at` (DateTimeField, nullable)

### 2.1 Model Transition Trigger
We will override `Lead.save()` to capture transitions into the `"Won"` stage:
```python
def save(self, *args, **kwargs):
    if self.stage == 'Won':
        if not self.won_at:
            self.won_at = timezone.now()
    else:
        self.won_at = None
    super().save(*args, **kwargs)
```

### 2.2 Schema Migrations
We will run terminal commands to generate and apply migrations:
```bash
python manage.py makemigrations core
python manage.py migrate core
```

---

## 3. API Context & Data Contract

The view `views.crm_analytics` will calculate the JSON payload passed to the frontend:

```json
{
  "monthly_revenue": [
    {"month": "Jul 2025", "revenue": 125000.00},
    {"month": "Aug 2025", "revenue": 95000.00}
  ],
  "win_rates": [
    {"name": "Arshad al Haq", "win_rate": 75.00},
    {"name": "Sales Rep A", "win_rate": 60.50}
  ],
  "top_products": [
    {"product": "1182001 - BAROX ULTRA 0W16", "quantity": 420.00},
    {"product": "1101001 - Barox ULTRA", "quantity": 380.00}
  ],
  "funnel": {
    "New": 15,
    "Qualified": 10,
    "Proposition": 6,
    "Won": 4,
    "dropoffs": {
      "New_to_Qualified": 33.3,
      "Qualified_to_Proposition": 40.0,
      "Proposition_to_Won": 33.3
    }
  },
  "deal_sizes": [
    {"month": "Jan 2026", "avg_deal_size": 42000.00},
    {"month": "Feb 2026", "avg_deal_size": 48500.00}
  ],
  "stale_leads_count": 6
}
```

---

## 4. Frontend Grid & Script Integration

### 4.1 Responsive HTML Layout
The dashboard template `crm_analytics.html` will inherit from `base.html` and define four rows matching the layout specs:

```html
<!-- Stale Leads Alert -->
<div id="stale-leads-alert" class="alert-box-danger" style="display: none;">
  ⚠️ WARNING: You have <strong id="alert-stale-count">0</strong> stale leads that haven't been updated for over 30 days. Please take action!
</div>

<!-- Row 1: KPI metrics -->
<div class="crm-metrics-grid">
  <!-- Total Pipeline, Win Rate %, Stale Leads Cards -->
</div>

<!-- Row 2: Monthly Revenue + Win Rates -->
<div class="grid-two">
  <div class="panel-card"><canvas id="chart-monthly-revenue"></canvas></div>
  <div class="panel-card"><canvas id="chart-win-rates"></canvas></div>
</div>

<!-- Row 3: Top Products + Funnel -->
<div class="grid-two">
  <div class="panel-card"><canvas id="chart-top-products"></canvas></div>
  <div class="panel-card"><canvas id="chart-funnel"></canvas></div>
</div>

<!-- Row 4: Deal Size trend -->
<div class="panel-card">
  <canvas id="chart-deal-size"></canvas>
</div>
```

### 4.2 Script Initialization
We will load Chart.js and parse the JSON string:
```javascript
const data = JSON.parse(document.getElementById('analytics-data').textContent);

// Set alert state
if (data.stale_leads_count > 5) {
    document.getElementById('alert-stale-count').textContent = data.stale_leads_count;
    document.getElementById('stale-leads-alert').style.display = 'block';
}
```
Chart visual configurations (border colors, fills, hover markers) will use the brand accent orange color (`#ff8f5d` or `var(--accent)`).
