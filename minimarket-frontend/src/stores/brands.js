import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { ref } from 'vue';

export const useBrandStore = defineStore('brands', () => {
  const brands = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const currentBrand = ref(null);

  async function fetchBrands() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/catalogo/marcas/?page_size=1000');
      brands.value = response.data.results;
    } catch (err) {
      console.error("Error fetching brands:", err);
      error.value = 'No se pudieron cargar las marcas.';
    } finally {
      loading.value = false;
    }
  }

  async function fetchBrand(id) {
    loading.value = true;
    error.value = null;
    currentBrand.value = null;
    try {
      const response = await apiClient.get(`/catalogo/marcas/${id}/`);
      currentBrand.value = response.data;
    } catch (err) {
      console.error(`Error fetching brand ${id}:`, err);
      error.value = 'No se pudo cargar la marca.';
    } finally {
      loading.value = false;
    }
  }

  async function createBrand(brandData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/catalogo/marcas/', brandData);
      await fetchBrands();
      return response.data;
    } catch (err) {
      console.error("Error creating brand:", err.response?.data || err);
      error.value = err.response?.data?.nombre?.[0] || 'Error al crear la marca.';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateBrand(id, brandData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/catalogo/marcas/${id}/`, brandData);
      await fetchBrands();
      currentBrand.value = null;
      return response.data;
    } catch (err) {
      console.error(`Error updating brand ${id}:`, err.response?.data || err);
      error.value = err.response?.data?.nombre?.[0] || 'Error al actualizar la marca.';
      return null;
    } finally {
      loading.value = false;
    }
  }

   async function deleteBrand(id) {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/catalogo/marcas/${id}/`);
      await fetchBrands();
    } catch (err) {
      console.error(`Error deleting brand ${id}:`, err);
       if (err.response && err.response.status >= 400 && err.response.data?.detail?.includes('protected')) {
           error.value = 'No se puede eliminar: la marca está en uso.';
      } else {
           error.value = 'Error al eliminar la marca.';
      }
    } finally {
      loading.value = false;
    }
  }

  return {
    brands, loading, error, currentBrand,
    fetchBrands, fetchBrand, createBrand, updateBrand, deleteBrand
  }
});
