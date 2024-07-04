<template>
    <div class="list__container">
        <router-link class="headerText" to="/catalog?type=service"> 
            <h2>{{ header }}</h2>
        </router-link>
        <ul class="container_product" v-if="!loading">
            <ServiceCard
            v-for="(service, index) in visibleServices"
            :key="service.id"
            :service="service"
            />
        </ul>
        <div v-if="loading" class="loading-indicator">
            <LoadingController :fetchData="fetchData" />
        </div>
        <div class="centred_info" v-if="!services.length && !loading">Тут пока нет услуг :(</div>
        <button class="btn soft-btn" @click="showMoreServices">Показать еще</button>
    </div>
</template>

<script>
import ServiceCard from '@/components/cards/ServiceCard.vue';
import LoadingController from '@/components/LoadingController.vue';
import { mapGetters } from 'vuex';

export default {
    props: {
        header: {
            type: String,
            default: "Услуги"
        },
    },
    components: {
        ServiceCard,
        LoadingController,
    },
    data() {
        return {
            visibleServiceCount: 3,
            step: 3,
            loading: true 
        };
    },
    computed: {
        ...mapGetters('products', ['getProductsByType']),
        services() {
            return this.getProductsByType('service') || [];
        },
        visibleServices() {
            return this.services.slice(0, this.visibleServiceCount);
        }
    },
    methods: {
        showMoreServices() {
            this.visibleServiceCount += this.step;
        },
        async fetchData() {
            try {
                await this.$store.dispatch('products/fetchProducts');
                this.loading = false;
            } catch (error) {
                console.error('Error fetching services:', error);
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
    width: 500px;
    height: 300px;
    bottom: 15px;
    left: 28%;
    background: var(--color-btn-green-background);
    border-radius: 100%;
    filter: blur(250px);
}

.container_product {
    display: grid;
    grid-template-columns: repeat(3,  1fr);
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