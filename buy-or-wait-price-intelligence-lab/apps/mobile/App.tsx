import React, { useCallback, useMemo, useState } from "react";
import { ActivityIndicator, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View, useWindowDimensions } from "react-native";
import * as DocumentPicker from "expo-document-picker";

import {
  confirmableCandidate,
  explainRecommendation,
  financeFixturePayload,
  governanceSummary,
  type FinanceFixture,
  type GovernedResponse,
  type IdentityCandidate,
  type IntakeMode,
  type IntakeResponse,
} from "./journey";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8001";
const DEFAULT_AS_OF = "2026-09-12T12:00:00+00:00";

type Screen = { kind: "home" } | { kind: "intake"; response: IntakeResponse } | { kind: "governed"; response: GovernedResponse; productTitle: string };
type Busy = null | "intake" | "confirm" | "governed";
type BetaDecision = {
  decision: string;
  recommended_action: string;
  price_verdict: string;
  affordability_verdict: string;
  safe_to_pay_now: string;
  earliest_financially_safe_date: string | null;
  minimum_projected_balance: string;
  price_confidence: string;
  financial_confidence: string;
  overall_confidence: string;
  financial_freshness: string;
  explanation: string;
  warnings: string[];
};

export default function App() {
  const { width } = useWindowDimensions();
  const desktop = width >= 720;
  const [query, setQuery] = useState("");
  const [screen, setScreen] = useState<Screen>({ kind: "home" });
  const [busy, setBusy] = useState<Busy>(null);
  const [error, setError] = useState<string | null>(null);
  const [finance, setFinance] = useState<FinanceFixture>("safe");
  const [financeStatus, setFinanceStatus] = useState<"disconnected" | "current" | "stale" | "incomplete">("disconnected");
  const [financeState, setFinanceState] = useState<Record<string, unknown> | null>(null);
  const [betaProduct, setBetaProduct] = useState("55-inch OLED TV");
  const [betaPrice, setBetaPrice] = useState("899.99");
  const [betaResult, setBetaResult] = useState<BetaDecision | null>(null);

  const request = useCallback(async (path: string, body: Record<string, unknown> = {}, method = "POST", authUser?: string): Promise<Record<string, unknown>> => {
    let response: Response;
    try {
      response = await fetch(`${API_BASE}${path}`, {
        method,
        headers: { "Content-Type": "application/json", ...(authUser ? { Authorization: `Bearer user:${authUser}` } : {}) },
        ...(method === "GET" ? {} : { body: JSON.stringify(body) }),
      });
    } catch (networkError) {
      throw new Error(networkError instanceof Error ? `Network error: ${networkError.message}` : "Network error");
    }
    let data: unknown;
    try {
      data = await response.json();
    } catch {
      data = null;
    }
    if (!response.ok) {
      const detail = (data && typeof data === "object" && "detail" in data && typeof (data as { detail: unknown }).detail === "string") ? (data as { detail: string }).detail : `Request failed with status ${response.status}`;
      throw new Error(detail);
    }
    return (data ?? {}) as Record<string, unknown>;
  }, []);

  const refreshFinance = useCallback(async (userId = "mobile-demo") => {
    const state = await request("/v1/state", {}, "GET", userId);
    setFinanceState(state);
    const freshness = String(state.freshness ?? "incomplete");
    setFinanceStatus(freshness === "current" || freshness === "stale" ? freshness : "incomplete");
  }, [request]);

  const connectFinances = useCallback(async () => {
    setError(null);
    try {
      try { await request("/v1/users?user_id=mobile-demo"); } catch (failure) {
        if (!(failure instanceof Error) || !failure.message.includes("409")) throw failure;
      }
      await request("/v1/profile", { home_currency: "USD", current_available_cash: "0", minimum_balance_to_keep: "0", payment_methods: ["full_payment", "wait", "partial_payment"] }, "PUT", "mobile-demo");
      await refreshFinance();
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : "Could not connect financial state.");
    }
  }, [refreshFinance, request]);

  const runBetaDecision = useCallback(async () => {
    setError(null); setBetaResult(null); setBusy("governed");
    try {
      const raw = await request("/v1/buy-or-wait", { product_name: betaProduct.trim(), price: betaPrice.trim(), currency: "USD", category: "electronics", allows_partial_payment: true, price_context: {} }, "POST", "mobile-demo");
      setBetaResult(raw as unknown as BetaDecision);
      await refreshFinance();
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : "Buy-or-wait evaluation failed.");
    } finally { setBusy(null); }
  }, [betaPrice, betaProduct, refreshFinance, request]);

  const importStatement = useCallback(async () => {
    setError(null);
    try {
      await connectFinances();
      const picked = await DocumentPicker.getDocumentAsync({ type: ["text/csv", "application/vnd.ms-ofx", "application/x-ofx", "application/qfx", "text/plain"], copyToCacheDirectory: true });
      if (picked.canceled || !picked.assets?.[0]) return;
      const asset = picked.assets[0];
      const form = new FormData();
      form.append("file", { uri: asset.uri, name: asset.name, type: asset.mimeType ?? "text/csv" } as unknown as Blob);
      const response = await fetch(`${API_BASE}/v1/imports/transactions`, { method: "POST", headers: { Authorization: "Bearer user:mobile-demo" }, body: form });
      if (!response.ok) throw new Error(`Statement import failed with status ${response.status}`);
      await refreshFinance();
    } catch (failure) { setError(failure instanceof Error ? failure.message : "Statement import failed."); }
  }, [connectFinances, refreshFinance]);

  const startIntake = useCallback(async (mode: IntakeMode) => {
    setError(null);
    if (mode !== "barcode" && !query.trim()) {
      // Barcode has a demo default; other modes require an input to avoid noisy 422s.
      setError("Enter a barcode, product URL, image reference, or search text first.");
      return;
    }
    setBusy("intake");
    try {
      const endpoint = mode === "barcode" ? "/v1/intake/barcode" : mode === "url" ? "/v1/intake/url" : mode === "photo" ? "/v1/intake/photo" : "/v1/intake/search";
      const body: Record<string, unknown> =
        mode === "barcode" ? { barcode: query.trim() || "036000291452" } :
        mode === "url" ? { product_url: query.trim() } :
        mode === "photo" ? { image_ref: query.trim() } :
        { query_text: query.trim() };
      const raw = (await request(endpoint, body)) as unknown as IntakeResponse;
      if (raw.state === "exact" && raw.product_id) {
        await runGoverned(raw.product_id, raw.product?.title ?? "Product");
      } else {
        setScreen({ kind: "intake", response: raw });
      }
    } catch (fail) {
      setError(fail instanceof Error ? fail.message : "Intake failed.");
    } finally {
      setBusy(null);
    }
  }, [query, request]);

  const runGoverned = useCallback(async (productId: string, productTitle: string) => {
    setError(null);
    setBusy("governed");
    try {
      const payload = financeFixturePayload(finance, DEFAULT_AS_OF);
      const raw = (await request(`/v1/products/${encodeURIComponent(productId)}/governed-evaluate`, payload)) as unknown as GovernedResponse;
      setScreen({ kind: "governed", response: raw, productTitle });
    } catch (fail) {
      setError(fail instanceof Error ? fail.message : "Governed evaluation failed.");
    } finally {
      setBusy(null);
    }
  }, [finance, request]);

  const confirmCandidate = useCallback(async (candidate: IdentityCandidate) => {
    const gate = confirmableCandidate({ state: "needs_confirmation", reason_codes: [], candidates: [candidate] });
    if (!gate) {
      setError("This candidate does not carry a strong identifier (GTIN or ASIN); confirmation is not available.");
      return;
    }
    setError(null);
    setBusy("confirm");
    try {
      const endpoint = gate.method === "barcode" ? "/v1/intake/barcode" : "/v1/intake/url";
      const body: Record<string, unknown> = gate.method === "barcode" ? { barcode: gate.identifier, user_confirmed: true } : { product_url: gate.identifier, user_confirmed: true };
      const raw = (await request(endpoint, body)) as unknown as IntakeResponse;
      if (raw.state !== "exact" || !raw.product_id) {
        setScreen({ kind: "intake", response: raw });
        return;
      }
      await runGoverned(raw.product_id, raw.product?.title ?? candidate.product.title);
    } catch (fail) {
      setError(fail instanceof Error ? fail.message : "Confirmation failed.");
    } finally {
      setBusy(null);
    }
  }, [request, runGoverned]);

  const reset = useCallback(() => {
    setScreen({ kind: "home" });
    setError(null);
  }, []);

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={[styles.scroll, desktop && styles.scrollDesktop]}>
        <View style={[styles.container, desktop && styles.containerDesktop]}>
          <FixtureBanner />
          <Text style={styles.eyebrow}>BUY OR WAIT?</Text>
          <Text style={styles.title}>Make the next purchase a safer one.</Text>
          <Text style={styles.subtitle}>Identify the exact item, check the price, then respect your financial safety boundary.</Text>

          <FinancePicker value={finance} onChange={setFinance} disabled={busy !== null} />

          <BetaFinancePanel status={financeStatus} state={financeState} product={betaProduct} price={betaPrice} result={betaResult} busy={busy !== null} onConnect={connectFinances} onImport={importStatement} onRefresh={() => refreshFinance()} onProduct={setBetaProduct} onPrice={setBetaPrice} onEvaluate={runBetaDecision} />

          <TextInput
            value={query}
            onChangeText={setQuery}
            placeholder="Barcode, link, image ref, or product search"
            placeholderTextColor="#7f91a8"
            style={styles.input}
            autoCapitalize="none"
            editable={busy === null}
          />
          <View style={[styles.grid, desktop && styles.gridDesktop]}>
            <Action label="Scan barcode" hint="Uses demo 036000291452 if empty" icon="▦" disabled={busy !== null} onPress={() => startIntake("barcode")} />
            <Action label="Take photo" hint="Enter image ref above" icon="◉" disabled={busy !== null} onPress={() => startIntake("photo")} />
            <Action label="Paste / share link" hint="Paste product URL above" icon="↗" disabled={busy !== null} onPress={() => startIntake("url")} />
            <Action label="Search item" hint="Enter product text above" icon="⌕" disabled={busy !== null} onPress={() => startIntake("search")} />
          </View>

          {busy && (
            <View style={styles.busyCard} accessibilityLiveRegion="polite">
              <ActivityIndicator color="#8be9c1" />
              <Text style={styles.busyText}>{busy === "intake" ? "Identifying product…" : busy === "confirm" ? "Confirming candidate…" : "Running governed evaluation…"}</Text>
            </View>
          )}

          {error && (
            <View style={styles.errorCard} accessibilityRole="alert">
              <Text style={styles.errorLabel}>SOMETHING WENT WRONG</Text>
              <Text style={styles.errorBody}>{error}</Text>
              <Pressable onPress={() => setError(null)} style={styles.secondaryButton}><Text style={styles.secondaryButtonText}>Dismiss</Text></Pressable>
            </View>
          )}

          {screen.kind === "intake" && (
            <IntakeResultCard response={screen.response} busy={busy !== null} onConfirm={confirmCandidate} onRestart={reset} />
          )}

          {screen.kind === "governed" && (
            <GovernedResultView response={screen.response} productTitle={screen.productTitle} onRestart={reset} desktop={desktop} />
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

function Action({ label, hint, icon, onPress, disabled }: { label: string; hint: string; icon: string; onPress: () => void; disabled: boolean }) {
  return (
    <Pressable onPress={onPress} disabled={disabled} style={({ pressed }) => [styles.action, pressed && styles.pressed, disabled && styles.disabled]}>
      <Text style={styles.actionIcon}>{icon}</Text>
      <View>
        <Text style={styles.actionText}>{label}</Text>
        <Text style={styles.actionHint}>{hint}</Text>
      </View>
    </Pressable>
  );
}

function FixtureBanner() {
  return (
    <View style={styles.fixtureBanner} accessibilityLabel="Fixture demo mode">
      <Text style={styles.fixtureLabel}>LEGACY DEMO LANE</Text>
      <Text style={styles.fixtureBody}>The original governed fixture journey remains for regression. Use the beta panel below for the real finance API and your authenticated financial state.</Text>
    </View>
  );
}

function BetaFinancePanel({ status, state, product, price, result, busy, onConnect, onImport, onRefresh, onProduct, onPrice, onEvaluate }: { status: string; state: Record<string, unknown> | null; product: string; price: string; result: BetaDecision | null; busy: boolean; onConnect: () => void; onImport: () => void; onRefresh: () => void; onProduct: (value: string) => void; onPrice: (value: string) => void; onEvaluate: () => void }) {
  const connected = status !== "disconnected";
  return <View style={styles.betaPanel} accessibilityLabel="Real finance beta loop">
    <Text style={styles.financePickerLabel}>REAL FINANCE BETA</Text>
    <Text style={styles.betaBody}>Connect or import your financial state, then evaluate a purchase with separate price and affordability reasoning.</Text>
    <View style={styles.betaStatusRow}>
      <Text style={styles.betaStatus}>Finance: {status}</Text>
      <View style={styles.betaActions}><Pressable onPress={connected ? onRefresh : onConnect} disabled={busy} style={styles.secondaryButton}><Text style={styles.secondaryButtonText}>{connected ? "Refresh state" : "Connect finances"}</Text></Pressable><Pressable onPress={onImport} disabled={busy} style={styles.secondaryButton}><Text style={styles.secondaryButtonText}>Import statement</Text></Pressable></View>
    </View>
    {state && <Text style={styles.actionHint}>Available cash {String(state.available_cash ?? "—")} · reserve {String(state.minimum_balance ?? "—")} · as of {String(state.financial_data_as_of ?? "not synced")}</Text>}
    <TextInput value={product} onChangeText={onProduct} placeholder="What are you considering?" placeholderTextColor="#7f91a8" style={styles.betaInput} />
    <TextInput value={price} onChangeText={onPrice} keyboardType="decimal-pad" placeholder="Price in USD" placeholderTextColor="#7f91a8" style={styles.betaInput} />
    <Pressable onPress={onEvaluate} disabled={!connected || busy} style={[styles.primaryButton, (!connected || busy) && styles.disabled]}><Text style={styles.primaryButtonText}>Run Buy-or-Wait</Text></Pressable>
    {result && <View style={styles.betaResult}><Text style={styles.cardLabel}>COMBINED RECOMMENDATION</Text><Text style={styles.decision}>{result.decision.replaceAll("_", " ")}</Text><Text style={styles.cardBody}>{result.explanation}</Text><Text style={styles.rowSub}>Price {result.price_verdict} ({result.price_confidence}) · finances {result.affordability_verdict} ({result.financial_confidence}) · freshness {result.financial_freshness}</Text><Text style={styles.rowSub}>Safe now {result.safe_to_pay_now} · safe full payment {result.earliest_financially_safe_date ?? "not within forecast"}</Text>{result.warnings.map(warning => <Text key={warning} style={styles.warning}>{warning}</Text>)}</View>}
  </View>;
}

function FinancePicker({ value, onChange, disabled }: { value: FinanceFixture; onChange: (v: FinanceFixture) => void; disabled: boolean }) {
  const options: { value: FinanceFixture; label: string; description: string }[] = [
    { value: "safe", label: "Safe budget", description: "Fixture: safe_now, safe amount today $2,000" },
    { value: "constrained", label: "Constrained", description: "Fixture: safe_later, waits for next paycheque" },
    { value: "unsafe", label: "Unsafe", description: "Fixture: not_affordable, minimum balance protected" },
  ];
  return (
    <View style={styles.financePicker}>
      <Text style={styles.financePickerLabel}>DEMO FINANCIAL POSTURE</Text>
      <View style={styles.financePickerRow}>
        {options.map(option => {
          const active = option.value === value;
          return (
            <Pressable key={option.value} onPress={() => onChange(option.value)} disabled={disabled} style={[styles.financeChip, active && styles.financeChipActive, disabled && styles.disabled]}>
              <Text style={[styles.financeChipLabel, active && styles.financeChipLabelActive]}>{option.label}</Text>
              <Text style={[styles.financeChipHint, active && styles.financeChipHintActive]}>{option.description}</Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

function IntakeResultCard({ response, busy, onConfirm, onRestart }: { response: IntakeResponse; busy: boolean; onConfirm: (candidate: IdentityCandidate) => void; onRestart: () => void }) {
  if (response.state === "unresolved") {
    return (
      <View style={styles.card}>
        <Text style={styles.cardLabel}>UNRESOLVED IDENTITY</Text>
        <Text style={styles.decision}>Could not identify item.</Text>
        <Text style={styles.cardBody}>Adjust your input and try again. The identity gate does not silently promote unknown items into a decision.</Text>
        <ReasonRow reasons={response.reason_codes} />
        <Pressable onPress={onRestart} style={styles.primaryButton}><Text style={styles.primaryButtonText}>Try another intake</Text></Pressable>
      </View>
    );
  }
  const candidates = response.candidates ?? [];
  return (
    <View style={styles.card}>
      <Text style={styles.cardLabel}>NEEDS CONFIRMATION</Text>
      <Text style={styles.decision}>Is this the right item?</Text>
      <Text style={styles.cardBody}>The identity gate wants a human check before we spend any evaluation on this product. Select the exact match to continue.</Text>
      <ReasonRow reasons={response.reason_codes} />
      {candidates.map(candidate => {
        const gate = confirmableCandidate({ state: "needs_confirmation", reason_codes: [], candidates: [candidate] });
        return (
          <View key={candidate.product.gtin ?? candidate.product.asin ?? candidate.product.title} style={styles.candidate}>
            <Text style={styles.candidateTitle}>{candidate.product.title}</Text>
            <Text style={styles.candidateMeta}>{describeIdentity(candidate.product)}</Text>
            <Text style={styles.candidateMeta}>Match score {candidate.score} · {candidate.evidence.join(", ")}</Text>
            {gate ? (
              <Pressable onPress={() => onConfirm(candidate)} disabled={busy} style={[styles.primaryButton, busy && styles.disabled]}>
                <Text style={styles.primaryButtonText}>Yes, this is the item</Text>
              </Pressable>
            ) : (
              <Text style={styles.candidateBlocked}>Cannot confirm — this candidate has no GTIN or ASIN to lock the identity.</Text>
            )}
          </View>
        );
      })}
      <Pressable onPress={onRestart} style={styles.secondaryButton}><Text style={styles.secondaryButtonText}>Cancel and search again</Text></Pressable>
    </View>
  );
}

function GovernedResultView({ response, productTitle, onRestart, desktop }: { response: GovernedResponse; productTitle: string; onRestart: () => void; desktop: boolean }) {
  const price = response.price_intelligence;
  const envelope = response.governance.envelope;
  const summary = useMemo(() => governanceSummary(response), [response]);
  const explanation = useMemo(() => explainRecommendation(response), [response]);
  const currency = "$";
  const priceRows: [string, string | null][] = [
    ["Current best price", price.current_best_price ? `${currency}${price.current_best_price}` : null],
    ["Historical low", price.historical_low ? `${currency}${price.historical_low}` : null],
    ["Historical high", price.historical_high ? `${currency}${price.historical_high}` : null],
    ["Historical average", price.historical_average ? `${currency}${Number(price.historical_average).toFixed(2)}` : null],
    ["Current percentile", price.price_percentile ? `${Number(price.price_percentile).toFixed(1)}%` : null],
    ["Trend", price.price_trend],
    ["History status", price.price_history_status],
    ["Price signal", price.price_signal],
    ["Observations", `${price.observation_count} in ${price.history_window_days} days`],
    ["Used offer", price.used_best_price ? `${currency}${price.used_best_price}` : null],
    ["Refurbished offer", price.refurbished_best_price ? `${currency}${price.refurbished_best_price}` : null],
  ];
  const financeRows: [string, string | null][] = [
    ["Financial state", response.financial_state.replaceAll("_", " ")],
    ["Safe amount today", envelope.safe_amount_today ? `${currency}${envelope.safe_amount_today}` : null],
    ["Protected minimum", envelope.protected_minimum_balance ? `${currency}${envelope.protected_minimum_balance}` : null],
    ["Finance-limited", (envelope.safe_amount_today !== null && envelope.current_price !== null && Number(envelope.safe_amount_today) < Number(envelope.current_price)) ? "Yes — safe amount below current price" : "No"],
  ];
  return (
    <View style={styles.card}>
      <Text style={styles.cardLabel}>GOVERNED RECOMMENDATION</Text>
      <Text style={styles.decision}>{formatRecommendation(response.recommendation)}</Text>
      <Text style={styles.cardBody}>{explanation}</Text>

      <SectionTitle>Product</SectionTitle>
      <Text style={styles.rowValue}>{productTitle}</Text>
      <Text style={styles.rowSub}>{describeIdentity(price)}</Text>

      <SectionTitle>Price intelligence</SectionTitle>
      <KeyValueGrid rows={priceRows} desktop={desktop} />

      <SectionTitle>Financial safety</SectionTitle>
      <KeyValueGrid rows={financeRows} desktop={desktop} />

      <SectionTitle>Governance</SectionTitle>
      <View style={styles.badgeRow}>
        <StatusBadge label="Reviewer" ok={summary.reviewer_passed} detail={response.governance.review.status} />
        <StatusBadge label="Certification" ok={summary.certification_passed} detail={response.governance.certification.status} />
        <StatusBadge label="Committee" ok={summary.committee_passed} detail={response.governance.committee.status} />
        <StatusBadge label="Final veto" ok={summary.final_safety_veto_passed} detail={summary.release_status} />
      </View>
      {response.governance.release.reason_codes.length > 0 && (
        <Text style={styles.rowSub}>Release: {response.governance.release.reason_codes.join(", ")}</Text>
      )}

      <SectionTitle>Raw reason codes</SectionTitle>
      <ReasonRow reasons={[...response.governance.review.critical_findings, ...response.governance.review.major_findings, ...response.governance.review.minor_findings, ...response.governance.release.reason_codes]} fallback="No adversarial findings recorded." />

      <Pressable onPress={onRestart} style={styles.primaryButton}><Text style={styles.primaryButtonText}>Start another purchase</Text></Pressable>
      <Text style={styles.footer}>Decision id · {response.decision_id}</Text>
      <Text style={styles.footer}>Mode · {response.mode}</Text>
    </View>
  );
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return <Text style={styles.sectionTitle}>{children}</Text>;
}

function KeyValueGrid({ rows, desktop }: { rows: [string, string | null][]; desktop: boolean }) {
  return (
    <View style={[styles.kvGrid, desktop && styles.kvGridDesktop]}>
      {rows.map(([label, value]) => (
        <View key={label} style={styles.kvRow}>
          <Text style={styles.kvLabel}>{label}</Text>
          <Text style={styles.kvValue}>{value ?? "—"}</Text>
        </View>
      ))}
    </View>
  );
}

function StatusBadge({ label, ok, detail }: { label: string; ok: boolean; detail: string }) {
  return (
    <View style={[styles.badge, ok ? styles.badgeOk : styles.badgeFail]}>
      <Text style={styles.badgeTop}>{label}</Text>
      <Text style={styles.badgeBottom}>{ok ? "PASS" : "BLOCKED"}</Text>
      <Text style={styles.badgeDetail}>{detail}</Text>
    </View>
  );
}

function ReasonRow({ reasons, fallback }: { reasons: readonly string[]; fallback?: string }) {
  if (!reasons.length) return fallback ? <Text style={styles.reason}>{fallback}</Text> : null;
  return <Text style={styles.reason}>{reasons.join(" · ")}</Text>;
}

function describeIdentity(product: { title?: string; brand?: string | null; model?: string | null; gtin?: string | null; asin?: string | null; variant?: Record<string, string> | null; product_id?: string }): string {
  const parts: string[] = [];
  if (product.brand) parts.push(product.brand);
  if (product.model) parts.push(product.model);
  if (product.variant) {
    for (const [k, v] of Object.entries(product.variant)) parts.push(`${k}: ${v}`);
  }
  if (product.gtin) parts.push(`GTIN ${product.gtin}`);
  else if (product.asin) parts.push(`ASIN ${product.asin}`);
  return parts.length ? parts.join(" · ") : "No detailed identity fields returned.";
}

function formatRecommendation(rec: string): string {
  return rec.replaceAll("_", " ");
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#0d1726" },
  scroll: { flexGrow: 1 },
  scrollDesktop: { alignItems: "center" },
  container: { padding: 24, gap: 16, width: "100%" },
  containerDesktop: { maxWidth: 900 },
  eyebrow: { color: "#8be9c1", letterSpacing: 2, fontWeight: "700", fontSize: 12 },
  title: { color: "#f7fbff", fontSize: 34, fontWeight: "800", lineHeight: 39 },
  subtitle: { color: "#b8c6d9", fontSize: 16, lineHeight: 24 },
  input: { backgroundColor: "#18263a", color: "#f7fbff", borderColor: "#2c405c", borderWidth: 1, borderRadius: 12, padding: 16, fontSize: 16 },
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 12 },
  gridDesktop: { justifyContent: "flex-start" },
  action: { backgroundColor: "#f7fbff", borderRadius: 14, padding: 16, minHeight: 116, width: "48%", justifyContent: "space-between" },
  pressed: { opacity: 0.75 },
  disabled: { opacity: 0.5 },
  actionIcon: { color: "#17304d", fontSize: 28 },
  actionText: { color: "#17304d", fontSize: 15, fontWeight: "700" },
  actionHint: { color: "#446", fontSize: 12, marginTop: 4 },
  busyCard: { backgroundColor: "#152741", borderRadius: 14, padding: 16, flexDirection: "row", alignItems: "center", gap: 12 },
  busyText: { color: "#d6e3f2", fontSize: 15 },
  errorCard: { backgroundColor: "#4b1c22", borderRadius: 14, padding: 16, gap: 8, borderColor: "#f26b70", borderWidth: 1 },
  errorLabel: { color: "#f9d0d3", letterSpacing: 2, fontWeight: "700", fontSize: 12 },
  errorBody: { color: "#f7fbff", fontSize: 15 },
  fixtureBanner: { backgroundColor: "#1b3d54", borderRadius: 14, padding: 12, borderColor: "#2c5874", borderWidth: 1 },
  fixtureLabel: { color: "#8be9c1", letterSpacing: 2, fontWeight: "700", fontSize: 11 },
  fixtureBody: { color: "#b8c6d9", fontSize: 13, marginTop: 4 },
  financePicker: { gap: 8 },
  financePickerLabel: { color: "#8be9c1", letterSpacing: 2, fontWeight: "700", fontSize: 11 },
  financePickerRow: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  financeChip: { backgroundColor: "#18263a", borderColor: "#2c405c", borderWidth: 1, borderRadius: 10, padding: 10, minWidth: 180, flexGrow: 1 },
  financeChipActive: { borderColor: "#8be9c1", backgroundColor: "#1e3852" },
  financeChipLabel: { color: "#f7fbff", fontSize: 14, fontWeight: "700" },
  financeChipLabelActive: { color: "#8be9c1" },
  financeChipHint: { color: "#9db2c9", fontSize: 12, marginTop: 4 },
  financeChipHintActive: { color: "#d6e3f2" },
  betaPanel: { backgroundColor: "#102d2b", borderRadius: 16, padding: 18, gap: 10, borderColor: "#3fa787", borderWidth: 1 },
  betaBody: { color: "#d6e3f2", fontSize: 14, lineHeight: 20 },
  betaStatusRow: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", gap: 12 },
  betaStatus: { color: "#8be9c1", fontWeight: "700", textTransform: "uppercase", fontSize: 12 },
  betaActions: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  betaInput: { backgroundColor: "#18263a", color: "#f7fbff", borderColor: "#2c5874", borderWidth: 1, borderRadius: 10, padding: 12, fontSize: 15 },
  betaResult: { backgroundColor: "#183a2f", borderRadius: 12, padding: 14, gap: 5, borderColor: "#3fa787", borderWidth: 1 },
  warning: { color: "#f4b47a", fontSize: 12, lineHeight: 18 },
  card: { backgroundColor: "#18334a", borderRadius: 16, padding: 20, gap: 8, borderColor: "#2c5874", borderWidth: 1 },
  cardLabel: { color: "#8be9c1", fontSize: 12, letterSpacing: 2, fontWeight: "700" },
  decision: { color: "#ffffff", fontSize: 26, fontWeight: "800" },
  cardBody: { color: "#d6e3f2", fontSize: 15, lineHeight: 22 },
  reason: { color: "#9db2c9", fontSize: 12, lineHeight: 18 },
  primaryButton: { backgroundColor: "#8be9c1", borderRadius: 12, padding: 14, alignItems: "center" },
  primaryButtonText: { color: "#0d1726", fontSize: 15, fontWeight: "700" },
  secondaryButton: { backgroundColor: "transparent", borderColor: "#8be9c1", borderWidth: 1, borderRadius: 12, padding: 12, alignItems: "center" },
  secondaryButtonText: { color: "#8be9c1", fontSize: 14, fontWeight: "700" },
  candidate: { backgroundColor: "#122a3d", borderRadius: 12, padding: 14, gap: 6, borderColor: "#26445f", borderWidth: 1 },
  candidateTitle: { color: "#f7fbff", fontSize: 16, fontWeight: "700" },
  candidateMeta: { color: "#a9b9cc", fontSize: 13 },
  candidateBlocked: { color: "#f4b47a", fontSize: 12 },
  sectionTitle: { color: "#8be9c1", fontSize: 12, letterSpacing: 2, fontWeight: "700", marginTop: 8 },
  rowValue: { color: "#f7fbff", fontSize: 16, fontWeight: "700" },
  rowSub: { color: "#a9b9cc", fontSize: 13 },
  kvGrid: { flexDirection: "column", gap: 4 },
  kvGridDesktop: { flexDirection: "row", flexWrap: "wrap", columnGap: 24, rowGap: 4 },
  kvRow: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 4, minWidth: 260, flexBasis: "auto" },
  kvLabel: { color: "#9db2c9", fontSize: 13 },
  kvValue: { color: "#f7fbff", fontSize: 13, fontWeight: "700" },
  badgeRow: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  badge: { paddingVertical: 10, paddingHorizontal: 12, borderRadius: 12, minWidth: 130, borderWidth: 1 },
  badgeOk: { backgroundColor: "#183a2f", borderColor: "#3fa787" },
  badgeFail: { backgroundColor: "#4b1c22", borderColor: "#f26b70" },
  badgeTop: { color: "#c8dccf", fontSize: 11, letterSpacing: 1, fontWeight: "700" },
  badgeBottom: { color: "#ffffff", fontSize: 15, fontWeight: "800", marginTop: 2 },
  badgeDetail: { color: "#a9b9cc", fontSize: 11, marginTop: 2 },
  footer: { color: "#5f7898", fontSize: 11 },
});
