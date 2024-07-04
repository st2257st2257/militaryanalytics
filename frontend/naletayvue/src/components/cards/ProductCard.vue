<template>
    <div class="product_item" :key="product.id" v-if="product.id">
        <router-link class="product_image" :to="{ name: 'ProductPage', params: { id: product.id }}">
            <img :src="productImageSrc" :alt="product.name">
        </router-link>
        <div class="product_details">
            <router-link :to="{ name: 'ProductPage', params: { id: product.id }}">
                <h3>
                    {{ product.name.length > 20 ? product.name.substring(0, 20) + '...' : product.name }}
                    <Badge v-if="product.ggz === 1"
                        text="Участвует в ГГЗ"
                        description="Этот продукт участвует в программе ГГЗ"
                        badgeClass="badge-ggz"
                        >
                        <template #icon>
                            <starIcon class="badge-icon" />
                        </template>
                    </Badge>
                </h3>
                <p>{{ product.price === 0 ? 'по запросу' : formattedPrice }}</p>
                <ul v-if="product.type === 'commodity'" class="product_features">
                    <li class="feature_item">
                        <speedIcon class="icon-margin" />
                        <span class="feature-label">{{ product.appends.first.maxFlightSpeed.label }}</span>
                        <span class="feature-value">{{ product.appends.first.maxFlightSpeed.value + " " + product.appends.first.maxFlightSpeed.dimension }}</span>
                    </li>
                    <li class="feature_item">
                        <timerIcon class="icon-margin" />
                        <span class="feature-label">{{ product.appends.first.maxDuration.label }}</span>
                        <span class="feature-value">{{ product.appends.first.maxDuration.value + " " + product.appends.first.maxDuration.dimension }}</span>
                    </li>
                    <li class="feature_item">
                        <navigationIcon class="icon-margin" />
                        <span class="feature-label">{{ product.appends.first.maxTakeoffWeight.label }}</span>
                        <span class="feature-value">{{ product.appends.first.maxTakeoffWeight.value }}</span>
                    </li>
                    <li class="feature_item">
                        <tickIcon class="icon-margin" />
                        <span class="feature-label">{{ product.appends.first.maxRangePayload.label }}</span>
                        <span class="feature-value">{{ product.appends.first.maxRangePayload.value + " " + product.appends.first.maxRangePayload.dimension }}</span>
                    </li>
                </ul>
                <ul v-else class="product_features">
                    {{ truncatedDescription }}
                </ul>
            </router-link>

            <div class="product_buttons">
                <button class="btn green-btn" @click="addToCart(product, availableAddons)">
                    <shoperIcon class="icon-margin" />Заказать
                </button>
                <router-link v-if="product.id" :to="{ name: 'ProductPage', params: { id: product.id }}">
                    <button class="mini-btn transparent-btn">Подробнее</button>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
import shoperIcon from '@/assets/icons/shoper.svg';
import speedIcon from '@/assets/icons/speed.svg';
import timerIcon from '@/assets/icons/timer.svg';
import navigationIcon from '@/assets/icons/navigation.svg';
import tickIcon from '@/assets/icons/tick.svg';
import Badge from '@/components/BadgeComponent.vue';
import starIcon from '@/assets/icons/star.svg';
import { formatCurrency, convertCurrency } from '@/utils/format.js';
import { inject } from 'vue';

export default {
    props: {
        product: {
            type: Object,
            required: true
        },
        selectedCurrency: {
            type: String,
            default: 'RUB'
        },
        exchangeRates: {
            type: Object,
        }
    },
    components: {
        shoperIcon,
        speedIcon,
        timerIcon,
        navigationIcon,
        tickIcon,
        starIcon,
        Badge
    },
    computed: {
        truncatedDescription() {
            const maxLength = 145;
            if (this.product.description.length > maxLength) {
                return this.product.description.substring(0, maxLength) + '...';
            } else {
                return this.product.description;
            }
        },
        productImageSrc() {
            if (this.product && this.product.appends && this.product.appends.settings && this.product.appends.settings.link1) {
                return this.product.appends.settings.link1.value;
            } else {
                return '';
            }
        },
        formattedPrice() {
            let price = this.product.price;
            if (this.selectedCurrency !== 'RUB' && this.exchangeRates[this.selectedCurrency]) {
                price = convertCurrency(this.product.price, this.exchangeRates[this.selectedCurrency]);
            }
            return formatCurrency(price, this.selectedCurrency);
        },
        availableAddons() {
            return this.product && this.product.appends && this.product.appends.specification && this.product.appends.specification.value ? Object.entries(this.product.appends.specification.value).map(([key, value]) => ({
                id: key.trim(),
                name: key.trim(),
                value: key.trim(),
                label: value.trim(),
                checked: false
            })) : [];
        }
    },
    setup(props) {
        const cart = inject('Cart');

        const addToCart = (product, addons) => {
            const productWithAddons = {
                ...product,
                addons: addons
            };
            cart.addItem(productWithAddons);
        };

        return {
            addToCart,
        };
    },
};
</script>

<style scoped>
.product_item {
    cursor: default;
    width: 100%;
    min-width: 159px;
    max-width: 300px;
    height: 440px;
    border-radius: 25px;
    background: var(--color-background);
    transition: all 0.25s ease-in-out;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
}

.product_item:hover {
    box-shadow: 0px 0px 15px rgba(0,0,0,.2);
}

.product_image {
    height: 100%;
    max-height: 40%;
}

.product_image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.product_features {
    display: flex;
    width: 100%;
    flex-flow: column;
    text-align: left;
    list-style-type: none;
    max-height: 150px;
    overflow: hidden;
}

.feature_item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    height: 30px;
    font-size: 12px;
    font-weight: 400;
    color: var(--color-mute-text)
}

.feature-label {
    flex: 1;
    line-height: 12px;
}

.feature-value {
    margin-left: 10px;
    white-space: nowrap;
}

.icon-margin {
    width: 22px;
    height: 22px;
    margin-right: 8px;
}

.product_details {
    display: flex;
    flex-flow: column;
    width: 100%;
    height: 100%;
    max-height: 75%;
    padding: 5px 20px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
}

.product_details > a {
    display: flex;
    flex-flow: column;
    width: 100%;
    gap:5px;
}

.product_details h3 {
    font-size: 20px;
    font-weight: 500;
    line-height: 28.8px;
    letter-spacing: -0.02em;
    text-align: left;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 15px;
}

.product_details p {
    font-size: 14px;
    font-weight: 400;
    line-height: 16.8px;
    letter-spacing: -0.02em;
    text-align: left;
}

.product_buttons {
    z-index: 2;
    width: 95%;
    gap: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
    margin-bottom: 10px;
    height: fit-content;
}

@media (max-width: 1180px) {
    .product_item {
        max-width: 100%;
        height: 520px;
    }
}

@media (max-width: 768px) {
    .product_item {
        height: 520px;
    }

    .product_buttons button {
        width: 80%;
    }

    .product_buttons a {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
    }

    .product_buttons {
        z-index: 2;
        width: 100%;
        display: flex;
        text-align: center;
        gap: 10px;
        flex-flow: column;
        align-items: center;
    }

}

@media (max-width: 580px) {
    .product_item {
        height: 100%;
        height: 420px;
    }

    .product_buttons a {
        display: none;
    }
}
</style>
