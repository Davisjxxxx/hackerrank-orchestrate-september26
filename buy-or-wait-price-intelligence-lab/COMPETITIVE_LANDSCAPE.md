# Competitive Landscape — Buy or Wait? V0.2

**Research date:** 2026-09-12

## Executive finding

The shopping-price side of the concept is a proven market, and **ShopSavvy is the closest existing product** found in current research. It already supports barcode/photo/name/link-style product discovery, multi-retailer comparison, historical price charts, alerts, and buy/wait-style price guidance.

However, current research did **not** identify a mainstream product that clearly combines all of the following in one deterministic decision flow:

1. real-time product capture (barcode/photo/link/search);
2. multi-retailer historical/current price intelligence;
3. user-specific financial safety based on cash flow, obligations, minimum balance, debt, and timing;
4. a combined `BUY NOW / HOLD / FINANCIALLY WAIT / DO NOT BUY` recommendation where financial safety has veto authority.

That combined decision layer is the strategic differentiation to protect.

## Closest market products

### ShopSavvy

Closest direct competitor on product/price intelligence.

Observed capabilities:

- barcode scanning;
- photo and product search;
- link/product lookup;
- current prices across many retailers;
- multi-retailer price history;
- target-price alerts;
- scheduled monitoring;
- price predictions / buy timing;
- used/condition-aware comparison;
- public Data API;
- open-source MCP server for product lookup, current prices, price history, and monitoring.

Strategic implication: do not attempt to differentiate merely on barcode scanning or price history. Use ShopSavvy as a possible V1 data provider while differentiating on financial safety and decision orchestration.

Sources:

- https://shopsavvy.com/
- https://shopsavvy.com/features/barcode-scanner
- https://shopsavvy.com/features/price-history
- https://shopsavvy.com/data
- https://github.com/shopsavvy/shopsavvy-mcp-server

### Price.com

Observed capabilities include mobile price comparison, barcode scanner, photo search, price history, price-drop alerts, coupons, and cashback.

Source:

- https://help.price.com/knowledge-base/price-com-ios-android-app/

### Google Lens / Google Shopping

Google Lens can identify products from a photo and surface prices, deals, reviews, and retailers. Google also supports product price tracking and target prices in supported markets.

Sources:

- https://blog.google/products-and-platforms/products/shopping/visual-search-lens-shopping/
- https://support.google.com/googleshopping/answer/13971184

### Klarna

Klarna combines shopping, price comparison/alerts, flexible payment products, spending/budget features, and payment management. This creates conceptual overlap with Buy or Wait?, but current public product descriptions do not establish the same independent cash-flow safety simulation or financial-veto purchase recommendation proposed here.

Source:

- https://www.klarna.com/us/klarna-app/

### PayPal Honey

Honey provides Droplist price tracking, price history in some contexts, seller comparison, notifications, coupons, and deal discovery. It does not appear to provide the proposed financial-safety purchase decision engine.

Sources:

- https://help.joinhoney.com/article/79-what-is-droplist
- https://www.paypal.com/us/money-hub/article/guide-to-using-paypal-honey

### Can I Afford This?

A small App Store product focuses on purchase affordability using manually entered income/expenses/savings and cost-per-use concepts, but its public listing says it has no bank connection and it does not provide the broad price-history/product-identification layer.

Source:

- https://apps.apple.com/us/app/can-i-afford-this/id6769469649

## Relevant GitHub projects

### shopsavvy/shopsavvy-mcp-server

**Strong reference / reusable connector lane.** MIT-licensed MCP server integrating ShopSavvy's API. It supports product lookup by barcode/ASIN/URL/model number, current offers, historical price data, and scheduled product monitoring.

Useful for:

- API integration patterns;
- product identifier handling;
- current/history calls;
- monitoring workflow;
- error/rate-limit handling.

It does **not** implement our mobile UI or personal financial-safety decision engine.

Repository:

- https://github.com/shopsavvy/shopsavvy-mcp-server

### aymanggv/barcode-price-comparison-app (Pricezilla)

Academic Android project using barcode scanning, Firebase/Firestore, and local retailer price comparison. Useful as a simple reference for scan -> lookup -> results mobile flow, but it lacks historical timing, broad connector architecture, and financial-safety composition.

Repository:

- https://github.com/aymanggv/barcode-price-comparison-app

## Strategic positioning

Avoid positioning as merely a price-comparison or barcode-scanning app. Those categories are established and crowded.

Position the system as a **purchase decision agent**:

> Scan it, photograph it, or share the link. Buy or Wait? identifies the exact item, determines whether today's price is actually good, checks whether the purchase is safe for your real financial situation, and tells you whether to buy now, hold for a better price, wait financially, or skip it.

## Product moat candidates

- combined financial safety + market-timing decision;
- explicit safety veto over bargain/deal signals;
- deterministic and auditable decision record;
- personalized minimum-balance and future-obligation modeling;
- learned user tradeoff between savings and waiting time;
- cross-condition opportunity (new/open-box/refurbished/used) without condition mixing;
- decision-aware watchlists rather than generic price alerts;
- future connector-ready bank/credit/debt/investment context.
