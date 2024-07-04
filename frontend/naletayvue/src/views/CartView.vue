<template>
    <div class="cart_container">
        <div :class="[ 'cart-item_container', { 'centered': cartItems.length === 0 } ]">
            <h2>
                {{ cartItems.length === 0 ? 'В корзине пока пусто' : 'Корзина' }}
                <button v-if="cartItems.length != 0" class="btn error-btn" @click="clearCart">Очистить</button>
            </h2>
            
            <div v-if="cartItems.length === 0" class="cart-item-none_container centered">
                Воспользуйтесь поиском, чтобы найти всё, что нужно.
                Если в Корзине были Беспилотники, войдите, чтобы посмотреть список
                <router-link class="btn green-btn" to="/catalog">В каталог</router-link>
            </div>

            <template v-else>
                <CartItem 
                    v-for="(item, index) in cartItems" 
                    :key="index" 
                    :item="item"
                    :index="index"
                    @update="updateCart"
                    @remove="removeItem"
                />
            </template> 
        </div>
        <div class="order_container">
            <div class="order-price">
                <span class="price-item">
                    <h2>Итого</h2>
                    <h2>{{ formattedTotal }}</h2>
                </span>
                <span v-if="cartItems.length > 0" class="price-item">
                    <p>Беспилотники {{ totalQuantity + ' шт.'}}</p>
                    <p>{{ formattedTotal }}</p>
                </span>
                <span class="info-text">
                    Если вы не знаете, какой из представленных товаров поставщика 
                    лучше подходит под ваши задачи, либо есть дополнительные требования, 
                    просто загрузите спецификацию, и поставщик проконсультирует вас
                </span>
                <div class="file-upload">
                    Вы можете загрузить файл со спецификацией
                    <input id="fileInput_spec" type="file" ref="fileInput" @change="onFileChange" />
                    <label for="fileInput_spec" class="file-icon">
                        <specFileIcon />
                    </label>
                </div>
                <div v-if="files.length > 0" class="uploaded-files">
                    <div v-for="file in files" :key="file.name">{{ file.name }}</div>
                </div>
            </div>
            <button class="btn green-btn order-btn" @click="checkout">Оформить заказ</button>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import CartItem from '@/components/cart/CartItem.vue';
import specFileIcon from '@/assets/icons/saveFiles.svg';
import { formatCurrency } from '@/utils/format.js';
import Cart from '@/classes/cart/cart.js';

export default {
    components: {
        specFileIcon,
        CartItem,
    },
    computed: {
        ...mapGetters('cart', ['cartItems', 'cartItemsTotal', 'cartTotal']),
        totalQuantity() {
            return this.cartItems.reduce((acc, item) => acc + item.quantity, 0);
        },
        formattedTotal() {
            return formatCurrency(this.cartTotal, 'RUB');
        }
    },
    data() {
        return {
            files: [],
            cart: null
        };
    },
    created() {
        this.cart = new Cart(this.$store, this.$chatsManager);
    },
    methods: {
        clearCart(){
            this.cart.clear()
        },
        updateCart({ index, changes }) {
            this.cart.updateItem(index, changes);
        },
        removeItem(index) {
            this.cart.removeItem(index);
        },
        onFileChange(event) {
            const selectedFile = event.target.files[0];
            this.files = [selectedFile];
            this.cart.addFile(selectedFile);
        },
        checkout() {
            this.cart.processOrder();
        },
    }
};
</script>

<style scoped>
.cart_container {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    flex-flow: row wrap;
    width: 100%;
    max-width: 1280px;
    margin: 25px 0;
    box-sizing: border-box;
}

.cart-item_container {
    display: flex;
    flex-direction: column;
    gap: 15px;
    width: 68%;
    height: 100%;
    min-height: 400px;
    padding: 25px;
    background: var(--color-background-soft);
    border-radius: 15px;
}

.cart-item_container h2{
    display: flex;
    justify-content: flex-start;
    text-align: center;
    align-items: center;
    gap: 10px;
    width: fit-content;
}

.centered {
    justify-content: center;
    align-items: center;
    text-align: center;
}

.cart-item-none_container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    width: 80%;
    height: 100%;
    font-size: 14px;
}

.order_container {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 27%;
    min-height: 500px;
    padding: 25px;
    background: var(--color-background-soft);
    border-radius: 15px;
}

.order-price {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    width: 100%;
}

.price-item {
    display: flex;
    justify-content: space-between;
    width: 100%;
    height: 25px;
}

.info-text {
    text-align: justify;
    padding: 15px;
    border-radius: 10px;
    background: var(--color-background-info);
    color: var(--color-active-text);
}

.file-upload {
    display: flex;
    gap: 10px;
    width: 100%;
    padding-bottom: 15px;
    border-bottom: 1px solid var(--color-background-footer);
}

.file-upload input {
    display: none;
}

.uploaded-files {
    display: flex;
    width: 100%;
    font-size: 18px;
}

.order-btn {
    width: 95%;
    color: var(--color-active-text);
    background: var(--color-background-success);
}

@media (max-width: 1024px) {
    .cart-item_container, .order_container {
        width: 100%;
    }
    .order_container {
        margin: 25px 0;
    }
}

</style>
