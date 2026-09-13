import React, { useState } from "react";
import { ActivityIndicator, Alert, Pressable, SafeAreaView, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";

type IntakeMode = "barcode" | "photo" | "url" | "search";
type IntakeResponse = { state: string; product_id?: string; product?: { title: string; variant?: Record<string, string> }; reason_codes: string[] };
type DecisionResponse = { combined_decision: string; reason_codes: string[]; evidence: Record<string, unknown> };

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "http://localhost:8000";

export default function App() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<IntakeResponse | DecisionResponse | null>(null);

  async function intake(mode: IntakeMode) {
    setLoading(true);
    try {
      const endpoint = mode === "barcode" ? "/v1/intake/barcode" : mode === "url" ? "/v1/intake/url" : mode === "photo" ? "/v1/intake/photo" : "/v1/intake/search";
      const body = mode === "barcode" ? { barcode: query } : mode === "url" ? { product_url: query } : mode === "photo" ? { image_ref: query } : { query_text: query };
      const response = await fetch(`${API_BASE}${endpoint}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail ?? "Intake failed");
      setResult(data);
    } catch (error) {
      Alert.alert("Could not identify item", error instanceof Error ? error.message : "Try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.eyebrow}>BUY OR WAIT?</Text>
        <Text style={styles.title}>Make the next purchase a safer one.</Text>
        <Text style={styles.subtitle}>Identify the exact item, check the price, then respect your financial safety boundary.</Text>
        <TextInput value={query} onChangeText={setQuery} placeholder="Barcode, link, or product search" placeholderTextColor="#7f91a8" style={styles.input} autoCapitalize="none" />
        <View style={styles.grid}>
          <Action label="Scan barcode" icon="▦" onPress={() => intake("barcode")} />
          <Action label="Take photo" icon="◉" onPress={() => intake("photo")} />
          <Action label="Paste / share link" icon="↗" onPress={() => intake("url")} />
          <Action label="Search item" icon="⌕" onPress={() => intake("search")} />
        </View>
        {loading && <ActivityIndicator color="#8be9c1" style={styles.spinner} />}
        {result && <DecisionCard result={result} />}
      </ScrollView>
    </SafeAreaView>
  );
}

function Action({ label, icon, onPress }: { label: string; icon: string; onPress: () => void }) {
  return <Pressable onPress={onPress} style={({ pressed }) => [styles.action, pressed && styles.pressed]}><Text style={styles.actionIcon}>{icon}</Text><Text style={styles.actionText}>{label}</Text></Pressable>;
}

function DecisionCard({ result }: { result: IntakeResponse | DecisionResponse }) {
  const decision = "combined_decision" in result ? result.combined_decision.replaceAll("_", " ").toUpperCase() : result.state.replaceAll("_", " ").toUpperCase();
  return <View style={styles.card}><Text style={styles.cardLabel}>RESULT</Text><Text style={styles.decision}>{decision}</Text><Text style={styles.cardBody}>{"product" in result && result.product ? result.product.title : "Identity and safety evidence are kept with the decision."}</Text><Text style={styles.reason}>{result.reason_codes.join(" · ")}</Text></View>;
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: "#0d1726" },
  container: { padding: 24, gap: 16 },
  eyebrow: { color: "#8be9c1", letterSpacing: 2, fontWeight: "700", fontSize: 12 },
  title: { color: "#f7fbff", fontSize: 34, fontWeight: "800", lineHeight: 39 },
  subtitle: { color: "#b8c6d9", fontSize: 16, lineHeight: 24 },
  input: { backgroundColor: "#18263a", color: "#f7fbff", borderColor: "#2c405c", borderWidth: 1, borderRadius: 12, padding: 16, fontSize: 16 },
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 12 },
  action: { backgroundColor: "#f7fbff", borderRadius: 14, padding: 16, minHeight: 116, width: "47%", justifyContent: "space-between" },
  pressed: { opacity: 0.75 },
  actionIcon: { color: "#17304d", fontSize: 28 },
  actionText: { color: "#17304d", fontSize: 15, fontWeight: "700" },
  spinner: { margin: 12 },
  card: { backgroundColor: "#18334a", borderRadius: 16, padding: 20, gap: 8, borderColor: "#2c5874", borderWidth: 1 },
  cardLabel: { color: "#8be9c1", fontSize: 12, letterSpacing: 2, fontWeight: "700" },
  decision: { color: "#ffffff", fontSize: 25, fontWeight: "800" },
  cardBody: { color: "#d6e3f2", fontSize: 16 },
  reason: { color: "#9db2c9", fontSize: 12, lineHeight: 18 },
});
