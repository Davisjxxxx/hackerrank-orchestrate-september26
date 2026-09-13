"""Authority-first finance candidate path.

This package is intentionally parallel to ``code/main.py``.  It exposes
evidence-gated event construction for evaluation; production wiring is kept
out of this module until a candidate passes the bounded promotion gate.
"""

from .resolver import AuthorityCanonicalizer, CandidatePolicy, ControlClass, ControlState

__all__ = ["AuthorityCanonicalizer", "CandidatePolicy", "ControlClass", "ControlState"]
