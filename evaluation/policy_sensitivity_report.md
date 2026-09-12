# Policy sensitivity report

## WindowPolicy

Both named policies are run against all solved rows and targets. The scored runtime uses `days_0_through_89`, passed explicitly to every simulator.

## Same-day order

Named policy: canonical scheduled/pending events are applied before the request payment; current available balance is initialized once.

## FX rate date

Named policy: settlement date, with last available rate on or before that date.

## Installment eligibility

Named policy: blank `max_installment_months` disables installments; otherwise `number_of_payments <= max_installment_months`, before ranking.
