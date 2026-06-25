# Specification: Sales Analytics Dashboard

This specification defines the features, data structure, and layout requirements for a new **Sales Analytics Dashboard** ([templates/crm_analytics.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/crm_analytics.html)) in the CRM module to track sales metrics, deal sizes, win rates, and product sales.

---

## 1. Goal & Context

To improve sales team productivity, administrators and sales managers need a cohesive view of pipeline performance. The current CRM system lists leads in a Kanban board but lacks reporting, trends, and aggregate metrics.

This feature adds a Sales Analytics Dashboard that calculates performance metrics directly on the backend using Django ORM and renders them as premium, responsive charts using **Chart.js**.

---

## 2. User Stories

### Sales Administrator & Sales salesperson
* **US-1 (Revenue Performance Tracking)**: As a Sales salesperson, I want to view my monthly won revenue trended over the last 12 months in a line chart, so that I can monitor my performance against quotas.
* **US-2 (Win Rate Comparison)**: As an Admin, I want to compare the win rate percentages of all sales reps in a bar chart to identify top performers and coaching opportunities.
* **US-3 (Product Demand Analysis)**: As a Sales manager, I want to see the top 10 products sold by volume/revenue in a pie chart to understand which lubricants are in highest demand.
* **US-4 (Funnel Analysis)**: As a Sales salesperson, I want to view the lead conversion funnel count and drop-off rate between stages, helping me optimize my follow-ups.
* **US-5 (Deal Size Trend)**: As an Admin, I want to track the average deal size trend over the last 6 months to evaluate pricing strategy shifts.
* **US-6 (Stale Leads Risk Monitoring)**: As a Sales rep, I want to be alerted with a prominent red alert box when there are more than 5 stale leads, prompting me to take action on neglected opportunities.

---

## 3. Database Schema Modifications

To support accurate chronological and product-specific reporting, we will upgrade the `Lead` model:

### 3.1 Model Changes: `Lead`
We will add three optional fields to the `Lead` model in [core/models.py](file:///home/ahmedhaq/Work/Pricing-app-master/core/models.py):
* `product`: `ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="leads")`
  * Links a pipeline opportunity to a specific product record.
* `quantity`: `DecimalField(max_digits=12, decimal_places=2, default=0)`
  * Tracks the unit volume of the opportunity.
* `won_at`: `DateTimeField(null=True, blank=True)`
  * Stores the exact timestamp when a lead's stage was set to `Won`.
  * **Auto-population logic**: Inside `Lead.save()`, if the stage is set to `Won` and `won_at` is null, set `won_at` to the current timestamp (`timezone.now()`). If the stage is changed away from `Won`, reset `won_at` to `None`.

---

## 4. Functional Requirements

### 4.1 Backend Aggregation & Analytics Views (Django View)
An analytics endpoint (mapping to route `/crm/analytics/`) will perform calculations on the server side:

1. **Monthly Won Revenue (12-Month Trend)**:
   * Query leads where `stage = 'Won'` and `won_at` falls in the last 12 months.
   * Group by month/year and sum the `revenue` field.
   * Return an ordered array of monthly totals.
2. **Sales Rep Win Rate**:
   * Get all active users belonging to the `Sales` group or having admin access.
   * For each salesperson, calculate:
     $$\text{Win Rate \%} = \left( \frac{\text{Leads where stage = 'Won'}}{\text{Total Assigned Leads}} \right) \times 100$$
   * Exclude users with 0 assigned leads. Return names and win rate percentages.
3. **Top 10 Products Sold**:
   * Sum the quantities of products associated with:
     * Leads where `stage = 'Won'`.
     * Active `Quotation` records.
   * Group by `Product SKU` + `Product Name`.
   * Order descending and return the top 10 items.
4. **Lead Conversion Funnel**:
   * Count leads in each stage: `New`, `Qualified`, `Proposition`, `Won`.
   * Calculate conversion drop-off percentage between consecutive stages.
5. **Average Deal Size Trend (6-Month Trend)**:
   * Query leads where `stage = 'Won'` and `won_at` is in the last 6 months.
   * Group by month/year and calculate:
     $$\text{Average Deal Size} = \text{Average(revenue)}$$
6. **Stale Leads Alert Calculation**:
   * Count leads where `stage` is neither `Won` nor `Lost` (or other closing stages) AND `updated_at` is older than 30 days.

---

### 4.2 Dashboard Layout & Chart.js Rendering

#### KPI Metrics Grid (Top Row)
* **Total Pipeline Value**: Sum of `revenue` for all active open leads (`New`, `Qualified`, `Proposition`).
* **Global Win Rate**: (Total Won Leads / Total Leads) * 100.
* **Stale Leads Count**: Calculated stale lead metric. If count > 5, render a prominent Red Alert block at the very top.

#### Charts Structure
* **Row 2**:
  * Left: Monthly Won Revenue (Line chart, smooth curves, orange accent color fill).
  * Right: Win Rate by Sales Rep (Bar chart, vertical bars).
* **Row 3**:
  * Left: Top 10 Products Sold (Pie or Doughnut chart).
  * Right: Lead Conversion Funnel (Horizontal bar chart or custom CSS/JS funnel blocks).
* **Row 4**:
  * Average Deal Size Trend (Line or Bar chart showing monthly averages).

---

## 5. Non-Functional Requirements

* **No Dummy Data**: All charts must load empty states if there is no database record, rather than fall back to static fake data.
* **Security & Access Control**: Access must be restricted to users in the `Sales` group or Admins.
* **Responsive Charts**: Ensure Chart.js containers have `responsive: true` and `maintainAspectRatio: false` configured, styling them cleanly across mobile and desktop.
