import datetime
from dateutil.relativedelta import relativedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# NYT Top 100 Films of the 21st Century (partial list - you'll need to complete this)
films = [
    "Parasite",
    "Mulholland Drive", 
    "There Will Be Blood",
    "In the Mood for Love",
    "Moonlight",
    "No Country for Old Men",
    "Eternal Sunshine of the Spotless Mind",
    "Get Out",
    "Spirited Away",
    "The Social Network",
    "Mad Max: Fury Road",
    "The Zone of Interest",
    "Children of Men",
    "Inglourious Basterds",
    "City of God",
    "Crouching Tiger, Hidden Dragon",
    "Brokeback Mountain",
    "Y Tu Mamá También",
    "Zodiac",
    "The Wolf of Wall Street",
    "The Royal Tenenbaums",
    "The Grand Budapest Hotel",
    "Boyhood",
    "Her",
    "Phantom Thread",
    # Add the remaining 75 films here...
    # You can find the complete list at: https://www.nytimes.com/interactive/2025/01/02/movies/best-movies-21st-century.html
    # Or extract them from the IMDB page you provided
]

# Email addresses to invite (loaded from environment variables)
email_addresses = [
    os.getenv('EMAIL_1'),
    os.getenv('EMAIL_2')
]

# Filter out None values in case environment variables aren't set
email_addresses = [email for email in email_addresses if email is not None]

# Validate that we have email addresses
if not email_addresses:
    print("Error: No email addresses found in environment variables.")
    print("Please set EMAIL_1 and EMAIL_2 environment variables.")
    exit(1)

def authenticate_google_calendar():
    """Authenticate with Google Calendar API"""
    creds = None
    
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return build('calendar', 'v3', credentials=creds)

def get_first_sunday_of_month(year, month):
    """Get the first Sunday of a given month and year"""
    first_day = datetime.date(year, month, 1)
    # Find the first Sunday (weekday 6)
    days_ahead = 6 - first_day.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return first_day + datetime.timedelta(days_ahead)

def create_movie_night_event(service, film_title, date, month_number):
    """Create a calendar event for movie night"""
    # Event details
    event_start = datetime.datetime.combine(date, datetime.time(19, 0))  # 7:00 PM
    event_end = datetime.datetime.combine(date, datetime.time(22, 0))    # 10:00 PM
    
    event = {
        'summary': f'Movie Night #{month_number}: {film_title}',
        'description': f'Monthly movie night featuring "{film_title}" from the New York Times Top 100 Films of the 21st Century list.\n\nRank: #{month_number}/100',
        'start': {
            'dateTime': event_start.isoformat(),
            'timeZone': 'America/New_York',  # Adjust timezone as needed
        },
        'end': {
            'dateTime': event_end.isoformat(),
            'timeZone': 'America/New_York',
        },
        'attendees': [{'email': email} for email in email_addresses],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                {'method': 'popup', 'minutes': 60},       # 1 hour before
            ],
        },
        'guestsCanInviteOthers': True,
        'guestsCanSeeOtherGuests': True,
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
        print(f'Event created: {event.get("htmlLink")}')
        return event
    except Exception as e:
        print(f'Error creating event for {film_title}: {e}')
        return None

def main():
    """Main function to create all movie night events"""
    print("Starting NYT Top 100 Films Calendar Creation...")
    
    # Check if we have enough films
    if len(films) < 100:
        print(f"Warning: Only {len(films)} films provided. Please add the remaining {100 - len(films)} films to the list.")
        proceed = input("Do you want to proceed with the available films? (y/n): ")
        if proceed.lower() != 'y':
            return
    
    # Authenticate with Google Calendar
    print("Authenticating with Google Calendar...")
    service = authenticate_google_calendar()
    
    # Get current date
    today = datetime.date.today()
    current_year = today.year
    current_month = today.month
    
    # Create events for the next 100 months (or available films)
    films_to_process = min(len(films), 100)
    
    for i in range(films_to_process):
        # Calculate the target month
        target_date = datetime.date(current_year, current_month, 1) + relativedelta(months=i)
        
        # Get the first Sunday of that month
        first_sunday = get_first_sunday_of_month(target_date.year, target_date.month)
        
        # Create the event
        film_title = films[i]
        month_number = i + 1
        
        print(f"Creating event {month_number}/100: {film_title} on {first_sunday}")
        
        event = create_movie_night_event(service, film_title, first_sunday, month_number)
        
        if event:
            print(f"✓ Successfully created event for '{film_title}' on {first_sunday}")
        else:
            print(f"✗ Failed to create event for '{film_title}'")
    
    print(f"\nCompleted! Created {films_to_process} movie night events.")

if __name__ == '__main__':
    main()