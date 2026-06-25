# Technical Implementation Plan: Global Design System Upgrade

This plan outlines the technical design, architectural details, and specific stylesheet adjustments required to implement a unified, premium design system (pure white backgrounds, orange accents, clean sans-serif typography) across the entire Lubricant Pricing application.

---

## 1. Architecture Overview & Tech Stack Decisions

To maintain performance, simplicity, and cross-browser reliability, we will upgrade the visual layer using a pure **Vanilla CSS Custom Properties** (Variables) architecture.

* **Style Synchronization**: All files will inherit design variables from `:root` in [core/static/core/styles.css](file:///home/ahmedhaq/Work/Pricing-app-master/core/static/core/styles.css).
* **Typography**: Replace standard system sans-serif fonts with the premium Google Font family **Plus Jakarta Sans**, imported via [templates/base.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/base.html).
* **Grid & Layout Shell**: Standardize all containers to follow a consistent padding, margin, border-radius, and border structure.
* **Component Encapsulation**: Restructure standard dashboard pages (Products, Pricing, History, CRM) to inherit design tokens dynamically rather than utilizing inline style overrides.

---

## 2. API Contracts & Database Schema

### Database Schema
No database schema changes are required for this visual redesign.

### API Contracts
No backend HTTP API contract changes are required.

---

## 3. Style Tokens Definition (CSS Variables)

We will modify `:root` variables in `styles.css` to restrict the app's colors strictly to the White background, Orange accent, and status indicators:

```css
:root {
  color-scheme: light;
  
  /* Brand Accents */
  --accent: #ff8f5d;            /* Coral Orange accent */
  --accent-strong: #e76f41;     /* Active/Hover orange */
  --accent-soft: rgba(255, 143, 93, 0.08); /* Transparent tint */

  /* Neutral Backgrounds */
  --bg: #ffffff;                 /* Clean white page background */
  --bg-elevated: #ffffff;        /* Panel / modal sheets */
  --surface: #ffffff;           /* Table / Card sheets */
  --surface-strong: #fcfcfc;     /* Subtle light shading */
  --line: #e5e7eb;               /* Neutral light border grey */

  /* Typographic Colors */
  --text: #171717;               /* Crisp dark charcoal for reading */
  --muted: #737373;              /* Secondary gray metadata */

  /* Status Colors (Exempt from Orange/White rule) */
  --status-success: #10b981;     /* Won leads / green alerts */
  --status-warning: #f59e0b;     /* In-progress / yellow alerts */
  --status-danger: #ef4444;      /* Lost leads / delete buttons */

  /* Shadows & Radius */
  --shadow: 0 10px 30px rgba(0, 0, 0, 0.03), 0 1px 3px rgba(0, 0, 0, 0.02);
  --radius-xl: 16px;
  --radius-lg: 12px;
  --radius-md: 8px;
}
```

---

## 4. Implementation Steps by File

### 4.1 Update base.html
* Link Google Font family `Plus Jakarta Sans` with font weights `400, 500, 600, 700, 800`.
* Strip out background ambient spots: `.ambient`, `.ambient-a`, `.ambient-b`.
* Standardize header element styles and search bar forms.
* Set the sidebar drawer to a solid `#ffffff` background with `1px solid var(--line)` right border.

### 4.2 Restructure styles.css
* Update variables block in `:root`.
* Replace `html, body` background logic to remove multi-colored linear-gradients and dots patterns, setting it to solid `var(--bg)` (`#ffffff`).
* Re-style links, headers (`h1`, `h2`, `h3`), and navigation cards to inherit tokens.
* Re-style buttons:
  * `.primary-button`: solid orange background, white text.
  * `.ghost-button`: white background, thin orange border, orange text.
* Re-style tables to remove colored backdrops and define subtle horizontal dividing lines.
* Re-style forms and active inputs focus rings.

### 4.3 Clean Up Template Styling Override Code
* Inspect `dashboard.html`, `sales_dashboard.html`, `products.html`, `pricing.html`, and `invite_people.html`.
* Remove all inline overrides that hardcode non-conforming background colors or values (like yellow cost tags, grey cards, or dark buttons), replacing them with standard variables like `var(--accent-soft)`, `var(--status-success)`, and `var(--line)`.
