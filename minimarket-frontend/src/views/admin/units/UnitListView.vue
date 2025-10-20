<template>
  <div class="list-view-container">
    <h1>Gestión de Unidades de Medida</h1>
    <button @click="openModal()" class="add-button">Nueva Unidad</button>

    <div v-if="loading" class="loading">Cargando...</div>
    <div v-if="error" class="error-message global-error">{{ error }}</div>

    <table v-if="!loading && units.length > 0" class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Código</th>
          <th>Nombre</th>
          <th>Decimales</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="unit in units" :key="unit.id">
          <td>{{ unit.id }}</td>
          <td>{{ unit.codigo }}</td>
          <td>{{ unit.nombre }}</td>
          <td>{{ unit.decimales }}</td>
          <td class="actions">
            <button @click="openModal(unit)" class="edit-button" title="Editar">✏️</button>
            <button @click="confirmDelete(unit)" class="delete-button" title="Eliminar">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && units.length === 0">No hay unidades registradas.</p>

    <SimpleModal :show="showModal" @close="closeModal">
      <h2>{{ editingUnit ? 'Editar Unidad' : 'Nueva Unidad' }}</h2>
      <form @submit.prevent="handleSubmit" class="modal-form">
        <FormField label="Código:" :required="true">
          <input type="text" v-model="unitForm.codigo" required maxlength="10" />
        </FormField>
        <FormField label="Nombre:" :required="true">
          <input type="text" v-model="unitForm.nombre" required maxlength="50" />
        </FormField>
        <FormField label="Decimales Permitidos:" :required="true">
          <input type="number" v-model.number="unitForm.decimales" required min="0" max="6" />
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
import { useUnitStore } from '@/stores/units'
import { storeToRefs } from 'pinia'
import SimpleModal from '@/components/SimpleModal.vue'
import FormField from '@/components/FormField.vue'

const unitStore = useUnitStore()
const { units, loading, error } = storeToRefs(unitStore)

const showModal = ref(false)
const editingUnit = ref(null)
const unitForm = reactive({ codigo: '', nombre: '', decimales: 0 })
const formError = ref(null)

onMounted(() => {
  unitStore.fetchUnits()
})

const openModal = (unit = null) => {
  formError.value = null
  error.value = null
  if (unit) {
    editingUnit.value = unit
    Object.assign(unitForm, {
      codigo: unit.codigo,
      nombre: unit.nombre,
      decimales: unit.decimales,
    })
  } else {
    editingUnit.value = null
    Object.assign(unitForm, { codigo: '', nombre: '', decimales: 0 })
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingUnit.value = null
}

const handleSubmit = async () => {
  formError.value = null
  error.value = null
  let result = null
  if (editingUnit.value) {
    result = await unitStore.updateUnit(editingUnit.value.id, unitForm)
  } else {
    result = await unitStore.createUnit(unitForm)
  }
  if (result) {
    closeModal()
  } else {
    formError.value = unitStore.error
  }
}

const confirmDelete = (unit) => {
  error.value = null
  if (window.confirm(`¿Eliminar unidad "${unit.nombre} (${unit.codigo})"?`)) {
    unitStore.deleteUnit(unit.id)
  }
}
</script>

<style scoped>
@import '@/assets/admin-tables.css'; /* Asumiendo que crearás este archivo */
@import '@/assets/admin-modals.css'; /* Asumiendo que crearás este archivo */
</style>
