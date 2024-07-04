<template>
    <div class="cart-item">
        <span style="display: flex; flex-flow: column; width: 100%; gap: 5px;">
            <router-link :to="`/product/${item.id}`" class="item-info">
                <img :src="productImageSrc" :alt="item.name" class="item_image">
                <span>
                    <div>{{ item.name }}</div>
                    <div>{{ item.price === 0 ? 'по запросу' : formattedPrice }}</div>
                    <div>Продавец: {{ userCompanyName }}</div>
                </span>
            </router-link>
            <AddonConstructor :addons="addons" @applyAddons="applyAddons"/>
        </span>
        <div class="item-quantity">
            <button class="mini-btn" @click="updateItemQuantity(localItem.quantity - 1)">-</button>
            <span class="quantity">{{ localItem.quantity }}</span>
            <button class="mini-btn" @click="updateItemQuantity(localItem.quantity + 1)">+</button>
        </div>
        <button style="font-weight: 600;" class="mini-btn error-btn" @click="removeItem">X</button>
    </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { formatCurrency, convertCurrency } from '@/utils/format.js';
import AddonConstructor from '@/components/AddonConstructor.vue';

export default {
    props: {
        item: {
            type: Object,
            required: true,
        },
        index: {
            type: Number,
            required: true,
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
        AddonConstructor,
    },
    setup(props, { emit }) {
        const localItem = ref({ ...props.item });

        watch(() => props.item, (newItem) => {
            localItem.value = { ...newItem };
        }, { deep: true });

        const updateItemQuantity = (quantity) => {
            if (quantity <= 0) {
                emit('remove', props.index);
            } else {
                emit('update', { index: props.index, changes: { quantity } });
            }
        };

        const removeItem = () => {
            emit('remove', props.index);
        };

        const applyAddons = (selectedAddons) => {
            emit('update', { index: props.index, changes: { selectedAddons } });
        };

        const productImageSrc = computed(() => {
            return props.item.appends?.settings?.link1?.value || '';
        });

        const userCompanyName = computed(() => {
            console.log(props.item)
            return props.item.companyName || 'Неизвестный продавец';
        });

        const formattedPrice = computed(() => {
            let price = props.item.price * localItem.value.quantity;
            if (props.selectedCurrency !== 'RUB' && props.exchangeRates[props.selectedCurrency]) {
                price = convertCurrency(props.item.price, props.exchangeRates[props.selectedCurrency]);
            }
            return formatCurrency(price, props.selectedCurrency);
        });

        const addons = computed(() => {
            return props.item.addons ? props.item.addons.map(addon => ({
                ...addon,
                checked: localItem.value.selectedAddons?.some(selectedAddon => selectedAddon.id === addon.id) || false
            })) : [];
        });

        return {
            localItem,
            updateItemQuantity,
            removeItem,
            applyAddons,
            productImageSrc,
            userCompanyName,
            formattedPrice,
            addons
        };
    },
};
</script>

<style scoped>
.cart-item {
    width: 100%;
    min-height: 150px;
    display: flex;
    justify-content: space-between;
    padding: 15px;
    gap: 15px;
    border-radius: 15px;
    background: var(--color-background-soft);
}

.item-quantity {
    display: flex;
    gap: 15px;
    height: 40px;
    align-items: center;
}

@media (hover: hover) {
    .cart-item:hover {
        box-shadow: 0px 0px 10px rgba(0,0,0,.1);
    }
}

.item-info {
    display: flex;
    width: 100%;
    min-height: 120px;
    max-height: 100%;
    gap: 15px;
}

.item_image {
    width: 45%;
    min-width: 128px;
    max-width: 128px;
    min-height: 128px;
    max-height: 128px;
    border-radius: 10px;
    object-fit: cover;
    background: var(--color-background);
}

@media (max-width: 612px) { 
    .item_image {
        display: flex;
        min-width: none;
        max-width: none;
        min-height: 128px;
        max-height: 128px;
        width: 100%;
        height: 100%;
        border-radius: 10px;
    }

    .item-info {
        display: flex;
        width: 100%;
        flex-flow: column;
    }

    .cart-item {
        display: flex;
        gap: 15px;
        min-height: 150px;
        max-height: 400px;
        gap: 15px;
        padding: 15px;
        flex-flow: row wrap;
    }
}

.addon-section {
    margin-top: 10px;
}

.addon-section h3 {
    margin-bottom: 5px;
}
</style>
