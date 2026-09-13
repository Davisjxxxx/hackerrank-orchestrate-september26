"""Fail-closed governed decision pipeline.

All dollar arithmetic remains in the authoritative financial result.  The
components in this module select, challenge, certify, and release candidates;
none can mutate the financial record or safe-to-pay amount.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
from decimal import Decimal
import hashlib
import json
import platform
import sys
from typing import Any, Mapping, Protocol, Sequence
from types import MappingProxyType

from .models import FinancialCoverageState, FinancialSafetyResult, FinancialState, ProductIdentity
from .price_intelligence import PriceIntelligenceRecord


class RecommendationState(StrEnum):
    BUY_NOW = "BUY_NOW"
    HOLD_FOR_BETTER_PRICE = "HOLD_FOR_BETTER_PRICE"
    SET_PRICE_WATCH = "SET_PRICE_WATCH"
    CONSIDER_USED_OR_REFURBISHED = "CONSIDER_USED_OR_REFURBISHED"
    FINANCIALLY_WAIT = "FINANCIALLY_WAIT"
    NOT_RECOMMENDED = "NOT_RECOMMENDED"
    NEEDS_CONFIRMATION = "NEEDS_CONFIRMATION"


class ReviewStatus(StrEnum):
    PASS = "PASS"
    CHALLENGED = "CHALLENGED"
    ABSTAIN = "ABSTAIN"


class CertificationStatus(StrEnum):
    CERTIFIED = "CERTIFIED"
    CERTIFICATION_FAILED = "CERTIFICATION_FAILED"


class CommitteeStatus(StrEnum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ABSTAIN = "ABSTAIN"
    ESCALATE = "ESCALATE"


class ReleaseStatus(StrEnum):
    RELEASED = "RELEASED"
    RELEASE_BLOCKED = "RELEASE_BLOCKED"


MANDATORY_EVIDENCE = (
    "financial_input_validated", "canonicalization_completed", "lifecycle_resolution_completed",
    "dedup_completed", "fx_processing_completed", "recurrence_processing_completed",
    "pending_debits_checked", "pending_credits_excluded", "confirmed_income_checked",
    "simulation_completed", "protected_balance_verified", "candidate_plans_evaluated",
    "product_identity_verified", "current_market_check_status", "price_history_state_declared",
    "condition_handling_verified", "adversarial_review_completed", "critical_challenges_resolved",
    "decision_explanation_grounded",
)


@dataclass(frozen=True)
class DecisionCandidate:
    candidate_id: str
    recommendation: RecommendationState
    reason: str
    financial_state: FinancialState
    price_signal: str
    eligible: bool = True


@dataclass(frozen=True)
class DecisionEvidenceEnvelope:
    decision_id: str
    request_fingerprint: str
    product_fingerprint: str
    financial_engine_version: str
    financial_input_hash: str
    financial_decision_hash: str
    financial_safety_status: str
    safe_amount_today: Decimal | None
    payment_plan: Mapping[str, Any]
    minimum_projected_balance: Decimal | None
    protected_minimum_balance: Decimal | None
    price_engine_version: str
    price_input_hash: str
    price_observation_ids: tuple[str, ...]
    price_history_status: str
    price_signal: str
    price_confidence: Decimal
    candidate_recommendation: RecommendationState
    unresolved_evidence: tuple[str, ...]
    provenance: Mapping[str, Any]
    control_evidence: Mapping[str, Any]
    product_identity_confidence: Decimal
    current_price: Decimal | None
    governance_trace: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # Reviewers receive a snapshot, never a mutable reference to trusted
        # finance/payment/control data that could be edited before certification.
        object.__setattr__(self, "payment_plan", MappingProxyType(dict(self.payment_plan)))
        object.__setattr__(self, "control_evidence", MappingProxyType(dict(self.control_evidence)))
        object.__setattr__(self, "provenance", MappingProxyType(dict(self.provenance)))
        object.__setattr__(self, "unresolved_evidence", tuple(self.unresolved_evidence))

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(self)


@dataclass(frozen=True)
class ChallengeReport:
    review_id: str
    decision_id: str
    status: ReviewStatus
    critical_findings: tuple[str, ...]
    major_findings: tuple[str, ...]
    minor_findings: tuple[str, ...]
    counterexamples_tested: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    recommended_action: str


@dataclass(frozen=True)
class CertificationReport:
    decision_id: str
    status: CertificationStatus
    missing_evidence: tuple[str, ...]
    verified_evidence: tuple[str, ...]
    reason: str


@dataclass(frozen=True)
class CommitteeDecision:
    committee_id: str
    candidate_ids: tuple[str, ...]
    eligible_candidates: tuple[str, ...]
    member_assessments: Mapping[str, Mapping[str, str]]
    disagreements: tuple[str, ...]
    selected_candidate: str | None
    selection_reason: str
    status: CommitteeStatus


@dataclass(frozen=True)
class ReleaseResult:
    status: ReleaseStatus
    selected_candidate: str | None
    reason_codes: tuple[str, ...]


@dataclass(frozen=True)
class GovernedDecisionResult:
    envelope: DecisionEvidenceEnvelope
    candidates: tuple[DecisionCandidate, ...]
    review: ChallengeReport
    certification: CertificationReport
    committee: CommitteeDecision
    release: ReleaseResult

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(self)


class AdversarialReviewer(Protocol):
    def review(self, evidence_envelope: DecisionEvidenceEnvelope) -> ChallengeReport: ...


class LocalAdversarialReviewer:
    """A separate, deterministic challenge lens for local release decisions."""

    def review(self, evidence_envelope: DecisionEvidenceEnvelope) -> ChallengeReport:
        critical: list[str] = []
        major: list[str] = []
        minor: list[str] = []
        controls = evidence_envelope.control_evidence
        required_finance = ("pending_debits_checked", "pending_credits_excluded", "protected_balance_verified", "simulation_completed")
        for control in required_finance:
            if controls.get(control) is not True:
                critical.append(f"MISSING_FINANCE_CONTROL:{control}")
        if evidence_envelope.candidate_recommendation in {RecommendationState.BUY_NOW, RecommendationState.CONSIDER_USED_OR_REFURBISHED}:
            if evidence_envelope.financial_safety_status != FinancialState.SAFE_NOW.value:
                critical.append("BUY_CANDIDATE_WITHOUT_SAFE_NOW_FINANCE")
            if (evidence_envelope.current_price is not None and
                    (evidence_envelope.safe_amount_today is None or
                     evidence_envelope.safe_amount_today < evidence_envelope.current_price)):
                critical.append("SAFE_AMOUNT_COVERAGE_NOT_PROVEN")
        if evidence_envelope.product_identity_confidence < Decimal("0.85"):
            critical.append("PRODUCT_IDENTITY_BELOW_RELEASE_THRESHOLD")
        if evidence_envelope.price_history_status == "INSUFFICIENT":
            major.append("PRICE_HISTORY_INSUFFICIENT")
        if evidence_envelope.price_signal == "UNKNOWN":
            major.append("PRICE_SIGNAL_UNKNOWN")
        if evidence_envelope.unresolved_evidence:
            major.append("UNRESOLVED_EVIDENCE_PRESENT")
            evidence_blob = " ".join(evidence_envelope.unresolved_evidence).lower()
            critical_markers = {
                "duplicate_income": "DUPLICATE_INCOME_EVIDENCE",
                "unsupported_future_income": "UNSUPPORTED_FUTURE_INCOME",
                "omitted_liability": "OMITTED_LIABILITY_EVIDENCE",
                "pending_credit": "PENDING_CREDIT_MISUSE",
                "pending_debit": "PENDING_DEBIT_OMISSION",
                "identity_mismatch": "PRODUCT_IDENTITY_MISMATCH",
                "wrong_variant": "WRONG_PRODUCT_VARIANT",
                "condition_mismatch": "CONDITION_MISMATCH",
                "prompt_injection": "PROMPT_INJECTION",
                "duplicate_future": "DUPLICATE_FUTURE_OCCURRENCE",
            }
            for marker, finding in critical_markers.items():
                if marker in evidence_blob:
                    critical.append(finding)
            if ("sparse_history" in evidence_blob or "anomalous_price" in evidence_blob or "outlier" in evidence_blob
                    or "stale_recurrence" in evidence_blob or "seller_disagreement" in evidence_blob
                    or "source_inconsistency" in evidence_blob):
                major.append("PRICE_EVIDENCE_REQUIRES_REVIEW")
        if controls.get("unsupported_income_used") is True:
            critical.append("UNSUPPORTED_INCOME_USED")
        blob = json.dumps(_jsonable(evidence_envelope.provenance), sort_keys=True).lower()
        if any(token in blob for token in ("ignore trusted", "override finance", "system prompt", "disregard rules")):
            critical.append("UNTRUSTED_TEXT_PROMPT_INJECTION_DETECTED")
        if not evidence_envelope.price_observation_ids:
            minor.append("NO_PRICE_OBSERVATION_REFERENCES")
        status = ReviewStatus.ABSTAIN if critical else (ReviewStatus.CHALLENGED if major or minor else ReviewStatus.PASS)
        action = "BLOCK_RELEASE" if critical else ("REVIEW_BEFORE_RELEASE" if major or minor else "PROCEED_TO_CERTIFICATION")
        return ChallengeReport(
            review_id=_id("review", evidence_envelope.decision_id), decision_id=evidence_envelope.decision_id,
            status=status, critical_findings=tuple(sorted(set(critical))), major_findings=tuple(sorted(set(major))),
            minor_findings=tuple(sorted(set(minor))), counterexamples_tested=(
                "duplicate_income", "unsupported_future_income", "omitted_liability", "pending_credit_misuse",
                "pending_debit_omission", "stale_recurrence", "explicit_future_collision", "identity_variant_mismatch",
                "seller_condition_disagreement", "sparse_history", "historical_outlier", "price_source_inconsistency",
                "prompt_injection", "untrusted_text_state_mutation",
            ), evidence_refs=evidence_envelope.price_observation_ids, recommended_action=action,
        )


class CertificationGate:
    def certify(self, envelope: DecisionEvidenceEnvelope, review: ChallengeReport | None) -> CertificationReport:
        controls = envelope.control_evidence
        missing = tuple(sorted(key for key in MANDATORY_EVIDENCE if controls.get(key) is not True))
        if review is None:
            missing = tuple(sorted(set(missing) | {"adversarial_review_completed", "critical_challenges_resolved"}))
        elif review.status == ReviewStatus.ABSTAIN or review.critical_findings:
            missing = tuple(sorted(set(missing) | {"critical_challenges_resolved"}))
        status = CertificationStatus.CERTIFIED if not missing else CertificationStatus.CERTIFICATION_FAILED
        return CertificationReport(
            decision_id=envelope.decision_id, status=status, missing_evidence=missing,
            verified_evidence=tuple(key for key in MANDATORY_EVIDENCE if key not in missing),
            reason="all mandatory operations evidenced" if status == CertificationStatus.CERTIFIED else "CERTIFICATION_FAILED",
        )


class DecisionCommittee:
    """Selects among already valid candidates; it never votes on amounts."""

    def select(self, envelope: DecisionEvidenceEnvelope, candidates: Sequence[DecisionCandidate],
               certification: CertificationReport, review: ChallengeReport) -> CommitteeDecision:
        candidate_ids = tuple(candidate.candidate_id for candidate in candidates)
        financially_eligible = tuple(candidate.candidate_id for candidate in candidates if _candidate_financially_legal(candidate, envelope))
        assessments = {
            candidate.candidate_id: {
                "financial_conservatism": "pass" if _candidate_financially_legal(candidate, envelope) else "veto",
                "liquidity_preservation": "pass" if candidate.recommendation in {RecommendationState.FINANCIALLY_WAIT, RecommendationState.NOT_RECOMMENDED} else "review",
                "price_value": envelope.price_signal.lower(),
                "timing": candidate.recommendation.value,
                "fees": "not_redefined_by_committee",
                "used_refurb_value": "separate_condition_evidence",
                "evidence_quality": envelope.price_history_status.lower(),
                "uncertainty": "elevated" if envelope.price_history_status != "SUFFICIENT" else "bounded",
            }
            for candidate in candidates
        }
        if certification.status != CertificationStatus.CERTIFIED or review is None or review.critical_findings:
            status = CommitteeStatus.ESCALATE
            selected = None
            reason = "governance prerequisites are not satisfied"
        elif not financially_eligible:
            status = CommitteeStatus.REJECTED
            selected = None
            reason = "no candidate satisfies the deterministic finance veto"
        else:
            selected = financially_eligible[0]
            status = CommitteeStatus.APPROVED
            reason = "selected highest-priority candidate after hard finance eligibility"
        return CommitteeDecision(
            committee_id=_id("committee", envelope.decision_id), candidate_ids=candidate_ids,
            eligible_candidates=financially_eligible, member_assessments=assessments,
            disagreements=tuple(sorted({"price_history_uncertainty"} if envelope.price_history_status != "SUFFICIENT" else set())),
            selected_candidate=selected, selection_reason=reason, status=status,
        )


class FinalSafetyVeto:
    def release(self, envelope: DecisionEvidenceEnvelope, committee: CommitteeDecision,
                certification: CertificationReport | None, review: ChallengeReport | None,
                candidates: Sequence[DecisionCandidate]) -> ReleaseResult:
        reasons: list[str] = []
        selected_id = committee.selected_candidate if committee is not None else None
        selected = next((candidate for candidate in candidates if candidate.candidate_id == selected_id), None)
        if certification is None or certification.status != CertificationStatus.CERTIFIED:
            reasons.append("CERTIFICATION_FAILED")
        if review is None:
            reasons.append("ADVERSARIAL_REVIEW_NOT_EXECUTED")
        elif review.critical_findings:
            reasons.append("CRITICAL_CHALLENGE_UNRESOLVED")
        if committee is None:
            reasons.append("COMMITTEE_NOT_EXECUTED")
        elif committee.status != CommitteeStatus.APPROVED:
            reasons.append("COMMITTEE_NOT_APPROVED")
        elif selected_id not in committee.eligible_candidates:
            reasons.append("COMMITTEE_SELECTED_INELIGIBLE_CANDIDATE")
        if selected is None:
            reasons.append("NO_COMMITTEE_CANDIDATE")
        if selected and not _candidate_financially_legal(selected, envelope):
            reasons.append("FINANCIAL_SAFETY_VETO")
        if envelope.control_evidence.get("unsupported_income_used") is True:
            reasons.append("UNSUPPORTED_INCOME_USED")
        if envelope.control_evidence.get("pending_credits_excluded") is not True:
            reasons.append("PENDING_CREDIT_NOT_EXCLUDED")
        if envelope.control_evidence.get("protected_balance_verified") is not True:
            reasons.append("PROTECTED_BALANCE_NOT_VERIFIED")
        if envelope.control_evidence.get("payment_plan_legal") is not True:
            reasons.append("PAYMENT_PLAN_NOT_VERIFIED")
        if envelope.control_evidence.get("deadline_respected") is not True:
            reasons.append("DEADLINE_NOT_VERIFIED")
        if envelope.control_evidence.get("payment_plan_arithmetic_reconciles") is not True:
            reasons.append("PAYMENT_ARITHMETIC_NOT_VERIFIED")
        if (selected and selected.recommendation in {RecommendationState.BUY_NOW, RecommendationState.CONSIDER_USED_OR_REFURBISHED}
                and (envelope.safe_amount_today is None or envelope.current_price is None
                     or envelope.safe_amount_today < envelope.current_price)):
            reasons.append("SAFE_AMOUNT_BELOW_CURRENT_PRICE")
        if envelope.product_identity_confidence < Decimal("0.85"):
            reasons.append("PRODUCT_IDENTITY_NOT_CERTIFIED")
        if envelope.current_price is None:
            reasons.append("CURRENT_PRICE_MISSING")
        if reasons:
            return ReleaseResult(ReleaseStatus.RELEASE_BLOCKED, None, tuple(sorted(set(reasons))))
        return ReleaseResult(ReleaseStatus.RELEASED, selected.candidate_id if selected else None, ("DETERMINISTIC_VETO_PASSED",))


class DecisionSynthesis:
    def synthesize(self, financial: FinancialSafetyResult, price: PriceIntelligenceRecord) -> tuple[DecisionCandidate, ...]:
        candidates: list[tuple[RecommendationState, str]] = []
        if financial.financial_state == FinancialState.NOT_AFFORDABLE:
            state = RecommendationState.FINANCIALLY_WAIT if financial.earliest_safe_full_payment_date else RecommendationState.NOT_RECOMMENDED
            candidates.append((state, "financial safety does not support payment on the request date"))
        elif financial.financial_state in {FinancialState.SAFE_LATER, FinancialState.SAFE_WITH_PLAN}:
            candidates.append((RecommendationState.FINANCIALLY_WAIT, "safe payment capacity is later or requires a plan"))
        elif financial.financial_coverage_state != FinancialCoverageState.FULL:
            candidates.append((RecommendationState.NEEDS_CONFIRMATION, "authoritative finance evidence is incomplete"))
        elif financial.safe_amount_today is not None and price.current_best_price is not None and financial.safe_amount_today < price.current_best_price:
            candidates.append((RecommendationState.FINANCIALLY_WAIT, "safe-to-pay amount is below the current effective price"))
        elif price.price_signal in {"STRONG_BUY", "BUY"}:
            if price.alternative_offer is not None and price.used_best_price is not None and price.refurbished_best_price is not None:
                candidates.append((RecommendationState.CONSIDER_USED_OR_REFURBISHED, "a materially cheaper alternative condition is available"))
            candidates.append((RecommendationState.BUY_NOW, "financially safe and current price is attractive in covered history"))
        elif price.price_signal == "STRONG_WAIT":
            candidates.append((RecommendationState.HOLD_FOR_BETTER_PRICE, "current price is materially above the covered historical signal"))
        elif price.price_history_status == "INSUFFICIENT" or price.price_signal == "UNKNOWN":
            candidates.append((RecommendationState.SET_PRICE_WATCH, "history is insufficient to make a timing claim"))
        else:
            candidates.append((RecommendationState.SET_PRICE_WATCH, "affordability does not establish a good buying moment"))
        return tuple(
            DecisionCandidate(_id("candidate", f"{state.value}:{price.product_id}"), state, reason,
                              financial.financial_state, price.price_signal)
            for state, reason in candidates
        )


class GovernedDecisionService:
    def __init__(self, *, reviewer: AdversarialReviewer | None = None,
                 certifier: CertificationGate | None = None,
                 committee: DecisionCommittee | None = None,
                 veto: FinalSafetyVeto | None = None):
        self.reviewer = reviewer or LocalAdversarialReviewer()
        self.certifier = certifier or CertificationGate()
        self.committee = committee or DecisionCommittee()
        self.veto = veto or FinalSafetyVeto()
        self.synthesizer = DecisionSynthesis()

    def evaluate(self, *, request: Mapping[str, Any], product: ProductIdentity,
                 financial: FinancialSafetyResult, price: PriceIntelligenceRecord,
                 control_evidence: Mapping[str, Any], financial_input: Mapping[str, Any] | None = None,
                 financial_engine_version: str = "financial-provider-interface/1",
                 price_engine_version: str = "price-intelligence/1") -> GovernedDecisionResult:
        candidates = self.synthesizer.synthesize(financial, price)
        selected = candidates[0].recommendation if candidates else RecommendationState.NEEDS_CONFIRMATION
        product_payload = _jsonable(product)
        envelope = DecisionEvidenceEnvelope(
            decision_id=_id("decision", json.dumps({"request": request, "product": product_payload, "price": price.to_dict()}, sort_keys=True, default=str)),
            request_fingerprint=_fingerprint(request), product_fingerprint=_fingerprint(product_payload),
            financial_engine_version=financial_engine_version,
            financial_input_hash=_fingerprint(financial_input or request), financial_decision_hash=_fingerprint(financial),
            financial_safety_status=financial.financial_state.value,
            safe_amount_today=financial.safe_amount_today, payment_plan=financial.payment_plan,
            minimum_projected_balance=financial.minimum_balance, protected_minimum_balance=financial.minimum_balance,
            price_engine_version=price_engine_version, price_input_hash=_fingerprint(price.to_dict()),
            price_observation_ids=price.observation_ids, price_history_status=price.price_history_status,
            price_signal=price.price_signal, price_confidence=price.confidence,
            candidate_recommendation=selected, unresolved_evidence=tuple(str(item) for item in request.get("unresolved_evidence", ())),
            provenance={"product": product.source_provenance, "price": list(price.provenance),
                        "runtime": {"python": platform.python_version(), "implementation": sys.implementation.name},
                        "request_source": request.get("source", "local"),
                        "untrusted_request_evidence": dict(request)},
            control_evidence=dict(control_evidence), product_identity_confidence=product.identity_confidence,
            current_price=price.current_best_price,
        )
        review = self.reviewer.review(envelope)
        post_review_controls = dict(envelope.control_evidence)
        post_review_controls["adversarial_review_completed"] = True
        post_review_controls["critical_challenges_resolved"] = not review.critical_findings
        envelope = replace(envelope, control_evidence=post_review_controls)
        certification = self.certifier.certify(envelope, review)
        committee = self.committee.select(envelope, candidates, certification, review)
        release = self.veto.release(envelope, committee, certification, review, candidates)
        envelope = replace(envelope, governance_trace=("decision_synthesis", "adversarial_review", "certification_gate", "decision_committee", "deterministic_safety_veto"))
        return GovernedDecisionResult(envelope, candidates, review, certification, committee, release)


def _candidate_financially_legal(candidate: DecisionCandidate, envelope: DecisionEvidenceEnvelope) -> bool:
    if envelope.financial_safety_status == FinancialState.SAFE_NOW.value:
        return candidate.recommendation not in {RecommendationState.FINANCIALLY_WAIT, RecommendationState.NOT_RECOMMENDED}
    return candidate.recommendation in {RecommendationState.FINANCIALLY_WAIT, RecommendationState.NOT_RECOMMENDED, RecommendationState.NEEDS_CONFIRMATION}


def _fingerprint(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def _id(prefix: str, value: Any) -> str:
    return f"{prefix}_{hashlib.sha256(str(value).encode()).hexdigest()[:20]}"


def _jsonable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "__dataclass_fields__"):
        return {key: _jsonable(getattr(value, key)) for key in value.__dataclass_fields__}
    return value
