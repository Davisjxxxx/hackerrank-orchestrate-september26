// Pure helpers for the Buy or Wait? mobile journey. Kept side-effect-free so
// the confirmation gate and rendered decision can be tested without a device
// or a running backend. All financial arithmetic still lives in the API.

export type IntakeMode = "barcode" | "photo" | "url" | "search";
export type IntakeState = "exact" | "needs_confirmation" | "unresolved";

export type ProductIdentity = {
  title: string;
  brand?: string | null;
  model?: string | null;
  gtin?: string | null;
  asin?: string | null;
  mpn?: string | null;
  variant?: Record<string, string> | null;
  identity_confidence?: string | number | null;
  identity_evidence?: readonly string[] | null;
  source_provenance?: string | null;
};

export type IdentityCandidate = {
  product: ProductIdentity;
  score: number;
  evidence: readonly string[];
};

export type IntakeResponse = {
  state: IntakeState;
  product_id?: string;
  product?: ProductIdentity;
  candidates?: readonly IdentityCandidate[];
  reason_codes: readonly string[];
  normalized_input?: Record<string, unknown>;
};

export type PriceIntelligence = {
  product_id: string;
  current_best_price: string | null;
  current_offer_count: number;
  historical_low: string | null;
  historical_high: string | null;
  historical_average: string | null;
  observation_count: number;
  history_window_days: number;
  price_percentile: string | null;
  price_trend: string;
  used_best_price: string | null;
  refurbished_best_price: string | null;
  price_history_status: "SUFFICIENT" | "INSUFFICIENT" | "UNAVAILABLE";
  price_signal: "STRONG_BUY" | "BUY" | "NEUTRAL" | "WAIT" | "STRONG_WAIT" | "UNKNOWN";
  confidence: string;
  provenance: readonly string[];
  observation_ids: readonly string[];
};

export type GovernanceReport = {
  envelope: {
    decision_id: string;
    financial_safety_status: string;
    safe_amount_today: string | null;
    minimum_projected_balance: string | null;
    protected_minimum_balance: string | null;
    current_price: string | null;
    price_signal: string;
    price_history_status: string;
    product_identity_confidence: string;
    unresolved_evidence: readonly string[];
    governance_trace: readonly string[];
  };
  review: {
    status: "PASS" | "CHALLENGED" | "ABSTAIN";
    critical_findings: readonly string[];
    major_findings: readonly string[];
    minor_findings: readonly string[];
    recommended_action: string;
  };
  certification: {
    status: "CERTIFIED" | "CERTIFICATION_FAILED";
    missing_evidence: readonly string[];
    verified_evidence: readonly string[];
    reason: string;
  };
  committee: {
    status: "APPROVED" | "REJECTED" | "ABSTAIN" | "ESCALATE";
    selected_candidate: string | null;
    selection_reason: string;
  };
  release: {
    status: "RELEASED" | "RELEASE_BLOCKED";
    selected_candidate: string | null;
    reason_codes: readonly string[];
  };
};

export type GovernedResponse = {
  decision_id: string;
  product_id: string;
  recommendation:
    | "BUY_NOW"
    | "HOLD_FOR_BETTER_PRICE"
    | "SET_PRICE_WATCH"
    | "CONSIDER_USED_OR_REFURBISHED"
    | "FINANCIALLY_WAIT"
    | "NOT_RECOMMENDED"
    | "NEEDS_CONFIRMATION";
  financial_state: "safe_now" | "safe_with_plan" | "safe_later" | "not_affordable";
  price_intelligence: PriceIntelligence;
  governance: GovernanceReport;
  mode: string;
};

export type FinanceFixture = "safe" | "constrained" | "unsafe";

export type IntakeStep =
  | { kind: "idle" }
  | { kind: "intake_result"; response: IntakeResponse }
  | { kind: "confirmed"; product_id: string; product: ProductIdentity }
  | { kind: "governed"; response: GovernedResponse }
  | { kind: "error"; message: string; retryable: boolean };

// Deterministic mapping of the fixture-mode finance selection into the exact
// EvaluatePayload fields that the server-side FixtureFinancialSafetyProvider
// consumes. The frontend performs no financial arithmetic; these values are
// documented demo inputs, not projections. The current fixture price is $899;
// the safe budget shape mirrors that expected user posture for each demo case.
export function financeFixturePayload(fixture: FinanceFixture, asOfIso: string): Record<string, unknown> {
  const base = {
    urgency: "flexible",
    max_wait_days: 60,
    accepted_conditions: ["new"],
    minimum_savings_dollars: "25",
    minimum_savings_fraction: "0.08",
    financial_coverage_state: "full",
    as_of: asOfIso,
  };
  if (fixture === "safe") {
    return {
      ...base,
      financial_state: "safe_now",
      safe_amount_today: "2000",
      financial_reason_codes: ["FIXTURE_SAFE_NOW"],
    };
  }
  if (fixture === "constrained") {
    return {
      ...base,
      financial_state: "safe_later",
      safe_amount_today: "400",
      earliest_safe_full_payment_date: incrementIsoMonth(asOfIso, 1),
      recommended_payment_method: "wait",
      payment_plan: { note: "fixture: wait until next payroll" },
      financial_reason_codes: ["FIXTURE_SAFE_LATER"],
    };
  }
  return {
    ...base,
    financial_state: "not_affordable",
    safe_amount_today: "50",
    financial_reason_codes: ["FIXTURE_MINIMUM_BALANCE_PROTECTED"],
  };
}

function incrementIsoMonth(iso: string, months: number): string {
  const d = new Date(iso);
  d.setUTCMonth(d.getUTCMonth() + months);
  return d.toISOString();
}

// Confirmation is only allowed to progress a NEEDS_CONFIRMATION top candidate
// that carries a strong identifier (GTIN or ASIN). Anything weaker must stay
// gated and stay visibly ambiguous to the user rather than silently promoted.
export function confirmableCandidate(response: IntakeResponse): {
  candidate: IdentityCandidate;
  method: "barcode" | "url";
  identifier: string;
} | null {
  if (response.state !== "needs_confirmation") return null;
  const list = response.candidates ?? [];
  if (!list.length) return null;
  const top = list[0];
  if (top.product.gtin) {
    return { candidate: top, method: "barcode", identifier: top.product.gtin };
  }
  if (top.product.asin) {
    return {
      candidate: top,
      method: "url",
      identifier: `https://www.amazon.com/dp/${top.product.asin}`,
    };
  }
  return null;
}

// Present a short, human-friendly reason drawn from the governance envelope
// and price/financial signals. Raw reason codes remain available separately
// for auditability.
export function explainRecommendation(response: GovernedResponse): string {
  const rec = response.recommendation;
  const price = response.price_intelligence;
  const cur = price.current_best_price ? `$${price.current_best_price}` : "the current offer";
  const lo = price.historical_low ? `$${price.historical_low}` : "prior lows";
  if (rec === "BUY_NOW") return `Finances are safe now and ${cur} is attractive against the covered history (low ${lo}).`;
  if (rec === "CONSIDER_USED_OR_REFURBISHED") return `A materially cheaper used or refurbished offer is available; new-condition timing is neutral.`;
  if (rec === "HOLD_FOR_BETTER_PRICE") return `${cur} is materially above the covered historical signal (low ${lo}, trend ${price.price_trend}). Waiting is favored.`;
  if (rec === "SET_PRICE_WATCH") return `Price history is not decisive right now (status ${price.price_history_status}, signal ${price.price_signal}). Watching for a drop is safer than acting on ambiguous timing.`;
  if (rec === "FINANCIALLY_WAIT") return `Financial safety does not clear paying ${cur} today. Wait or plan the payment before revisiting the timing question.`;
  if (rec === "NOT_RECOMMENDED") return `Neither the finances nor the price allow a safe purchase within the forecast window.`;
  return `Product identity or evidence is incomplete; confirm before proceeding.`;
}

// Governance panel summary derives directly from the four fail-closed stages;
// display never reinterprets the release verdict.
export type GovernanceSummary = {
  reviewer_passed: boolean;
  certification_passed: boolean;
  committee_passed: boolean;
  final_safety_veto_passed: boolean;
  release_status: string;
};

export function governanceSummary(response: GovernedResponse): GovernanceSummary {
  const g = response.governance;
  return {
    reviewer_passed: g.review.status === "PASS" && g.review.critical_findings.length === 0,
    certification_passed: g.certification.status === "CERTIFIED",
    committee_passed: g.committee.status === "APPROVED",
    final_safety_veto_passed: g.release.status === "RELEASED",
    release_status: g.release.status,
  };
}
