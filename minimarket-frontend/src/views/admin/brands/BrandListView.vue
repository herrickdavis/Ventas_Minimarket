<template>
  <div class="list-view-container">
    <h1>Gestión de Marcas</h1>
    <button @click="openModal()" class="add-button">Nueva Marca</button>

    <div v-if="loading" class="loading">Cargando...</div>
    <div v-if="error" class="error-message global-error">{{ error }}</div>

    <table v-if="!loading && brands.length > 0" class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="brand in brands" :key="brand.id">
          <td>{{ brand.id }}</td>
          <td>{{ brand.nombre }}</td>
          <td class="actions">
            <button @click="openModal(brand)" class="edit-button" title="Editar">✏️</button>
            <button @click="confirmDelete(brand)" class="delete-button" title="Eliminar">🗑️</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && brands.length === 0">No hay marcas registradas.</p>

    <SimpleModal :show="showModal" @close="closeModal">
      <h2>{{ editingBrand ? 'Editar Marca' : 'Nueva Marca' }}</h2>
      <form @submit.prevent="handleSubmit" class="modal-form">
        <FormField label="Nombre:" :required="true">
          <input type="text" v-model="brandForm.nombre" required maxlength="100" />
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
import { useBrandStore } from '@/stores/brands' // Asegúrate de crear este archivo
import { storeToRefs } from 'pinia'
import SimpleModal from '@/components/SimpleModal.vue'
import FormField from '@/components/FormField.vue'

const brandStore = useBrandStore()
const { brands, loading, error } = storeToRefs(brandStore)

const showModal = ref(false)
const editingBrand = ref(null)
const brandForm = reactive({ nombre: '' })
const formError = ref(null)

onMounted(() => {
  brandStore.fetchBrands()
})

const openModal = (brand = null) => {
  formError.value = null
  error.value = null
  if (brand) {
    editingBrand.value = brand
    brandForm.nombre = brand.nombre
  } else {
    editingBrand.value = null
    brandForm.nombre = ''
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingBrand.value = null
}

const handleSubmit = async () => {
  formError.value = null
  error.value = null
  let result = null
  if (editingBrand.value) {
    result = await brandStore.updateBrand(editingBrand.value.id, brandForm)
  } else {
    result = await brandStore.createBrand(brandForm)
  }
  if (result) {
    closeModal()
  } else {
    formError.value = brandStore.error
  }
}

const confirmDelete = (brand) => {
  error.value = null
  if (window.confirm(`¿Eliminar marca "${brand.nombre}"?`)) {
    brandStore.deleteBrand(brand.id)
  }
}
</script>

<style scoped>
@import '@/assets/admin-tables.css';
@import '@/assets/admin-modals.css';
</style>
