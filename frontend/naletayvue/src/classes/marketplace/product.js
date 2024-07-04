class Product {
    constructor(data) {
        for (const key in data) {
            if (Object.hasOwnProperty.call(data, key)) {
                this[key] = data[key];
            }
        }
    }
}

export default Product;
