<template>
  <div class="dashboard-container">
    <h1>Dashboard</h1>
    <p>¡Bienvenido al panel de administración del Minimarket!</p>
    <div class="stats-grid">
       <div class="stat-card">
          <h3>Ventas Hoy</h3>
          <p class="stat-value">S/ 0.00</p>
          <small>(Pendiente implementar)</small>
       </div>
       <div class="stat-card">
          <h3>Productos Bajos Stock</h3>
          <p class="stat-value">0</p>
           <small>(Pendiente implementar)</small>
       </div>
       <div class="stat-card">
          <h3>Pedidos Web Pendientes</h3>
          <p class="stat-value">0</p>
           <small>(Pendiente implementar)</small>
       </div>
    </div>
    </div>
</template>

<script setup>
// Aquí iría la lógica para cargar datos del dashboard, por ejemplo:
// import { onMounted } from 'vue';
// onMounted(() => {
//   // Llamar a la API para obtener estadísticas
// });
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 30px;
}
.stat-card {
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  text-align: center;
}
.stat-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #6c757d; /* Gris */
  font-size: 1rem;
}
.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #343a40; /* Negro suave */
  margin-bottom: 5px;
}
.stat-card small {
    color: #adb5bd; /* Gris claro */
    font-style: italic;
}
</style>
