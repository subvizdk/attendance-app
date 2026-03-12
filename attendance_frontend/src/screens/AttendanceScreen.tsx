import React, { useEffect, useMemo, useState } from "react";
import { View, Text, FlatList, Pressable, StyleSheet, Alert } from "react-native";
import { api } from "../api/client";
import { getSelectedBatchId } from "../state/SelectionStore";
import { useNavigation } from "@react-navigation/native";

type Student = { id: number; student_id: string; full_name: string };
type Status = "P" | "A";

export default function AttendanceScreen() {
  const navigation: any = useNavigation();
  const [students, setStudents] = useState<Student[]>([]);
  const [batchId, setBatchId] = useState<number | null>(null);
  const [marks, setMarks] = useState<Record<number, Status>>({});
  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);

  const load = async () => {
    const bid = await getSelectedBatchId();
    setBatchId(bid);
    if (!bid) {
      setStudents([]);
      Alert.alert("Select batch", "Go to Home and select a batch first.");
      return;
    }
    const res = await api.get(`/batches/${bid}/students/`);
    setStudents(res.data);
    setMarks({});
  };

  useEffect(() => {
    const unsubscribe = navigation.addListener("focus", () => load());
    return unsubscribe;
  }, [navigation]);

  const toggle = (studentId: number, status: Status) => {
    setMarks(prev => ({ ...prev, [studentId]: status }));
  };

  const submit = async () => {
    if (!batchId) {
      Alert.alert("Select batch", "Go to Home and select a batch first.");
      return;
    }
    const sessionRes = await api.post("/attendance/sessions/", { batch: batchId, date: today, label: "Daily" });
    const sessionId = sessionRes.data.id as number;

    const payload = students.map(s => ({ student: s.id, status: marks[s.id] ?? "P" }));
    await api.put(`/attendance/sessions/${sessionId}/marks/`, { marks: payload });
    Alert.alert("Success", "Attendance submitted!");
  };

  return (
    <View style={styles.container}>
      <Text style={styles.date}>Today: {today}</Text>

      {!batchId ? <Text style={styles.hint}>No batch selected. Go to Home.</Text> : null}

      <FlatList
        data={students}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => {
          const current = marks[item.id] ?? "P";
          return (
            <View style={styles.rowCard}>
              <Text style={styles.rowName}>{item.full_name}</Text>
              <View style={styles.actions}>
                <Pressable style={[styles.btn, current === "P" ? styles.btnGreen : styles.btnGhost]} onPress={() => toggle(item.id, "P")}>
                  <Text style={styles.btnText}>Present</Text>
                </Pressable>
                <Pressable style={[styles.btn, current === "A" ? styles.btnRed : styles.btnGhost]} onPress={() => toggle(item.id, "A")}>
                  <Text style={styles.btnText}>Absent</Text>
                </Pressable>
              </View>
            </View>
          );
        }}
      />

      <Pressable style={styles.submit} onPress={submit}>
        <Text style={styles.submitText}>Submit Attendance</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F3F6FB", padding: 12 },
  date: { fontSize: 16, fontWeight: "900", marginBottom: 10 },
  hint: { color: "#556", marginBottom: 10 },
  rowCard: { backgroundColor: "white", borderRadius: 14, padding: 12, marginBottom: 10 },
  rowName: { fontSize: 15, fontWeight: "900", marginBottom: 10 },
  actions: { flexDirection: "row", gap: 10 },
  btn: { paddingVertical: 10, paddingHorizontal: 14, borderRadius: 10, minWidth: 92, alignItems: "center" },
  btnGhost: { backgroundColor: "#EEF2F7" },
  btnGreen: { backgroundColor: "#16A34A" },
  btnRed: { backgroundColor: "#DC2626" },
  btnText: { color: "white", fontWeight: "900" },
  submit: { backgroundColor: "#DC2626", borderRadius: 14, padding: 14, alignItems: "center", marginTop: 8 },
  submitText: { color: "white", fontWeight: "900", fontSize: 16 },
});
