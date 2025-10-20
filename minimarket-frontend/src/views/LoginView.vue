<template>
  <div class="login-wrapper">
    <div class="login-container">
      <h1><img src="/favicon.ico" alt="Logo" class="logo"> Minimarket Admin</h1>
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="username" required autocomplete="username">
        </div>
        <div class="form-group">
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" required autocomplete="current-password">
        </div>
        <button type="submit" :disabled="authStore.loading" class="login-button">
          <span v-if="authStore.loading">Ingresando...</span>
          <span v-else>Ingresar</span>
        </button>
        <p v-if="authStore.error" class="error-message">{{ authStore.error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const username = ref('');
const password = ref('');

const handleLogin = async () => {
  // Limpiar error anterior antes de intentar
  authStore.error = null;
  await authStore.login({ username: username.value, password: password.value });
};

// Limpiar error al montar el componente (por si quedó de un intento anterior)
onMounted(() => {
  authStore.error = null;
});
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5; /* Un fondo suave */
}
.login-container {
  background-color: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
}
.logo {
  width: 32px; /* Ajusta el tamaño según tu favicon */
  height: 32px;
  vertical-align: middle;
  margin-right: 8px;
}
h1 {
  margin-bottom: 10px;
  color: #333;
}
h2 {
  margin-bottom: 30px;
  color: #555;
  font-weight: normal;
}
.login-form .form-group {
  margin-bottom: 20px;
  text-align: left;
}
label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}
input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /* Importante para que el padding no aumente el ancho */
  font-size: 1rem;
}
.login-button {
  width: 100%;
  padding: 12px;
  background-color: #007bff; /* Azul primario */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;
}
.login-button:hover:not(:disabled) {
  background-color: #0056b3; /* Azul más oscuro al pasar el mouse */
}
.login-button:disabled {
  background-color: #aaa; /* Gris cuando está deshabilitado */
  cursor: not-allowed;
}
.error-message {
  color: #dc3545; /* Rojo para errores */
  margin-top: 15px;
  font-size: 0.9rem;
}
</style>
