import CartItem from '@/classes/cart/cartitem.js';
import api from '@/authAPI.js';

class Cart {
    constructor(store) {
        this.store = store;
        this.items = [];
        this.files = [];

        this.loadCartItemsFromStore();
        this.loadFilesFromStore();
    }

    loadCartItemsFromStore() {
        const items = this.store.getters['cart/cartItems'];
        this.loadCartItems(items);
    }

    loadFilesFromStore() {
        const files = this.store.getters['cart/cartFiles'];
        this.files = files;
    }

    loadCartItems(items) {
        this.items = Array.isArray(items) ? items.map(item => new CartItem(item)) : [];
    }

    async addItem(itemData) {
        await this.loadCartItemsFromStore()
        const existingItemIndex = this.items.findIndex(item => this.compareItems(item, itemData));
        if (existingItemIndex !== -1) {
            await this.updateItem(existingItemIndex, { quantity: this.items[existingItemIndex].quantity + 1 });
            window.notificationManager.addNotification('success', `${itemData.name} добавлен в корзину`);
        } else {
            const newItem = new CartItem(itemData);
            window.notificationManager.addNotification('success', `${itemData.name} добавлен в корзину`);
            this.items.push(newItem);
            await this.saveCartItemsToStore();
        }
    }

    async removeItem(index) {
        if (index !== -1) {
            const item = this.items[index];
            this.items.splice(index, 1);
            window.notificationManager.addNotification('error', `${item.name} удален из корзины`);
            await this.saveCartItemsToStore();
        }
    }

    async updateItem(index, changes) {
        const item = this.items[index];
        const updatedItemData = { ...item, ...changes };
        if (updatedItemData.quantity <= 0) {
            await this.removeItem(index);
        } else {
            this.items[index] = new CartItem(updatedItemData);
            await this.saveCartItemsToStore();
        }
    }

    async clear() {
        this.items = [];
        this.files = [];
        await this.saveCartItemsToStore();
        await this.saveFilesToStore();
        window.notificationManager.addNotification('error', `Корзина была очищена`);
    }

    calculateQuantity() {
        return this.items.reduce((acc, item) => acc + item.quantity, 0);
    }

    calculateTotal() {
        return this.items.reduce((acc, item) => acc + item.price * item.quantity, 0);
    }

    async addFile(file) {
        this.files = [file];
        window.notificationManager.addNotification('success', `${file.name} был успешно загружен`);
        await this.saveFilesToStore();
    }

    async saveCartItemsToStore() {
        await this.store.dispatch('cart/setCartItems', this.items.map(item => ({ ...item })));
    }

    async saveFilesToStore() {
        await this.store.dispatch('cart/setFiles', this.files.map(file => ({ ...file })));
    }

    async processOrder() {
        if (this.items.length === 0) {
            window.notificationManager.addNotification('error', `Корзина пуста`);
            return false;
        }
    
        const currentUser = this.store.getters['user/currentUser'];
    
        if (!currentUser) {
            window.loginModal.open();
            window.notificationManager.addNotification('error', `Войдите чтобы сделать заказ`);
            return false;
        }
    
        try {
            this.items.forEach(item => {
                if (!item.userLogin) {
                    console.warn(`Item ${item.name} is missing userLogin property`);
                }
            });
    
            const uniqueUsers = Array.from(new Set(this.items.map(item => item.userLogin)));
    
            for (const user of uniqueUsers) {
                const userItems = this.items.filter(item => item.userLogin === user);
                this.processUserOrder(user, userItems, currentUser);
            }
    
            return true;
        } catch (error) {
            console.error('Ошибка при обработке заказа:', error);
            window.notificationManager.addNotification('error', `Произошла ошибка при обработке заказа: ${error.message}`);
            return false;
        }
    }
    
    async processUserOrder(user, userItems, currentUser) {
        if (userItems.length > 0) {
            const productIdArray = [];
            const quantityArray = [];
    
            userItems.forEach(item => {
                productIdArray.push(item.id);
                quantityArray.push(item.quantity);
            });

            const formData = new FormData();
            formData.append('action', "setMulti");
            formData.append('productIdArray', productIdArray.join(','));
            formData.append('quantityArray', quantityArray.join(','));
    
            const response = await api.post('/products/set/', formData);
            const isChatCreated = await window.chatsManager.addChat(currentUser.username, user);
            console.log(isChatCreated)

            if (isChatCreated) {
                const numberOrder = Math.floor(Math.random() * 1000) + 1;
                const orderMessageJSON = {
                    messageType: 'order',
                    orderNumber: numberOrder,
                    user: currentUser.username,
                    items: userItems.map(item => ({
                        name: item.name,
                        quantity: item.quantity,
                        price: item.price,
                        selectedAddons: item.selectedAddons,
                        fileName: item.fileName
                    }))
                };
    
                await window.chatsManager.loadChats(currentUser.username);
    
                const chat = await window.chatsManager.getChatByUsers(currentUser.username, user);
    
                if (chat) {
                    await chat.addSystemMessage(JSON.stringify(orderMessageJSON), this.files);
                    window.notificationManager.addNotification('success', `Заказ #${numberOrder} был успешно создан для пользователя ${user}`);
                    await this.clear()
                } else {
                    window.notificationManager.addNotification('error', `Не удалось создать заказ для пользователя ${user}`);
                }
            }
        } else {
            console.warn(`No items found for user ${user}`);
        }
    }
     
    compareItems(item1, item2) {
        return item1.id === item2.id && JSON.stringify(item1.selectedAddons) === JSON.stringify(item2.selectedAddons);
    }
}

export default Cart;
