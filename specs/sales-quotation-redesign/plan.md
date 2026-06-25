# Technical Implementation Plan: Sales Quotation Redesign

This plan outlines the HTML layout structure, A4 print styling rules, inline SVG design, and real-time JavaScript calculation engine to rebuild the Sales Quotation template ([templates/quotation_document.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/quotation_document.html)) to match the branding, structure, and styling of the redesigned [templates/proforma_invoice_document.html](file:///home/ahmedhaq/Work/Pricing-app-master/templates/proforma_invoice_document.html) and reference [SALES QUOTATION.pdf](file:///home/ahmedhaq/Work/Pricing-app-master/SALES QUOTATION.pdf).

---

## 1. Grid & Page Layout Structure

To ensure a perfect 2-page print layout matching the proforma invoice, the document will be structured as:

```html
<div class="document-container">
  <!-- PAGE 1 -->
  <div class="page page-1">
    <!-- Header: Logo, Supplier details, Metadata -->
    <!-- Customer & Supplier circulation sections -->
    <!-- Items Grid (12 Rows) -->
    <!-- Terms & Conditions (Bottom Left) + Totals (Bottom Right) -->
    <!-- Total Amount in Words Box -->
  </div>

  <div class="page-break"></div>

  <!-- PAGE 2 -->
  <div class="page page-2">
    <!-- Header: Logo, Supplier details, Metadata -->
    <!-- Bank Details Section -->
  </div>
</div>
```

### CSS Print Rules
* Page break separation:
  ```css
  .page-break {
      display: block;
      page-break-after: always;
      break-after: page;
  }
  ```
* Standard A4 sizing logic:
  ```css
  body {
      background: #f5f5f5;
      margin: 0;
      padding: 20px;
  }
  .document-container {
      width: 210mm;
      margin: 0 auto;
      background: #fff;
  }
  .page {
      width: 210mm;
      height: 297mm;
      padding: 12mm 15mm;
      box-sizing: border-box;
      position: relative;
      display: flex;
      flex-direction: column;
  }
  @media print {
      body { background: none; padding: 0; }
      .document-container { width: 100%; margin: 0; }
      .page { width: 100%; height: 100%; padding: 12mm 15mm; }
  }
  ```

---

## 2. Inline SVG Branding

To render the Vanol logo without external image file dependencies, we will embed the same inline SVG used in the proforma invoice:

```html
<svg width="160" height="60" viewBox="0 0 180 70">
  <rect x="2" y="2" width="176" height="66" rx="33" ry="33" fill="#13472b" stroke="#ffffff" stroke-width="2"/>
  <rect x="5" y="5" width="170" height="60" rx="30" ry="30" fill="none" stroke="#dc3545" stroke-width="1.5"/>
  <text x="90" y="20" font-family="Arial, sans-serif" font-size="8" font-weight="bold" font-style="italic" fill="#ffffff" text-anchor="middle">THE QUALITY LEADS!</text>
  <text x="90" y="50" font-family="'Brush Script MT', cursive, Georgia, serif" font-size="34" font-weight="bold" fill="#dc3545" stroke="#ffffff" stroke-width="1.2" text-anchor="middle" font-style="italic">Vanol</text>
  <g fill="#ffffff" transform="translate(68, 55)">
    <polygon points="4,0 5.2,2.8 8,2.8 5.6,4.4 6.4,7.2 4,5.6 1.6,7.2 2.4,4.4 0,2.8 2.8,2.8" transform="translate(0,0) scale(0.6)"/>
    <polygon points="4,0 5.2,2.8 8,2.8 5.6,4.4 6.4,7.2 4,5.6 1.6,7.2 2.4,4.4 0,2.8 2.8,2.8" transform="translate(10,0) scale(0.6)"/>
    <polygon points="4,0 5.2,2.8 8,2.8 5.6,4.4 6.4,7.2 4,5.6 1.6,7.2 2.4,4.4 0,2.8 2.8,2.8" transform="translate(20,0) scale(0.6)"/>
    <polygon points="4,0 5.2,2.8 8,2.8 5.6,4.4 6.4,7.2 4,5.6 1.6,7.2 2.4,4.4 0,2.8 2.8,2.8" transform="translate(30,0) scale(0.6)"/>
    <polygon points="4,0 5.2,2.8 8,2.8 5.6,4.4 6.4,7.2 4,5.6 1.6,7.2 2.4,4.4 0,2.8 2.8,2.8" transform="translate(40,0) scale(0.6)"/>
  </g>
</svg>
```

---

## 3. Real-Time Calculation Engine (JavaScript)

We will include a JavaScript module inside the template that:
1. **Listens to Events**: Uses `input` event listeners on the `document-container` to detect modifications in cells with class `.qty` or `.price` or `#logistics-charges`.
2. **Computes Rows**:
   * Reads numerical values (stripping symbols and commas).
   * Computes `Total Amount = Qty * Price`.
   * Updates corresponding row total text nodes.
3. **Computes Totals**:
   * Sums all row Total Amounts to update `Sub Total` / `Total EX Factory Amount`.
   * Adds `Logistics` (editable cell) to update `Total Amount`.
4. **Number-to-Words Converter**: Runs a helper function to convert the numeric total (e.g. `44164.00`) to words (`"Forty Four Thousand One Hundred Sixty Four and 00/100"`) and populates the amount-in-words container.
