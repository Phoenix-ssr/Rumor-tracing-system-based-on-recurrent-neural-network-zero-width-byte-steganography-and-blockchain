const web3 = require('web3');
const ethRPC = "http://localhost:8545";
const port = 3000;
const provider = new web3.providers.HttpProvider(ethRPC);
const web3Client = new web3(provider);
const coinbase = '0x5f289771459e459366c3437a75843cf4bbecc041'; //矿工

const contract = require("truffle-contract");
const express = require('express');
const app = express();
const cors = require('cors');

app.use(cors());

/*
function eraseErrorOfContract(arr) {
    for (let contrc of arr) {
        if (typeof contrc.currentProvider.sendAsync !== "function") {
            contrc.currentProvider.sendAsync = function() {
                return contrc.currentProvider.send.apply(
                    contrc.currentProvider, arguments
                );
            }
        }
    }
}
*/

//const traceabilityJSON = require('../build/contracts/testTraceability_addTime');
//const traceability = contract(traceabilityJSON);

var contract_abi = [{
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "constant": false,
        "inputs": [{
                "internalType": "uint256",
                "name": "a",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "b",
                "type": "uint256"
            }
        ],
        "name": "addtest",
        "outputs": [{
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
        }],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [],
        "name": "getCount",
        "outputs": [{
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
        }],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    }
];

var MetaCoin = contract({
    abi: contract_abi
});


MetaCoin.setProvider(provider);
var traceabilityInst;
//eraseErrorOfContract([traceability]);

// 账户地址
var account_one = "0x5b69f37680ba9be71280c8c8da2b157ada702a43";
// 合约地址
var contract_address = "0x2E2649493100Cf511cd4064Fa72DFbd4dbC6912F";

MetaCoin.at(contract_address).then(function(instance) {
    traceabilityInst = instance;
    return instance.getBalance.call(account_one);
}).then(function(balance) {
    console.log(balance.toNumber());
}).catch(function(err) {
    console.log(err);
});

app.get('/add', function(req, res) { // app => router  
    //let currentTime = new Date().toLocaleString();
    traceabilityInst.addtest(1, 2, { from: coinbase, gas: 0x138000 }).then(result => {
        console.log(result);
        //res.send('Hello World!')
        res.send("您已将信息上链！交易hash:" + result.tx);
    }).catch(err => {
        console.log(err);
        res.send(err)
    });
});
app.get('/get', function(req, res) { //get 传参测试 res返回数据
    traceabilityInst.getCount({ from: coinbase, gas: 0x138000 }).then(result => {
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