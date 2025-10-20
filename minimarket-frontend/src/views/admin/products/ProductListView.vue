<template>
  <div class="product-list-container">
    <h1>Gestión de Productos</h1>

    <button class="add-button" @click="goToCreateProduct">Nuevo Producto</button>

    <div v-if="productStore.loading" class="loading">Cargando productos...</div>
    <div v-if="productStore.error" class="error-message">{{ productStore.error }}</div>

    <table v-if="!productStore.loading && products.length > 0" class="products-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>SKU</th>
          <th>Nombre</th>
          <th>Tipo</th>
          <th>Categoría</th>
          <th>Marca</th>
          <th>Unidad Base</th>
          <th>Vendible</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.sku || '-' }}</td>
          <td>{{ product.nombre }}</td>
          <td>{{ product.tipo }}</td>
          <td>{{ product.categoria || '-' }}</td>
          <td>{{ product.marca || '-' }}</td>
          <td>{{ product.unidad_base || '-' }}</td>
          <td>{{ product.es_vendible ? 'Sí' : 'No' }}</td>
          <td>
            <button @click="goToEditProduct(product.id)" class="edit-button">Editar</button>
            <button @click="confirmDelete(product)" class="delete-button">Eliminar</button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!productStore.loading && products.length === 0">No hay productos registrados.</p>

    <div class="pagination" v-if="!productStore.loading && pagination.totalPages > 1">
        <button @click="changePage(pagination.currentPage - 1)" :disabled="!pagination.previous">
            &laquo; Anterior
        </button>
        <span>Página {{ pagination.currentPage }} de {{ pagination.totalPages }}</span>
        <button @click="changePage(pagination.currentPage + 1)" :disabled="!pagination.next">
            Siguiente &raquo;
        </button>
    </div>

  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useProductStore } from '@/stores/products';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router'; // Importar router

const productStore = useProductStore();
const { products, loading, error, pagination } = storeToRefs(productStore);
const router = useRouter(); // Instancia del router

// Cargar productos al montar
onMounted(() => {
  productStore.fetchProducts();
});

// Cambiar de página
const changePage = (page) => {
  if (page > 0 && page <= pagination.value.totalPages) {
    productStore.fetchProducts(page);
  }
};

// Confirmar eliminación
const confirmDelete = (product) => {
  if (window.confirm(`¿Estás seguro de que quieres eliminar el producto "${product.nombre}"? Esta acción no se puede deshacer.`)) {
    productStore.deleteProduct(product.id);
  }
};

// Navegación (requiere definir las rutas 'admin-product-create' y 'admin-product-edit')
const goToCreateProduct = () => {
    // router.push({ name: 'admin-product-create' });
    alert('Funcionalidad de Crear Producto pendiente.'); // Placeholder
};

const goToEditProduct = (productId) => {
    // router.push({ name: 'admin-product-edit', params: { id: productId } });
     alert(`Funcionalidad de Editar Producto ${productId} pendiente.`); // Placeholder
};

// TODO: Implementar búsqueda
// const searchTerm = ref('');
// const searchProducts = () => {
//   productStore.fetchProducts(1, searchTerm.value);
// };

</script>

<style scoped>
/* Estilos similares a CategoryListView, adaptados */
.product-list-container {
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

.products-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.products-table th,
.products-table td {
  border: 1px solid #dee2e6;
  padding: 10px 12px; /* Un poco menos padding */
  text-align: left;
  font-size: 0.9rem; /* Texto más pequeño */
  vertical-align: middle;
}

.products-table th {
  background-color: #f8f9fa;
  font-weight: bold;
}

.products-table tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}

.edit-button, .delete-button {
  padding: 5px 8px; /* Botones más pequeños */
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 5px;
  font-size: 0.8rem;
}

.edit-button {
  background-color: #ffc107;
  color: #212529;
}
.edit-button:hover { background-color: #e0a800; }

.delete-button {
  background-color: #dc3545;
  color: white;
}
.delete-button:hover { background-color: #c82333; }

.pagination {
  margin-top: 20px;
  text-align: center;
}
.pagination button {
  padding: 8px 12px;
  margin: 0 5px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.pagination button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
.pagination span {
  margin: 0 10px;
  vertical-align: middle;
}
</style>
