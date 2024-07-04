import { mapGetters } from 'vuex';

export default {
    data() {
        return {
            loading: false
        };
    },
    computed: {
        ...mapGetters('products', ['allProducts']),
        product() {
            const productId = this.$route.params.id;
            return this.allProducts.find(product => product.id === parseInt(productId));
        },
    },
    methods: {
        async fetchData() {
            try {
                const success = await this.fetchProducts();
                this.loading = !success;
                return success
            } catch (error) {
                console.error('Ошибка загрузки продуктов:', error);
                this.loading = false;
                return false
            }
        },
        async fetchProducts() {
            try {
                const success = await this.$store.dispatch('products/fetchProducts');
                return success;
            } catch (error) {
                console.error('Ошибка загрузки продуктов:', error);
                return false;
            }
        }
    },
};
