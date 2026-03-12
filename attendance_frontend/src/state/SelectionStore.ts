import AsyncStorage from "@react-native-async-storage/async-storage";

export async function getSelectedBatchId(): Promise<number | null> {
  const v = await AsyncStorage.getItem("selectedBatchId");
  return v ? Number(v) : null;
}

export async function setSelectedBatchId(batchId: number) {
  await AsyncStorage.setItem("selectedBatchId", String(batchId));
}
