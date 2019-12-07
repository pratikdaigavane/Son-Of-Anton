// Exxpress and all requires
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const jwt = require('jsonwebtoken');
const csv = require('csvtojson');
let dbconn = false;

mongoose.connect('mongodb+srv://user1:DNlP4zZPgpJNgJux@cluster0-mujak.mongodb.net/test?retryWrites=true&w=majority', {useNewUrlParser: true, useUnifiedTopology: true});
mongoose.connection.once('open', () => {
    //connecetd!
    dbconn = true;
    console.log("OK")
}).on('error', (err) => {
    //error (=err)
});

var app = express();
app.use(bodyParser.urlencoded({extended: true}));

const User = require('./models/user');
const que = require('./models/questions');

function verifyToken(req, res, next) {
    const bearerHeader = req.headers['authorization'];
    if (typeof bearerHeader !== 'undefined') {
        const bearerToken = bearerHeader.split(' ')[1];
        req.token = bearerToken;
        jwt.verify(req.token, 'secretkey', (err, user) => {
            if (err)
                res.sendStatus(403);
            else
                req.user = user;
        });
        next();
    } else {
        res.sendStatus(403);
    }
}


app.post('/api/login', (req, res) => {
    // var user = new User({username: req.body.username, password: req.body.password});
    User.findOne({username: req.body.username, password: req.body.password}).then((result)=>{
        if(result){
            console.log(result);
            jwt.sign({user: result}, 'secretkey', (err, token) => {
                res.json({token});
            })
        }else
            res.status(400).json({status: 'invalid_username_password'});
    });
});



app.post('/api/register', (req, res) => {
        console.log(req.body);
        let user = new User({
            name: req.body.name,
            username: req.body.username,
            password: req.body.password,
            cf_handle: req.body.cf_handle,
            rating: 1500
        });


        User.findOne({username: req.body.username}).then((result) => {
                if (result == null) {
                    User.findOne({cf_handle: req.body.cf_handle}).then((result) => {
                        if (result == null) {
                            let us = user.save();
                            if (typeof us === 'undefined')
                                res.sendStatus(500);
                            else
                                res.json({status: 'success'});
                        }else
                            res.json({status: 'duplicate_cf_handle'})
                    })
                }
                else
                    res.json({status: 'duplicate_username'})
            }
        );
    }
);

app.get('/api/testlogin', verifyToken, (req, res) => {
    res.end("OK");
});

app.post('/api/ladder', verifyToken,(req, res)=>{

    let username = req.user.name;
    let currProb = req.user.ladder_current;
    currProb=7;
    let resp = {
        ques: [],
        curr: currProb
    };
    csv().fromFile('ps.csv').then((jsonObj)=>{
        //console.log(jsonObj)
        for(let i=0;i<currProb;i++)
        {
            resp.ques.push(jsonObj[i]);
        }
        console.log(resp.ques);
        res.json(resp);
    });




});
if (app.listen(8888))
    console.log("Listening on port 8000");
