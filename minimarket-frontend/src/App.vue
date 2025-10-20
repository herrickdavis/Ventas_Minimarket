<template>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

// Al cargar la aplicación, verifica si hay un token válido
// para mantener la sesión activa si se recarga la página.
const authStore = useAuthStore()
onMounted(() => {
  // authStore.checkAuth() // Puedes descomentar esto si implementas la lógica checkAuth en la store
})
</script>

<style>
/* Estilos globales básicos */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  margin: 0;
  line-height: 1.5;
  color: #212529;
  background-color: #f8f9fa; /* Fondo general */
}

/* Puedes importar un archivo CSS global aquí si prefieres */
/* @import '@/assets/base.css'; */
</style>
