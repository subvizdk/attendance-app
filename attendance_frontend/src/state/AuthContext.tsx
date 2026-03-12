import React, { createContext, useContext, useEffect, useMemo, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { api, setAuthToken } from "../api/client";

type AuthState = {
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const saved = await AsyncStorage.getItem("accessToken");
      if (saved) {
        setToken(saved);
        setAuthToken(saved);
      }
      setLoading(false);
    })();
  }, []);

  const login = async (username: string, password: string) => {
    const res = await api.post("/auth/token/", { username, password });
    const access = res.data.access as string;
    setToken(access);
    setAuthToken(access);
    await AsyncStorage.setItem("accessToken", access);
  };

  const logout = async () => {
    setToken(null);
    setAuthToken(null);
    await AsyncStorage.removeItem("accessToken");
  };

  const value = useMemo(() => ({ token, login, logout, loading }), [token, loading]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
