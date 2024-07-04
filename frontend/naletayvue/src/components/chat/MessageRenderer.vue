<template>
    <div v-if="isOrderMessage" class="order-message">
        {{ `Оформлен новый заказ №${parsedMessage.orderNumber}` }}
        <ul class="order-items">
            <li v-for="(item, index) in parsedMessage.items" :key="index" class="order-item">
                <div class="item-name">
                    {{ item.name }} <span class="item-quantity">({{ item.quantity }} шт. по {{ item.price }} руб.)</span>
                </div>
                <ul class="addons-list" v-if="item.selectedAddons && item.selectedAddons.length > 0">
                    <li v-for="(addon, index) in item.selectedAddons" :key="index" class="addon-item">
                        + {{ addon.label }}
                    </li>
                </ul>
            </li>
        </ul>
    </div>
    <div v-else>
        {{ orderMessage }}
    </div>
</template>

<script>
export default {
    props: {
        orderMessage: [Object, String]
    },
    data() {
        return {
            parsedMessage: null
        };
    },
    computed: {
        isOrderMessage() {
            return this.parsedMessage && this.parsedMessage.messageType === 'order';
        }
    },
    watch: {
        orderMessage: {
            immediate: true,
            handler(newVal) {
                if (this.isObjectWithMessageType(newVal)) {
                    try {
                        this.parsedMessage = typeof newVal === 'string' ? JSON.parse(newVal) : newVal;
                    } catch (error) {
                        console.error('Error parsing JSON:', error);
                        this.parsedMessage = null;
                    }
                } else {
                    this.parsedMessage = null;
                }
            }
        }
    },
    methods: {
        isObjectWithMessageType(message) {
            if (typeof message === 'object' && message !== null) {
                return true;
            }
            if (typeof message === 'string') {
                try {
                    JSON.parse(message);
                    return true;
                } catch (error) {
                    return false;
                }
            }
            return false;
        }

    },
};
</script>

<style scoped>
.order-message {
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 5px;
    background: var(--color-background-soft);
    border-left: 6px solid var(--color-background-success);
    box-sizing: border-box;
    font-family: 'Arial', sans-serif;
}

.order-message ul {
    list-style-type: none;
    padding: 0;
}

.order-items {
    margin-top: 10px;
}

.order-item {
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--color-border);
}

.item-name {
    font-weight: bold;
}

.item-quantity {
    font-weight: normal;
    font-size: 0.9rem;
    color: var(--color-text-secondary);
}

.addons-list {
    margin-top: 5px;
    padding-left: 15px;
}

.addon-item {
    font-size: 0.9rem;
    color: var(--color-text-secondary);
}

</style>
