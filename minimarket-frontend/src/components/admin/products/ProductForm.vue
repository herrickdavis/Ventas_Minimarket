<template>
  <div class="product-form-container">
    <h2>{{ isEditing ? 'Editar Producto' : 'Nuevo Producto' }}</h2>
    <form @submit.prevent="submitForm">
      <div v-if="formError" class="error-message global-error">{{ formError }}</div>

      <div class="form-grid">
        <FormField label="Nombre:" required>
          <input type="text" v-model="productData.nombre" required />
        </FormField>
        <FormField label="SKU:">
          <input type="text" v-model="productData.sku" />
        </FormField>
        <FormField label="Tipo:" required>
          <select v-model="productData.tipo" required>
            <option value="simple">Simple</option>
            <option value="variable">Variable</option>
            <option value="combo">Combo</option>
          </select>
        </FormField>
        <FormField label="Categoría:" required>
          <select v-model="productData.categoria" required>
            <option :value="null">-- Seleccione --</option>
            <option v-for="cat in categoryOptions" :key="cat.id" :value="cat.id">
              {{ cat.nombre }}
            </option>
          </select>
        </FormField>
        <FormField label="Marca:">
          <select v-model="productData.marca">
            <option :value="null">-- Seleccione --</option>
            <option v-for="brand in brandOptions" :key="brand.id" :value="brand.id">
              {{ brand.nombre }}
            </option>
          </select>
          <small v-if="brandLoading">Cargando marcas...</small>
        </FormField>
        <FormField label="Unidad Base:" required>
          <select v-model="productData.unidad_base" required>
            <option :value="null">-- Seleccione --</option>
            <option v-for="unit in unitOptions" :key="unit.id" :value="unit.id">
              {{ unit.nombre }} ({{ unit.codigo }})
            </option>
          </select>
          <small v-if="unitLoading">Cargando unidades...</small>
        </FormField>
        <FormField label="Clase Impuesto:">
          <select v-model="productData.clase_impuesto">
            <option :value="null">-- Ninguno --</option>
            <option v-for="tax in taxOptions" :key="tax.id" :value="tax.id">
              {{ tax.nombre }}
            </option>
          </select>
          <small v-if="taxLoading">Cargando impuestos...</small>
        </FormField>
        <FormField label="Umbral Bajo Stock:">
          <input type="number" step="any" min="0" v-model.number="productData.umbral_bajo_stock" />
        </FormField>
        <FormField label="URL Imagen:">
          <input type="url" v-model="productData.imagen_url" />
        </FormField>
      </div>

      <FormField label="Descripción:" class="full-width">
        <textarea v-model="productData.descripcion" rows="3"></textarea>
      </FormField>

      <div class="form-group checkboxes">
        <label><input type="checkbox" v-model="productData.es_vendible" /> Es Vendible</label>
        <label><input type="checkbox" v-model="productData.es_comprable" /> Es Comprable</label>
        <label
          ><input type="checkbox" v-model="productData.es_producto_fisico" /> Es Producto
          Físico</label
        >
      </div>

      <section v-if="productData.tipo === 'variable'" class="variants-section">
        <h3>Variantes del Producto</h3>
        <small class="error-message" v-if="variantError">{{ variantError }}</small>
        <div v-for="(variant, index) in productData.variantes" :key="index" class="variant-item">
          <input
            type="text"
            v-model="variant.nombre"
            placeholder="Nombre Variante (ej: 500g)"
            required
          />
          <input type="text" v-model="variant.sku" placeholder="SKU Variante (opcional)" />
          <input
            type="number"
            step="0.01"
            min="0"
            v-model.number="variant.precio_sobrescrito"
            placeholder="Precio (opcional)"
          />
          <input
            type="text"
            v-model="variant.datos_atributo_str"
            placeholder='Atributos JSON (ej: {"peso": "500g"})'
          />
          <button type="button" @click="removeVariant(index)" class="remove-variant-btn">✖</button>
        </div>
        <button type="button" @click="addVariant" class="add-variant-btn">+ Añadir Variante</button>
      </section>

      <section v-if="productData.tipo === 'combo'" class="combo-section">
        <h3>Items del Combo</h3>
        <small class="error-message" v-if="comboError">{{ comboError }}</small>
        <div v-for="(item, index) in productData.items_combo" :key="index" class="combo-item">
          <select v-model="item.producto_item" required>
            <option :value="null">-- Seleccione Producto --</option>
            <option v-for="p in simpleProductsForCombo" :key="p.id" :value="p.id">
              {{ p.nombre }}
            </option>
          </select>
          <input
            type="number"
            step="any"
            min="0.001"
            v-model.number="item.cantidad_item"
            placeholder="Cantidad"
            required
          />
          <button type="button" @click="removeItemCombo(index)" class="remove-item-btn">✖</button>
        </div>
        <button type="button" @click="addItemCombo" class="add-item-btn">
          + Añadir Item al Combo
        </button>
      </section>

      <div class="form-actions">
        <button type="button" @click="cancelForm" class="cancel-button">Cancelar</button>
        <button type="submit" :disabled="isSubmitting" class="save-button">
          {{ isSubmitting ? 'Guardando...' : isEditing ? 'Actualizar Producto' : 'Crear Producto' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, reactive } from 'vue'
import { useProductStore } from '@/stores/products'
import { useCategoryStore } from '@/stores/categories'
import { useBrandStore } from '@/stores/brands' // Necesitas crear esta store
import { useUnitStore } from '@/stores/units' // Necesitas crear esta store
import { useTaxStore } from '@/stores/taxes' // Necesitas crear esta store
import { storeToRefs } from 'pinia'
import { useRouter, useRoute } from 'vue-router'
import FormField from '@/components/FormField.vue' // Asumiendo componente para labels/inputs

const props = defineProps({ productId: { type: [String, Number], default: null } })

const productStore = useProductStore()
const categoryStore = useCategoryStore()
const brandStore = useBrandStore()
const unitStore = useUnitStore()
const taxStore = useTaxStore()

const router = useRouter()
const route = useRoute()

const isEditing = computed(() => !!props.productId)
const formError = ref(null)
const isSubmitting = ref(false) // Para controlar el estado de envío

// Usar reactive para manejar el objeto complejo del formulario
const productData = reactive({
  nombre: '',
  sku: '',
  descripcion: '',
  tipo: 'simple',
  marca: null,
  categoria: null,
  clase_impuesto: null,
  unidad_base: null,
  es_vendible: true,
  es_comprable: true,
  es_producto_fisico: true,
  umbral_bajo_stock: null,
  imagen_url: '',
  variantes: [], // Para tipo 'variable'
  items_combo: [], // Para tipo 'combo'
})

// Cargar opciones para selects
const { categories: categoryOptions, loading: catLoading } = storeToRefs(categoryStore)
const { brands: brandOptions, loading: brandLoading } = storeToRefs(brandStore)
const { units: unitOptions, loading: unitLoading } = storeToRefs(unitStore)
const { taxes: taxOptions, loading: taxLoading } = storeToRefs(taxStore)
const { products: allProducts } = storeToRefs(productStore) // Para combo

onMounted(async () => {
  // Cargar todas las opciones necesarias
  categoryStore.fetchCategories()
  brandStore.fetchBrands() // Cargar marcas
  unitStore.fetchUnits() // Cargar unidades
  taxStore.fetchTaxes() // Cargar impuestos
  productStore.fetchProducts(1, '', 1000) // Cargar productos para combo (sin paginación)

  if (isEditing.value) {
    await productStore.fetchProduct(props.productId)
    if (productStore.product) {
      // Mapear datos al estado reactivo
      Object.assign(productData, {
        ...productStore.product,
        // Asegurar IDs para FKs
        marca: productStore.product.marca || null,
        categoria: productStore.product.categoria_id || null, // API da categoria (string) y no ID?
        clase_impuesto: productStore.product.clase_impuesto || null,
        unidad_base: productStore.product.unidad_base_id || null, // API da unidad_base (string)?
        // Mapear variantes y combos si existen
        variantes: (productStore.product.variantes || []).map((v) => ({
          ...v,
          datos_atributo_str: JSON.stringify(v.datos_atributo || {}),
        })),
        items_combo: (productStore.product.items_combo || []).map((c) => ({
          ...c,
          producto_item: c.producto_item_id,
        })), // Asumiendo API devuelve ID
      })
      // Corrección FKs si API devuelve objetos
      productData.marca = productStore.product.marca?.id ?? productData.marca
      productData.clase_impuesto =
        productStore.product.clase_impuesto?.id ?? productData.clase_impuesto
    } else {
      formError.value = 'No se pudo cargar el producto para editar.'
    }
  }
})

// --- Lógica Variantes ---
const variantError = ref(null)
const addVariant = () => {
  productData.variantes.push({
    nombre: '',
    sku: '',
    precio_sobrescrito: null,
    datos_atributo_str: '{}',
  })
}
const removeVariant = (index) => {
  productData.variantes.splice(index, 1)
}
const validateAndParseVariants = () => {
  variantError.value = null
  const parsedVariants = []
  for (const variant of productData.variantes) {
    if (!variant.nombre) {
      variantError.value = 'Todas las variantes deben tener un nombre.'
      return null
    }
    try {
      variant.datos_atributo = JSON.parse(variant.datos_atributo_str || '{}')
      // Eliminar la versión string antes de enviar
      const { datos_atributo_str, ...rest } = variant
      parsedVariants.push(rest)
    } catch (e) {
      variantError.value = `Error en JSON de atributos de la variante "${variant.nombre}": ${e.message}`
      return null
    }
  }
  return parsedVariants
}

// --- Lógica Combos ---
const comboError = ref(null)
const simpleProductsForCombo = computed(() => {
  // Filtrar productos que no sean tipo 'combo' para evitar recursión
  return allProducts.value.filter((p) => p.tipo !== 'combo')
})
const addItemCombo = () => {
  productData.items_combo.push({ producto_item: null, cantidad_item: 1 })
}
const removeItemCombo = (index) => {
  productData.items_combo.splice(index, 1)
}
const validateCombos = () => {
  comboError.value = null
  for (const item of productData.items_combo) {
    if (!item.producto_item || !item.cantidad_item || item.cantidad_item <= 0) {
      comboError.value = 'Todos los items del combo deben tener un producto y cantidad válida.'
      return false
    }
  }
  return true
}

// Enviar formulario
const submitForm = async () => {
  formError.value = null
  isSubmitting.value = true

  const dataToSend = { ...productData }

  // Limpiar/Validar Variantes si aplica
  if (dataToSend.tipo === 'variable') {
    const parsedVariants = validateAndParseVariants()
    if (!parsedVariants) {
      isSubmitting.value = false
      return
    }
    dataToSend.variantes_set = parsedVariants // DRF anidado espera _set
    dataToSend.items_combo = undefined // No enviar combos
    dataToSend.items_combo_set = []
  } else {
    dataToSend.variantes = undefined // No enviar variantes
    dataToSend.variantes_set = []
  }

  // Limpiar/Validar Combos si aplica
  if (dataToSend.tipo === 'combo') {
    if (!validateCombos()) {
      isSubmitting.value = false
      return
    }
    dataToSend.items_combo_set = dataToSend.items_combo // DRF anidado espera _set
    dataToSend.variantes = undefined // No enviar variantes
    dataToSend.variantes_set = []
  } else if (dataToSend.tipo !== 'variable') {
    // Si no es combo ni variable
    dataToSend.items_combo = undefined // No enviar combos
    dataToSend.items_combo_set = []
  }

  // Ajustar campos numéricos y FKs
  if (dataToSend.umbral_bajo_stock === '' || dataToSend.umbral_bajo_stock === null)
    dataToSend.umbral_bajo_stock = null
  else dataToSend.umbral_bajo_stock = Number(dataToSend.umbral_bajo_stock)

  // Asegurar que las FK envíen solo el ID
  dataToSend.marca = dataToSend.marca || null
  dataToSend.categoria = dataToSend.categoria || null
  dataToSend.unidad_base = dataToSend.unidad_base || null
  dataToSend.clase_impuesto = dataToSend.clase_impuesto || null

  // Remover campos extra antes de enviar
  delete dataToSend.variantes
  delete dataToSend.items_combo

  console.log('Enviando datos:', dataToSend) // Para depurar

  let result = null
  try {
    if (isEditing.value) {
      result = await productStore.updateProduct(props.productId, dataToSend)
    } else {
      result = await productStore.createProduct(dataToSend)
    }

    if (result) {
      router.push({ name: 'admin-products' })
    } else {
      formError.value = productStore.error || 'Ocurrió un error desconocido.'
    }
  } catch (e) {
    console.error('Error inesperado en submitForm:', e)
    formError.value = 'Error inesperado al guardar.'
  } finally {
    isSubmitting.value = false
  }
}

const cancelForm = () => {
  router.push({ name: 'admin-products' })
}
</script>

<style scoped>
.product-form-container {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.product-form-container h2 {
  margin-top: 0;
  margin-bottom: 30px;
}
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px 25px;
} /* Más gap horizontal */
.form-group {
  margin-bottom: 0; /* Controlado por el grid gap */
}
.form-group.full-width {
  grid-column: 1 / -1;
}
.form-group.checkboxes {
  grid-column: 1 / -1;
  display: flex;
  flex-wrap: wrap;
  gap: 15px 30px;
  align-items: center;
  padding-top: 10px;
}
.form-group.checkboxes label {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0;
  font-weight: normal;
}
.form-group.checkboxes input[type='checkbox'] {
  width: auto;
}
label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  font-size: 0.9rem;
  color: #495057;
}
input[type='text'],
input[type='number'],
input[type='url'],
select,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 0.95rem;
}
input:focus,
select:focus,
textarea:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
textarea {
  resize: vertical;
  min-height: 80px;
}
small {
  font-size: 0.8rem;
  color: #6c757d;
  display: block;
  margin-top: 4px;
}

.error-message {
  color: #dc3545;
  margin-bottom: 15px;
  font-size: 0.9rem;
}
.global-error {
  border: 1px solid #dc3545;
  background-color: #f8d7da;
  padding: 10px;
  border-radius: 4px;
}

/* Estilos Secciones Variantes y Combo */
.variants-section,
.combo-section {
  margin-top: 30px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}
.variants-section h3,
.combo-section h3 {
  margin-bottom: 15px;
}
.variant-item,
.combo-item {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr auto auto; /* Ajustado para combo */
  gap: 10px;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}
.combo-item {
  grid-template-columns: 3fr 1fr auto;
} /* Layout diferente para combo */
.variant-item input,
.combo-item input,
.combo-item select {
  font-size: 0.9rem;
  padding: 8px;
}
.remove-variant-btn,
.remove-item-btn {
  background: none;
  border: none;
  color: #dc3545;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 0 5px;
}
.add-variant-btn,
.add-item-btn {
  background-color: #e9ecef;
  color: #495057;
  border: 1px dashed #ced4da;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  font-size: 0.9rem;
}
.add-variant-btn:hover,
.add-item-btn:hover {
  background-color: #dee2e6;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 30px;
  gap: 10px;
}
.form-actions button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
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
  cursor: not-allowed;
}
</style>
