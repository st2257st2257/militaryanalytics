class Order {
    constructor({ id, products, owner, status = 1, ...rest }) {
        this.id = id;
        this.products = products;
        this.owner = owner;
        this.status = status;
        Object.assign(this, rest);
    }

    static fromData(id, data) {
        return new Order({
            id,
            products: data.products,
            owner: {
                login: data.user_login,
                name: data.user_full_name,
            },
            status: data.order_status_id,
            date: data.date,
            seller: {
                login: data.seller_login,
                name: data.seller_name,
                email: data.seller_email,
                fullName: data.seller_full_name,
            }
        });
    }

    getStatusText() {
        const statusMap = {
            1: 'В ожидании',
            2: 'Подтвержден',
            3: 'Отправлен',
            4: 'Доставлен',
            0: 'Отменен',
        };
        return statusMap[this.status] || 'Неизвестен';
    }
}

export default Order;
