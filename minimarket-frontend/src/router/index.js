import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView from '../views/LoginView.vue'
import AdminLayout from '../layouts/AdminLayout.vue'
import DashboardView from '../views/admin/DashboardView.vue'

// Importaciones dinámicas (Lazy Loading)
const ProductListView = () => import('../views/admin/products/ProductListView.vue')
const ProductCreateView = () => import('../views/admin/products/ProductCreateView.vue')
const ProductEditView = () => import('../views/admin/products/ProductEditView.vue')
const CategoryListView = () => import('../views/admin/categories/CategoryListView.vue')
const UnitListView = () => import('../views/admin/units/UnitListView.vue') // DESCOMENTADO
const BrandListView = () => import('../views/admin/brands/BrandListView.vue') // NUEVO
const TaxListView = () => import('../views/admin/taxes/TaxListView.vue') // NUEVO
const PriceListView = () => import('../views/admin/prices/PriceListView.vue') // DESCOMENTADO

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      beforeEnter: (to, from, next) => {
        const authStore = useAuthStore()
        if (authStore.isAuthenticated) next({ name: 'admin-dashboard' })
        else next()
      },
    },
    // --- Rutas Protegidas ---
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true },
      children: [
        { path: 'dashboard', name: 'admin-dashboard', component: DashboardView },
        // Catálogo
        { path: 'productos', name: 'admin-products', component: ProductListView },
        { path: 'productos/nuevo', name: 'admin-product-create', component: ProductCreateView },
        {
          path: 'productos/editar/:id',
          name: 'admin-product-edit',
          component: ProductEditView,
          props: true,
        },
        { path: 'categorias', name: 'admin-categories', component: CategoryListView },
        { path: 'unidades', name: 'admin-units', component: UnitListView }, // DESCOMENTADO
        { path: 'marcas', name: 'admin-brands', component: BrandListView }, // NUEVO
        { path: 'impuestos', name: 'admin-taxes', component: TaxListView }, // NUEVO
        { path: 'precios', name: 'admin-pricelists', component: PriceListView }, // DESCOMENTADO y renombrado name
        // --- TODO: Añadir rutas de Inventario, Gestión, Finanzas, Seguridad ---
      ],
    },
    // --- Default & 404 ---
    {
      path: '/',
      redirect: (to) => {
        const a = useAuthStore()
        return a.isAuthenticated ? { name: 'admin-dashboard' } : { name: 'login' }
      },
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', redirect: '/' },
  ],
})

// --- Guardia Global ---
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.matched.some((record) => record.meta.requiresAuth) && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
