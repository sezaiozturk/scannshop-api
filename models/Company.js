const mongoose = require("mongoose");
const CompanySchema = new mongoose.Schema({
    companyName: String,
    companyType: String,
    city: String,
    district: String,
    neighbourhood: String,
    name: String,
    surName: String,
    email: String,
    phoneNumber: String,
    password: String,
});

const CompanyModel = mongoose.model("companys", CompanySchema);
module.exports = CompanyModel;
