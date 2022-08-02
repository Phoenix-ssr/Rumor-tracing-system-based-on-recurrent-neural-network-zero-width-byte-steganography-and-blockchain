const web3 = require('web3');
const ethRPC = "http://localhost:8545";
const port = 3000;
const provider = new web3.providers.HttpProvider(ethRPC);
const web3Client = new web3(provider);
const coinbase = '0x5f289771459e459366c3437a75843cf4bbecc041'; //矿工

var address = '';

var fs = require('fs');
var abi = JSON.parse();
var contract = web3.eth.contract(abi);
var instance = contract.at(address);



app.get('/add', function(req, res) { // app => router  
    //let currentTime = new Date().toLocaleString();
    traceabilityInst.addtest(1, 2, { from: coinbase, gas: 600 }).then(result => {
        console.log(result);
        res.send("您已将信息上链！交易hash:" + result.tx);
    }).catch(err => {
        console.log(err);
        res.send(JSON.stringify(err))
    });
});
app.get('/get', function(req, res) { //get 传参测试 res返回数据
    traceabilityInst.getcount().then(result => {
        console.log(result);
        res.send("获得:" + result.tx);
    }).catch(err => {
        console.log(err);
        res.send(JSON.stringify(err))
    });
});

app.get('/', function(req, res) { //get 传参测试 res返回数据
    res.send('Hello World!' + req.query.a + req.query.b)
});





var server = app.listen(port, function() {
    var host = server.address().address;
    var port = server.address().port;
    console.log('Express started on http://' + host + ':' + port);
});