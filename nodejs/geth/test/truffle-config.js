
require("babel-register")({
	ignore:/node_modules\/(?!zeppelin-solidity)/
});
require('babel-polyfill');

module.exports = {

  networks: {
     development: {
      host: "127.0.0.1",     // Localhost (default: none)
      port: 8545,            // Standard Ethereum port (default: none)
      network_id: "*",       // Any network (default: none)
      //gas:800
     }
  },
  mocha: {
    useColors:true
  },


    solc: {
        optimizer: {
          enabled: false,
          runs: 200
        },
    }
  
};
