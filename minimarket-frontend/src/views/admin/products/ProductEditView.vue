<template>
  <div>
    <ProductForm :product-id="route.params.id" />
  </div>
</template>

<script setup>
import ProductForm from '@/components/admin/products/ProductForm.vue';
import { useRoute } from 'vue-router';

const route = useRoute(); // Para acceder a los parámetros de la URL (el ID)
</script>
