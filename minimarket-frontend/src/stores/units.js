import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { ref } from 'vue';

export const useUnitStore = defineStore('units', () => {
  const units = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const currentUnit = ref(null);

  async function fetchUnits() {
    loading.value = true;
    error.value = null;
    try {
      // Pedir todas sin paginación para selects
      const response = await apiClient.get('/catalogo/unidades/?page_size=1000');
      units.value = response.data.results;
    } catch (err) {
      console.error("Error fetching units:", err);
      error.value = 'No se pudieron cargar las unidades.';
    } finally {
      loading.value = false;
    }
  }

  async function fetchUnit(id) {
    loading.value = true;
    error.value = null;
    currentUnit.value = null;
    try {
      const response = await apiClient.get(`/catalogo/unidades/${id}/`);
      currentUnit.value = response.data;
    } catch (err) {
      console.error(`Error fetching unit ${id}:`, err);
      error.value = 'No se pudo cargar la unidad.';
    } finally {
      loading.value = false;
    }
  }

  async function createUnit(unitData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.post('/catalogo/unidades/', unitData);
      await fetchUnits();
      return response.data;
    } catch (err) {
      console.error("Error creating unit:", err.response?.data || err);
      error.value = err.response?.data?.codigo?.[0] || err.response?.data?.nombre?.[0] || 'Error al crear la unidad.';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateUnit(id, unitData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/catalogo/unidades/${id}/`, unitData);
      await fetchUnits();
      currentUnit.value = null;
      return response.data;
    } catch (err) {
      console.error(`Error updating unit ${id}:`, err.response?.data || err);
      error.value = err.response?.data?.codigo?.[0] || err.response?.data?.nombre?.[0] || 'Error al actualizar la unidad.';
      return null;
    } finally {
      loading.value = false;
    }
  }

   async function deleteUnit(id) {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/catalogo/unidades/${id}/`);
      await fetchUnits();
    } catch (err) {
      console.error(`Error deleting unit ${id}:`, err);
       if (err.response && err.response.status >= 400 && err.response.data?.detail?.includes('protected')) {
           error.value = 'No se puede eliminar: la unidad está en uso.';
      } else {
           error.value = 'Error al eliminar la unidad.';
      }
    } finally {
      loading.value = false;
    }
  }

  return {
    units, loading, error, currentUnit,
    fetchUnits, fetchUnit, createUnit, updateUnit, deleteUnit
  }
});
