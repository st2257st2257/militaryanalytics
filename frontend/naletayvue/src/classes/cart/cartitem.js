class CartItem {
    constructor(data) {
        Object.assign(this, data);
        this.quantity = data.quantity || 1;
    }

    update(data) {
        Object.assign(this, data);
    }
}

export default CartItem;
