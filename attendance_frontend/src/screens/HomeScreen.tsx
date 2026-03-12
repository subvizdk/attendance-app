import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, Pressable, Alert } from "react-native";
import { Picker } from "@react-native-picker/picker";
import { api } from "../api/client";
import { getSelectedBatchId, setSelectedBatchId } from "../state/SelectionStore";

type Branch = { id: number; name: string; code: string };
type Level = { id: number; name: string; order: number };
type Batch = { id: number; name: string; year: number; branch: number; level: number; is_active: boolean };

export default function HomeScreen() {
  const [branches, setBranches] = useState<Branch[]>([]);
  const [levels, setLevels] = useState<Level[]>([]);
  const [batches, setBatches] = useState<Batch[]>([]);

  const [branchId, setBranchId] = useState<number | null>(null);
  const [levelId, setLevelId] = useState<number | null>(null);
  const [batchId, setBatchId] = useState<number | null>(null);

  useEffect(() => {
    (async () => {
      const [br, lv] = await Promise.all([api.get("/branches/"), api.get("/levels/")]);
      setBranches(br.data);
      setLevels(lv.data);

      const savedBatch = await getSelectedBatchId();
      if (savedBatch) setBatchId(savedBatch);
    })();
  }, []);

  useEffect(() => {
    // Load batches only when both selected
    (async () => {
      if (!branchId || !levelId) {
        setBatches([]);
        setBatchId(null);
        return;
      }
      const bt = await api.get(`/batches/?branch_id=${branchId}&level_id=${levelId}&is_active=true`);
      setBatches(bt.data);
      setBatchId(null);
    })();
  }, [branchId, levelId]);

  const save = async () => {
    if (!batchId) {
      Alert.alert("Select batch", "Please select a batch first.");
      return;
    }
    await setSelectedBatchId(batchId);
    Alert.alert("Saved", "Selected batch saved.");
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.hi}>Vanakkam 👋</Text>
        <Text style={styles.role}>Teacher</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Choose Class</Text>

        <Text style={styles.label}>Branch</Text>
        <View style={styles.pickerWrap}>
          <Picker selectedValue={branchId} onValueChange={(v) => setBranchId(v)}>
            <Picker.Item label="Select branch..." value={null} />
            {branches.map(b => <Picker.Item key={b.id} label={b.name} value={b.id} />)}
          </Picker>
        </View>

        <Text style={styles.label}>Level</Text>
        <View style={styles.pickerWrap}>
          <Picker selectedValue={levelId} onValueChange={(v) => setLevelId(v)}>
            <Picker.Item label="Select level..." value={null} />
            {levels.map(l => <Picker.Item key={l.id} label={l.name} value={l.id} />)}
          </Picker>
        </View>

        <Text style={styles.label}>Batch</Text>
        <View style={styles.pickerWrap}>
          <Picker selectedValue={batchId} onValueChange={(v) => setBatchId(v)} enabled={!!branchId && !!levelId}>
            <Picker.Item label="Select batch..." value={null} />
            {batches.map(b => <Picker.Item key={b.id} label={`${b.name} (${b.year})`} value={b.id} />)}
          </Picker>
        </View>

        <Pressable style={styles.saveBtn} onPress={save}>
          <Text style={styles.saveText}>Save Selected Batch</Text>
        </Pressable>
      </View>

      <View style={styles.grid}>
        <View style={[styles.tile, { backgroundColor: "#2563EB" }]}>
          <Text style={styles.tileTitle}>Attendance</Text>
          <Text style={styles.tileSub}>Mark daily</Text>
        </View>
        <View style={[styles.tile, { backgroundColor: "#16A34A" }]}>
          <Text style={styles.tileTitle}>Students</Text>
          <Text style={styles.tileSub}>Manage list</Text>
        </View>
        <View style={[styles.tile, { backgroundColor: "#F59E0B" }]}>
          <Text style={styles.tileTitle}>Batches</Text>
          <Text style={styles.tileSub}>By year</Text>
        </View>
        <View style={[styles.tile, { backgroundColor: "#DC2626" }]}>
          <Text style={styles.tileTitle}>Reports</Text>
          <Text style={styles.tileSub}>Coming soon</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F3F6FB", padding: 12 },
  header: { backgroundColor: "#0B5ED7", borderRadius: 16, padding: 16, marginBottom: 12 },
  hi: { color: "white", fontSize: 22, fontWeight: "900" },
  role: { color: "white", marginTop: 4, opacity: 0.9 },
  card: { backgroundColor: "white", borderRadius: 16, padding: 12, marginBottom: 12 },
  sectionTitle: { fontSize: 16, fontWeight: "900", marginBottom: 8 },
  label: { marginTop: 10, fontWeight: "800", color: "#425" },
  pickerWrap: { backgroundColor: "#F3F6FB", borderRadius: 12, marginTop: 6 },
  saveBtn: { marginTop: 12, backgroundColor: "#0B5ED7", borderRadius: 12, padding: 12, alignItems: "center" },
  saveText: { color: "white", fontWeight: "900" },
  grid: { flexDirection: "row", flexWrap: "wrap", gap: 10 },
  tile: { width: "48%", borderRadius: 16, padding: 16, minHeight: 90, justifyContent: "center" },
  tileTitle: { color: "white", fontWeight: "900", fontSize: 16 },
  tileSub: { color: "white", marginTop: 6, opacity: 0.9 },
});
