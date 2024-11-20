from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

# Predefined users with no home times initially
users_home_times = {
    "Mark": {"original": None, "delay": timedelta(0)},
    "Josina": {"original": None, "delay": timedelta(0)},
    "Daniël": {"original": None, "delay": timedelta(0)},
    "Matteo": {"original": None, "delay": timedelta(0)},
    "Nadia": {"original": None, "delay": timedelta(0)},
}

@app.route('/')
def index():
    # Define the starting reference time (6:00 AM)
    start_of_day = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)

    # Filter out users with no original time and sort by adjusted time
    sorted_home_times = sorted(
        ((user, times) for user, times in users_home_times.items() if times["original"]),
        key=lambda item: (
            (item[1]["original"] - start_of_day).total_seconds() % (24 * 3600)  # Wrap-around logic
        )
    )

    # Format the sorted home times for display
    formatted_home_times = {}
    for user, times in sorted_home_times:
        original_time = times["original"].strftime('%H:%M')
        
        # Format delay based on its length
        if times["delay"].total_seconds() > 0:
            delay_minutes = int(times["delay"].total_seconds() / 60)
            if delay_minutes > 120:
                # Convert delay into hours and minutes if over 120 minutes
                hours = delay_minutes // 60
                minutes = delay_minutes % 60
                formatted_home_times[user] = f"{original_time} + {hours}u{minutes:02d}"
            else:
                formatted_home_times[user] = f"{original_time} +{delay_minutes}"
        else:
            formatted_home_times[user] = original_time

    return render_template('index.html', home_times=formatted_home_times)

@app.route('/updatetime', methods=['GET', 'POST'])
def updatetime():
    if request.method == 'POST':
        # Get the submitted data
        username = request.form['username']
        new_time_str = request.form['new_time']

        # Update the home time for the specified user
        if username in users_home_times:
            new_time = datetime.strptime(new_time_str, '%H:%M')
            original_time = users_home_times[username]["original"]

            if original_time:
                # If the new time is later, calculate the delay
                if new_time > original_time:
                    delay = new_time - original_time
                    print(delay)
                    users_home_times[username]["delay"] = delay
                if new_time < original_time:
                    if (original_time - new_time).total_seconds() > 42300:
                        new_time = new_time + timedelta(days=1)
                        delay = new_time - original_time
                        users_home_times[username]["delay"] = delay
                    else:
                        users_home_times[username]["original"] = new_time
                        users_home_times[username]["delay"] = timedelta(0)

            else:
                # If no original time, set it to the new time
                users_home_times[username]["original"] = new_time

            return redirect(url_for('index'))  # Redirect to the homepage after update
        else:
            return "User not found", 404

    return render_template('updatetime.html')

if __name__ == '__main__':
    app.run(debug=True)