# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from re import template
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

details = {
    'saurav': '+91 9829292929',
    'raju' : '+91 9500000012'
}

class Action_get_num(Action):
    def name(self)-> Text:
        return "action_your_num"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # dispatcher.utter_message(text="Hello World!")
        print(tracker.get_slot('num'))
        # dispatcher.utter_template('utter_your_num', tracker, number=details[str(tracker.get_slot('NAME')).lower()])
        return []
    
class ActionFormInfo(FormAction):

    def name(self) -> Text:
        return "form_info"

    @staticmethod
    def required_slots(tracker: Tracker)-> List[Text]:
        '''A list of req slots that the form has to fill'''
        return ["NAME","BRAND"]
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text,Any]
    ) -> List[Dict]:
        '''Define what the form has 
        to do after all slots are filled'''
        #utter submit template
        dispatcher.utter_message(template="utter_submit", name=tracker.get_slot('NAME'),
                                    handset=tracker.get_slot('BRAND'))
        return []
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        '''
        a dict to map req slots to 
        -  an extracted entity
        - intent: value-pairs
        a whole message
        or a list of them where a first match will be picked
        '''
        return {
            "name": self.from_entity(entity="NAME", intent="my_name_is"),
            "headset": self.from_entity(entity='BRAND', intent='headset')
        }
    @staticmethod
    def brand_db() -> List[Text]:
        """Database of supported cuisines"""

        return [
            "samsung",
            "One plus",
            "I-phone",
        ]
    def validate_brand(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        print(value)
        if value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"BRAND": value}
        else:
            print(value)
            dispatcher.utter_message(template="utter_wrong_value")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"BRAND": None}

    # def run(self, dispatcher: CollectingDispatcher,
    #         tracker: Tracker,
    #         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    #     dispatcher.utter_message(text="Hello World!")

    #     return []
