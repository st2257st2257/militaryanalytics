<template>
    <div class="orders-container">
        <LoadingController :fetchData="fetchOrders" v-if="loading" />
        <template v-else>
            <Dropdown
                class="order-type-container"
                :options="orderTypeOptions"
                :selected="selectedOrderType"
                @select="filterOrdersByType"
                placeholder="Выберите тип заказа"
            /> 
            <div class="no-orders-message">Обсуждение и обмен документами по заказам в разделе "Чаты"</div>
            <div v-if="filteredOrders.length === 0" class="no-orders-message">У вас пока нет заказов :(</div>
            <div v-else class="orders-list">
                <div v-for="order in filteredOrders" :key="order.id" class="order-item">
                    <div class="order-details">
                        <router-link :to="`/order/${order.id}`" class="details-container">
                            <p>Заказ №{{ order.id + " | " + formatDate(order.date)}}</p>
                            <p>{{ order.seller.name }} </p>
                            <p>{{ 'Кол-во товаров: ' + order.products.length }}</p>
                        </router-link>
                        <span class="status-container">
                            <div :class="'status-' + getStatusString(order.status)">{{ getStatusText(order.status) }}</div>
                        </span>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import LoadingController from '@/components/LoadingController.vue';
import Dropdown from '@/components/inputs/Dropdown.vue';
import { mapGetters } from 'vuex';
import { formatCurrency } from '@/utils/format.js';

export default {
    components: {
        LoadingController,
        Dropdown,
    },
    data() {
        return {
            loading: true,
            selectedOrder: null,
            selectedStatus: null,
            selectedOrderType: 'all',
            statusOptions: [
                { value: 1, text: 'Отправлен запрос' },
                { value: 2, text: 'Принят' },
                { value: 3, text: 'Оплачен' },
                { value: 4, text: 'Передан на доставку' },
                { value: 5, text: 'Выполнен'},
                { value: 0, text: 'Отменен' },
            ],
            orderTypeOptions: [
                { value: 'all', text: 'Все заказы' },
                { value: 'madeByUser', text: 'Покупки' },
                { value: 'toBeCompleted', text: 'Ваши заказы' },
            ],
        };
    },
    computed: {
        ...mapGetters('user', ['currentUser', 'isAuthenticated']),
        ...mapGetters({
            orders: 'orders/orders',
        }),
        filteredOrders() {
            if (this.selectedOrderType === 'madeByUser') {
                return this.orders.filter(order => order.owner.login === this.currentUser.username);
            } else if (this.selectedOrderType === 'toBeCompleted') {
                return this.orders.filter(order => order.seller.login === this.currentUser.username);
            } else {
                return this.orders;
            }
        },
    },
    methods: {
        formatDate(date) {
            const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
            return date ? new Date(date).toLocaleDateString('ru-RU', options) : 'Нет данных';
        },
        formatCurrency(amount) {
            return formatCurrency(amount, 'RUB');
        },
        async fetchOrders() {
            this.loading = true;
            try {
                await this.$store.dispatch('orders/fetchOrders');
                this.loading = false;
            } catch (error) {
                this.loading = true;
                throw error;
            }
        },
        async confirmStatusChange(order, status) {
            this.selectedOrder = order;
            this.selectedStatus = status;
            const result = await window.confirmModal.open(`Вы уверены, что хотите изменить статус заказа с "${this.getStatusText(order.status)}" на "${this.getStatusText(status)}"?`);
            if (result) {
                await this.applyStatusChange();
            }
        },
        async applyStatusChange() {
            try {
                await this.$store.dispatch('orders/updateOrderStatus', { orderId: this.selectedOrder.id, status: this.selectedStatus });
                await this.fetchOrders();
            } catch (error) {
                window.notificationManager.addNotification('error', 'Ошибка при изменении статуса заказа');
            }
        },
        getStatusText(status) {
            const statusOption = this.statusOptions.find(option => option.value === status);
            return statusOption ? statusOption.text : status;
        },
        getStatusString(status) {
            const statusStringMap = {
                1: 'pending',
                2: 'confirmed',
                3: 'paid',
                4: 'delivery',
                5: 'fulfilled',
                0: 'canceled',
            };
                
            return statusStringMap[status] || 'unknown';
        },
        filterOrdersByType(selectedType) {
            this.selectedOrderType = selectedType;
        },
    },
    async mounted() {
        await this.fetchOrders();
    }
};
</script>

<style scoped>
.orders-container {
    display: flex;
    flex-direction: column;
}

.details-container {
    display: flex;
    flex-flow: column;
    width: 100%;
    padding: 15px;
}

.no-orders-message {
    text-align: center;
    font-size: 18px;
    color: #888;
}

.orders-list {
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 15px;
}

.order-item {
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #fff;
    transition: box-shadow 0.3s ease;
    cursor: pointer;
}

.order-item:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.order-details {
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.status-container {
    display: flex;
    flex-flow: column;
    height: fit-content;
    padding: 10px;
}

.status-container > div {
    padding: 10px;
    text-align: center;
    min-width: 200px;
    border-radius: 10px;
    color: var(--color-active-text);
}

.order-type-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: fit-content;
    height: 45px;
    margin-bottom: 15px;
    background: var(--color-background-soft);
}

</style>
