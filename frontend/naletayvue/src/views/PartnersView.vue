<template>
    <div>
        <LoadingController :fetchData="fetchPartners" v-if="loading" />
        <div v-else class="partners-container">
            <div v-for="partner in visiblePartners" :key="partner.login" class="partner-card">
                <img :src="partner.company_logo" alt="Partner Logo" class="partner-logo" />
                <div class="partner-info">
                    <h2>{{ partner.company_name }}</h2>
                    <p>{{ partner.fullDescription }}</p>
                    <button @click="goToProfile(partner.login)" class="btn green-btn">Подробнее</button>
                </div>
            </div>
            <button v-if="visiblePartners.length < partners.length" @click="showMore" class="btn grey-btn">Показать ещё</button>
        </div>
    </div>
</template>

<script>
import api from '@/authAPI.js';
import LoadingController from '@/components/LoadingController.vue';

export default {
    components: {
        LoadingController
    },
    name: 'Partners',
    data() {
        return {
            partners: [],
            visibleCount: 4,
            loading: false,
        };
    },
    computed: {
        visiblePartners() {
            return this.partners.slice(0, this.visibleCount);
        }
    },
    methods: {
        async fetchPartners() {
            try {
                const formData = new FormData();
                formData.append('actionType', 'getAllSellers');
                this.loading = true;
                const response = await api.post('/user/get_partners/', formData);
                if (response.data.result)  {
                    this.loading = false;
                    const partnersData = [];
                    for (let key in response.data) {
                        if (response.data.hasOwnProperty(key) && key !== 'result') {
                            partnersData.push(response.data[key]);
                        }
                    }
                    this.partners = partnersData;
                } else {
                    console.error('Failed to fetch partners: no result');
                    throw new Error('Failed to fetch partners: no result');
                }
            } catch (error) {
                console.error('Failed to fetch partners:', error);
                throw error;
            }
        },
        goToProfile(login) {
            this.$router.push({ name: 'UserProfiles', params: { userId: login } });
        },
        showMore() {
            this.visibleCount += 4;
        }
    },
    mounted() {
        this.fetchPartners();
    },
};
</script>

<style scoped>
.partners-container {
    display: grid;
    grid-template-columns: repeat(2, minmax(300px, 1fr));
    gap: 16px;
    justify-items: center;
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
}

.partner-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 25px;
    width: 100%;
    height: 212px;
    padding: 16px;
    background: #F7F9FA;
    border-radius: 15px;
}

.partner-logo {
    width: 30%;
    object-fit: contain;
    height: 100%;
    min-width: 156px;
    min-height: 156px;
    max-height: 156px;
    background: var(--color-background);
    padding: 45px;
    border-radius: 15px;
}

.partner-info {
    display: flex;
    flex-flow: column;
    justify-content: space-between;
    height: 90%;
    text-align: left;
    color: var(--color-black-text)
}

.partner-info p {
    font-size: 14px;
    line-height: 16px;
    height: 100%;
    overflow: hidden;
}

.partner-info h2 {
    font-weight: 700;
}


@media (max-width: 900px) {
    .partners-container {
        grid-template-columns: 1fr;
    }

    .partner-card {
        flex-direction: column;
        align-items: center;
        height: auto;
    }

    .partner-logo {
        width: 100%;
        height: 256px;
        object-fit: contain;
    }

    .partner-info {
        min-height: 150px;
        text-align: left;
    }
}
</style>
