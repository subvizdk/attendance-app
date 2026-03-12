import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import HomeScreen from "../screens/HomeScreen";
import StudentsScreen from "../screens/StudentsScreen";
import AttendanceScreen from "../screens/AttendanceScreen";
import SettingsScreen from "../screens/SettingsScreen";

const Tab = createBottomTabNavigator();

export default function Tabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: true }}>
      <Tab.Screen name="Home" component={HomeScreen} options={{ title: "Home Dashboard" }} />
      <Tab.Screen name="Students" component={StudentsScreen} options={{ title: "Student List" }} />
      <Tab.Screen name="Attendance" component={AttendanceScreen} options={{ title: "Attendance" }} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  );
}
