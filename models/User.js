const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const UserSchema = new mongoose.Schema({
    name: String,
    email: String,
    password: String,
});

UserSchema.methods.createAuthToken = () => {
    return jwt.sign({_id: this._id}, 'jwtPrivateKey');
};

const UserModel = mongoose.model('users', UserSchema);
module.exports = UserModel;
