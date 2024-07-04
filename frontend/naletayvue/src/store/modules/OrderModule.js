import api from '@/authAPI.js';
import Order from '@/classes/marketplace/order.js';

const orderModule = {
    namespaced: true,
    state: {
        orders: [],
    },
    mutations: {
        setOrders(state, orders) {
            state.orders = orders;
        },
        updateOrderStatus(state, { orderId, status }) {
            const order = state.orders.find(order => order.id === orderId);
            if (order) {
                order.status = status;
            }
        },
    },
    actions: {
        async fetchOrders({ commit }) {
            try {
                const formData = new FormData();
                formData.append('action', 'getAllOrders');
                const response = await api.post('/products/get/', formData);

                if (!response.data.result || !response.data.data) {
                    console.error('Ошибка при получении заказов:', response.data);
                    return false;
                }

                const ordersData = response.data.data;
                const orders = [];

                Object.entries(ordersData).forEach(([sellerEmail, sellerOrders]) => {
                  Object.entries(sellerOrders).forEach(([orderId, orderDetails]) => {
                      if (typeof orderDetails === 'object' && !Array.isArray(orderDetails)) {
                          const products = [];
              
                          Object.keys(orderDetails).forEach(key => {
                              if (!isNaN(key)) {
                                  const orderRes = orderDetails[key].orderRes;
                                  if (orderRes) {
                                      const product = {
                                          id: parseInt(key),
                                          name: orderRes.productName,
                                          specifications: orderRes.specifications,
                                          category: orderRes.category,
                                          subCategory: orderRes.subCategory,
                                          totalPrice: orderRes.totalPrice,
                                          quantity: orderRes.quantity
                                      };
                                      products.push(product);
                                  } else {
                                      console.error(`Order details missing for order ID: ${orderId}`);
                                  }
                              }
                          });
              
                          const order = Order.fromData(parseInt(orderId), {
                              products,
                              user_login: orderDetails[Object.keys(orderDetails)[0]].orderRes.user_login,
                              user_full_name: orderDetails[Object.keys(orderDetails)[0]].orderRes.user_full_name,
                              order_status_id: orderDetails[Object.keys(orderDetails)[0]].orderRes.order_status_id,
                              date: orderDetails[Object.keys(orderDetails)[0]].orderRes.date,
                              seller_login: orderDetails[Object.keys(orderDetails)[0]].orderRes.seller_login,
                              seller_name: orderDetails[Object.keys(orderDetails)[0]].orderRes.seller_name,
                              seller_email: orderDetails[Object.keys(orderDetails)[0]].orderRes.seller_email,
                              seller_full_name: orderDetails[Object.keys(orderDetails)[0]].orderRes.seller_full_name,
                          });
                          orders.push(order);
                      } else {
                          console.error(`Invalid order details structure for seller ${sellerEmail}`);
                      }
                  });
              });
              
              commit('setOrders', orders);

            } catch (error) {
                console.error('Ошибка при получении заказов:', error);
                throw error;
            }
        },
        async updateOrderStatus({ commit, dispatch }, { orderId, status }) {
            try {
                const formData = new FormData();
                formData.append('action', 'editStatus');
                formData.append('orderId', orderId);
                formData.append('newStatus', status);
                const response = await api.post('/products/set/', formData);

                if (!response.data.result) {
                    console.error('Ошибка при обновлении статуса заказа:', response.data);
                    return false;
                }
                
                window.notificationManager.addNotification('success', `Вы успешно изменили статус заказа №${orderId}`, 3000, true);
                commit('updateOrderStatus', { orderId, status });
                dispatch('fetchOrders');

            } catch (error) {
                console.error('Ошибка при обновлении статуса заказа:', error);
                throw error;
            }
        },
    },
    getters: {
        orders(state) {
            return state.orders;
        },
        getOrderById: (state) => (id) => {
            return state.orders.find(order => order.id === id);
        },
    },
};

export default orderModule;
