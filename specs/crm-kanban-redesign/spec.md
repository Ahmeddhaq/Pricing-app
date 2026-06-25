# Specification: CRM Kanban Dashboard Redesign & Optimization

This specification outlines the redesign and optimization of the CRM Sales Pipeline dashboard ([templates/crm_dashboard.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/crm_dashboard.html)) to create an interactive, visually stunning, and highly productive workspace for the Sales team.

---

## 1. Goal & Context

The current CRM Sales Pipeline dashboard has several user experience and visual limitations:
* **Disruptive Full-Page Reloads**: Moving a card from one stage to another or editing a lead submits a POST request that reloads the entire page, causing delays and breaking user flow.
* **Lack of Insights**: No pipeline aggregation exists. Sales agents cannot see the total value of opportunities at a glance, either globally or per-stage.
* **Basic Styling**: The design uses flat CSS values and lacks depth, visual cues, and empty states. Drop targets have no hover/active states.
* **No Search or Filtering**: Managing a growing volume of leads is difficult without live search or filtering.
* **Basic Actions**: Moving cards requires dragging, which is difficult on tablets or mobile devices.

The goal is to redesign the layout, styles, and Javascript code to turn this board into a professional, fluid dashboard that enhances productivity.

---

## 2. User Stories

### Sales salesperson
* **US-1 (Fluid Drag-and-Drop)**: As a Sales salesperson, I want to drag opportunity cards between stages and see changes applied immediately in the background without refreshing the page, keeping my focus sharp.
* **US-2 (Pipeline Statistics)**: As a Sales salesperson, I want to see a KPI header showing total pipeline metrics and column-specific revenue aggregates so that I know exactly how much value is in each part of my funnel.
* **US-3 (Fuzzy Live Search)**: As a Sales salesperson, I want to search and filter leads by name, email, or stage in real-time to find specific opportunities instantly.
* **US-4 (Click-to-Move Actions)**: As a Sales salesperson, I want a menu option to move cards to other columns via simple clicks so that I can easily update opportunities on my mobile device or tablet.
* **US-5 (Premium Aesthetic & Feedback)**: As a Sales salesperson, I want the board to use a professional color palette, clean typography, drop-zone highlights, and smooth micro-animations.

---

## 3. Functional Requirements

### 3.1 Pipeline Metrics Header
* **FR-1**: Add a KPI overview section at the top of the CRM dashboard containing:
  * **Total Pipeline Value**: Combined revenue of all active opportunities (`New` + `Qualified` + `Proposition` stages).
  * **Won Deals Value**: Combined revenue of opportunities in the `Won` stage.
  * **Active Leads**: Count of opportunities currently active in the pipeline.
  * **Conversion Rate**: Percentage of total opportunities that have reached the `Won` stage.
* **FR-2**: Metrics must update dynamically via JavaScript when cards are moved, added, or deleted, without page reloads.

### 3.2 Column Headers & Aggregates
* **FR-3**: Display the count of leads and the total revenue sum for that column within the header (e.g., `Qualified (3) • AED 125,000.00`).
* **FR-4**: Style column status tags with unique color codes to establish clear visual hierarchy:
  * **New**: Indigo/Blue (e.g., `#3b82f6` tag / `#eff6ff` background)
  * **Qualified**: Amber/Orange (e.g., `#f59e0b` tag / `#fef3c7` background)
  * **Proposition**: Violet/Purple (e.g., `#8b5cf6` tag / `#f5f3ff` background)
  * **Won**: Emerald/Green (e.g., `#10b981` tag / `#ecfdf5` background)

### 3.3 Dynamic Background Updates (AJAX Drag-and-Drop)
* **FR-5**: Modify the drop handler to make a background `fetch()` POST request to `/crm/lead/<id>/update/` containing the updated stage.
* **FR-6**: Implement drop-zone visual feedback:
  * Highlight the active column outline and background when dragging a card over it.
  * Show a dashed placeholder where the card will land.
* **FR-7**: Dynamically update column counts, column revenue totals, and header KPIs on card drop.
* **FR-8**: Handle failures gracefully: if the AJAX request fails, revert the card to its original column and display an error notification toast.

### 3.4 Client-Side Live Search & Filtering
* **FR-9**: Place a search input bar in the dashboard actions header.
* **FR-10**: Filter cards in real-time as the user types, checking for fuzzy matches in `Opportunity Name`, `Contact Name`, `Email`, and `Phone`.
* **FR-11**: Show empty states with dashed borders, descriptive icons, and helpful text when a column has zero cards or when no leads match the search queries.

### 3.5 Action Menus & Mobile Compatibility
* **FR-12**: Re-style the kebab action menu (`⋮`) on cards to use absolute positioning, preventing the menu from getting clipped by column boundaries.
* **FR-13**: Add a "Move to Stage..." submenu with options for `New`, `Qualified`, `Proposition`, and `Won` to support touch/mobile click interactions.
* **FR-14**: Keep buttons to generate Quotation (`/documents/lead-quotation/<id>/`) and Proforma (`/documents/lead-proforma/<id>/`) PDFs.

### 3.6 Premium Modals & Forms
* **FR-15**: Redesign the Add and Edit modals:
  * Add backdrop filters (`backdrop-filter: blur(8px)`) and scale transitions (`transform: scale(0.95)` to `scale(1)`).
  * Use clean, modern inputs with outline focus rings.
  * Form submissions for adding or editing can use AJAX (optionally) or standard redirects with animations.

---

## 4. Non-Functional Requirements

* **Performance & Fluidity**: Keep animations at 60 FPS using GPU-accelerated CSS properties (`transform`, `opacity`). Page must load instantly without layout shifting (CLS).
* **Security**: Include the Django CSRF token in the headers of all background requests (`X-CSRFToken`).
* **Responsiveness**: Ensure the Kanban board scroll layout is optimized for desktop, tablet, and mobile views. Use standard styling variables defined in `styles.css`.
