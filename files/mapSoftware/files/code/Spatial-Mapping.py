# Initialize base map centered on Downtown Phoenix
phoenix_hub = [33.4484, -112.0740]
road_trip_map = folium.Map(location=phoenix_hub, zoom_start=9, tiles='CartoDB positron')

# Add Central Phoenix Marker
folium.Marker(
    location=phoenix_hub,
    popup='<b>Phoenix, USA</b><br>Central Hub',
    icon=folium.Icon(color='red', icon='star'),
).add_to(road_trip_map)

# Loop through destinations and add markers with connecting lines
for _, row in df_trips.iterrows():
  dest_coords = [row['Lat'], row['Lon']]

  # Add destination marker
  folium.Marker(
      location=dest_coords,
      popup=(
          f"<b>{row['Destination']}</b><br>Drive Time:"
          f" {row['Drive_Time_Mins']} mins<br>Highlights:"
          f" {row['Key_Highlights']}"
      ),
      tooltip=f"{row['Destination']} ({row['Drive_Time_Mins']}m)",
      icon=folium.Icon(color='blue', icon='map-marker'),
  ).add_to(road_trip_map)

  # Draw visual route line from Phoenix to destination
  folium.PolyLine(
      locations=[phoenix_hub, dest_coords],
      color='orange',
      weight=2.5,
      opacity=0.7,
  ).add_to(road_trip_map)

# Save output to interactive HTML file
road_trip_map.save('phoenix_road_trips_interactive.html')
