from config import NUTRIX_APP_ID, NUTRIX_API_KEY, SHEETY_USERNAME, SHEETY_AUTH_HEADER, SHEETY_SPREADSHEET
import requests
from datetime import datetime
import os
import json

# this is the natural language processing api
nutrix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
nutrix_header = {
    "x-app-id": NUTRIX_APP_ID,
    "x-app-key": NUTRIX_API_KEY
}

# this is the api which posts to google sheets
sheety_endpoint = f"https://api.sheety.co/{SHEETY_USERNAME}/MyWorkouts/workouts"
sheety_header = {
    "Content-Type": "application/json",
    "Authorization": SHEETY_AUTH_HEADER
}


# takes user input and processes it using NLP
def process_language(workout):

    post_body = {
        "query": workout
    }

    post_workout_response = requests.post(url=nutrix_endpoint, headers=nutrix_header, json=post_body)
    return post_workout_response.json()


def generate_payload(json_data):
    if len(json_data['exercises']) >= 1:
        exercise = json_data["exercises"][0]["user_input"]
        duration = json_data["exercises"][0]["duration_min"]
        calories = json_data["exercises"][0]["nf_calories"]

        dt = datetime.now()
        time_now = dt.now().strftime("%-I:%M %p")
        today_date = dt.date().strftime("%b %d, %Y")

        payload = {
            "workout": {
                "date": today_date,
                "time": time_now,
                "exercise": exercise,
                "duration": duration,
                "calories": calories
            }
        }

        return payload
    else:
        return False


def add_row(workout_event):
    add_row_endpoint = f"https://api.sheety.co/{SHEETY_SPREADSHEET}/myWorkouts/workouts"
    add_row_response = requests.post(url=add_row_endpoint, json=workout_event, headers=sheety_header)
    return add_row_response


# ----------MAIN-------------

workout_description = input("What was your activity and duration? (in minutes or hours): ")

json_workout = process_language(workout_description)

# If there's a problem with user input, return an error
if generate_payload(json_workout):
    json_payload = generate_payload(json_workout)
    add_row_reply = add_row(json_payload)
    print("\nSuccess. The following workout was added:\n")
    print(add_row_reply.text)
else:
    print("An error occurred. Workout not added")






