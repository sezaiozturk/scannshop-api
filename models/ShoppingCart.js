const mongoose = require('mongoose');
const ShoppingCartSchema = new mongoose.Schema({
    userId: String,
    shoppingCarts: Array,
});

const ShoppingCartModel = mongoose.model('shoppingCarts', ShoppingCartSchema);
module.exports = ShoppingCartModel;
