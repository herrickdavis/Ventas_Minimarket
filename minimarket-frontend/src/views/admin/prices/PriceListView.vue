<template>
  <div class="list-view-container">
    <h1>Gestión de Listas de Precios</h1>
    <button @click="openPriceListModal()" class="add-button">Nueva Lista</button>

    <div v-if="loading" class="loading">Cargando...</div>
    <div v-if="error" class="error-message global-error">{{ error }}</div>

    <table v-if="!loading && priceLists.length > 0" class="data-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Descripción</th>
          <th>Activo</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="list in priceLists" :key="list.id">
          <td>{{ list.id }}</td>
          <td>{{ list.nombre }}</td>
          <td>{{ list.descripcion || '-' }}</td>
          <td>{{ list.activo ? 'Sí' : 'No' }}</td>
          <td class="actions">
            <button @click="openPriceListModal(list)" class="edit-button" title="Editar Lista">
              ✏️
            </button>
            <button @click="viewRules(list)" class="view-button" title="Ver Reglas">👁️</button>
            <button
              @click="confirmDeletePriceList(list)"
              class="delete-button"
              title="Eliminar Lista"
            >
              🗑️
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-if="!loading && priceLists.length === 0">No hay listas de precios registradas.</p>

    <SimpleModal :show="showPriceListModal" @close="closePriceListModal">
      <h2>{{ editingPriceList ? 'Editar Lista' : 'Nueva Lista' }}</h2>
      <form @submit.prevent="handlePriceListSubmit" class="modal-form">
        <FormField label="Nombre:" required>
          <input type="text" v-model="priceListForm.nombre" required />
        </FormField>
        <FormField label="Descripción:">
          <textarea v-model="priceListForm.descripcion"></textarea>
        </FormField>
        <FormField label="">
          <label><input type="checkbox" v-model="priceListForm.activo" /> Activo</label>
        </FormField>
        <p v-if="formError" class="error-message">{{ formError }}</p>
        <div class="modal-actions">
          <button type="button" @click="closePriceListModal" class="cancel-button">Cancelar</button>
          <button type="submit" :disabled="loading" class="save-button">Guardar</button>
        </div>
      </form>
    </SimpleModal>

    <SimpleModal :show="showRulesModal" @close="closeRulesModal" modal-size="large">
      <h2>Reglas para: {{ currentPriceList?.nombre }}</h2>
      <button @click="openRuleModal()" class="add-button">Nueva Regla</button>
      <div v-if="loading" class="loading">Cargando reglas...</div>
      <div v-if="error" class="error-message global-error">{{ error }}</div>
      <table v-if="!loading && rules.length > 0" class="data-table rules-table">
        <thead>
          <tr>
            <th>Producto/Variante</th>
            <th>Unidad</th>
            <th>Precio</th>
            <th>Min. Cant.</th>
            <th>Fechas</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="rule in rules" :key="rule.id">
            <td>{{ getRuleTargetName(rule) }}</td>
            <td>{{ getUnitCode(rule.unidad) }}</td>
            <td>{{ rule.precio }}</td>
            <td>{{ rule.cantidad_minima }}</td>
            <td>{{ rule.fecha_inicio || '' }} - {{ rule.fecha_fin || '' }}</td>
            <td class="actions">
              <button @click="openRuleModal(rule)" class="edit-button" title="Editar Regla">
                ✏️
              </button>
              <button @click="confirmDeleteRule(rule)" class="delete-button" title="Eliminar Regla">
                🗑️
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="!loading && rules.length === 0">No hay reglas para esta lista.</p>
      <div class="modal-actions">
        <button type="button" @click="closeRulesModal" class="cancel-button">Cerrar</button>
      </div>
    </SimpleModal>

    <SimpleModal :show="showRuleModal" @close="closeRuleModal">
      <h2>{{ editingRule ? 'Editar Regla' : 'Nueva Regla' }}</h2>
      <form @submit.prevent="handleRuleSubmit" class="modal-form">
        <FormField label="Producto:" required>
          <select v-model="ruleForm.producto">
            <option :value="null">Seleccione</option>
          </select>
        </FormField>
        <FormField label="Unidad:" required>
          <select v-model="ruleForm.unidad">
            <option :value="null">Seleccione</option>
          </select>
        </FormField>
        <FormField label="Precio:" required>
          <input type="number" step="0.01" min="0" v-model.number="ruleForm.precio" required />
        </FormField>
        <FormField label="Cantidad Mínima:">
          <input type="number" step="0.001" min="0" v-model.number="ruleForm.cantidad_minima" />
        </FormField>
        <FormField label="Fecha Inicio:">
          <input type="date" v-model="ruleForm.fecha_inicio" />
        </FormField>
        <FormField label="Fecha Fin:">
          <input type="date" v-model="ruleForm.fecha_fin" />
        </FormField>
        <p v-if="formError" class="error-message">{{ formError }}</p>
        <div class="modal-actions">
          <button type="button" @click="closeRuleModal" class="cancel-button">Cancelar</button>
          <button type="submit" :disabled="loading" class="save-button">Guardar</button>
        </div>
      </form>
    </SimpleModal>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { usePriceListStore } from '@/stores/pricelists'
import { useProductStore } from '@/stores/products' // Para nombres de productos
import { useUnitStore } from '@/stores/units' // Para nombres de unidades
import { storeToRefs } from 'pinia'
import SimpleModal from '@/components/SimpleModal.vue'
import FormField from '@/components/FormField.vue'

const priceListStore = usePriceListStore()
const productStore = useProductStore()
const unitStore = useUnitStore()

const { priceLists, rules, loading, error, currentPriceList } = storeToRefs(priceListStore)
const { products } = storeToRefs(productStore) // Para mostrar nombres
const { units } = storeToRefs(unitStore) // Para mostrar códigos

const showPriceListModal = ref(false)
const editingPriceList = ref(null)
const priceListForm = reactive({ nombre: '', descripcion: '', activo: true })

const showRulesModal = ref(false)
const showRuleModal = ref(false)
const editingRule = ref(null)
const ruleForm = reactive({
  /* ... campos de regla ... */
})

const formError = ref(null)

onMounted(() => {
  priceListStore.fetchPriceLists()
  productStore.fetchProducts(1, '', 1000) // Cargar productos para selects
  unitStore.fetchUnits() // Cargar unidades para selects
})

// --- Manejo Modal Listas ---
const openPriceListModal = (list = null) => {
  formError.value = null
  error.value = null
  if (list) {
    editingPriceList.value = list
    Object.assign(priceListForm, {
      nombre: list.nombre,
      descripcion: list.descripcion,
      activo: list.activo,
    })
  } else {
    editingPriceList.value = null
    Object.assign(priceListForm, { nombre: '', descripcion: '', activo: true })
  }
  showPriceListModal.value = true
}
const closePriceListModal = () => {
  showPriceListModal.value = false
  editingPriceList.value = null
}
const handlePriceListSubmit = async () => {
  // TODO: Implementar createPriceList y updatePriceList en la store
  alert('Funcionalidad pendiente')
  // if (result) closePriceListModal(); else formError.value = priceListStore.error;
}
const confirmDeletePriceList = (list) => {
  error.value = null
  // TODO: Implementar deletePriceList en la store
  alert('Funcionalidad pendiente')
  // if (window.confirm(...)) priceListStore.deletePriceList(list.id);
}

// --- Manejo Modal Reglas ---
const viewRules = async (list) => {
  priceListStore.currentPriceList = list // Guardar lista actual
  await priceListStore.fetchRulesForList(list.id)
  showRulesModal.value = true
}
const closeRulesModal = () => {
  showRulesModal.value = false
  priceListStore.currentPriceList = null
  rules.value = []
}

const openRuleModal = (rule = null) => {
  formError.value = null
  error.value = null
  // TODO: Resetear ruleForm
  if (rule) {
    editingRule.value = rule
    // TODO: Llenar ruleForm con datos de rule
  } else {
    editingRule.value = null
  }
  showRuleModal.value = true
}
const closeRuleModal = () => {
  showRuleModal.value = false
  editingRule.value = null
}
const handleRuleSubmit = async () => {
  // TODO: Implementar createPriceRule y updatePriceRule
  alert('Funcionalidad pendiente')
  // if (result) { closeRuleModal(); priceListStore.fetchRulesForList(...); } else { formError.value = ... }
}
const confirmDeleteRule = (rule) => {
  error.value = null
  // TODO: Implementar deletePriceRule
  alert('Funcionalidad pendiente')
  // if (window.confirm(...)) priceListStore.deletePriceRule(rule.id, currentPriceList.value.id);
}

// --- Helpers para mostrar nombres/códigos en tabla de reglas ---
const getRuleTargetName = (rule) => {
  // TODO: Buscar nombre de producto o variante basado en rule.producto / rule.variante
  return `ID Prod: ${rule.producto || '-'} / Var: ${rule.variante || '-'}`
}
const getUnitCode = (unitId) => {
  const unit = units.value.find((u) => u.id === unitId)
  return unit ? unit.codigo : 'ID:' + unitId
}
</script>

<style scoped>
@import '@/assets/admin-tables.css';
@import '@/assets/admin-modals.css';
.rules-table td,
.rules-table th {
  font-size: 0.85rem;
  padding: 8px 10px;
}
.view-button {
  color: #17a2b8;
  margin-left: 5px;
} /* Cyan */
/* Estilo para modal grande */
.modal-overlay >>> .modal-content.large {
  max-width: 800px;
}
</style>
