import json

# Define the schedule parameters
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
start_time = "08:00"
end_time = "16:00"
hours_per_day = 8
hours_per_session = 1

# Calculate the number of sessions
num_days = len(days)
num_hours = hours_per_day * num_days
num_sessions = num_hours // hours_per_session

# Generate the sessions
sessions = []
for i in range(num_sessions):
    # Calculate the session's time, day, and room
    hour = int(start_time[:2]) + i
    minute = int(start_time[3:])
    if hour >= 24:
        hour -= 24
    time = f"{hour:02d}:{minute:02d}"
    day = days[i // hours_per_day]
    room = i + 1
    
    # Create the session dictionary
    session = {
        "session_id": i + 1,
        "day": day,
        "time": time,
        "room": room,
        "instructor": None,
        "group": None
    }
    sessions.append(session)

# Save the sessions to a JSON file
with open("sessions.json", "w") as f:
    json.dump(sessions, f)
