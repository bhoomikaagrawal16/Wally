from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pymongo import MongoClient

# Establish MongoDB connection
client = MongoClient("mongodb+srv://agrawalbhoomika1611:EaoQYSqHi3KFdMaY@wally.jzmnf.mongodb.net/?retryWrites=true&w=majority&appName=wally")
db = client["walmart_db"]  # Your database name

orders_collection = db['orders']
products_collection = db['products']
stores_collection = db['stores']
users_collection = db['users']

class ActionFetchOrderStatus(Action):
    def name(self) -> Text:
        return "action_fetch_order_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        user_id = tracker.get_slot("user_id")
        order_data = orders_collection.find_one({"order_id": order_id, "user_id": user_id})
        
        if order_data:
            order_status = order_data.get("status", "unknown")
            delivery_date = order_data.get("delivery_date", "unknown")
            dispatcher.utter_message(text=f"Your order {order_id} is currently {order_status} and is expected to be delivered by {delivery_date}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find any details for your order.")
        
        return []

class ActionCancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        user_id = tracker.get_slot("user_id")
        result = orders_collection.update_one({"order_id": order_id, "user_id": user_id}, {"$set": {"status": "cancelled"}})
        
        if result.matched_count:
            dispatcher.utter_message(text=f"Your order {order_id} has been successfully cancelled.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't cancel the order. Please check the details and try again.")
        
        return []

class ActionReturnOrder(Action):
    def name(self) -> Text:
        return "action_return_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        user_id = tracker.get_slot("user_id")
        result = orders_collection.update_one({"order_id": order_id, "user_id": user_id}, {"$set": {"status": "return_initiated"}})
        
        if result.matched_count:
            dispatcher.utter_message(text=f"Return process for order {order_id} has been initiated.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't initiate the return process. Please check the details and try again.")
        
        return []

class ActionFetchProductAvailability(Action):
    def name(self) -> Text:
        return "action_fetch_product_availability"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_id = tracker.get_slot("product_id")
        product_data = products_collection.find_one({"product_id": product_id})
        
        if product_data:
            availability = product_data.get("availability", "unknown")
            dispatcher.utter_message(text=f"The product {product_id} is {availability}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find details about this product.")
        
        return []

class ActionFetchProductPrice(Action):
    def name(self) -> Text:
        return "action_fetch_product_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_id = tracker.get_slot("product_id")
        product_data = products_collection.find_one({"product_id": product_id})
        
        if product_data:
            price = product_data.get("price", "unknown")
            dispatcher.utter_message(text=f"The price for product {product_id} is {price}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the price for this product.")
        
        return []

class ActionFetchStoreLocation(Action):
    def name(self) -> Text:
        return "action_fetch_store_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        store_data = stores_collection.find_one({"store_id": "1"})
        
        if store_data:
            store_address = store_data.get("address", "unknown")
            dispatcher.utter_message(text=f"The nearest store is located at {store_address}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the store details.")
        
        return []

class ActionFetchStoreHours(Action):
    def name(self) -> Text:
        return "action_fetch_store_hours"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        store_data = stores_collection.find_one({"store_id": "1"})
        
        if store_data:
            store_hours = store_data.get("hours", "unknown")
            dispatcher.utter_message(text=f"The store hours for today are {store_hours}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the store hours.")
        
        return []

class ActionFetchRefundStatus(Action):
    def name(self) -> Text:
        return "action_fetch_refund_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("order_id")
        user_id = tracker.get_slot("user_id")
        order_data = orders_collection.find_one({"order_id": order_id, "user_id": user_id})
        
        if order_data:
            refund_status = order_data.get("refund_status", "unknown")
            dispatcher.utter_message(text=f"The refund for order {order_id} is currently {refund_status}.")
        else:
            dispatcher.utter_message(text="Sorry, I couldn't find the refund status for your order.")
        
        return []
