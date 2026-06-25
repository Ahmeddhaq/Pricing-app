# Specification: Proforma Invoice Template Redesign

This specification outlines the redesign of the Proforma Invoice print layout ([templates/proforma_invoice_document.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/proforma_invoice_document.html)) to match the branding, structure, and 2-page pagination of the reference [PROFORMA INVOICE.pdf](file:///home/ahmedhaq/Work/Pricing-app-master/PROFORMA INVOICE.pdf).

---

## 1. User Stories

* **US-1 (Branding Alignment)**: As a Sales salesperson, I want the exported Proforma Invoice to display the official **Vanol** company logo and professional layout so that the document is brand-compliant.
* **US-2 (Pagination & Structure)**: As a Sales salesperson, I want the document to cleanly fit onto exactly 2 A4 pages when printed or saved to PDF (Page 1: Supplier, Client, Items, Terms, Totals; Page 2: Bank Details) without overlapping text or cut-offs.
* **US-3 (Manual Override & Auto-Calculation)**: As a Sales salesperson, I want to edit quantities, unit prices, or terms directly on the print view screen, and have the sums, VAT, and "Total Amount in words" automatically recalculate in real-time.

---

## 2. Functional Requirements

### 2.1 Layout & Content Blocks

#### Page 1: Main Proforma Invoice
* **Header**:
  * Inline SVG representation of the **Vanol FZE** logo in top-left.
  * Document Title **PROFORMA INVOICE** in top-right.
  * Supplier contact details (VANOL FZE, Plot S40805, Dubai, Phone, Email) below the logo.
  * Invoice metadata block (Invoice No, Invoice Date, Your Ref No, Our Ref No) on top-right.
* **Circulation Blocks**:
  * Side-by-side tables for **INVOICE TO** and **SHIP TO** detailing Company Name, Address, Contact Name, Contact Phone, and Email.
* **Items Grid**:
  * 12-row table containing columns: `S.No.`, `No` (SKU), `Description`, `UOM/Type` (Packaging), `Quantity`, `Unit Price (USD)`, `VAT%`, `VAT(USD)`, `Amount (USD)`.
  * Pre-fills row 1 with the target quotation details (if available).
* **Footer Tables**:
  * **Terms & Conditions** (bottom left): Payment Terms, Delivery Terms, Port of Destination, Port of Loading.
  * **Totals Table** (bottom right): Sub Total (USD), Logistics and Other Charges (USD), VAT (USD), Total Amount (USD).
  * **Amount in Words Box**: Text block calculating: `Total Amount in words : USD [Amount in Words] only`.
  * **Footer Line**: System generation warning message.

#### Page 2: Bank Details
* **Header**: Repeat Vanol Logo and **PROFORMA INVOICE** document title.
* **Bank Details Block**:
  * Name: National Bank of Ras Al Khaimah
  * Address: RAKBANK, P.O. Box 1531, Dubai, UAE
  * Account No., IBAN, Swift Code NRAKAEAK.

### 2.2 Print Configuration
* **Page breaks**: Enforce CSS page break rules (`page-break-after: always;` / `break-after: page;`) separating Page 1 and Page 2.
* **A4 sizing**: Set container dimensions strictly to standard A4 print margins (`210mm` x `297mm`).

### 2.3 Interactive Features & Calculations (JavaScript)
* **Editable Fields**: Apply `contenteditable="true"` to data fields.
* **Auto-calculation**:
  * On editing `Quantity`, `Unit Price`, or `VAT%`:
    * Compute `VAT(USD) = Quantity * Unit Price * (VAT% / 100)`
    * Compute `Amount = (Quantity * Unit Price) + VAT(USD)`
    * Compute `Sub Total = Sum of all row Amounts`
    * Compute `Total Amount = Sub Total + Logistics + VAT`
* **Words Converter**: Dynamically convert `Total Amount` to English words in the text box.

---

## 3. Non-Functional Requirements

* **HTML Structure**: Structured using clean, standards-compliant HTML tables and flex layouts.
* **Print Styling**: Vanilla CSS optimized for print layouts to suppress background shading issues on different browsers.
