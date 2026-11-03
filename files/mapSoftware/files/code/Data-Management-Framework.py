import folium
import pandas as pd

# Define structured dataset for Phoenix Valley Road Trips
data = [
    {
        'ID': 1,
        'Destination': 'Tempe',
        'Drive_Time_Mins': 55,
        'Tier': 'Medium (45–60m)',
        'Key_Highlights': (
            'Arizona State Univ., Lakes & Trails, Dining & Nightlife'
        ),
        'Lat': 33.4255,
        'Lon': -111.9400,
    },
    {
        'ID': 2,
        'Destination': 'Gilbert',
        'Drive_Time_Mins': 45,
        'Tier': 'Medium (40–50m)',
        'Key_Highlights': (
            'Family-Friendly, Local Dining, Parks & Recreation'
        ),
        'Lat': 33.3528,
        'Lon': -111.7890,
    },
    {
        'ID': 3,
        'Destination': 'Chandler',
        'Drive_Time_Mins': 35,
        'Tier': 'Short (30–40m)',
        'Key_Highlights': (
            'Tech & Business Hub, Shopping & Dining, Parks & Recreation'
        ),
        'Lat': 33.3061,
        'Lon': -111.8413,
    },
    {
        'ID': 4,
        'Destination': 'Peoria',
        'Drive_Time_Mins': 45,
        'Tier': 'Medium (40–50m)',
        'Key_Highlights': (
            'Outdoor Recreation, Lakes & Hiking, Family Attractions'
        ),
        'Lat': 33.5806,
        'Lon': -112.2374,
    },
    {
        'ID': 5,
        'Destination': 'Goodyear',
        'Drive_Time_Mins': 35,
        'Tier': 'Short (30–40m)',
        'Key_Highlights': (
            'Small-Town Charm, Parks & Recreation, Local Dining & Shops'
        ),
        'Lat': 33.4353,
        'Lon': -112.3599,
    },
    {
        'ID': 6,
        'Destination': 'Glendale',
        'Drive_Time_Mins': 45,
        'Tier': 'Medium (40–50m)',
        'Key_Highlights': (
            'Sports & Events, Shopping & Dining, Entertainment District'
        ),
        'Lat': 33.5387,
        'Lon': -112.1860,
    },
    {
        'ID': 7,
        'Destination': 'Mesa',
        'Drive_Time_Mins': 50,
        'Tier': 'Medium (45–55m)',
        'Key_Highlights': (
            'Museums & Culture, Shopping & Dining, Family Attractions'
        ),
        'Lat': 33.4152,
        'Lon': -111.8315,
    },
    {
        'ID': 8,
        'Destination': 'Scottsdale',
        'Drive_Time_Mins': 75,
        'Tier': 'Extended (1h 15m)',
        'Key_Highlights': (
            'Upscale Shopping, Art, Culture & Dining, Desert Parks & Resorts'
        ),
        'Lat': 33.4942,
        'Lon': -111.9261,
    },
    {
        'ID': 9,
        'Destination': 'Sedona',
        'Drive_Time_Mins': 90,
        'Tier': 'Day Trip (1h 30m)',
        'Key_Highlights': (
            'Red Rock Views, Hiking & Trails, Scenic Drives, Vortex Sites'
        ),
        'Lat': 34.8697,
        'Lon': -111.7610,
    },
    {
        'ID': 10,
        'Destination': 'Flagstaff',
        'Drive_Time_Mins': 165,
        'Tier': 'Long Trip (2h 45m)',
        'Key_Highlights': (
            'Cooler Weather, Pine Forests, Outdoor Adventure, Historic'
            ' Downtown'
        ),
        'Lat': 35.1983,
        'Lon': -111.6513,
    },
]

df_trips = pd.DataFrame(data)
