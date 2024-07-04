<template>
    <div class="list__container">
        <div v-if="!loading" class="background"></div>
        <span style="text-align: left;">
            <router-link class="headerText" to="/catalog?type=commodity"> 
                <h2>{{ header }}</h2>
            </router-link>
            <CheckboxGroup v-if="!searchTypes"
            :checkboxesData="searchTypes"
            inputType="radio"
            displayType="button"
            @selected="updateSelectedValues"
            />
        </span>
        <ul class="container_product" v-if="!loading">
            <ProductCard
            v-for="(commodity, index) in visibleCommodity"
            :key="commodity.id"
            :product="commodity"
            />
        </ul>
        <div v-if="loading" class="loading-indicator">
            <LoadingController :fetchData="fetchData"/>
        </div>
        <div class="centred_info" v-if="!commodity.length && !loading">Тут пока нет товаров :(</div>
        <span class='button__more'>
            <button class="btn soft-btn" @click="showMoreCommodity">Показать еще</button>
        </span>
    </div>
</template>

<script>
import ProductCard from '@/components/cards/ProductCard.vue';
import CheckboxGroup from '@/components/inputs/CheckboxGroup.vue';
import ProductDataMixin from '@/mixins/ProductDataMixin';
import LoadingController from '@/components/LoadingController.vue';
import { mapGetters } from 'vuex';

export default {
    props: {
        header: {
            type: String,
            default: "Каталог"
        },
    },
    components: {
        ProductCard,
        CheckboxGroup,
        LoadingController
    },
    mixins: [ProductDataMixin],
    data() {
        return {
            visibleCommodityCount: 4,
            step: 4,
            selectedTypeFilter: [],
            searchTypes: [
                { id: 1, name: 'option', value: 'all', label: 'Все' },
            ],
            loading: true 
        };
    },
    computed: {
        ...mapGetters('products', ['getProductsByType']),
        commodity() {
            const products = this.getProductsByType('commodity');
            if (this.selectedTypeFilter === 'all' || this.selectedTypeFilter.length === 0) {
                return products;
            }
            return products.filter(product => product.type === this.selectedTypeFilter);
        },
        visibleCommodity() {
            return this.commodity.slice(0, this.visibleCommodityCount);
        }
    },
    methods: {
        updateSelectedValues(values) {
            this.selectedTypeFilter = values[0].value;
        },
        showMoreCommodity() {
            this.visibleCommodityCount += this.step;
        },
        async fetchData() {
            try {
                const response = await this.$store.dispatch('products/fetchProducts');
                this.loading = false;
            } catch (error) {
            console.error('Error fetching products:', error);
                this.loading = true;
                throw error;
            }
        }
    },
    mounted() {
        this.loading = true;
    }
};
</script>

<style scoped>
.background {
    z-index: -1;
    position: absolute;
    max-width: 500px;
    height: 300px;
    bottom: 15px;
    left: 28%;
    background: var(--color-btn-green-background);
    border-radius: 100%;
    filter: blur(250px);
}

.container_product {
    display: grid;
    grid-template-columns: repeat(4,  1fr);
    gap: 16px;
}

.button__more {
    display: flex;
    width: 100%;   
}

.headerText {
    color: var(--color-black-text)
}

@media (max-width: 1180px) {
    .container_product {
        display: grid;
        width: 100%;
        justify-content: center;
        align-items: center;
        grid-template-columns: repeat(2,  1fr);
        gap: 16px;
    }
}

@media (max-width: 768px) {
    .list__container h2 {
        text-align: center;
    }

    .container_product {
        grid-template-columns: repeat(2, 1fr);
    }

    .btn.soft-btn {
        width: 40%;
    }
}

@media (max-width: 580px) {
    .container_product {
        grid-template-columns: repeat(1, 1fr);
    }

    .btn.soft-btn {
        width: 100%;
    }
}
</style>
