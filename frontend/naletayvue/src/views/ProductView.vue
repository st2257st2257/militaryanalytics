<template>
    <div style="width: 100%;">
        <div v-if="!loading">
            <div v-if="product" class="product-page">
                <div class="product-info-container">
                    <ImageSlider :items="productItems"/>
                    <div class="default-info-data">
                        <span class="data_constructor">
                            <h1 style="display: flex; gap: 10px;">{{ product.name }}
                                <div class="badges_container">
                                    <Badge v-if="product.ggz === 1"
                                        text="Участвует в ГГЗ"
                                        description="Этот продукт участвует в программе ГГЗ"
                                        badgeClass="badge-ggz"
                                        >
                                        <template #icon>
                                            <starIcon class="badge-icon" />
                                        </template>
                                    </Badge>
                                </div>
                            </h1>
                            <p style="display: flex; align-items: center;" v-if="product.companyName">
                                Продавец: {{ product.companyName }}
                                <newChatIcon v-if="isAuthenticated" class="chat-btn" @click="openChat(product.userLogin)" />
                            </p>
                        </span>
                        <ul v-if="product.type === 'commodity'" class="product-features">
                            <li class="feature-item">
                                <speedIcon class="icon-margin" />
                                {{ product.appends.first.maxFlightSpeed.label + " " + product.appends.first.maxFlightSpeed.value + " " + product.appends.first.maxFlightSpeed.dimension }}
                            </li>
                            <li class="feature-item">
                                <timerIcon class="icon-margin" />
                                {{ product.appends.first.maxDuration.label + " " + product.appends.first.maxDuration.value + " " + product.appends.first.maxDuration.dimension }}
                            </li>
                            <li class="feature-item">
                                <navigationIcon class="icon-margin" />
                                {{ product.appends.first.maxTakeoffWeight.label + " " + product.appends.first.maxTakeoffWeight.value }}
                            </li>
                            <li class="feature-item">
                                <tickIcon class="icon-margin" />
                                {{ product.appends.first.maxRangePayload.label + " " + product.appends.first.maxRangePayload.value + " " + product.appends.first.maxRangePayload.dimension }}
                            </li>
                        </ul>
                        <ul class="product-features">
                            <li class="feature-item">{{ product.description }}</li>
                        </ul>
                        <span class="buy-buttons">
                            <AddonConstructor
                            :addons="availableAddons"
                            @applyAddons="applyAddons"
                            />
                            <div style="display: flex; gap:15px; align-items: center;">
                                <button class="btn green-btn" @click="addToCart">
                                    <shoperIcon class="icon-margin" /> Заказать
                                </button>
                                <button class="btn" @click="openLeasingForm(product)">
                                    <shoperIcon class="icon-margin" />В лизинг
                                </button>
                            </div>
                        </span>
                    </div>
                </div>

                <div v-if="displayedCharacteristics.length >= 1" class="characteristic-container">
                    <div v-for="(item, index) in displayedCharacteristics" :key="index" class="characteristic-item">
                    <span>{{ item.label }}:</span>
                        <span style="text-align: right; justify-content: flex-end; align-items: flex-end;">

                            <template v-if="item.label === 'Файл спецификации'">
                                <a :href="item.value" class="btn green-btn" style="height: 40px;" download>Скачать спецификации</a>
                            </template>

                            <template v-else-if="item.value != 'nan'">
                                {{ item.value + " " + item.dimension }}
                            </template>
                            
                            <template v-else> Нет данных</template>
                        </span>
                    </div>
                    <button style="margin-top: 15px;" class="btn soft-btn" @click="toggleShowAllCharacteristics">
                        {{ showAllCharacteristics ? 'Скрыть' : 'Показать все' }}
                    </button>
                </div>
                <ServicesList header="Вас могло бы заинтересовать" />
                <CommodityList header="Похожие Беспилотники" />
            </div>

            <div v-else>
                <ErrorMessage title="Товар недоступен" message="К сожалению, этот товар был удален или стал недоступен. Пожалуйста, вернитесь на главную страницу и выберите другой товар." />
            </div>
        </div>

        <div v-else class="loading-indicator"><LoadingController :fetchData="fetchData"/></div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import ErrorMessage from '@/components/ErrorMessage.vue';
import ServicesList from '@/components/ServicesList.vue';
import CommodityList from '@/components/CommodityList.vue';
import AddonConstructor from '@/components/AddonConstructor.vue';
import ProductDataMixin from '@/mixins/ProductDataMixin';
import LoadingController from '@/components/LoadingController.vue';
import ImageSlider from '@/components/ImageSlider.vue';
import Badge from '@/components/BadgeComponent.vue';

import shoperIcon from '@/assets/icons/shoper.svg';
import speedIcon from '@/assets/icons/speed.svg';
import timerIcon from '@/assets/icons/timer.svg';
import navigationIcon from '@/assets/icons/navigation.svg';
import tickIcon from '@/assets/icons/tick.svg';
import newChatIcon from '@/assets/icons/chat.svg';
import starIcon from '@/assets/icons/star.svg';

import { inject } from 'vue';

export default {
    name: 'ProductView',
    components: {
        ErrorMessage,
        CommodityList,
        ServicesList,
        AddonConstructor,
        LoadingController,
        shoperIcon,
        speedIcon,
        timerIcon,
        navigationIcon,
        tickIcon,
        newChatIcon,
        starIcon,
        ImageSlider,
        Badge
    },
    mixins: [ProductDataMixin],
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated']),
        ...mapGetters('products', ['allProducts']),
        product() {
            const productId = this.$route.params.id;
            return this.allProducts.find(product => product.id === parseInt(productId));
        },
        displayedCharacteristics() {
            if (this.product && this.product.appends && this.product.appends.second) {
                const characteristics = Object.entries(this.product.appends.second).map(([key, value]) => ({
                    label: value.label,
                    value: value.value,
                    dimension: ['link', 'bool', 'text'].includes(value.dimension) ? '' : value.dimension,
                }));

                if (!this.showAllCharacteristics) {
                    return characteristics.slice(0, this.visibleCharacteristicsCount);
                } else {
                    return characteristics;
                }
            } else {
                return [];
            }
        },
        productItems() {
            const items = [];
            if (this.product && this.product.appends.settings) {
                for (let i = 1; i <= 5; i++) {
                    const linkKey = `link${i}`;
                    if (this.product.appends.settings[linkKey]) {
                        items.push(this.product.appends.settings[linkKey].value);
                    }
                }
            }
            return items;
        },
        availableAddons() {
            return this.product && this.product.appends && this.product.appends.specification && this.product.appends.specification ? Object.entries(this.product.appends.specification.value).map(([key, value]) => ({
                id: key.trim(),
                name: key.trim(),
                value: key.trim(),
                label: value.trim(),
                checked: false
            })) : [];
        }
    },
    data() {
        return {
            showAllCharacteristics: false,
            visibleCharacteristicsCount: 8,
            loading: true,
            selectedAddons: [],
            chatsManager: inject('chatsManager')
        };
    },
    methods: {
        async openChat(seller){
            const isChatCreated = await this.chatsManager.addChat(this.currentUser.username, seller);
            if (isChatCreated) {
                window.notificationManager.addNotification('success', `Чат с продавцом был создан`);
                const сhat = await this.chatsManager.getChatByUsers(this.currentUser.username, seller);
                if (сhat) {
                    this.$router.push({ name: 'Chats', query: { chatId: сhat.id } });
                }
            }
        },
        openLeasingForm(product) {
            product.addons = this.selectedAddons;
            window.leasingModal.open(product);
        },
        toggleShowAllCharacteristics() {
            this.showAllCharacteristics = !this.showAllCharacteristics;
        },
        useAlert(message) {
            alert(message);
        },
        applyAddons(selectedAddons) {
            this.selectedAddons = selectedAddons;
            window.notificationManager.addNotification('success', `Комплектация успешно обновлена`);
        },
        addToCart() {
            const productWithAddons = {
                ...this.product,
                selectedAddons: this.selectedAddons,
                addons: this.availableAddons
            };
            this.cart.addItem(productWithAddons);
        }
    },
    setup() {
        const cart = inject('Cart');

        return {
            cart,
        };
    },
    async mounted() {
        await this.fetchData();
        this.showAllCharacteristics = false;
    },
};
</script>

<style>
.product-page {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 1280px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 8px;
    gap: 35px;
}

.product-info-container {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.product-features {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    list-style: none;
    padding: 0;
    max-width: 600px;
}

.buy-buttons {
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: flex-start;
    gap: 20px;
}

.feature-item {
    display: flex;
    justify-content: center;
    align-items: center;
    width: fit-content;
    font-size: 14px;
}

.default-info-data {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.data_constructor {
    display: flex;
    flex-flow: column;
    gap: 5px;
    max-width: 400px;
}

.product-image {
    width: 350px;
    height: 350px;
    object-fit: cover;
    border-radius: 15px;
}

.characteristic-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 25px;
    background: #f8f9fa;
    border-radius: 20px;
}

.characteristic-item span {
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: flex-start;
    width: 50%;
}

.characteristic-item {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    gap: 15px;
    border-bottom: 1px solid #edeff2;
}

.chat-btn {
    user-select: none;
    cursor: pointer;
    width: 32px;
    height: 32px;
    padding: 5px;
    border-radius: 50px;
    background: var(--color-btn-green-background);
    margin-left: 10px;
}

.chat-btn:hover {
    transform: scale(1.05);
}

.chat-btn:active {
    transform: scale(0.95);
}

@media (max-width: 768px) {
    .product-page {
        padding: 15px;
    }

    .product-info-container {
        flex-direction: column;
        align-items: center;
    }

    .product-image {
        width: 100%;
        height: auto;
    }
}
</style>
