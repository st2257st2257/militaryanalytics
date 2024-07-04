<template>
    <div class="order-detail-container">
        <LoadingController :fetchData="fetchOrderDetails" v-if="loading" />
        <template v-else>
            <ErrorMessage v-if="error" :title="errorTitle" :message="errorMessage" :type="errorType" />
            <div v-else-if="order">
                <div class="order-content">
                    <div class="order-info-column">
                        <div class="order-header-container">
                            <div class="order-header">
                                <h1>Заказ №{{ order.id }}</h1>
                                <p class="header-details">Дата: {{ formatDate(order.date) }}
                                    <span class="order-price">{{ formatCurrency(order.totalPrice) }}</span>
                                </p>
                            </div>
                            <div class="order-info">
                                <p>Поставщик: {{ order.seller_full_name || 'Нет данных' }}</p>
                                <button style="align-self: flex-end;" v-if="isOrderOwner && order.status != 0" @click="cancelOrder" class="btn error-btn">Отменить заказ</button>
                            </div>
                        </div>
                        <div class="order-details">
                            <h2>Информация о заказе</h2>
                            <div class="detail-row">
                                <p>Покупатель: {{ order.user_full_name || 'Нет данных' }}</p>
                                <p>Электронная почта: {{ order.user_email || 'Нет данных' }}</p>
                                <p>Телефон: {{ order.user_phone || 'Нет данных' }}</p>
                            </div>
                        </div>
                        <div class="order-items">
                            <h2>Беспилотники</h2>
                            <div v-for="(subOrder, index) in order.subOrders" :key="index" class="order-item">
                                <div class="item-details">
                                    <h3>Товар: {{ subOrder.productName }}</h3>
                                    <div v-for="(value, key) in subOrder.specifications" :key="key">
                                        <p>{{ value }}</p>
                                    </div>
                                    <Dropdown
                                        :class="'order-status status-'+ getStatusEng(subOrder.order_status_id)"
                                        :options="statusOptions"
                                        :selected='subOrder.order_status_id.toString()'
                                        :confirmable="true"
                                        @select="(status) => confirmStatusChange(subOrder, status)"
                                        v-if="canEdit"
                                    />
                                    <p :class="'order-status status-'+ getStatusEng(subOrder.order_status_id)" v-else>{{ getStatusText(subOrder.order_status_id) }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="order-status-column">
                        <h2>Статус заказа</h2>
                        <div style="display: flex; gap: 10px; flex-direction: column;">
                            <p :class="'order-status status-'+ getStatusEng(order.status)" >{{ getStatusText(order.status) }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<script>
import Dropdown from '@/components/inputs/Dropdown.vue';
import LoadingController from '@/components/LoadingController.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';
import { formatCurrency } from '@/utils/format.js';
import api from '@/authAPI.js';

export default {
    components: {
        Dropdown,
        LoadingController,
        ErrorMessage,
    },
    props: {
        orderId: {
            type: Number,
            required: true,
        }
    },
    data() {
        return {
            order: null,
            canEdit: false,
            statusOptions: [
                { value: '1', text: 'Отправлен запрос', eng: "pending" },
                { value: '2', text: 'Принят', eng: "confirmed" },
                { value: '3', text: 'Оплачен', eng: "paid" },
                { value: '4', text: 'Передан на доставку', eng: "delivery" },
                { value: '5', text: 'Выполнен', eng: "fulfilled" },
                { value: '0', text: 'Отменен', eng: "canceled" },
            ],
            loading: true,
            error: null,
            errorTitle: '',
            errorMessage: '',
            errorType: 'default',
            selectedOrder: null,
            selectedStatus: null,
        };
    },
    computed: {
        isOrderOwner() {
            return this.order && this.order.owner.login === this.$store.getters['user/currentUser'].username;
        }
    },
    methods: {
        formatDate(date) {
            const options = { year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: 'numeric' };
            return date ? new Date(date).toLocaleDateString('ru-RU', options) : 'Нет данных';
        },
        formatCurrency(amount) {
            return formatCurrency(amount, 'RUB');
        },
        getStatusText(status) {
            const statusOption = this.statusOptions.find(option => option.value === status.toString());
            return statusOption ? statusOption.text : 'Нет данных';
        },
        getStatusEng(status) {
            const statusOption = this.statusOptions.find(option => option.value === status.toString());
            return statusOption ? statusOption.eng : 'unknown';
        },
        async confirmStatusChange(order, status) {
            this.selectedOrder = order;
            this.selectedStatus = status;
            const result = await window.confirmModal.open(`Вы уверены, что хотите изменить статус заказа с "${this.getStatusText(order.order_status_id)}" на "${this.getStatusText(status)}"?`);
            if (result) {
                await this.applyStatusChange();
            }
        },
        async applyStatusChange() {
            try {
                await this.$store.dispatch('orders/updateOrderStatus', { orderId: this.selectedOrder.id, status: this.selectedStatus });
                await this.fetchOrderDetails();
                window.notificationManager.addNotification('success', `Статус заказа №${this.selectedOrder.id} успешно изменен`);
            } catch (error) {
                console.error('Ошибка при изменении статуса заказа:', error);
                window.notificationManager.addNotification('error', 'Ошибка при изменении статуса заказа');
            }
        },
        async cancelOrder() {
            try {
                const cancelPromises = this.order.subOrders.map(subOrder => 
                    this.$store.dispatch('orders/updateOrderStatus', { orderId: subOrder.id, status: 0 })
                );
                await Promise.all(cancelPromises);
                await this.fetchOrderDetails();
                window.notificationManager.addNotification('success', `Заказ №${this.order.id} успешно отменен`);
            } catch (error) {
                console.error('Ошибка при отмене заказа:', error);
                window.notificationManager.addNotification('error', 'Ошибка при отмене заказа');
            }
        },
        async fetchOrderDetails() {
            try {
                this.loading = true;
                const formData = new FormData();
                formData.append('action', 'getAllOrdersBySellerOrderId');
                formData.append('sellerOrderId', this.orderId);
                const response = await api.post('/products/get/', formData);

                if (!response.data.result || !response.data.data) {
                    console.error('Ошибка при получении данных заказа:', response.data);
                    this.error = true;
                    this.errorTitle = 'Ошибка';
                    this.errorMessage = 'Возможно вы пытаетесь попасть на страницу заказа, который уже не существует или был удален, попробуйте еще раз';
                    this.errorType = 'notfound';
                } else {
                    const orderData = response.data.data;
                    let mainOrderDetails = null;
                    let subOrders = [];

                    for (const email in orderData) {
                        const orders = orderData[email];
                        mainOrderDetails = orders[Object.keys(orders)[0]].orderRes;
                        for (const subOrderId in orders) {
                            subOrders.push({
                                id: subOrderId,
                                productName: orders[subOrderId].orderRes.productName,
                                specifications: orders[subOrderId].orderRes.specifications,
                                totalPrice: orders[subOrderId].orderRes.totalPrice,
                                date: orders[subOrderId].orderRes.date,
                                order_status_id: orders[subOrderId].orderRes.order_status_id,
                            });
                        }
                        break;
                    }

                    if (!mainOrderDetails) {
                        console.error('Ошибка: заказ не найден');
                        this.error = true;
                        this.errorTitle = 'Ошибка';
                        this.errorMessage = 'Заказ не найден. Попробуйте снова.';
                        this.errorType = 'notfound';
                        this.loading = false;
                        return;
                    }

                    this.order = {
                        id: this.orderId,
                        date: mainOrderDetails.date,
                        totalPrice: mainOrderDetails.totalPrice,
                        seller_full_name: mainOrderDetails.seller_full_name,
                        user_full_name: mainOrderDetails.user_full_name,
                        user_email: mainOrderDetails.user_email,
                        user_phone: mainOrderDetails.user_phone,
                        subOrders: subOrders,
                        status: mainOrderDetails.order_status_id,
                        seller_login: mainOrderDetails.seller_login,
                        owner: {
                            login: mainOrderDetails.user_login,
                            fullName: mainOrderDetails.user_full_name,
                        }
                    };

                    this.canEdit = this.order.seller_login === this.$store.getters['user/currentUser'].username;
                    this.loading = false;
                }

            } catch (error) {
                console.error('Ошибка при получении деталей заказа:', error);
                window.notificationManager.addNotification('error', 'Ошибка при получении деталей заказа');
                this.error = true;
                this.errorTitle = 'Ошибка';
                this.errorMessage = 'Не удалось получить детали заказа. Попробуйте снова.';
                this.loading = false;
                throw error;
            }
        },
        truncate(text, length) {
            return text.length > length ? text.substring(0, length) + '...' : text;
        },
    },
    async mounted() {
        await this.fetchOrderDetails();
    },
};
</script>

<style scoped>
.order-detail-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    max-width: 1280px;
    gap: 20px;
    box-sizing: border-box;
    border-radius: 10px;
    padding: 20px;
}

.order-content {
    display: flex;
    flex-direction: column;
}

.order-status-column {
    display: flex;
    flex-flow: column;
    align-items: flex-end;
    flex: 0.3;
    gap: 10px;
    margin: 10px 0;
}

.order-info-column {
    flex: 1;
    margin: 10px 0;
}

.order-header-container {
    display: flex;
    flex-flow: column;
    gap: 15px;
    background-color: var(--color-background-soft);
    padding: 10px;
    box-sizing: border-box;
    border-radius: 15px;
}

.order-header > h1 {
    display: flex;
    min-width: fit-content;
}

.header-details {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    font-size: 15px;
}

.order-header {
    display: flex;
    width: 100%;
    justify-content: center;
    align-items: center;
    flex-direction: row;
    gap: 15px;
}

.order-info, .order-status, .order-details, .order-items {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.order-status {
    display: flex;
    width: 100%;
    text-align: right;
}

.order-items {
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    color: var(--color-active-text);
    background: var(--color-btn-green-background);
}

.order-price {
    display: flex;
    font-size: 18px;
    font-weight: 600;
    padding: 5px;
    border-radius: 10px;
    border: 2px solid var(--color-btn-green-background);
}

.order-details {
    padding: 10px;
}

.detail-row {
    display: flex;
    flex-direction: column;
}

.order-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #fff;
}

.item-image {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 5px;
}

.item-details {
    display: flex;
    flex-direction: column;
    gap: 5px;
    color: var(--color-btn-green-background);
}

.item-price {
    margin-left: auto;
    font-weight: bold;
}

@media (min-width: 768px) {
    .order-content {
        flex-direction: row;
        justify-content: space-between;
    }
    .order-info-column, .order-status-column {
        margin: 10px;
    }
}

@media (max-width: 767px) {
    .order-content {
        flex-direction: column;
    }
    .order-info-column, .order-status-column {
        margin: 0;
    }
}

.order-status {
    display: flex;
    padding: 10px;
    text-align: center;
    width: fit-content;
    min-width: 150px;
    border-radius: 10px;
    color: var(--color-active-text);
}

</style>
