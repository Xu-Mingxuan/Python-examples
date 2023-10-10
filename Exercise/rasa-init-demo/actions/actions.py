from typing import Any, Text, Dict, List

import arrow
import dateparser
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import sqlite3



city_db = {'brussels': 'Europe/Brussels',
           'zagreb' : 'Europe/Zagreb',
           'london' : 'Europe/Dublin',
           'lisbon' : 'Europe/Lisbon',
           'amsterdam' : 'Europe/Amsterdam',
           'seattle' : 'US/Pacific' ,
           'beijing': 'Asia/Shanghai'
          }
 



class Actiontelltime(Action):
    def name(self) -> Text:
        return "action_tell_time"
    
    def run(
            self, 
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:dict[Text, Any]) -> List[dict[Text, Any]]:
        current_place = tracker.get_slot("place")
        utc = arrow.utcnow()

        if not current_place:
            msg = f"It's {utc.format('HH:mm')} utc now. You can also give me a place(brussels, zagreb, london, lisbon, amsterdam, seattle, beijing)"
            dispatcher.utter_message(text=msg)
            return[]
        
        tz_string = city_db.get(current_place,None)
        if not tz_string:
            msg = f"It's I didn't recognize {current_place}.Is it spelled correctly?"
            dispatcher.utter_message(text=msg)
            return[]
        
        msg = f"It's {utc.to(city_db[current_place]).format('HH: mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)
        return[]
    

class Actioninquiremessage(Action):
    def name(self) -> Text:
        return "action_inquire_message"
    
    def run(
            self, 
            dispatcher:CollectingDispatcher,
            tracker:Tracker,
            domain:dict[Text, Any]) -> List[dict[Text, Any]]:
        

        name = tracker.get_slot("name")
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM flighttwo WHERE name= ?', (name,))
        values = cursor.fetchall()
        if values:
            for row in values:
                name_value = row[0]
                from_city_value = row[1]
                to_city_value = row[2]
                depature_date_value = row[3]

                dispatcher.utter_message(f"Name: {name_value}")
                dispatcher.utter_message(f"From_city: {from_city_value}")
                dispatcher.utter_message(f"To_city: {to_city_value}")
                dispatcher.utter_message(f"depature_date: {depature_date_value}")

        else:
              dispatcher.utter_message("No results found.(Maybe you can give me a name.)")

        return []



class Actionentermessage(Action):
    def name(self) -> Text:
        return "action_enter_message"
    
    def run(
        self, 
        dispatcher:CollectingDispatcher,
        tracker:Tracker,
        domain:dict[Text, Any]) -> List[dict[Text, Any]]:
    
        slot1_value = tracker.get_slot("name")
        slot2_value = tracker.get_slot("from_city")
        slot3_value = tracker.get_slot("to_city")
        slot4_value = tracker.get_slot("departure_date")

        dispatcher.utter_message(response="utter_confirm_booking",from_city = slot2_value, to_city = slot3_value, departure_date = slot4_value)



        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO flighttwo (name, from_city, to_city, department_date) VALUES (?, ?, ?, ?)', (slot1_value, slot2_value, slot3_value, slot4_value))
        
        conn.commit()
        conn.close()

        return []

class Actiondeletticket(Action):
    def name(self) -> Text:
        return "action_delet_ticket"

    def run(
        self, 
        dispatcher:CollectingDispatcher,
        tracker:Tracker,
        domain:dict[Text, Any]) -> List[dict[Text, Any]]:


        slot_value = tracker.get_slot("name")
        if slot_value:
            conn = sqlite3.connect('flight.db')
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM flighttwo WHERE name =?", (slot_value,))
            conn.commit()
            conn.close()
            dispatcher.utter_message("Ticket canceled successfully.")
        else:
            dispatcher.utter_message("No message value found.(Maybe you can give me a name.)")
        
        return []





class ValidateSimpleCityForm(FormValidationAction):
    def name(self) -> Text:
        return"validate_simple_city_form"
    

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value"""

        name = tracker.get_slot("name")
        return {"name": name}


    def validate_from_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate from_city value"""
        
        from_city = tracker.get_slot("from_city")
        from_city_text = str(from_city)
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute("SELECT from_city FROM flight WHERE from_city= ?", (from_city,))
        values = cursor.fetchall()
        if values:
          values = values[0]
          if from_city_text not in values:
            dispatcher.utter_message(text="We only accept the tickets we support.")
            return {"from_city": None}
          dispatcher.utter_message(text=f"You want to have a ticket set off from {from_city}.")

          return {"from_city": from_city}
        else:
          dispatcher.utter_message(text="No flights available.")
          return {"from_city": None}
    
    
    def validate_to_city(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate to_city value"""
        
        to_city = tracker.get_slot("to_city")
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT to_city from flight WHERE to_city= "{to_city}"''')        
        values = cursor.fetchall()
        if values:
          values = values[0]
          if to_city not in values:
            dispatcher.utter_message(text="We only accept the tickets we support.")
            return {"to_city": None}
          dispatcher.utter_message(text=f"You want to have a ticket go to {to_city}.")
          return {"to_city": to_city}
        else:
          dispatcher.utter_message(text="No flights available.")
          return {"to_city": None}
    

    def validate_departure_date(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    )  -> Dict[Text, Any]:
        """Validate departure_date value"""

        departure_date = tracker.get_slot("departure_date")
        conn = sqlite3.connect('flight.db')
        cursor = conn.cursor()
        cursor.execute(f'''SELECT departure_date from flight WHERE departure_date= "{departure_date}"''')        
        values = cursor.fetchall()

        if values:
          values = values[0]
          if departure_date not in values:
            dispatcher.utter_message(text="We only accept the dates we have.")
            return {"departure_date": None}
          dispatcher.utter_message(text=f"You want to set off on {departure_date}.")

          return {"departure_date": departure_date}
        else:
          dispatcher.utter_message(text="No flights available on the specified date.")
          return {"departure_date": None}
    


