import { createContext } from 'react';

// Crear el contexto de autenticación vacío
// Este contexto va a contener toda la info del usuario y las funciones
// como login, logout, etc. Lo separamos en otro archivo para tenerlo
// organizado y poder importarlo desde cualquier lado
export const AuthContext = createContext();