const mongoose = require("mongoose");
const ProductSchema = new mongoose.Schema({
    companyId: String,
    category: String,
    image: String,
    barkod: String,
    name: String,
    price: Number,
    date: Date,
});

const ProductModel = mongoose.model("products", ProductSchema);
module.exports = ProductModel;
