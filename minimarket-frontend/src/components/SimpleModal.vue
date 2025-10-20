<template>
  <transition name="modal-fade">
    <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-content">
        <button class="modal-close" @click="$emit('close')">&times;</button>
        <slot></slot> </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  show: Boolean
});
defineEmits(['close']);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* Más oscuro */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050; /* Bootstrap z-index */
}

.modal-content {
  background-color: white;
  padding: 25px 30px; /* Más padding */
  border-radius: 8px;
  width: 90%;
  max-width: 550px; /* Un poco más ancho */
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
  position: relative; /* Para el botón de cerrar */
  max-height: 90vh; /* Altura máxima */
  overflow-y: auto; /* Scroll si es necesario */
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.8rem; /* Más grande */
  color: #6c757d; /* Gris */
  cursor: pointer;
  line-height: 1; /* Alinear mejor la X */
}
.modal-close:hover {
  color: #343a40; /* Más oscuro */
}

/* Transición Fade */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}
</style>
