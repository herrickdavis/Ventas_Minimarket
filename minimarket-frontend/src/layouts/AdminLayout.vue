<template>
  <div class="admin-layout">
    <header class="navbar">
      <div class="navbar-brand">
         <img src="/favicon.ico" alt="Logo" class="logo">
         <span>Minimarket Admin</span>
      </div>
      <div class="navbar-user">
        <span>Hola, {{ authStore.getUsername }}</span>
        <button @click="logout" class="logout-button">Cerrar Sesión</button>
      </div>
       </header>
    <div class="main-content">
      <aside class="sidebar">
        <nav>
          <ul>
            <li><router-link :to="{ name: 'admin-dashboard' }">Dashboard</router-link></li>

            <li class="menu-header">CATÁLOGO</li>
            <li><router-link :to="{ name: 'admin-products' }">Productos</router-link></li>
            <li><router-link :to="{ name: 'admin-categories' }">Categorías</router-link></li>
            <li><router-link :to="{ name: 'admin-units' }">Unidades</router-link></li>
            <li><router-link :to="{ name: 'admin-brands' }">Marcas</router-link></li>
            <li><router-link :to="{ name: 'admin-taxes' }">Impuestos</router-link></li>
            <li><router-link :to="{ name: 'admin-pricelists' }">Listas Precios</router-link></li>

            <li class="menu-header">INVENTARIO</li>
            <li class="menu-header">GESTIÓN</li>
             <li class="menu-header">FINANZAS</li>
             <li class="menu-header">SEGURIDAD</li>
             </ul>
        </nav>
      </aside>
      <main class="content-area">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
  authStore.logout();
};

if (!authStore.isAuthenticated) {
  router.push({ name: 'login' });
}
</script>

<style scoped>
:root {
  --sidebar-width: 240px;
  --navbar-height: 60px;
}

.admin-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8f9fa;
}
.navbar {
  height: var(--navbar-height);
  background-color: #ffffff;
  color: #343a40;
  padding: 0 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  flex-shrink: 0; /* Evita que se encoja */
}
.navbar-brand {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1.2rem;
}
.logo {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}
.navbar-user span {
  margin-right: 15px;
  color: #495057;
}
.logout-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}
.main-content {
  display: flex;
  flex-grow: 1;
  /* Calcular altura restante para habilitar scroll independiente */
  height: calc(100vh - var(--navbar-height));
}
.sidebar {
  width: var(--sidebar-width);
  background-color: #343a40;
  color: #adb5bd;
  padding: 20px 0;
  flex-shrink: 0;
  overflow-y: auto; /* Scroll si el menú es muy largo */
}
.sidebar ul { list-style: none; padding: 0; margin: 0; }
.sidebar li { margin: 0; }
.sidebar a {
  display: block;
  padding: 12px 20px;
  text-decoration: none;
  color: #adb5bd;
  transition: background-color 0.2s ease, color 0.2s ease;
  border-left: 3px solid transparent;
  white-space: nowrap; /* Evita que el texto se parta */
}
.sidebar a:hover { background-color: #495057; color: #ffffff; }
.sidebar a.router-link-exact-active {
  background-color: #007bff;
  color: #ffffff;
  font-weight: 500; /* Un poco menos bold */
  border-left-color: #ffffff;
}
.menu-header {
  padding: 15px 20px 8px;
  font-size: 0.75rem; /* Más pequeño */
  color: #6c757d;
  text-transform: uppercase;
  font-weight: bold;
  letter-spacing: 0.5px; /* Espaciado ligero */
}
.content-area {
  flex-grow: 1;
  padding: 30px;
  overflow-y: auto; /* Scroll principal */
}

/* Transiciones */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* Media Query Simple (Ejemplo para ocultar sidebar en pantallas pequeñas) */
@media (max-width: 768px) {
  /* .sidebar {
    position: fixed;
    left: -var(--sidebar-width);
    height: calc(100vh - var(--navbar-height));
    transition: left 0.3s ease;
    z-index: 999;
  } */
  /* Necesitaríamos JS para mostrar/ocultar el sidebar con un botón */
   .sidebar { display: none; } /* Ocultar por simplicidad ahora */
   .content-area { padding: 15px; } /* Menos padding en móvil */
}
</style>
