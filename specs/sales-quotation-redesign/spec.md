# Specification: Sales Quotation Template Redesign

This specification outlines the redesign of the Sales Quotation print layout ([templates/quotation_document.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/quotation_document.html)) to match the branding, structure, and styling of the reference [SALES QUOTATION.pdf](file:///home/ahmedhaq/Work/Pricing-app-master/SALES QUOTATION.pdf) while leveraging the layout structure, color scheme, inline SVG logo, and interactive page flow from the redesigned [templates/proforma_invoice_document.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/proforma_invoice_document.html).

---

## 1. User Stories

* **US-1 (Branding Alignment)**: As a Sales salesperson, I want the exported Sales Quotation to display the official **Vanol** company logo and professional layout so that the document is brand-compliant and consistent with the proforma invoice.
* **US-2 (Pagination & Structure)**: As a Sales salesperson, I want the document to cleanly fit onto exactly 2 A4 pages when printed or saved to PDF (Page 1: Supplier, Customer, Items, Terms, Totals; Page 2: Bank Details) without overlapping text or cut-offs.
* **US-3 (Manual Override & Auto-Calculation)**: As a Sales salesperson, I want to edit quantities, unit prices, or terms directly on the print view screen, and have the row totals, subtotal (EX Factory Amount), logistics cost, and "Total Amount in words" automatically recalculate in real-time.

---

## 2. Functional Requirements

### 2.1 Layout & Content Blocks

#### Page 1: Main Sales Quotation
* **Header**:
  * Inline SVG representation of the **Vanol FZE** logo in top-left (same as proforma invoice).
  * Document Title **SALES QUOTATION** in top-right.
  * Supplier contact details (VANOL FZE, Plot S40805, Dubai, Phone, Email) below the logo.
  * Quotation metadata block (Date Issued, Document No., Validity) on top-right.
* **Circulation Blocks**:
  * Side-by-side tables for **CUSTOMER** and **SUPPLIER** detailing Company Name, Address, Contact Name, Contact Phone, and Email.
* **Items Grid**:
  * 12-row table containing columns: `Sr.`, `Description`, `Specification`, `Unit of Package`, `Quantity`, `Unit Price (USD)`, `Total Amount (USD)`.
  * Pre-fills row 1 with the target quotation or lead details (if available).
* **Footer Tables**:
  * **Terms and Conditions** (bottom left):
    * Payment Terms (default: `50% at the time of order and rest before dispatching`)
    * Price (default: `Price is based on above agreed volume`)
    * Delivery Terms (default: `EXWorks`)
    * Port of Destination (default: `Jebel Ali`)
    * Port of Loading (default: `VANOL WAREHOUSE`)
  * **Totals Table** (bottom right):
    * Total EX Factory Amount in USD
    * Logistics Cost 40FT (default: `0.00`)
    * Total Amount in USD
  * **Amount in Words Box**: Text block calculating: `Total Amount in words : USD [Amount in Words] only`.
  * **Footer Line**: System generation warning message.

#### Page 2: Bank Details
* **Header**: Repeat Vanol Logo and **SALES QUOTATION** document title.
* **Bank Details Block**:
  * VANOL FZE (USD Bank Account Details)
  * Bank Name: ADCB
  * Account Holder Name: VANOL FZE
  * Account Number: 120227119992005
  * IBAN: AE2900300120227119992005
  * Swift Code: ADCBAEAXXX

### 2.2 Print Configuration
* **Page breaks**: Enforce CSS page break rules (`page-break-after: always;` / `break-after: page;`) separating Page 1 and Page 2.
* **A4 sizing**: Set container dimensions strictly to standard A4 print margins (`210mm` x `297mm`).

### 2.3 Interactive Features & Calculations (JavaScript)
* **Editable Fields**: Apply `contenteditable="true"` to data fields.
* **Auto-calculation**:
  * On editing `Quantity` or `Unit Price (USD)`:
    * Compute `Total Amount (USD) = Quantity * Unit Price`
    * Compute `Total EX Factory Amount in USD. = Sum of all row Total Amounts`
    * Compute `Total Amount in USD = Total EX Factory Amount + Logistics Cost 40FT`
  * Words Converter: Dynamically convert `Total Amount` to English words in the text box.

---

## 3. Non-Functional Requirements

* **HTML Structure**: Structured using clean, standards-compliant HTML tables and flex layouts.
* **Print Styling**: Vanilla CSS optimized for print layouts to suppress background shading issues on different browsers.
