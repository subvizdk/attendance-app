import React, { useEffect, useMemo, useState } from 'react';
import { ActivityIndicator, FlatList, SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { createAttendance, fetchStudents } from './src/api/client';

const statuses = ['present', 'absent', 'late'];

export default function App() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedStatus, setSelectedStatus] = useState({});

  useEffect(() => {
    const load = async () => {
      try {
        const data = await fetchStudents();
        setStudents(data);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const today = useMemo(() => new Date().toISOString().slice(0, 10), []);

  const markAttendance = async (studentId) => {
    const status = selectedStatus[studentId] ?? 'present';
    await createAttendance({ student_id: studentId, status, date: today, remarks: '' });
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.center}>
        <ActivityIndicator size="large" />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Student Attendance ({today})</Text>
      <FlatList
        data={students}
        keyExtractor={(item) => String(item.id)}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.name}>{item.admission_number} · {item.first_name} {item.last_name}</Text>
            <Text style={styles.batch}>{item.current_batch?.name} {item.current_batch?.academic_year}</Text>
            <View style={styles.row}>
              {statuses.map((status) => (
                <TouchableOpacity
                  key={status}
                  onPress={() => setSelectedStatus((prev) => ({ ...prev, [item.id]: status }))}
                  style={[styles.statusBtn, selectedStatus[item.id] === status && styles.selected]}
                >
                  <Text style={styles.statusText}>{status.toUpperCase()}</Text>
                </TouchableOpacity>
              ))}
            </View>
            <TouchableOpacity style={styles.submit} onPress={() => markAttendance(item.id)}>
              <Text style={styles.submitText}>Save</Text>
            </TouchableOpacity>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8fafc', padding: 16 },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  title: { fontSize: 22, fontWeight: '700', marginBottom: 16 },
  card: { backgroundColor: '#fff', borderRadius: 8, padding: 12, marginBottom: 12 },
  name: { fontWeight: '600', marginBottom: 4 },
  batch: { color: '#475569', marginBottom: 8 },
  row: { flexDirection: 'row', gap: 8 },
  statusBtn: { borderWidth: 1, borderColor: '#cbd5e1', borderRadius: 6, paddingVertical: 6, paddingHorizontal: 8 },
  selected: { backgroundColor: '#dbeafe', borderColor: '#3b82f6' },
  statusText: { fontSize: 12 },
  submit: { marginTop: 10, backgroundColor: '#1d4ed8', borderRadius: 6, padding: 10, alignItems: 'center' },
  submitText: { color: '#fff', fontWeight: '600' }
});
