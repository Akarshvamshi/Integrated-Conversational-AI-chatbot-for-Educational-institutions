import json
import logging
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pathlib import Path
from sanic import Sanic
from sanic.response import file

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Sanic("RasaApp")


@app.route("/favicon.ico")
async def favicon(request):
    return await file("static/images/favicon.ico")


class ActionCourseThing(Action):
    def name(self) -> Text:
        return "action_course_thing"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the value of the slot 'course_slot'
        course_slot = tracker.get_slot('course_slot')

        # If the course_slot is not filled, ask the user to specify the course
        if not course_slot:
            dispatcher.utter_message(text='Which course would you like to know about? Please specify the course name.')
            return []

        # Proceed if the course_slot is filled
        data_file = Path("data/course_detals.json")

        try:
            # Load the JSON data
            with data_file.open() as f:
                course_details = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(text="The data file is missing.")
            return []
        except json.JSONDecodeError:
            dispatcher.utter_message(text="The data file is not a valid JSON.")
            return []

        course_key = course_slot.lower()
        if course_key in course_details:

            details = course_details[course_key]
            response = ("Yes! We offer the course, here are the details:\n"
                        f"Details about the {course_slot.upper()} course:\n"
                        f"Duration: {details['duration']}\n"
                        f"Description: {details['description']}")
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I don't have details for the selected course.")

        return []


class ActionCourseFeeDetails(Action):
    def name(self) -> Text:
        return "action_course_fee_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the course name from the slot
        course_slot = tracker.get_slot('course_slot')

        # If the course_slot is not filled, ask the user to specify the course
        if not course_slot:
            dispatcher.utter_message(
                text='Which course fee details would you like to know about? Please specify the course name.')
            return []

        data_file1 = Path("data/Fee_details.json")

        try:

            with data_file1.open() as file:
                fee_details = json.load(file)
        except FileNotFoundError:
            dispatcher.utter_message(text="The data file is missing.")
            return []
        except json.JSONDecodeError:
            dispatcher.utter_message(text="The data file is not a valid JSON.")
            return []

        fee_details_lower = {key.lower(): value for key, value in fee_details.items()}

        course_key = course_slot.lower()  # Convert course name to lowercase

        if course_key in fee_details_lower:
            course_fee_detail = fee_details_lower[course_key]
            response = (
                f"The {course_slot} course details are as follows:\n"
                f"Duration: {course_fee_detail['duration']}\n"
                f"Description: {course_fee_detail['description']}\n"
                f"Fees: {course_fee_detail['fees']}"
            )
        else:
            response = "Sorry, I don't have the fee details for the requested course."

        dispatcher.utter_message(text=response)
        return []


class ActionHodDetails(Action):
    def name(self) -> Text:
        return "action_hod_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hod_slot = tracker.get_slot('hod_slot')

        if not hod_slot:
            dispatcher.utter_message(
                text='Which course head details would you like to know about? Please specify the course name.')
            return []

        data_file1 = Path("data/faculty_details.json")

        try:
            # Load the JSON data
            with data_file1.open() as file4:
                hod_details = json.load(file4)
        except FileNotFoundError:
            dispatcher.utter_message(text="The data file is missing.")
            return []
        except json.JSONDecodeError:
            dispatcher.utter_message(text="The data file is not a valid JSON.")
            return []

        hod_key = hod_slot.lower()  # Convert course name to lowercase

        if hod_key in hod_details:
            hod_course_detail = hod_details[hod_key]
            response = (
                f"The hod of the department {hod_slot}:\n"
                f" {hod_course_detail['Name']}\n"
            )
        else:
            response = "Sorry, I don't have the head details for the requested course."

        dispatcher.utter_message(text=response)
        return []
