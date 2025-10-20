<template>
  <div class="form-group">
    <label v-if="label" :for="inputId"
      >{{ label }} <span v-if="required" class="required">*</span></label
    >
    <slot></slot> <small v-if="helpText" class="form-text text-muted">{{ helpText }}</small>
    <div v-if="error" class="invalid-feedback">{{ error }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  inputId: String, // Para el 'for' del label
  required: Boolean,
  helpText: String,
  error: String, // Mensaje de error específico del campo
})

// Generar un ID si no se proporciona
const generatedId = computed(
  () => props.inputId || `field-${Math.random().toString(36).substr(2, 9)}`,
)
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem; /* Espaciado estándar */
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  font-size: 0.9rem;
  color: #495057;
}
.required {
  color: #dc3545; /* Rojo */
  margin-left: 2px;
}
.form-text {
  font-size: 0.8rem;
  color: #6c757d;
  display: block;
  margin-top: 0.25rem;
}
.invalid-feedback {
  color: #dc3545;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

/* Estilos para los slots (inputs, selects) si es necesario */
:slotted(input),
:slotted(select),
:slotted(textarea) {
  /* Puedes añadir estilos por defecto aquí si quieres */
  /* Por ejemplo: border-radius: 4px; */
}
</style>
