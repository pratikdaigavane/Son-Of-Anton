// Exxpress and all requires
const mongoose = require('mongoose');

var dbconn = false;

mongoose.connect('mongodb+srv://user1:DNlP4zZPgpJNgJux@cluster0-mujak.mongodb.net/test?retryWrites=true&w=majority', {useNewUrlParser: true});

mongoose.connection.once('open', () => {
    //connecetd!
    dbconn = true;
    console.log("OK")
}).on('error', (err) => {
    //error (=err)
});