const sessions = [];
const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

// Generate sessions for each day
for (let i = 0; i < days.length; i++) {
  const day = days[i];

  // Generate sessions for each hour of the day (8am to 4pm)
  for (let j = 8; j < 16; j++) {
    // Generate sessions for each minute of the hour
    for (let k = 0; k < 60; k++) {
      const time = `${j}:${k < 10 ? '0' : ''}${k}`;
      const session = {
        session_id: sessions.length + 1,
        day,
        time,
        room: null,
        instructor: null,
        group: null,
      };
      sessions.push(session);
    }
  }
}

console.log(sessions);
