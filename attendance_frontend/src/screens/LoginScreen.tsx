import React, { useState } from "react";
import { View, Text, TextInput, Pressable, StyleSheet } from "react-native";
import { useAuth } from "../state/AuthContext";

export default function LoginScreen() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const onLogin = async () => {
    setError(null);
    setBusy(true);
    try {
      await login(username.trim(), password);
    } catch {
      setError("Login failed. Check username/password.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.title}>Attendance</Text>
        <Text style={styles.subtitle}>Teacher Login</Text>

        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        {error ? <Text style={styles.error}>{error}</Text> : null}

        <Pressable style={styles.btn} onPress={onLogin} disabled={busy}>
          <Text style={styles.btnText}>{busy ? "Signing in..." : "Login"}</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0B5ED7", justifyContent: "center", padding: 16 },
  card: { backgroundColor: "white", borderRadius: 16, padding: 16 },
  title: { fontSize: 28, fontWeight: "900", color: "#0B5ED7" },
  subtitle: { marginTop: 6, color: "#556" },
  input: { marginTop: 12, backgroundColor: "#F3F6FB", borderRadius: 12, paddingHorizontal: 12, height: 48 },
  btn: { marginTop: 16, backgroundColor: "#DC2626", borderRadius: 12, padding: 14, alignItems: "center" },
  btnText: { color: "white", fontWeight: "800", fontSize: 16 },
  error: { marginTop: 10, color: "#DC2626", fontWeight: "700" },
});
