"""Provider-neutral real-world Buy or Wait financial platform."""

from .affordability import AffordabilityService
from .api import create_app
from .canonical import CanonicalStateService
from .composition import BuyOrWaitService
from .recurrence import RecurringStreamDetector

__all__ = ["AffordabilityService", "BuyOrWaitService", "CanonicalStateService", "RecurringStreamDetector", "create_app"]
