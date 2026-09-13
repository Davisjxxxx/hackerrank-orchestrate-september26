from .gmail import GmailConnector
from .plaid import PlaidConnector


def default_connectors() -> dict[str, object]:
    return {"plaid": PlaidConnector(), "gmail": GmailConnector()}
