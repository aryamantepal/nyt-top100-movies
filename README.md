# Movie Night Calendar Generator 🎬

Automatically create Google Calendar events for monthly movie nights featuring films from the New York Times Top 100 Films of the 21st Century list. Perfect for organizing regular movie screenings with friends!

## Features

- 📅 Creates calendar events on the first Sunday of each month
- 🎭 Uses curated film list from NYT's Top 100 Films of the 21st Century
- 📧 Automatically sends invitations to specified email addresses
- ⏰ Sets 3-hour time blocks (7 PM - 10 PM) with customizable reminders
- 🔔 Includes email (24 hours) and popup (1 hour) reminders
- 🎯 Handles authentication and rate limiting automatically

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/movie-night-calendar.git
cd movie-night-calendar
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dateutil python-dotenv
```

### 3. Set Up Google Calendar API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API:
   - Navigate to **APIs & Services** > **Library**
   - Search for "Google Calendar API" and enable it
4. Create OAuth 2.0 credentials:
   - Go to **APIs & Services** > **Credentials**
   - Click **Create Credentials** > **OAuth 2.0 Client IDs**
   - Choose **Desktop application**
   - Download the JSON file and save it as `credentials.json` in your project folder

### 4. Configure OAuth Consent Screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Add test users (the email addresses you want to invite):
   - Scroll to **Test users** section
   - Click **Add users** and add all participant email addresses
   - This allows the app to send calendar invites while in testing mode

### 5. Set Up Environment Variables

Create a `.env` file in your project root:

```env
EMAIL_1=your.email@gmail.com
EMAIL_2=friend@gmail.com
# Add more emails as needed (you'll need to modify the script)
```

### 6. Run the Script

```bash
python movie_calendar.py
```

On first run, your browser will open for Google authentication. Grant calendar access to continue.

## Customization

### Adding More Participants

To invite more people, modify the email section in `movie_calendar.py`:

```python
email_addresses = [
    os.getenv('EMAIL_1'),
    os.getenv('EMAIL_2'),
    os.getenv('EMAIL_3'),  # Add more as needed
    os.getenv('EMAIL_4'),
]
```

And update your `.env` file accordingly.

### Changing the Movie List

Replace the `films` array with your own movie list:

```python
films = [
    "Your Movie 1",
    "Your Movie 2",
    # ... add up to 100 movies
]
```

### Adjusting Time and Date

Modify these settings in the `create_movie_night_event` function:

```python
# Change event time (currently 7 PM - 10 PM)
event_start = datetime.datetime.combine(date, datetime.time(19, 0))  # 7 PM
event_end = datetime.datetime.combine(date, datetime.time(22, 0))    # 10 PM

# Change timezone
'timeZone': 'America/New_York',  # Update to your timezone
```

To change from "first Sunday" to another day, modify `get_first_sunday_of_month()`:

```python
def get_first_friday_of_month(year, month):
    """Get the first Friday of a given month and year"""
    first_day = datetime.date(year, month, 1)
    days_ahead = 4 - first_day.weekday()  # Friday = 4
    if days_ahead <= 0:
        days_ahead += 7
    return first_day + datetime.timedelta(days_ahead)
```

### Changing Reminders

Modify the reminders in the event creation:

```python
'reminders': {
    'useDefault': False,
    'overrides': [
        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
        {'method': 'popup', 'minutes': 60},       # 1 hour before
        {'method': 'email', 'minutes': 7 * 24 * 60},  # 1 week before
    ],
},
```

## File Structure

```
movie-night-calendar/
├── movie_calendar.py       # Main script
├── credentials.json        # Google API credentials (you create this)
├── token.pickle           # Auto-generated auth token
├── .env                   # Your email configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Troubleshooting

### "Access blocked" Error
- Make sure you've added all participant emails as test users in Google Cloud Console
- Alternatively, publish your app (for broader access)

### Events Not Appearing
- Check you're looking at the right calendar (primary calendar)
- Events start from the current month and span multiple years
- Search for "Movie Night" in Google Calendar
- Use the direct event links from the script output

### Authentication Issues
- Delete `token.pickle` and re-run to re-authenticate
- Ensure `credentials.json` is in the correct location
- Verify Google Calendar API is enabled in Google Cloud Console

### Rate Limiting
The script includes automatic delays to prevent rate limiting, but if you encounter issues:
- Increase the delay in the main loop: `time.sleep(0.5)`
- Run the script during off-peak hours

## Requirements

- Python 3.6+
- Google account with Calendar access
- Google Cloud Project with Calendar API enabled

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Film list based on The New York Times' "The 25 Best Films of the 21st Century" and expanded with other critically acclaimed films
- Built using Google Calendar API
- Inspired by the need to actually watch all those movies in our watchlists!

---

**Pro Tip**: The script creates events for 50+ months, so your movie nights are scheduled well into the future! Perfect for maintaining consistency in your film viewing schedule. 🍿