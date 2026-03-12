import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet } from "react-native";
import { api } from "../api/client";

type Student = {
  id: number;
  student_id: string;
  full_name: string;
  phone: string;
};

export default function StudentDetailsScreen({ route }: any) {
  const { studentId } = route.params;
  const [student, setStudent] = useState<Student | null>(null);

  useEffect(() => {
    api.get(`/students/${studentId}/`).then(res => setStudent(res.data));
  }, [studentId]);

  if (!student) return <View style={styles.container}><Text>Loading...</Text></View>;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.name}>{student.full_name}</Text>
        <Text style={styles.sub}>Roll No: {student.student_id}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Personal Info</Text>
        <Text style={styles.item}>Phone: {student.phone || "-"}</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Attendance Summary</Text>
        <Text style={styles.item}>Coming soon…</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F3F6FB", padding: 12 },
  header: { backgroundColor: "#0B5ED7", borderRadius: 18, padding: 16, marginBottom: 12 },
  name: { color: "white", fontSize: 22, fontWeight: "900" },
  sub: { color: "white", marginTop: 6, opacity: 0.9 },
  card: { backgroundColor: "white", borderRadius: 14, padding: 12, marginBottom: 12 },
  sectionTitle: { fontWeight: "900", marginBottom: 8, color: "#123" },
  item: { color: "#364152" },
});
