# Buy or Wait? capability matrix

Legend: PRESENT = working in the canonical lab or integration layer; PARTIAL
= a working seam with fixture/deployment limitations; MISSING = not built in
this lane; POST-HACKATHON = intentionally deferred.

| Capability | Status | Evidence / boundary |
|---|---|---|
| Product search | PRESENT | deterministic text intake and fixture resolver |
| URL intake | PRESENT | normalized URL and safe host/ASIN parsing |
| Barcode intake | PRESENT | GTIN validation and canonical identity |
| Image/screenshot intake | PARTIAL | image/OCR evidence seam; native capture deferred |
| Product identity resolution | PRESENT | confidence and ambiguity gate |
| Current offer discovery | PARTIAL | connector protocols and recorded fixture; no live validation |
| Price normalization | PRESENT | Decimal landed price, currency, shipping, freshness |
| Price history | PRESENT | canonical in-memory store plus SQLite persistence port |
| Historical statistics | PRESENT | low/high/average/median/percentile and robust target |
| Price trend | PRESENT | deterministic trend in `PriceIntelligenceRecord` |
| Price watch | PRESENT | tenant-scoped repository, evaluation, idempotent triggers |
| Used offers | PRESENT | condition-aware alternative handling |
| Refurbished offers | PRESENT | condition-aware alternative handling |
| Financial decision integration | PARTIAL | protected `FinancialDecisionProvider`; committed checkpoint adapter seam |
| Decision synthesis | PRESENT | canonical uppercase product recommendation states |
| API | PRESENT | existing FastAPI plus governed evaluation route |
| Frontend | PARTIAL | imported Expo shell; governance response is API-visible |
| Mobile app | PARTIAL | adapter-seam actions; native camera/barcode/OCR deferred |
| Persistence | PRESENT | SQLite port; API default remains fixture/in-memory |
| Provider interfaces | PRESENT | resolver, current, history, used, watch ports |
| Tests | PRESENT | canonical lab 87 tests plus new integration tests |
| Governance | PRESENT | evidence envelope, certification, veto |
| Adversarial review | PRESENT | deterministic local reviewer and future provider seam |
| Certification | PRESENT | mandatory-evidence fail-closed gate |
| Committee | PRESENT | candidate-only lenses; hard finance eligibility |
| Final safety veto | PRESENT | deterministic release check |
| Production authentication | POST-HACKATHON | fixture bearer seam exists; production token verifier deferred |
| Connected accounts | POST-HACKATHON | normalized adapter interfaces documented |
| Cortex gate | PARTIAL | first-class reviewer seam and plan; no hard dependency |
| Live provider operations | POST-HACKATHON | credentials/terms/scheduler/observability required |
