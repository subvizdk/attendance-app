import React, { useEffect, useMemo, useState } from "react";
import { View, Text, TextInput, FlatList, Pressable, StyleSheet, Alert } from "react-native";
import { api } from "../api/client";
import { getSelectedBatchId } from "../state/SelectionStore";
import { useNavigation } from "@react-navigation/native";

type Student = {
  id: number;
  student_id: string;
  full_name: string;
  phone: string;
};

export default function StudentsScreen() {
  const navigation: any = useNavigation();
  const [query, setQuery] = useState("");
  const [students, setStudents] = useState<Student[]>([]);
  const [batchId, setBatchId] = useState<number | null>(null);

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
  };

  useEffect(() => {
    const unsubscribe = navigation.addListener("focus", () => load());
    return unsubscribe;
  }, [navigation]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return students;
    return students.filter(s => `${s.student_id} ${s.full_name}`.toLowerCase().includes(q));
  }, [query, students]);

  return (
    <View style={styles.container}>
      <View style={styles.searchRow}>
        <TextInput value={query} onChangeText={setQuery} placeholder="Search students..." style={styles.search} />
      </View>

      {!batchId ? <Text style={styles.hint}>No batch selected. Go to Home.</Text> : null}

      <FlatList
        data={filtered}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <Pressable onPress={() => navigation.navigate("StudentDetails", { studentId: item.id })} style={styles.card}>
            <View style={{ flex: 1 }}>
              <Text style={styles.name}>{item.full_name}</Text>
              <Text style={styles.sub}>Roll No: {item.student_id}</Text>
            </View>
            <Text style={styles.chev}>›</Text>
          </Pressable>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F3F6FB", padding: 12 },
  searchRow: { flexDirection: "row", marginBottom: 10 },
  search: { flex: 1, backgroundColor: "white", borderRadius: 12, paddingHorizontal: 12, height: 44 },
  card: { backgroundColor: "white", borderRadius: 14, padding: 12, marginBottom: 10, flexDirection: "row", alignItems: "center" },
  name: { fontSize: 16, fontWeight: "900" },
  sub: { marginTop: 4, color: "#5E6B7A" },
  chev: { fontSize: 24, color: "#9AA7B4", paddingLeft: 10 },
  hint: { color: "#556", marginBottom: 10 },
});
