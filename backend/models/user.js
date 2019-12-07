const mongoose = require('mongoose');

const Schema = mongoose.Schema;

var schema_users = new Schema({
    name: String,
    username: {type: String, required: true},
    password: String,
    cf_handle: String,
    last_updated: { type: Date, default: Date.now },
});


module.exports = mongoose.model('user', schema_users);