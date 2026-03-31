// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PhoneServeRewards {
    address public owner;
    
    // The 90/10 Split Logic
    function distributeRewards(address payable nodeOperator) public payable {
        uint256 total = msg.value;
        uint256 operatorAmount = (total * 90) / 100;
        uint256 maintenanceAmount = total - operatorAmount;
        
        nodeOperator.transfer(operatorAmount);
        // Maintenance fee stays in the contract for network costs
    }
}
