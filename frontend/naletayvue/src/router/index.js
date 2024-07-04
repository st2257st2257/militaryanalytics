import { createRouter, createWebHistory } from 'vue-router';
import { defineAsyncComponent } from 'vue';
import HomeView from "@/views/HomeView.vue";
import ErrorMessage from '@/components/ErrorMessage.vue';
import LoadingController from '@/components/LoadingController.vue';
import PlaceholderView from '@/views/PlaceholderView.vue';
import store from '@/store';

const loadView = (view) => {
  return defineAsyncComponent({
    loader: () => import(`@/views/${view}.vue`),
    loadingComponent: LoadingController,
    errorComponent: ErrorMessage,
    delay: 200,
    timeout: 30000,
  });
};

const loadAccountView = (view) => {
  return defineAsyncComponent({
    loader: () => import(`@/views/userPages/${view}.vue`),
    loadingComponent: LoadingController,
    errorComponent: ErrorMessage,
    delay: 200,
    timeout: 30000,
  });
};

const routes = [
  {
    path: '/',
    name: 'Placeholder',
    component: PlaceholderView,
    meta: { showBreadcrumbs: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: HomeView,
    meta: { breadcrumb: 'Главная', showBreadcrumbs: false }
  },
  {
    path: '/profile/:userId',
    name: 'UserProfiles',
    component: loadAccountView('UserProfile'),
    props: true,
    meta: { breadcrumb: 'Профиль пользователя №', showBreadcrumbs: true }
  },
  {
    path: '/recovery',
    name: 'RecoveryPassword',
    component: loadAccountView('RecoveryPassword'),
    meta: { breadcrumb: 'Восстановление пароля', showBreadcrumbs: true }
  },
  {
    path: '/profile',
    component: loadView('UserPageView'),
    meta: { requiresAuth: true, breadcrumb: 'Профиль', showBreadcrumbs: true },
    children: [
      {
        path: '',
        name: 'UserProfile',
        component: loadAccountView('UserProfile'),
        props: (route) => ({ userId: store.getters['user/currentUser'].username }),
        meta: { breadcrumb: '', showBreadcrumbs: true }
      },
      {
        path: 'upload',
        name: 'UploadAssortment',
        component: loadAccountView('uploadAssortment'),
        meta: { breadcrumb: 'Загрузка ассортимента', showBreadcrumbs: true }
      },
      {
        path: 'legal-info',
        name: 'LegalInfo',
        component: loadAccountView('LegalInfo'),
        meta: { breadcrumb: 'Юридическая информация', showBreadcrumbs: true }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: loadAccountView('Orders'),
        meta: { breadcrumb: 'Заказы', showBreadcrumbs: true }
      },
      {
        path: 'chat',
        name: 'Chats',
        props: (route) => ({ chatId: route.query.chatId }),
        component: loadAccountView('ChatView'),
        meta: { breadcrumb: 'Чат', showBreadcrumbs: true }
      },
      {
        path: 'settings',
        component: loadAccountView('SettingsView'),
        meta: { breadcrumb: 'Настройки', showBreadcrumbs: true },
        children: [
          {
            path: 'profile',
            name: 'ProfileSettings',
            component: loadAccountView('ProfileSettings'),
            meta: { breadcrumb: '', showBreadcrumbs: true }
          },
          {
            path: 'security',
            alias: '',
            name: 'SecuritySettings',
            component: loadAccountView('SecuritySettings'),
            meta: { breadcrumb: '', showBreadcrumbs: true }
          }
        ]
      }
    ]
  },
  {
    path: '/partners',
    name: 'PartnersPage',
    component: loadView('PartnersView'),
    meta: { breadcrumb: 'Партнеры', showBreadcrumbs: true }
  },
  {
    path: '/catalog',
    name: 'CatalogPage',
    component: loadView('CatalogView'),
    meta: { breadcrumb: 'Каталог', showBreadcrumbs: true }
  },
  {
    path: '/product/:id',
    name: 'ProductPage',
    component: loadView('ProductView'),
    props: true,
    meta: { 
      breadcrumb: `Артикул №`,
      showBreadcrumbs: true
    }
  },
  {
    path: '/cart',
    name: 'CartPage',
    component: loadView('CartView'),
    meta: { breadcrumb: 'Корзина', showBreadcrumbs: true }
  },
  {
    path: '/about',
    name: 'AboutPage',
    component: loadView('AboutProgramsView'),
    meta: { breadcrumb: 'О программе', showBreadcrumbs: true }
  },
  {
    path: '/programs',
    name: 'ProgramPage',
    component: loadView('GosProgramsView'),
    meta: { breadcrumb: 'Программы', showBreadcrumbs: true }
  },
  {
    path: '/customers',
    name: 'CustomersPage',
    component: loadView('ForCustomersView'),
    meta: { breadcrumb: 'Клиентам', showBreadcrumbs: true }
  },
  {
    path: '/suppliers',
    name: 'SuppliersPage',
    component: loadView('ForSuppliersView'),
    meta: { breadcrumb: 'Поставщикам', showBreadcrumbs: true }
  },
  {
    path: '/order/:orderId',
    name: 'OrderDetails',
    component: loadView('OrderDetailsView'),
    props: true,
    meta: { requiresAuth: true, breadcrumb: 'Детали заказа №', showBreadcrumbs: true, parent: 'UserProfile' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: ErrorMessage,
    props: {
      title: "Страница не найдена",
      message: "Извините, запрашиваемая страница не найдена. Пожалуйста, проверьте правильность введенного URL или вернитесь на главную страницу.",
      type: "notfound",
    },
    meta: { showBreadcrumbs: false }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else if (to.hash) {
      return {
        selector: to.hash,
        behavior: 'smooth',
      };
    } else if (to.path !== from.path) {
      return { top: 0, behavior: 'smooth' };
    }
  },
});


router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const isAuthenticated = store.getters['user/isAuthenticated'];

  if (!requiresAuth) {
    next();
    return;
  }

  if (isAuthenticated) {
    const userRole = store.getters['user/hasRole'];
    const allowedRoles = to.meta.allowedRoles;

    if (!allowedRoles || allowedRoles.includes(userRole)) {
      next();
      return;
    }

    next({ name: 'Home' });
    return;
  }

  next({ name: 'Home' });
});

export default router;
