import axios from 'axios';

// La URL base de tu backend Django
const API_URL = 'http://127.0.0.1:8000/api/';

// Creamos una instancia de Axios
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

// Interceptor para añadir el Token a cada petición (si existe)
apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken'); // Usamos localStorage
  if (token) {
    config.headers['Authorization'] = `Token ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// Interceptor para manejar errores 401 (No Autorizado)
apiClient.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response && error.response.status === 401) {
    console.error("Error 401: No autorizado o token inválido. Redirigiendo a login.");
    localStorage.removeItem('authToken');
    localStorage.removeItem('user'); // Borrar también datos de usuario
    // Solo redirige si no estamos ya en la página de login
    if (window.location.pathname !== '/login') {
       window.location.href = '/login'; // Forzar recarga a la página de login
    }
  }
  return Promise.reject(error);
});

export default apiClient;
