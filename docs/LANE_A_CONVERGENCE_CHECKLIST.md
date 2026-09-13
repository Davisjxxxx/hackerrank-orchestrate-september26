# Lane A convergence checklist

This checklist preserves Lane B checkpoint `c3a6782ac05257af816406fb18f6087ccfe0b5e4`
as the rollback point. Lane A finance changes must arrive through the adapter;
do not rewrite the product shell or finance semantics during convergence.

## 1. Inputs and expected merge surface

- Merge the approved Lane A finance commit only after its own tests and review.
- Expected conflict surface: `code/main.py`, root finance evaluation artifacts,
  root `README.md`/docs if changed by both lanes, `conftest.py` if Lane A has
  root pytest configuration, and any shared packaging metadata.
- Lane B product paths (`buy-or-wait-price-intelligence-lab/`) should remain
  additive. `output.csv`, solved fixtures, and evaluation semantics stay Lane A
  owned.
- Rollback point: `c3a6782ac05257af816406fb18f6087ccfe0b5e4` before adapter
  injection.

## 2. Adapter mapping

Implement `FinancialDecisionProvider.evaluate()` with an authenticated,
immutable Lane A result:

| Lane A output | Product field |
|---|---|
| `affordable_now` | `FinancialState.SAFE_NOW` |
| `affordable_with_plan` | `FinancialState.SAFE_WITH_PLAN` |
| `affordable_later` | `FinancialState.SAFE_LATER` |
| `not_affordable` | `FinancialState.NOT_AFFORDABLE` |
| `amount_safe_to_pay` | `safe_amount_today` |
| `earliest_date_for_full_payment` | `earliest_safe_full_payment_date` |
| `recommended_payment_method` | `recommended_payment_method` |
| `payment_plan` | validated chronological `payment_plan` |
| profile minimum reserve | `minimum_balance` / protected reserve evidence |

The adapter must preserve request ID, request date/as-of, finance engine
version, input hash, output hash, lifecycle evidence, pending debit/credit
decisions, recurrence evidence, and unsupported-income status. Missing or
malformed fields fail closed; no value is inferred from explanation text.

## 3. Post-merge gates

1. Run Lane A's full finance contract and full-dataset output validation.
2. Run `python -m pytest -q` at repository root and verify only root finance
   tests are collected.
3. Run `python -m pytest -q` from `buy-or-wait-price-intelligence-lab`.
4. Run retained red-team tests explicitly from their workspace.
5. Run the governed demos and assert A/B/C outcomes and fixture labels.
6. Regenerate OpenAPI; run compileall, mobile typecheck, Expo config, and
   `git diff --check`.
7. Verify unsafe finance cannot release even with `STRONG_BUY`, and that the
   adapter's safe amount/payment plan remain unchanged through every stage.

## 4. Acceptance and rollback

Accept only when all gates are green, no critical/high findings remain, and
the final release status is proven by the exact merged tree. If any adapter
mapping, output contract, or governance gate fails, return to the rollback
point, leave the failure visible, and do not claim finance convergence.
