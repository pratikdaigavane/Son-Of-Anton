const mongoose = require('mongoose');

const Schema = mongoose.Schema;

var questions = new Schema({
    prb_no: String,
    prb_name: String,
    prb_des: String,
    prb_input: String,
    prb_output: String,
    prb_link: String
});

module.exports = mongoose.model('questions', questions);
