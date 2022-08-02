var testTraceability_addTime = artifacts.require("testTraceability_addTime.sol"); 
var rumor = artifacts.require("./rumor.sol");
//合约位置
var strings = artifacts.require("./strings.sol");  
 
module.exports = function(deployer) {  
	deployer.deploy(strings,  {from:"0x5f289771459e459366c3437a75843cf4bbecc041"});// 部署合约，使用旷工地址（保证gas费充足）  		
	deployer.link(strings, rumor);   // 库链接  
	deployer.deploy(rumor,  {from:"0x5f289771459e459366c3437a75843cf4bbecc041"});// 部署合约    
};  