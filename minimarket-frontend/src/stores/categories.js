import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { ref } from 'vue';

export const useCategoryStore = defineStore('categories', () => {
  const categories = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const currentCategory = ref(null);

  async function fetchCategories() {
    loading.value = true;
    error.value = null;
    try {
      // Pedir todas las categorías sin paginación para los selects
      const response = await apiClient.get('/catalogo/categorias/?page_size=1000');
      categories.value = response.data.results;
    } catch (err) {
      console.error("Error fetching categories:", err);
      error.value = 'No se pudieron cargar las categorías.';
    } finally {
      loading.value = false;
    }
  }

  async function fetchCategory(id) {
    loading.value = true;
    error.value = null;
    currentCategory.value = null;
    try {
      const response = await apiClient.get(`/catalogo/categorias/${id}/`);
      currentCategory.value = response.data;
    } catch (err) {
      console.error(`Error fetching category ${id}:`, err);
      error.value = 'No se pudo cargar la categoría.';
    } finally {
      loading.value = false;
    }
  }

  async function createCategory(categoryData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/catalogo/categorias/', categoryData);
      await fetchCategories();
      return response.data;
    } catch (err) {
      console.error("Error creating category:", err.response?.data || err);
      error.value = err.response?.data?.nombre?.[0] || 'Error al crear la categoría.';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateCategory(id, categoryData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/catalogo/categorias/${id}/`, categoryData);
      await fetchCategories();
      currentCategory.value = null;
      return response.data;
    } catch (err) {
      console.error(`Error updating category ${id}:`, err.response?.data || err);
      error.value = err.response?.data?.nombre?.[0] || 'Error al actualizar la categoría.';
      return null;
    } finally {
      loading.value = false;
    }
  }

   async function deleteCategory(id) {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/catalogo/categorias/${id}/`);
      await fetchCategories();
    } catch (err) {
      console.error(`Error deleting category ${id}:`, err);
      if (err.response && err.response.status >= 400 && err.response.data?.detail?.includes('protected')) {
           error.value = 'No se puede eliminar: la categoría está en uso.';
      } else {
           error.value = 'Error al eliminar la categoría.';
      }
    } finally {
      loading.value = false;
    }
  }

  return {
    categories, loading, error, currentCategory,
    fetchCategories, fetchCategory, createCategory, updateCategory, deleteCategory
  }
});
