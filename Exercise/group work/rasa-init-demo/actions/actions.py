from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import sqlite3

# city_db = {'brussels': 'Europe/Brussels',
#            'zagreb' : 'Europe/Zagreb',
#            'london' : 'Europe/Dublin',
#            'lisbon' : 'Europe/Lisbon',
#            'amsterdam' : 'Europe/Amsterdam',
#            'seattle' : 'US/Pacific' ,
#           }
 
# date_db ={
#     'today' : arrow.now(),
#     'tomorrow' : arrow.now().shift(days=1),
# }

# class Actiontelltime(Action):
#     def name(self) -> Text:
#         return "action_tell_time"
    
#     def run(
#             self, 
#             dispatcher:CollectingDispatcher,
#             tracker:Tracker,
#             domain:dict[Text, Any]) -> List[dict[Text, Any]]:
#         current_place = tracker.get_slot("place")
#         utc = arrow.utcnow()

#         if not current_place:
#             msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place"
#             dispatcher.utter_message(text=msg)
#             return[]
        
#         tz_string = city_db.get(current_place,None)
#         if not tz_string:
#             msg = f"It's I didn't recognize {current_place}.Is it spelled correctly?"
#             dispatcher.utter_message(text=msg)
#             return[]
        
#         msg = f"It's {utc.to(city_db[current_place] ).format('HH: mm') } in {current_place} now."
#         dispatcher.utter_message(text=msg)
#         return[]


class ValidateSimpleCityForm(FormValidationAction):
    def name(self) -> Text:
        return"validate_simple_city_form"
    
    def validate_from_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate from_city value"""
        
        from_city = False
        from_city = tracker.get_slot("from_city")
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT from_city from flight WHERE from_city= "{from_city}"''')        
        values = cursor.fetchall()
        
        if from_city not in values:
            dispatcher.utter_message(text=f"we only accept the ticket we support for.")
            return{"from_city": None}
        dispatcher.utter_message(text=f"You want to have a ticket set off from{from_city}.")
        print(from_city)
        return {"from_city": from_city}
    
    def validate_to_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate to_city value"""
        
        to_city = False
        to_city = tracker.get_slot("to_city")
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT to_city from flight WHERE to_city= "{to_city}"''')        
        values = cursor.fetchall()



        to_city = tracker.get_slot("to_city")
        if to_city not in values:
            dispatcher.utter_message(text=f"we only accept the ticket we support for.")
            return{"to_city": None}
        dispatcher.utter_message(text=f"You want to have a ticket set off from{to_city}.")
        return {"to_city": to_city}
    

    def validate_departure_date(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    )  -> Dict[Text, Any]:
        """Validate departure_date value"""

        departure_date = False
        departure_date = tracker.get_slot("departure_date")
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT departure_date from flight WHERE departure_date= "{departure_date}"''')        
        values = cursor.fetchall()

        departure_date = tracker.get_slot("departure_date")
        if slot_value not in values:
            dispatcher.utter_message(text=f"we only accept the date we have.")
            return{"department_date": None}
        dispatcher.utter_message(text=f"You want to set off ({departure_date}).")
        return{"departure_date": departure_date}
    


    