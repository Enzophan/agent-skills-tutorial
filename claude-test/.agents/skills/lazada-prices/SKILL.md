---
name: lazada-prices
description: Aggregate prices of a product from various stores on lazada.vn. Use this skill when users want to compare prices for a specific product across different sellers on Lazada Vietnam. Provide a product name as input, and the skill will return a simple list showing prices, seller names, and basic seller information from various stores on lazada.vn.
---

# Lazada Price Aggregator Skill

This skill helps you aggregate and compare prices for a specific product from various stores on Lazada Vietnam (lazada.vn).

## How to Use

When a user asks for prices on Lazada Vietnam, use the bundled scraper script at `scripts/lazada_scraper.py`:

```bash
# Basic search (prints results to terminal)
python3 scripts/lazada_scraper.py "product name"

# Search and also export to Excel (.xlsx)
python3 scripts/lazada_scraper.py "product name" --excel
```

The `--excel` flag exports the results to an Excel file with clickable links.

### Requirements

- Python 3
- Playwright: `pip install playwright && playwright install chromium`
- openpyxl: `pip install openpyxl` (required for `--excel`)

## Input

Provide the product name to search:
- "iPhone 15 Pro"
- "Samsung Galaxy S24"
- "adidas barreda Nam"

## Output

**Terminal output:**
- Product name (cleaned of promotional prefixes)
- Price in VND
- Discount (if available)
- Seller location
- Units sold (if available)
- Rating (if available)
- **Product link** (direct Lazada URL)

**Excel file** (when `--excel` is used):
Same fields as above in a formatted `.xlsx` file with:
- Auto-filter on all columns
- Clickable hyperlinks in the Link column
- Lazada-branded red header styling

## Example

**User:** "Compare prices for iPhone 15 Pro on Lazada Vietnam"

**Run:**
```bash
python3 scripts/lazada_scraper.py "iPhone 15 Pro" --excel
```

**Terminal output:**
```
1. iPhone 15 Pro 128GB Chính Hãng
   Giá: 22.990.000 ₫
   Giảm: 10% Off
   Vị trí: Hà Nội
   Đã bán: 1.2K Đã bán
   Đánh giá: (45)/5
   Link: https://www.lazada.vn/products/pdp-i1234567890.html
```

**Excel file:** `lazada_prices_iPhone_15_Pro.xlsx` saved to the current directory.

## Implementation Notes

- Uses Playwright to render Lazada's JavaScript-heavy search results page
- Extracts: title, price, discount, location, sales count, rating, and product URL
- Store/brand names are only available on individual product pages, not in search listings
- The `--excel` flag uses openpyxl to create a formatted spreadsheet
- Product links are included in both terminal output and Excel export

The skill does not perform deep product analysis or extract detailed specifications — it focuses specifically on price aggregation for comparison purposes.
