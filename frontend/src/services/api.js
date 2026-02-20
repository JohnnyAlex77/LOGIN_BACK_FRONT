import axios from 'axios';

// Creamos una instancia de Axios con configuración base
// Esto nos permite tener una configuración centralizada para todas las peticiones
const api = axios.create({
  baseURL: 'http://localhost:8000/api',  // Todas las rutas empiezan con /api
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // Importante para enviar cookies (refresh token)
});

// El access token se guarda en memoria (variable), no en localStorage
// Esto es más seguro contra ataques XSS
let accessToken = null;

// Funciones para manejar el token centralizadamente
export const setAccessToken = (token) => {
  accessToken = token;
};

export const getAccessToken = () => accessToken;

export const clearAccessToken = () => {
  accessToken = null;
};

// Interceptor de peticiones - se ejecuta antes de cada llamada
// Aquí agregamos el token a los headers si existe
api.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor de respuestas - se ejecuta después de cada respuesta
// Aquí manejamos errores 401 (no autorizado) y refrescamos el token
api.interceptors.response.use(
  (response) => response,  // Si la respuesta es exitosa, la pasamos
  async (error) => {
    const originalRequest = error.config;

    // Si es error 401 y no hemos intentado refrescar aún
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;  // Marcamos para no entrar en bucle

      try {
        // Intentamos obtener un nuevo access token usando el refresh token
        // Notar que usamos axios directo (no la instancia api) para evitar ciclos
        const refreshResponse = await axios.post(
          'http://localhost:8000/api/auth/refresh/',
          {},
          { withCredentials: true }  // Importante: el refresh token viene en cookie
        );

        if (refreshResponse.data.access) {
          // Nuevo token obtenido, lo guardamos y reintentamos la petición original
          setAccessToken(refreshResponse.data.access);
          originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Si falla el refresh, limpiamos todo y redirigimos al login
        clearAccessToken();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    // Si no es 401 o ya intentamos refrescar, rechazamos con el error original
    return Promise.reject(error);
  }
);

export default api;