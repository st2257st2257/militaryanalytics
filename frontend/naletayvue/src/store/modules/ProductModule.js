import axios from 'axios';
import Product from '@/classes/marketplace/product.js';

const ProductModule = {
  namespaced: true,
  state: {
    products: {},
    types: [],
    filters: {},
  },
  mutations: {
    setProducts(state, productsData) {
      state.products = {};
      for (const [key, product] of Object.entries(productsData)) {
        const type = product.type;
        if (!state.products[type]) {
          state.products[type] = [];
        }

        if (product.appends && product.appends.second && product.appends.second.mainBranches && product.appends.second.mainPurposes) {
          const industries = extractValues(product.appends.second.mainBranches).join(', ');
          const applications = extractValues(product.appends.second.mainPurposes).join(', ');
          product.appends.second.mainBranches.value = industries;
          product.appends.second.mainPurposes.value = applications;
        }

        const newProduct = new Product({
          id: Number(key),
          ...product,
          ...product.appends,
        });
        
        state.products[type].push(newProduct);
      }
    },
    setTypes(state, types) {
      state.types = ['all', ...types];
    },
    setFilters(state, { type, filters }) {
      state.filters[type] = filters;
    },
  },
  actions: {
    async fetchProducts({ commit, dispatch, state }) {
      try {
        const formData = new URLSearchParams();
        formData.append('type', 'all');
        const response = await axios.post(
          `${import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'}/products/products/`,
          formData,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          }
        );

        const productsData = response.data;
        commit('setProducts', productsData);

        const totalProductsCount = Object.values(state.products).flat().length;
        const allProductsLoaded = totalProductsCount === Object.keys(productsData).length;

        if (allProductsLoaded) {
          dispatch('loadFilterData');
          console.log('All products loaded successfully');
          return true;
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        throw error;
      }
    },
    loadFilterData({ commit, state }) {
      const { types, filters } = extractFiltersData(state.products);

      commit('setTypes', types);
      Object.keys(filters).forEach(type => {
        commit('setFilters', { type, filters: filters[type] });
      });
    }
  },
  getters: {
    getProductsByType: (state) => (type) => {
        if (type === 'all') {
            return Object.values(state.products).flat();
        }
        return state.products[type] || [];
    },
    getFilterDataByType: (state) => (type) => {
        return state.filters[type] || {};
    },
    allProducts(state) {
        return Object.values(state.products).flat();
    },
    types(state) {
        return state.types;
    },
    getAllFilters(state) {
        const allFilters = {
            categories: new Set(),
            subcategories: new Set(),
            suppliers: new Set(),
            industries: new Set(),
            applications: new Set(),
        };

        for (const filter of Object.values(state.filters)) {
            filter.categories.forEach(item => allFilters.categories.add(item));
            filter.subcategories.forEach(item => allFilters.subcategories.add(item));
            filter.suppliers.forEach(item => allFilters.suppliers.add(item));
            filter.industries.forEach(item => allFilters.industries.add(item));
            filter.applications.forEach(item => allFilters.applications.add(item));
        }

        return {
            categories: Array.from(allFilters.categories),
            subcategories: Array.from(allFilters.subcategories),
            suppliers: Array.from(allFilters.suppliers),
            industries: Array.from(allFilters.industries),
            applications: Array.from(allFilters.applications),
        };
    },
  }
};

function extractFiltersData(productsData) {
  const typesSet = new Set();
  const filters = {};

  for (const products of Object.values(productsData)) {
    for (const product of products) {
      const type = product.type;
      if (!filters[type]) {
        filters[type] = {
          categories: new Set(),
          subcategories: new Set(),
          suppliers: new Set(),
          industries: new Set(),
          applications: new Set(),
        };
      }

      if (product.appends?.settings) {
        const { settings } = product.appends;

        if (product.type) typesSet.add(product.type.trim());
        if (settings.category?.value) filters[type].categories.add(settings.category.value.trim());
        if (settings.subcategory?.value) filters[type].subcategories.add(settings.subcategory.value.trim());
        if (settings.manufacturer?.value) filters[type].suppliers.add(settings.manufacturer.value.trim());
      }

      if (product.appends?.second) {
        const { second } = product.appends;
        if (second.mainBranches) {
          extractValues(second.mainBranches).forEach(branch => filters[type].industries.add(branch));
        }
        if (second.mainPurposes) {
          extractValues(second.mainPurposes).forEach(purpose => filters[type].applications.add(purpose));
        }
      }
    }
  }

  const filtersArray = {};
  Object.keys(filters).forEach(type => {
    filtersArray[type] = {
      categories: Array.from(filters[type].categories),
      subcategories: Array.from(filters[type].subcategories),
      suppliers: Array.from(filters[type].suppliers),
      industries: Array.from(filters[type].industries),
      applications: Array.from(filters[type].applications),
    };
  });

  return {
    types: Array.from(typesSet),
    filters: filtersArray,
  };
}

function extractValues(field) {
  return Object.keys(field).reduce((values, key) => {
    if (key.startsWith('value') && field[key]) {
      field[key].split(/[\r\n]+|,\s*/).forEach(item => item.trim() && values.push(item.trim()));
    }
    return values;
  }, []);
}

export default ProductModule;
