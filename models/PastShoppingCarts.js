const mongoose = require('mongoose');
const PastShoppingCartSchema = new mongoose.Schema({
    userId: String,
    pastShoppingCarts: [
        {
            companyId: String,
            companyName: String,
            shoppingCarts: Array,
        },
    ],
});

const PastShoppingCartModel = mongoose.model(
    'pastShoppingCarts',
    PastShoppingCartSchema,
);
module.exports = PastShoppingCartModel;
