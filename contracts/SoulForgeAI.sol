// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface ISoulForgeAI {
    struct AgentState {
        uint8 tier;
        uint32 level;
        uint64 xp;
        bytes32 memoryIpfsHash;
        uint256 dailyAllowanceWei;
        uint256 spentTodayWei;
        uint256 lastResetTimestamp;
    }

    struct CapabilityFlags {
        bool legalTriageEnabled;
        bool yieldAutoClaimEnabled;
        bool proxyRoutingEnabled;
        bool highComputeAccess;
    }

    event AgentInitialized(address indexed soulOwner, uint256 indexed tokenId);
    event AgentUpgraded(address indexed soulOwner, uint8 newTier, uint32 newLevel);
    event MemoryHashUpdated(address indexed soulOwner, bytes32 newMemoryHash);
    event CapabilityUnlocked(address indexed soulOwner, string capabilityName);
    event DelegatedActionExecuted(address indexed soulOwner, address indexed target, uint256 value);

    function initializeAgent(address soulOwner) external returns (uint256 tokenId);
    function upgradeModule(uint8 moduleId) external payable;
    function updateMemoryHash(bytes32 newHash) external;
    function executeDelegatedAction(address target, uint256 value, bytes calldata data) external returns (bytes memory result);
    function getAgentState(address soulOwner) external view returns (AgentState memory);
    function getCapabilities(address soulOwner) external view returns (CapabilityFlags memory);
    function isActionAllowed(address soulOwner, uint256 value) external view returns (bool);
}

contract SoulForgeAIAgent is ISoulForgeAI {
    address public immutable soulForgeRegistry;
    mapping(address => AgentState) private _agentStates;
    mapping(address => CapabilityFlags) private _capabilities;
    mapping(address => address) public agentSessionKeys;

    modifier onlySoulOwnerOrSessionKey(address soulOwner) {
        require(
            msg.sender == soulOwner || msg.sender == agentSessionKeys[soulOwner],
            "SoulForge: Unauthorized agent caller"
        );
        _;
    }

    constructor(address _registry) {
        soulForgeRegistry = _registry;
    }

    function initializeAgent(address soulOwner) external override returns (uint256 tokenId) {
        require(_agentStates[soulOwner].level == 0, "Agent already exists");
        _agentStates[soulOwner] = AgentState({
            tier: 1,
            level: 1,
            xp: 0,
            memoryIpfsHash: bytes32(0),
            dailyAllowanceWei: 0.005 ether,
            spentTodayWei: 0,
            lastResetTimestamp: block.timestamp
        });
        _capabilities[soulOwner] = CapabilityFlags({
            legalTriageEnabled: false,
            yieldAutoClaimEnabled: true,
            proxyRoutingEnabled: true,
            highComputeAccess: false
        });
        tokenId = uint256(uint160(soulOwner));
        emit AgentInitialized(soulOwner, tokenId);
        return tokenId;
    }

    function setSessionKey(address sessionKey) external {
        agentSessionKeys[msg.sender] = sessionKey;
    }

    function updateMemoryHash(bytes32 newHash) external override onlySoulOwnerOrSessionKey(msg.sender) {
        _agentStates[msg.sender].memoryIpfsHash = newHash;
        emit MemoryHashUpdated(msg.sender, newHash);
    }

    function upgradeModule(uint8 moduleId) external payable override {
        AgentState storage state = _agentStates[msg.sender];
        CapabilityFlags storage caps = _capabilities[msg.sender];

        if (moduleId == 1) {
            require(!caps.legalTriageEnabled, "Already unlocked");
            require(msg.value >= 0.01 ether, "Insufficient fee");
            caps.legalTriageEnabled = true;
            state.xp += 500;
            emit CapabilityUnlocked(msg.sender, "LegalTriage");
        } else if (moduleId == 2) {
            require(!caps.highComputeAccess, "Already unlocked");
            require(msg.value >= 0.02 ether, "Insufficient fee");
            caps.highComputeAccess = true;
            state.xp += 1000;
            emit CapabilityUnlocked(msg.sender, "HighCompute");
        }

        if (state.xp >= state.level * 1000) {
            state.level += 1;
            if (state.level % 5 == 0) state.tier += 1;
            emit AgentUpgraded(msg.sender, state.tier, state.level);
        }
    }

    function executeDelegatedAction(address target, uint256 value, bytes calldata data) external override returns (bytes memory result) {
        address soulOwner = msg.sender;
        if (msg.sender == agentSessionKeys[soulOwner]) {
            AgentState storage state = _agentStates[soulOwner];
            if (block.timestamp > state.lastResetTimestamp + 1 days) {
                state.spentTodayWei = 0;
                state.lastResetTimestamp = block.timestamp;
            }
            require(state.spentTodayWei + value <= state.dailyAllowanceWei, "Exceeds daily allowance");
            state.spentTodayWei += value;
        }

        (bool success, bytes memory returnData) = target.call{value: value}(data);
        require(success, "Delegated execution failed");

        emit DelegatedActionExecuted(soulOwner, target, value);
        return returnData;
    }

    function getAgentState(address soulOwner) external view override returns (AgentState memory) {
        return _agentStates[soulOwner];
    }

    function getCapabilities(address soulOwner) external view override returns (CapabilityFlags memory) {
        return _capabilities[soulOwner];
    }

    function isActionAllowed(address soulOwner, uint256 value) external view override returns (bool) {
        AgentState memory state = _agentStates[soulOwner];
        return (state.spentTodayWei + value <= state.dailyAllowanceWei);
    }
}
