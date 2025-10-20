import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { ref } from 'vue';

export const usePriceListStore = defineStore('pricelists', () => {
  const priceLists = ref([]);
  const rules = ref([]); // Guardar reglas por separado o anidadas? Separado es más fácil
  const loading = ref(false);
  const error = ref(null);
  const currentPriceList = ref(null);

  // --- Listas de Precios ---
  async function fetchPriceLists() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/catalogo/listas-precios/?page_size=1000');
      priceLists.value = response.data.results;
    } catch (err) {
      console.error("Error fetching price lists:", err);
      error.value = 'No se pudieron cargar las listas de precios.';
    } finally {
      loading.value = false;
    }
  }
  async function createPriceList(data) { /* ... similar a otros create ... */ }
  async function updatePriceList(id, data) { /* ... similar a otros update ... */ }
  async function deletePriceList(id) { /* ... similar a otros delete ... */ }

  // --- Reglas de Precios ---
  async function fetchRulesForList(listId) {
     loading.value = true;
     error.value = null;
     rules.value = []; // Limpiar reglas anteriores
     try {
       // Asumiendo que el backend permite filtrar reglas por lista_precio_id
       const response = await apiClient.get(`/catalogo/reglas-precios/?lista_precio_id=${listId}&page_size=1000`);
       rules.value = response.data.results;
     } catch (err) {
       console.error(`Error fetching rules for list ${listId}:`, err);
       error.value = 'No se pudieron cargar las reglas de precio.';
     } finally {
       loading.value = false;
     }
  }
  async function createPriceRule(data) {
     // POST a /catalogo/reglas-precios/
     // data debe incluir lista_precio_id, producto_id o variante_id, unidad_id, precio, etc.
     // Luego, recargar las reglas con fetchRulesForList(data.lista_precio_id)
  }
  async function updatePriceRule(id, data) {
     // PUT a /catalogo/reglas-precios/{id}/
     // Luego, recargar las reglas
   }
  async function deletePriceRule(id, listId) {
     // DELETE a /catalogo/reglas-precios/{id}/
     // Luego, recargar las reglas con fetchRulesForList(listId)
  }


  return {
    priceLists, rules, loading, error, currentPriceList,
    fetchPriceLists, createPriceList, updatePriceList, deletePriceList,
    fetchRulesForList, createPriceRule, updatePriceRule, deletePriceRule
  }
});
