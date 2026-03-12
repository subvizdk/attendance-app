import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useAuth } from "../state/AuthContext";
import LoginScreen from "../screens/LoginScreen";
import Tabs from "./Tabs";
import StudentDetailsScreen from "../screens/StudentDetailsScreen";

export type RootStackParamList = {
  Login: undefined;
  Main: undefined;
  StudentDetails: { studentId: number };
};

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function RootStack() {
  const { token, loading } = useAuth();
  if (loading) return null;

  return (
    <Stack.Navigator>
      {!token ? (
        <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
      ) : (
        <>
          <Stack.Screen name="Main" component={Tabs} options={{ headerShown: false }} />
          <Stack.Screen name="StudentDetails" component={StudentDetailsScreen} options={{ title: "Student Details" }} />
        </>
      )}
    </Stack.Navigator>
  );
}
