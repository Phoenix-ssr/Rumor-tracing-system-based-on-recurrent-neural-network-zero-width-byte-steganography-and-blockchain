const web3 = require('web3');
const ethRPC = "http://localhost:8545"; //私链的http服务
const port = 3000; //express的端口配置
const provider = new web3.providers.HttpProvider(ethRPC); //用于连接基于 http和https 的 JSON-RPC 服务器
const web3Client = new web3(provider); //初始化连接
const coinbase = '0x5f289771459e459366c3437a75843cf4bbecc041'; //矿工

const contract = require("truffle-contract"); //用来与以太坊智能合约交互的JavaScript库
const express = require('express'); //Node.js Web 应用程序框架
const app = express(); //创建一个服务
const cors = require('cors'); //跨域
app.use(cors()); //启用跨域

//合约的abi 
var contract_abi = [{
        "inputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [{
                "indexed": false,
                "internalType": "uint256",
                "name": "messageId",
                "type": "uint256"
            },
            {
                "indexed": false,
                "internalType": "string",
                "name": "trace",
                "type": "string"
            }
        ],
        "name": "SavedMessage",
        "type": "event"
    },
    {
        "constant": false,
        "inputs": [{
                "internalType": "string",
                "name": "ID",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "time",
                "type": "string"
            }
        ],
        "name": "addMessageLine",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [{
                "internalType": "string",
                "name": "ID",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "message",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "time",
                "type": "string"
            }
        ],
        "name": "addMessageLine2",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [{
            "internalType": "string",
            "name": "ID",
            "type": "string"
        }],
        "name": "getTrace",
        "outputs": [{
            "internalType": "string",
            "name": "",
            "type": "string"
        }],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": false,
        "inputs": [{
            "internalType": "string",
            "name": "ID",
            "type": "string"
        }],
        "name": "getTrace2",
        "outputs": [{
            "internalType": "string",
            "name": "",
            "type": "string"
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
// 账户地址
var account_one = "0x5b69f37680ba9be71280c8c8da2b157ada702a43";
// 合约地址
var contract_address = "0x8779529eAD851C709061B9902356D4e18BD36148"; //data0

MetaCoin.at(contract_address).then(function(instance) {
    traceabilityInst = instance;
    return instance.getBalance.call(account_one);
}).then(function(balance) {
    console.log(balance.toNumber());
}).catch(function(err) {
    console.log(err);
});

app.get('/add', function(req, res) { // req传参 query get参数 参数名
    let currentTime = new Date().toLocaleString();
    traceabilityInst.addMessageLine(req.query.id, req.query.message, currentTime, { from: coinbase, gas: 0x138000 }).then(result => {
        console.log(result);
        res.send("您已将信息上链！交易hash:" + result.tx); //打印交易hash
    }).catch(err => {
        console.log(err);
        res.send(err)
    });
});
app.get('/add2', function(req, res) { // req传参 query get参数 参数名
    let currentTime = new Date().toLocaleString();
    traceabilityInst.addMessageLine2(req.query.id, req.query.message, currentTime, { from: coinbase, gas: 0x138000 }).then(result => {
        console.log(result);
        res.send("您已将信息上链！交易hash:" + result.tx); //打印交易hash
    }).catch(err => {
        console.log(err);
        res.send(err)
    });
});
app.get('/get', function(req, res) { //get  res返回数据    
    traceabilityInst.getTrace.call(req.query.id, { from: coinbase, gas: 0x138000 }).then(result => { //call获取智能合约信息
        console.log(result);
        res.send("获得:" + result.tx + "\n" + result);
    }).catch(err => {
        console.log(err);
        res.send(JSON.stringify(err))
    });
});
app.get('/get2', function(req, res) { //get  res返回数据    
    traceabilityInst.getTrace2.call(req.query.id, { from: coinbase, gas: 0x138000 }).then(result => { //call获取智能合约信息
        console.log(result);
        res.send("获得:" + result.tx + "\n" + result);
    }).catch(err => {
        console.log(err);
        res.send(JSON.stringify(err))
    });
});
app.get('/', function(req, res) { //get  res返回数据
    res.send('Hello World!' + req.query.a + req.query.b)
});





var server = app.listen(port, function() { //开启服务，打印ip和port
    var host = server.address().address;
    var port = server.address().port;
    console.log('Express started on http://' + host + ':' + port);
});