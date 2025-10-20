import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Intentar cargar desde localStorage al iniciar
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('authToken') || null,
    error: null,
    loading: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    // Podríamos añadir más getters si tuviéramos más datos del usuario
    getUsername: (state) => state.user?.username || 'Usuario',
  },
  actions: {
    async login(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.post('/auth-token/', credentials);
        const token = response.data.token;

        this.token = token;
        localStorage.setItem('authToken', token);

        // Simulamos guardar el username. Idealmente, haríamos otra llamada
        // a un endpoint /api/user/me/ para obtener los datos completos del usuario.
        this.user = { username: credentials.username };
        localStorage.setItem('user', JSON.stringify(this.user));

        // Establecer el header para futuras peticiones en esta sesión
        apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;

        console.log("Login exitoso, redirigiendo...");
        // Redirigir al dashboard del admin
        await router.push({ name: 'admin-dashboard' });

      } catch (err) {
        console.error("Error en login:", err.response?.data || err.message);
        // Intentar obtener un mensaje de error específico del backend
        this.error = err.response?.data?.non_field_errors?.[0] || 'Usuario o contraseña incorrectos.';
        // Limpiar estado en caso de error
        this.token = null;
        this.user = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        delete apiClient.defaults.headers.common['Authorization'];
      } finally {
        this.loading = false;
      }
    },
    logout() {
      console.log("Cerrando sesión...");
      this.token = null;
      this.user = null;
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      delete apiClient.defaults.headers.common['Authorization'];
      // Redirigimos al login
      router.push({ name: 'login' });
    },
    // Acción para verificar el token al cargar la app (opcional pero útil)
    checkAuth() {
      const token = localStorage.getItem('authToken');
      if (token) {
        this.token = token;
        this.user = JSON.parse(localStorage.getItem('user')) || null;
        apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
      } else {
        this.logout(); // Asegurar que todo esté limpio si no hay token
      }
    }
  }
});
