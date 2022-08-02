pragma solidity ^0.5.16;
//pragma experimental ABIEncoderV2;
import "./strings.sol"; 

contract rumor{
/*区块链存储*/
	using strings for *;  
	string constant optStr = "==>";  
	string constant leftOpt = "(";  
	string constant rightOpt = ")";  
	/*智能合约在执行过程中所发生的一系列事件*/
	event SavedMessage(uint256 messageId,string trace);
	/*结构体*/
	struct Message {  
		string trace;
		string trace2;   
	}
	
	mapping(string => Message) allMessage;
	 
	constructor () public{  
	}  
	/*溯源链*/
	function addMessageLine(string memory ID, string memory message ,string memory time) public {
		string memory info1 = time.toSlice().concat(rightOpt.toSlice());  //(time
		string memory info2 = leftOpt.toSlice().concat(info1.toSlice());  // time) 
		string memory info3 = message.toSlice().concat(info2.toSlice());  //(time)message
		string memory concatStr = info3.toSlice().concat(optStr.toSlice());  //==>(time)message
		allMessage[ID].trace = allMessage[ID].trace.toSlice().concat(concatStr.toSlice());//==>(time)message + trace
	}
		/*溯源链2*/
	function addMessageLine2(string memory ID, string memory message ,string memory time) public {
		string memory info1 = time.toSlice().concat(rightOpt.toSlice());  //(time
		string memory info2 = leftOpt.toSlice().concat(info1.toSlice());  // time) 
		string memory info3 = message.toSlice().concat(info2.toSlice());  //(time)message
		string memory concatStr = info3.toSlice().concat(optStr.toSlice());  //==>(time)message
		allMessage[ID].trace2 = allMessage[ID].trace2.toSlice().concat(concatStr.toSlice());//==>(time)message + trace2
	}
	/*获取信息*/
	function getTrace(string memory ID) public returns (string memory){
		return allMessage[ID].trace;
	}
	function getTrace2(string memory ID) public returns (string memory){
		return allMessage[ID].trace2;
	}
}