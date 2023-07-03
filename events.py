import json
from web3 import Web3
from dotenv import load_dotenv
import os


# load_dotenv("../contracts/.env")


def get_web3_object(RPC_URL):
    return Web3(Web3.HTTPProvider(RPC_URL))


def get_chain_id(network_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    networks_json_path = os.path.join(script_dir, "..", "contracts", "networks.json")
    with open(networks_json_path) as file:
        data = json.load(file)

    for network in data.get("networks", []):
        if network.get("nameOfNetwork") == network_name:
            return network.get("chainId")

    return None


def get_network_name(chain_id):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    networks_json_path = os.path.join(script_dir, "..", "contracts", "networks.json")
    with open(networks_json_path) as file:
        data = json.load(file)

    for network in data.get("networks", []):
        if network.get("chainId") == chain_id:
            return network.get("nameOfNetwork")

    return None


def get_rpc_url(chain_id):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    networks_json_path = os.path.join(script_dir, "..", "contracts", "networks.json")
    print(networks_json_path)
    with open(networks_json_path) as file:
        data = json.load(file)

    for network in data.get("networks", []):
        if network.get("chainId") == chain_id:
            print(chain_id)
            return network.get("RPC_URL")

    return None


def get_contract_address(contractName, chain_id):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    networks_json_path = os.path.join(
        script_dir,
        "..",
        f"contracts/broadcast/DeployProtocol.s.sol/{chain_id}",
        "run-latest.json",
    )
    if chain_id is not None:
        file_path = networks_json_path
        with open(file_path, "r") as file:
            data = json.load(file)

        for transaction in data.get("transactions", []):
            contract_name = transaction.get("contractName")
            contract_address = transaction.get("contractAddress")

            if contract_name == contractName:
                result_address = contract_address
                break

        return result_address

    return None


def get_contract_abi(contract_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    networks_json_path = os.path.join(
        script_dir,
        "..",
        f"contracts/out/{contract_name}.sol",
        f"{contract_name}.json",
    )
    with open(networks_json_path) as f:
        abi = json.load(f)["abi"]
        return abi


def fetch_event_from_transaction(w3, contract, transaction_hash, event_name):
    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

    contract_abi = contract.abi

    event_signature_hash = None
    for item in contract_abi:
        if item["type"] == "event" and item["name"] == event_name:
            event_signature_hash = w3.keccak(
                text=f"{event_name}({','.join([input['type'] for input in item['inputs']])})"
            ).hex()
            break

    if event_signature_hash is None:
        raise ValueError(f"Event {event_name} not found in the contract ABI")

    for log in tx_receipt["logs"]:
        if log["topics"][0].hex() == event_signature_hash:
            decoded_log = contract.events[event_name]().process_log(log)

            return decoded_log["args"]

    return None


def fetch_event(contract_name, chain_id, transaction_hash, event_name):
    RPC_URL = get_rpc_url(chain_id)
    print(chain_id)

    w3 = get_web3_object(RPC_URL)
    contract_abi = get_contract_abi(contract_name)
    # print(contract_abi)

    contract_address = get_contract_address(f"{contract_name}", chain_id)
    # print(contract_address)
    contract_contract = w3.eth.contract(address=contract_address, abi=contract_abi)
    print("*********************************************")

    event_data = fetch_event_from_transaction(
        w3, contract_contract, transaction_hash, event_name
    )

    return event_data


# ******************************************************************************************
# ****************** Events description ****************************************************

"""
Below the description of each events + the functions that emits it

1. TokenBought
Contract : Marketplace
Event Arguments:
buyer: The address of the user who bought the TOM tokens.
amount: The amount of TOM tokens purchased.

Function: buyTokens(uint256 _amount)
Description: This function allows users to buy TOM tokens from the Marketplace.
Arguments:
_amount: The amount of TOM tokens the user wants to buy.


2. userRegistered
Contract : Marketplace
Event Arguments:
user: The address of the user who got registered.

Function: registerUser()
Description: This function allows a new user to register themselves in the Marketplace.

3. ItemListed
Contract : Marketplace
Event Arguments:
seller: The address of the seller who listed the item.
itemId: The unique identifier of the item.
name: The name of the item.
image: The image of the item.
description: The description of the item.
price: The price of the item.
quantity: The quantity of the item available for sale.
postingFee: The fee charged for listing the item.

Function: listItem(string _name, string _image, string _description, uint256 _price, uint256 _quantity, uint256 _postingFee)
Description: This function allows sellers to list a new item in the Marketplace.
Arguments:
_name: The name of the item.
_image: The image of the item.
_description: The description of the item.
_price: The price of the item.
_quantity: The quantity of the item available for sale.
_postingFee: The fee charged for listing the item.

4. ItemUpdated
Contract : Marketplace
Event Arguments:
seller: The address of the seller who updated the item.
itemId: The unique identifier of the item.
name: The updated name of the item.
image: The updated image of the item.
description: The updated description of the item.
price: The updated price of the item.
quantity: The updated quantity of the item.
postingFee: The updated fee for listing the item.

Function1: updateItem(uint256 _itemId, string _name, string _image, string _description, uint256 _price, uint256 _quantity, uint256 _postingFee)
Description: This function allows sellers to update the details of an already listed item.
Arguments:
_itemId: The unique identifier of the item.
_name: The updated name of the item.
_image: The updated image of the item.
_description: The updated description of the item.
_price: The updated price of the item.
_quantity: The updated quantity of the item.
_postingFee: The updated fee for listing the item.

Function2: orderItem(uint256 itemId, uint256 quantity)
Description: Order an item and updates existing item.
Arguments:
seller: The address of the seller.
buyer: The address of the buyer.
itemId: The ID of the item being ordered.
price: The total price of the order.
quantity: The quantity of the item being ordered.
rewards: Any additional rewards associated with the order.

5. ItemCanceled
Contract : Marketplace
Event Arguments:
seller: The address of the seller who canceled

Function: cancelItem(uint256 _itemId)
Description: This function allows a seller or the contract owner to cancel a listed item.
Arguments:
_itemId: The unique identifier of the item to be canceled.

6. OrderSent
Contract : Escrow
Event Arguments:
seller: The address of the seller.
buyer: The address of the buyer.
order: A unique identifier for the order generated using a hash.
itemId: The ID of the item being ordered.
price: The total price of the order.
quantity: The quantity of the item being ordered.
rewards: Any additional rewards associated with the order.
state: The current state of the order, in this case, FundsLocked.

Function: orderItem(uint256 itemId, uint256 quantity)
Description: Order an item and Locks the funds from the buyer when an order is placed. This is to ensure 
that the funds are held by the escrow until the order is complete. This function calls the lockFunds function 
of the Escrow contract that emits this event
Arguments:
seller: The address of the seller.
buyer: The address of the buyer.
itemId: The ID of the item being ordered.
price: The total price of the order.
quantity: The quantity of the item being ordered.
rewards: Any additional rewards associated with the order.

7. FundsReleased
Contract : Escrow
Event Arguments:
orderId: A unique identifier for the order.
seller: The address of the seller to whom the funds are released.
amount: The amount of funds released.

Function: confirmDelivery(uint256 orderId)
Description: Releases the funds to the seller once the buyer confirms the receipt or the order is deemed complete.
This function calls the releaseFunds function of the Escrow contract that emits this event.
Arguments:
orderId: A unique identifier for the order.
buyer: The address of the buyer.

8. FundsRefunded
Contract : Escrow
Event Arguments:
orderId: A unique identifier for the order.
buyer: The address of the buyer who is refunded.
amount: The amount of funds refunded.

Function: cancelOrder(uint256 orderId)
Description: Refunds the funds to the buyer in case of a dispute or if the order cannot be completed. This calls
the refundFunds function of the escrow contract that emits this event.
Arguments:
orderId: A unique identifier for the order.
buyer: The address of the buyer.

9. RewardsClaimed
Contract : Marketplace
Event Arguments:
user: The address of the user.
rewards: The rewards amount claimed by the user.

Function: claimRewards()
Description: Claims rewards if amount spent > 500 dollars

"""


# **********************************************  Examples *******************************************

##### ************************ SETUP ******************************************
# w3 = get_web3_object("FANTOM_RPC_URL")


# marketplace_abi = get_contract_abi("../contracts/out/Marketplace.sol/Marketplace.json")
# escrow_abi = get_contract_abi("../contracts/out/Escrow.sol/Escrow.json")

# marketplace_address = get_contract_address("Marketplace", "Fantom testnet")
# marketplace_contract = w3.eth.contract(address=marketplace_address, abi=marketplace_abi)

# escrow_address = get_contract_address("Escrow", "Fantom testnet")
# escrow_contract = w3.eth.contract(address=escrow_address, abi=escrow_abi)

# # ***************************************************************************************************

# transaction_hash = "0x60b5bc6f5b53e106367d986f5b451b7440b1215d29cf9e8e8ab33156e0aeb33f"
# event_name = "userRegistered"
# event_data = fetch_event_from_transaction(
#     w3, marketplace_contract, transaction_hash, event_name
# )
# print(event_data)

# transaction_hash = "0xbebca6bdfcf1d2fd115fb172e337641e3346f1a4fb3015ac2a519dd6ec438943"
# event_name = "TokenBought"
# event_data = fetch_event_from_transaction(
#     w3, marketplace_contract, transaction_hash, event_name
# )
# print(event_data)

transaction_hash = "0xee9503b2aaf8a8ab55abdc7dc363cb5e83e65766716a50613283e9956e8a2346"
event_name = "ItemListed"
event_data = fetch_event("Marketplace", "4002", transaction_hash, event_name)
print(event_data)

# transaction_hash = "0x2bc1a720b893883ce0a66eca8066f2dd51e2aab5000659a9604d6da9f09496bf"
# event_name = "ItemUpdated"
# event_data = fetch_event_from_transaction(
#     w3, marketplace_contract, transaction_hash, event_name
# )
# print(event_data)

# transaction_hash = "0x772785c5528a44a2065f0f5aa5be7a03fd1ca69d175536251a03e4741d60e09c"
# event_name = "ItemCanceled"
# event_data = fetch_event_from_transaction(
#     w3, marketplace_contract, transaction_hash, event_name
# )
# print(event_data)

# transaction_hash = "0xb51cb4d02dd2d44ae3f49b492b46ab7fd99d5a074f7fe27fe812bcd01380478b"
# event_name = "OrderSent"
# event_data = fetch_event_from_transaction(
#     w3, escrow_contract, transaction_hash, event_name
# )
# print(event_data)

# transaction_hash = "0x603ca4a15b7403a3ef3bc943ecb86091bdd04b66e9cf646767737c4f3595de97"
# event_name = "FundsRefunded"
# event_data = fetch_event_from_transaction(
#     w3, escrow_contract, transaction_hash, event_name
# )
# print(event_data)

# transaction_hash = "0x731879b0b5fd1b69a6770c2c144409daf589a31c8fc8075161ea9255d1522dab"
# event_name = "FundsReleased"
# event_data = fetch_event_from_transaction(
#     w3, escrow_contract, transaction_hash, event_name
# )
# print(event_data)
