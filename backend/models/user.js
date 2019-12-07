const mongoose = require('mongoose');

const Schema = mongoose.Schema;

var schema_users = new Schema({
    name: String,
    username: String,
    email: String,
    password: String,
    cf_handle: String,
    ladder_current: {type: Number, default: 1},
    last_updated: { type: Date, default: Date.now },
    rating: {type: Number, default: 1500}
});



module.exports = mongoose.model('user', schema_users);
