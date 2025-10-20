<template>
  <div class="list-view-container">
    <h1>Gestión de Clases de Impuesto</h1>
    <button @click="openModal()" class="add-button">Nueva Clase Impuesto</button>

    <div v-if="loading" class="loading">Cargando...</div>
    <div v-if="error" class="error-message global-error">{{ error }}</div>

    <table v-if="!loading && taxes.length > 0" class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Porcentaje (%)</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tax in taxes" :key="tax.id">
          <td>{{ tax.id }}</td>
          <td>{{ tax.nombre }}</td>
          <td>{{ tax.porcentaje }}</td>
          <td class="actions">
            <button @click="openModal(tax)" class="edit-button" title="Editar">✏️</button>
            <button @click="confirmDelete(tax)" class="delete-button" title="Eliminar">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && taxes.length === 0">No hay clases de impuesto registradas.</p>

    <SimpleModal :show="showModal" @close="closeModal">
      <h2>{{ editingTax ? 'Editar Clase Impuesto' : 'Nueva Clase Impuesto' }}</h2>
      <form @submit.prevent="handleSubmit" class="modal-form">
        <FormField label="Nombre:" :required="true">
          <input type="text" v-model="taxForm.nombre" required maxlength="100" />
        </FormField>
        <FormField label="Porcentaje:" :required="true">
          <input
            type="number"
            step="0.01"
            min="0"
            max="100"
            v-model.number="taxForm.porcentaje"
            required
          />
        </FormField>
        <p v-if="formError" class="error-message">{{ formError }}</p>
        <div class="modal-actions">
          <button type="button" @click="closeModal" class="cancel-button">Cancelar</button>
          <button type="submit" :disabled="loading" class="save-button">
            {{ loading ? 'Guardando...' : 'Guardar' }}
          </button>
        </div>
      </form>
    </SimpleModal>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useTaxStore } from '@/stores/taxes' // Asegúrate de crear este archivo
import { storeToRefs } from 'pinia'
import SimpleModal from '@/components/SimpleModal.vue'
import FormField from '@/components/FormField.vue'

const taxStore = useTaxStore()
const { taxes, loading, error } = storeToRefs(taxStore)

const showModal = ref(false)
const editingTax = ref(null)
const taxForm = reactive({ nombre: '', porcentaje: 0.0 })
const formError = ref(null)

onMounted(() => {
  taxStore.fetchTaxes()
})

const openModal = (tax = null) => {
  formError.value = null
  error.value = null
  if (tax) {
    editingTax.value = tax
    Object.assign(taxForm, { nombre: tax.nombre, porcentaje: tax.porcentaje })
  } else {
    editingTax.value = null
    Object.assign(taxForm, { nombre: '', porcentaje: 0.0 })
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingTax.value = null
}

const handleSubmit = async () => {
  formError.value = null
  error.value = null
  let result = null
  if (editingTax.value) {
    result = await taxStore.updateTax(editingTax.value.id, taxForm)
  } else {
    result = await taxStore.createTax(taxForm)
  }
  if (result) {
    closeModal()
  } else {
    formError.value = taxStore.error
  }
}

const confirmDelete = (tax) => {
  error.value = null
  if (window.confirm(`¿Eliminar clase de impuesto "${tax.nombre}"?`)) {
    taxStore.deleteTax(tax.id)
  }
}
</script>

<style scoped>
@import '@/assets/admin-tables.css';
@import '@/assets/admin-modals.css';
</style>
