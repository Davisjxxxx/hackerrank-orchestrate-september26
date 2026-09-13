from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .affordability import AffordabilityService
from .canonical import CanonicalStateService
from .db import Base, FinancialEvent, FinancialProfile, User
from .ingestion import TransactionImportService
from .schemas import DecisionInput, EventInput


def main() -> None:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        user_id = "demo-user"
        session.add(User(id=user_id)); session.add(FinancialProfile(user_id=user_id, home_currency="USD", current_available_cash=Decimal("3000"), minimum_balance_to_keep=Decimal("1000"), payment_methods=["full_payment", "wait", "partial_payment"], flexible_categories=["dining"]))
        session.commit()
        today = date.today()
        rows = ["date,description,debit,credit,category,id"]
        for months_back in (3, 2, 1):
            d = today - timedelta(days=30 * months_back)
            rows.extend([f"{d},Employer salary,,2500,income,salary-{months_back}", f"{d},Apartment rent,1200,,housing,rent-{months_back}", f"{d},Power utility,140,,utilities,utility-{months_back}"])
        importer = TransactionImportService()
        importer.commit(session, user_id=user_id, filename="demo.csv", content="\n".join(rows).encode(), events=importer.preview("demo.csv", "\n".join(rows).encode()))
        session.add(FinancialEvent(user_id=user_id, source="demo", event_type="expense", direction="debit", amount=Decimal("500"), currency="USD", transaction_date=today - timedelta(days=1), settlement_date=None, status="pending", description="Pending car repair", category="transport", recurrence_eligible=False))
        session.add(FinancialEvent(user_id=user_id, source="demo", event_type="income", direction="credit", amount=Decimal("900"), currency="USD", transaction_date=today, settlement_date=None, status="pending", description="Pending bonus", category="bonus", recurrence_eligible=False))
        session.commit()
        canonical = CanonicalStateService().state(session, user_id, as_of=today)
        request = DecisionInput(amount=Decimal("1000"), currency="USD", description="Laptop", category="electronics", request_date=today)
        result = AffordabilityService().evaluate(canonical, request)
        print("import transactions -> normalized canonical events -> recurring streams -> deterministic decision")
        print({"pending_debits_reserved": len(canonical.pending_debits), "pending_credits_excluded": len(canonical.pending_credits), "streams": len(canonical.streams), "decision": result.model_dump(mode="json")})

if __name__ == "__main__": main()
