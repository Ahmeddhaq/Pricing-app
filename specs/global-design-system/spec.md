# Specification: Global Design System Upgrade

This document specifies a comprehensive, premium design system for the entire application. The goal is to establish a unified visual language with a clean, modern aesthetic using a restricted color palette (Orange and White) and clean sans-serif typography.

---

## 1. Goal & Context

The current application UI uses a mix of blue ambient gradients, multi-colored highlights, and variable spacing patterns that look inconsistent across pages. 

This specification defines a global CSS design token framework and component standard to align all views (Main Dashboard, Products List, Pricing, CRM Kanban, Invite Users, and Account Settings) under a single cohesive theme:
* **Backgrounds**: Pure white (`#FFFFFF`) with subtle light-neutral block shading.
* **Accents**: Premium Orange (`#ff8f5d` or similar) for interactions, primary actions, highlights, and navigation focus.
* **Status Indicators Only**: Green for success/won, Red for danger/lost, Yellow/Amber for warning/in-progress. No other primary/secondary colors are allowed.
* **Typography**: Highly legible, premium sans-serif typography.
* **Consistency**: Shared cards, tables, menus, headers, and navigation states across the app.

---

## 2. User Stories

### All Users
* **US-1 (Premium Visual Identity)**: As a user, I want the application to have a clean, light, and cohesive visual theme (White background, Orange accent) so that it feels like a professional, premium enterprise tool.
* **US-2 (Legibility & Reading Flow)**: As a user, I want a clean, modern sans-serif font with uniform sizes and hierarchies so that data tables, prices, and CRM stages are easy to read.
* **US-3 (Consistency Across Pages)**: As a user, I want to experience the exact same navigation layout, borders, buttons, and card patterns on every page I open.
* **US-4 (Responsive Adaptability)**: As a user, I want the entire layout to adjust smoothly when viewing on desktops, laptops, tablets, or mobile screens, keeping interactive elements easily accessible.
* **US-5 (Interactive Feedback)**: As a user, I want subtle, high-quality hover animations and focus outlines using the orange accent so that I know what elements I am interacting with.

---

## 3. Functional Requirements

### 3.1 Design System Color Tokens (CSS Variables)
* **FR-1**: Declare all brand, layout, and text styles in a central `:root` block in [styles.css](file:///home/ahmedhaq/Work/Pricing-app-master/core/static/core/styles.css):
  * **Brand Colors**:
    * `--accent`: `#ff8f5d` (Primary brand orange)
    * `--accent-strong`: `#e76f41` (Hover state orange)
    * `--accent-soft`: `rgba(255, 143, 93, 0.08)` (Subtle highlight orange)
  * **Layout Colors**:
    * `--bg`: `#ffffff` (Primary app background)
    * `--bg-elevated`: `#ffffff` (Elevated cards/panels)
    * `--surface`: `#ffffff` (Card background sheets)
    * `--surface-strong`: `#fcfcfc` (Alternative subtle gray-white layout block)
    * `--line`: `#e5e7eb` (Clean border gray - Tailwind neutral-200 equivalent)
  * **Text Colors**:
    * `--text`: `#171717` (Deep dark gray/charcoal for reading)
    * `--muted`: `#737373` (Neutral gray for metadata and captions)
  * **Borders & Corners**:
    * `--radius-xl`: `16px` (For main panels, large components)
    * `--radius-lg`: `12px` (For metric cards, columns, modals)
    * `--radius-md`: `8px` (For input boxes, smaller tags)
* **FR-2**: Status colors must be used *exclusively* for pipeline stages or warnings:
  * `--status-success`: `#10b981` (Green for "Won" or success states)
  * `--status-warning`: `#f59e0b` (Yellow/Amber for in-progress / qualified states)
  * `--status-danger`: `#ef4444` (Red for deletions or lost states)
* **FR-3**: Suppress all other background color blobs, multi-color ambient spots (`.ambient-a`, `.ambient-b`), and complex blue background gradients.

### 3.2 Typography Rules
* **FR-4**: Use standard Google Fonts import for a premium sans-serif family (e.g. `Plus Jakarta Sans` or `Inter`) in [base.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/base.html).
* **FR-5**: Clean up heading sizes to establish clear typographic rhythm:
  * Headers `h1`, `h2`, `h3` must be crisp, have a bold weight (700+), and utilize tight letter-spacing (`-0.03em`).
  * Body copy must use `--text` with a comfortable font-size (`0.9rem` - `0.95rem`) and line-height (`1.6`).

### 3.3 Components Design System
* **FR-6 (App Sidebar Shell)**:
  * Background is pure white with a vertical right border (`1px solid var(--line)`).
  * Brand Mark: Re-style logo box with a solid orange background (`var(--accent)`) and clean black/white icon label.
  * Nav links: Remove solid blue/grey active cards. Highlight active items using pure orange text and a thin vertical orange left bar.
* **FR-7 (Cards & Columns)**:
  * Card elements (metric blocks, products list rows, kanban cards) must have white background, a clean border (`1px solid var(--line)`), and soft drop shadows (`box-shadow: 0 4px 18px rgba(0, 0, 0, 0.02)`).
  * Drop shadow transitions: cards hover states must raise smoothly (`transform: translateY(-2px)`).
* **FR-8 (Data Tables)**:
  * Table rows must be bordered cleanly at the bottom only, with no solid colored backdrops.
  * Table headers must be styled in capital letters, small font size (`0.75rem`), with a bold weight (600) and grey color (`var(--muted)`).
* **FR-9 (Interactive Buttons & Forms)**:
  * Primary button: Solid orange background (`var(--accent)`), white text (`#ffffff`), and a soft orange glow shadow on hover.
  * Ghost/Secondary button: White background, orange border (`1px solid var(--accent)`), and orange text.
  * Inputs and dropdowns: Light grey base (`var(--surface-strong)`), transitioning to a bold orange border and orange focus ring upon active focus.

---

## 4. Non-Functional Requirements

* **Performance & Smoothness**: All CSS transformations and hover transitions must utilize hardware acceleration and execute over `150ms` using `ease-out` timing curves.
* **Responsive Scaling**: Elements must wrap or scroll horizontally smoothly on mobile viewports. Ensure navigation adapts to a sidebar slider on small screens.
* **Strict Style Inheritance**: Inline styling attributes in template files must be completely removed, enforcing centralized styling rules from `styles.css`.
