import { defineStore } from 'pinia';
import apiClient from '@/services/api';
import { ref } from 'vue';

export const useProductStore = defineStore('products', () => {
  // Estado
  const products = ref([]); // Lista de productos
  const product = ref(null); // Producto individual para detalle/edición
  const pagination = ref({ // Información de paginación
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
    totalPages: 1,
  });
  const loading = ref(false);
  const error = ref(null);

  // --- Acciones CRUD ---

  async function fetchProducts(page = 1, search = '') {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/catalogo/productos/', {
        params: {
          page: page,
          search: search // Permitir búsqueda si el backend la soporta
        }
      });
      products.value = response.data.results;
      pagination.value = {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        currentPage: page,
        // Asumiendo PAGE_SIZE=10 del backend
        totalPages: Math.ceil(response.data.count / 10)
      };
    } catch (err) {
      console.error("Error fetching products:", err);
      error.value = 'No se pudieron cargar los productos.';
      products.value = []; // Limpiar en caso de error
    } finally {
      loading.value = false;
    }
  }

  async function fetchProduct(id) {
    loading.value = true;
    error.value = null;
    product.value = null;
    try {
      const response = await apiClient.get(`/catalogo/productos/${id}/`);
      product.value = response.data;
    } catch (err) {
      console.error(`Error fetching product ${id}:`, err);
      error.value = 'No se pudo cargar el producto.';
    } finally {
      loading.value = false;
    }
  }

  async function createProduct(productData) {
    loading.value = true;
    error.value = null;
    try {
      // Nota: El backend espera IDs para las relaciones (marca, categoria, etc.)
      // El formulario deberá enviar los IDs correctos.
      const response = await apiClient.post('/catalogo/productos/', productData);
      // Podríamos añadir el nuevo producto a la lista localmente
      // o simplemente recargar la página actual
      await fetchProducts(pagination.value.currentPage);
      return response.data; // Devuelve el producto creado
    } catch (err) {
      console.error("Error creating product:", err.response?.data || err);
      error.value = parseApiErrors(err.response?.data) || 'Error al crear el producto.';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateProduct(id, productData) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.put(`/catalogo/productos/${id}/`, productData);
      product.value = null; // Limpiar vista de detalle/edición
      await fetchProducts(pagination.value.currentPage); // Recargar lista
      return response.data;
    } catch (err) {
      console.error(`Error updating product ${id}:`, err.response?.data || err);
      error.value = parseApiErrors(err.response?.data) || 'Error al actualizar el producto.';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function deleteProduct(id) {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/catalogo/productos/${id}/`);
      await fetchProducts(pagination.value.currentPage); // Recargar lista
    } catch (err) {
      console.error(`Error deleting product ${id}:`, err);
       if (err.response && err.response.status === 400 && err.response.data?.detail?.includes('protected')) {
           error.value = 'No se puede eliminar: el producto está en uso (ventas, inventario, etc.).';
      } else {
           error.value = 'Error al eliminar el producto.';
      }
    } finally {
      loading.value = false;
    }
  }

  // Helper para parsear errores de la API de DRF
  function parseApiErrors(apiErrors) {
      if (!apiErrors) return null;
      let messages = [];
      for (const key in apiErrors) {
          if (Object.hasOwnProperty.call(apiErrors, key)) {
              const errorsForKey = apiErrors[key];
              if (Array.isArray(errorsForKey)) {
                  messages.push(`${key}: ${errorsForKey.join(', ')}`);
              } else {
                   messages.push(`${key}: ${errorsForKey}`);
              }
          }
      }
      return messages.join(' | ');
  }


  // Exponer estado y acciones
  return {
    products,
    product,
    pagination,
    loading,
    error,
    fetchProducts,
    fetchProduct,
    createProduct,
    updateProduct,
    deleteProduct
  }
});
