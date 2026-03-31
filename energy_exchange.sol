// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EdgeTechEnergyExchange {
    struct Node {
        uint256 energyBalance;
        address payable wallet;
    }

    mapping(string => Node) public nodes;

    // Node A sells 5kWh to Node B
    function transferEnergy(string memory sellerID, string memory buyerID, uint256 kwh) public payable {
        uint256 price = 0.05 ether; // Example 2026 Energy Rate
        uint256 totalCost = kwh * price;
        
        require(msg.value >= totalCost, "Insufficient funds for energy trade.");
        
        // The 90/10 Sovereignty Split
        uint256 sellerShare = (totalCost * 90) / 100;
        uint256 networkFee = totalCost - sellerShare;
        
        // Execute the trade
        nodes[sellerID].wallet.transfer(sellerShare);
        // networkFee stays in contract for mesh maintenance
    }
}
