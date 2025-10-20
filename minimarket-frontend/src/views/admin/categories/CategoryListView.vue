<template>
  <div class="list-view-container">
    <h1>Gestión de Categorías</h1>
    <button @click="openModal()" class="add-button">Nueva Categoría</button>

    <div v-if="loading" class="loading">Cargando...</div>
    <div v-if="error" class="error-message global-error">{{ error }}</div>

    <table v-if="!loading && categories.length > 0" class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Categoría Padre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in categories" :key="category.id">
          <td>{{ category.id }}</td>
          <td>{{ category.nombre }}</td>
          <td>{{ getParentCategoryName(category.padre) }}</td>
          <td class="actions">
            <button @click="openModal(category)" class="edit-button" title="Editar">✏️</button>
            <button @click="confirmDelete(category)" class="delete-button" title="Eliminar">
              🗑️
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && categories.length === 0">No hay categorías registradas.</p>

    <SimpleModal :show="showModal" @close="closeModal">
      <h2>{{ editingCategory ? 'Editar Categoría' : 'Nueva Categoría' }}</h2>
      <form @submit.prevent="handleSubmit" class="modal-form">
        <div class="form-group">
          <label for="categoryName">Nombre:</label>
          <input type="text" id="categoryName" v-model="categoryForm.nombre" required />
        </div>
        <div class="form-group">
          <label for="categoryParent">Categoría Padre (Opcional):</label>
          <select id="categoryParent" v-model="categoryForm.padre">
            <option :value="null">-- Ninguna --</option>
            <option v-for="cat in availableParents" :key="cat.id" :value="cat.id">
              {{ cat.nombre }}
            </option>
          </select>
        </div>
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
import { ref, onMounted, computed } from 'vue'
import { useCategoryStore } from '@/stores/categories'
import { storeToRefs } from 'pinia'
import SimpleModal from '@/components/SimpleModal.vue' // Asumiendo que crearás este componente

const categoryStore = useCategoryStore()
const { categories, loading, error } = storeToRefs(categoryStore)

const showModal = ref(false)
const editingCategory = ref(null)
const categoryForm = ref({ nombre: '', padre: null })
const formError = ref(null)

onMounted(() => {
  categoryStore.fetchCategories()
})

const getParentCategoryName = (parentId) => {
  if (!parentId) return '-'
  const parent = categories.value.find((cat) => cat.id === parentId)
  return parent ? parent.nombre : 'ID: ' + parentId // Mostrar ID si no se encuentra
}

const openModal = (category = null) => {
  formError.value = null
  error.value = null // Limpiar errores
  if (category) {
    editingCategory.value = category
    categoryForm.value.nombre = category.nombre
    categoryForm.value.padre = category.padre
  } else {
    editingCategory.value = null
    categoryForm.value = { nombre: '', padre: null }
  }
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingCategory.value = null
}

const handleSubmit = async () => {
  formError.value = null
  error.value = null
  let result = null
  const dataToSend = { ...categoryForm.value }
  // Asegurar que padre sea null si no se selecciona
  if (dataToSend.padre === undefined || dataToSend.padre === '') {
    dataToSend.padre = null
  }

  if (editingCategory.value) {
    result = await categoryStore.updateCategory(editingCategory.value.id, dataToSend)
  } else {
    result = await categoryStore.createCategory(dataToSend)
  }

  if (result) {
    closeModal()
  } else {
    formError.value = categoryStore.error // Mostrar error en el form
  }
}

const confirmDelete = (category) => {
  error.value = null // Limpiar error global
  if (window.confirm(`¿Eliminar categoría "${category.nombre}"?`)) {
    categoryStore.deleteCategory(category.id)
  }
}

const availableParents = computed(() => {
  if (editingCategory.value) {
    return categories.value.filter((cat) => cat.id !== editingCategory.value.id)
  }
  return categories.value
})
</script>

<style scoped>
/* Importar estilos comunes si los tienes */
/* @import '@/assets/admin-tables.css'; */
/* @import '@/assets/admin-modals.css'; */

/* Estilos básicos si no usas archivos externos */
.list-view-container {
  padding: 20px;
}
.add-button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 1rem;
}
.add-button:hover {
  background-color: #0056b3;
}
.loading {
  margin-top: 20px;
  font-style: italic;
  color: #6c757d;
}
.error-message {
  color: #dc3545;
  margin-top: 10px;
}
.global-error {
  border: 1px solid #dc3545;
  background-color: #f8d7da;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.data-table th,
.data-table td {
  border: 1px solid #dee2e6;
  padding: 12px 15px;
  text-align: left;
}
.data-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}
.data-table tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}
.actions button {
  padding: 5px 8px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 5px;
  font-size: 1rem;
  background: none;
}
.edit-button {
  color: #ffc107;
}
.delete-button {
  color: #dc3545;
}

/* Estilos Modal (necesitas crear SimpleModal.vue) */
.modal-form .form-group {
  margin-bottom: 15px;
}
.modal-form label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.modal-form input,
.modal-form select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  gap: 10px;
}
.modal-actions button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.cancel-button {
  background-color: #6c757d;
  color: white;
}
.save-button {
  background-color: #28a745;
  color: white;
}
.save-button:disabled {
  background-color: #aaa;
}
</style>
