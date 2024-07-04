<template>
    <div class="catalog_container">
        <!-- Фильтры -->
        <div class="filters-container">
            <FiltersComponent />
        </div>

        <div class="products-list" v-if="!loading">
            <ProductCard v-if="visibleProducts.length > 0"
                v-for="product in visibleProducts"
                :key="product.id"
                :product="product"
            />
            <div v-else class="notice_products">По такому запросу ничего не найдено :(</div>
        </div>

        <div v-if="loading" class="loading-indicator">
            <LoadingController :fetchData="fetchData" />
        </div>

        <!-- Scroll to Top Button -->
        <button class="scroll-to-top" @click="scrollToTop">↑</button>
    </div>
</template>

<script>
import FiltersComponent from '@/components/FiltersComponent.vue';
import ProductCard from '@/components/cards/ProductCard.vue';
import LoadingController from '@/components/LoadingController.vue';
import { mapGetters } from 'vuex';
import ProductDataMixin from '@/mixins/ProductDataMixin.js';

export default {
    components: {
        FiltersComponent,
        ProductCard,
        LoadingController
    },
    mixins: [ProductDataMixin],
    computed: {
        ...mapGetters('products', ['allProducts', 'getProductsByType']),
    },
    watch: {
        '$route.query': {
            immediate: true,
            handler(newQuery) {
                this.applyFilters(newQuery);
            },
        },
    },
    data() {
        return {
            visibleProducts: [],
            loading: true,
            rangeFilters: ['price', 'maxDuration', 'maxFlightSpeed', 'maxRangePayload', 'numberOfEngines', 'communicationRange', 'maxFlightAltitude', 'minCrew', 'minTakeoffSpeed']
        };
    },
    async mounted() {
        this.loading = true;
        await this.fetchData();
    },
    methods: {
        async fetchData() {
            try {
                await this.$store.dispatch('products/fetchProducts');
                this.loading = false;
                this.applyFilters(this.$route.query);
            } catch (error) {
                console.error('Ошибка загрузки продуктов:', error);
                this.loading = true;
                throw error;
            }
        },
        applyFilters(query) {
            if (Object.keys(query).length === 0) {
                this.visibleProducts = this.allProducts;
            }
            const filters = this.parseFiltersFromQuery(query);
            this.visibleProducts = this.filterProducts(filters);
        },
        parseFiltersFromQuery(query) {
            const filters = {};
            for (const key in query) {
                if (query[key] === "") {
                    continue;
                }
                if (this.rangeFilters.includes(key)) {
                    filters[key] = this.stringToRangeObject(query[key]);
                } else {
                    filters[key] = query[key];
                }
            }
            return filters;
        },
        filterProducts(filters) {
            let products = this.allProducts;
            if (filters.type && filters.type !== 'all') {
                products = this.getProductsByType(filters.type);
            }
            return products.filter(product => {
                return Object.entries(filters).every(([key, value]) => {
                    if (value === 'all' && key === 'type') {
                        return true;
                    }
                    if (this.rangeFilters.includes(key)) {
                        const minCondition = !value.min || this.searchInObject(product, key, value.min, 'greater');
                        const maxCondition = !value.max || this.searchInObject(product, key, value.max, 'less');
                        return minCondition && maxCondition;
                    } else if (key === 'warranty') {
                        if (value === "Да") {
                            return this.searchInObject(product, 'standardWarranty')
                        } else {
                            return this.searchInObject(product, 'standardWarranty', 'nan'); 
                        }
                    } else {
                        return this.searchInObject(product, key, value, 'contains');
                    }
                });
            });
        },
        searchInObject(obj, key, value, condition) {
            if (!value) return true;

            const numericValue = parseFloat(value);
            if (obj && obj.hasOwnProperty(key)) {
                const objValue = obj[key] && typeof obj[key] === 'object' && obj[key].hasOwnProperty('value') ? obj[key].value : obj[key];
                if (typeof objValue === 'number' || !isNaN(parseFloat(objValue))) {
                    const numericObjValue = parseFloat(objValue);
                    if (condition === 'greater') {
                        return numericObjValue >= numericValue;
                    } else if (condition === 'less') {
                        return numericObjValue <= numericValue;
                    } else if (condition === 'equal') {
                        return numericObjValue === numericValue;
                    }
                } else if (typeof objValue === 'string') {
                    return objValue.toLowerCase().includes(value.toLowerCase());
                }
            }
            for (let k in obj) {
                if (typeof obj[k] === "object" && this.searchInObject(obj[k], key, value, condition)) {
                    return true;
                }
            }
            return false;
        },
        stringToRangeObject(str) {
            try {
                return JSON.parse(str);
            } catch (e) {
                return { min: 0, max: 1000000 };
            }
        },
        scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    },
};
</script>

<style scoped>
.catalog_container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    text-align: center;
    flex-flow: row nowrap;
    gap: 10px;
    width: 100%;
    max-width: 1280px;
    margin-bottom: 25px;
    padding: 0 !important;
    box-sizing: border-box;
    z-index: 2;
}

.filters-container {
    display: flex;
    width: 20%;
    height: 100%;
    min-width: 300px;
    position: relative;
}

.filters-container .filters {
    position: sticky;
    top: 10px;
    align-self: flex-start;
}

.products-list {
    display: grid;
    justify-content: center;
    align-items: center;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    width: 100%;
}

.notice_products {
    display: flex;
    grid-column: span 3;
    width: 100%;
    justify-content: center;
    text-align: center;
    padding-top: 15px;
    font-size: 22px;
}

.scroll-to-top {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: var(--color-btn-green-background);
    color: white;
    border: none;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    font-size: 24px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.scroll-to-top:active {
    transform: scale(0.9);
}

.scroll-to-top:hover {
    box-shadow: 0px 0px 0px 8px rgba(8,139,149, 0.5);
}

@media (max-width: 1180px) {
    .products-list {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        width: 100%;
    }
}

@media (max-width: 1024px) {
    .catalog_container {
        gap: 15px;
        padding: 0px 20px !important;
        flex-direction: column;
    }

    .filters-container {
        width: 100%;
        justify-content: center;
    }

    .products-list {
        margin-top: 15px;
        justify-content: center;
        align-items: center;
        grid-template-columns: repeat(2, 1fr);
    }

    .filters-container .filters {
        position: relative;
    }
}

@media (max-width: 768px) {
    .products-list {
        grid-template-columns: 1fr;
    }
}
</style>
