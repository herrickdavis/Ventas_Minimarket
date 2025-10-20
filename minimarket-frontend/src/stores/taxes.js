import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { ref } from 'vue';

export const useTaxStore = defineStore('taxes', () => {
  const taxes = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const currentTax = ref(null);

  async function fetchTaxes() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/catalogo/clases-impuestos/?page_size=1000');
      taxes.value = response.data.results;
    } catch (err) {
      console.error("Error fetching taxes:", err);
      error.value = 'No se pudieron cargar las clases de impuesto.';
    } finally {
      loading.value = false;
    }
  }

  async function fetchTax(id) {
    loading.value = true;
    error.value = null;
    currentTax.value = null;
    try {
      const response = await apiClient.get(`/catalogo/clases-impuestos/${id}/`);
      currentTax.value = response.data;
    } catch (err) {
      console.error(`Error fetching tax ${id}:`, err);
      error.value = 'No se pudo cargar la clase de impuesto.';
    } finally {
      loading.value = false;
    }
  }

  async function createTax(taxData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/catalogo/clases-impuestos/', taxData);
      await fetchTaxes();
      return response.data;
    } catch (err) {
      console.error("Error creating tax:", err.response?.data || err);
      error.value = err.response?.data?.nombre?.[0] || 'Error al crear la clase de impuesto.';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateTax(id, taxData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/catalogo/clases-impuestos/${id}/`, taxData);
      await fetchTaxes();
      currentTax.value = null;
      return response.data;
    } catch (err) {
      console.error(`Error updating tax ${id}:`, err.response?.data || err);
      error.value = err.response?.data?.nombre?.[0] || 'Error al actualizar la clase de impuesto.';
      return null;
    } finally {
      loading.value = false;
    }
  }

   async function deleteTax(id) {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/catalogo/clases-impuestos/${id}/`);
      await fetchTaxes();
    } catch (err) {
      console.error(`Error deleting tax ${id}:`, err);
       if (err.response && err.response.status >= 400 && err.response.data?.detail?.includes('protected')) {
           error.value = 'No se puede eliminar: la clase de impuesto está en uso.';
      } else {
           error.value = 'Error al eliminar la clase de impuesto.';
      }
    } finally {
      loading.value = false;
    }
  }

  return {
    taxes, loading, error, currentTax,
    fetchTaxes, fetchTax, createTax, updateTax, deleteTax
  }
});
