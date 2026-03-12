import React from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";
import { useAuth } from "../state/AuthContext";

export default function SettingsScreen() {
  const { logout } = useAuth();

  return (
    <View style={styles.container}>
      <View style={styles.profileCard}>
        <View style={styles.avatar} />
        <View style={{ flex: 1 }}>
          <Text style={styles.name}>Teacher Name</Text>
          <Text style={styles.role}>Teacher</Text>
        </View>
      </View>

      <View style={styles.item}>
        <Text style={styles.itemLabel}>Language</Text>
        <Text style={styles.itemValue}>English</Text>
      </View>

      <View style={styles.item}>
        <Text style={styles.itemLabel}>About</Text>
        <Text style={styles.itemValue}>App Version 1.0</Text>
      </View>

      <Pressable style={styles.logoutBtn} onPress={logout}>
        <Text style={styles.logoutText}>Log Out</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F3F6FB", padding: 12 },
  profileCard: { backgroundColor: "#0B5ED7", borderRadius: 16, padding: 14, flexDirection: "row", alignItems: "center", marginBottom: 12 },
  avatar: { width: 44, height: 44, borderRadius: 22, backgroundColor: "white", marginRight: 12, opacity: 0.9 },
  name: { color: "white", fontWeight: "900", fontSize: 16 },
  role: { color: "white", opacity: 0.9, marginTop: 2 },
  item: { backgroundColor: "white", borderRadius: 12, padding: 14, flexDirection: "row", justifyContent: "space-between", marginBottom: 10 },
  itemLabel: { fontWeight: "900", color: "#123" },
  itemValue: { color: "#567" },
  logoutBtn: { backgroundColor: "#DC2626", borderRadius: 14, padding: 14, alignItems: "center", marginTop: 12 },
  logoutText: { color: "white", fontWeight: "900", fontSize: 16 },
});
