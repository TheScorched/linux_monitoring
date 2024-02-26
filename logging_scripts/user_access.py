import csv
from datetime import datetime, timedelta
import subprocess
import re

def parse_login_time(line):
    match = re.search(r'(\w{3})\s+(\d+)\s+(\d+):(\d+)', line)
    if not match:
        return None

    month, day, hour, minute = match.groups()
    year = datetime.now().year
    return datetime(year, datetime.strptime(month, '%b').month, int(day), int(hour), int(minute))

def append_to_csv(filename, login_date, username, login_count, currently_logged_in_duration):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([login_date, username, login_count, currently_logged_in_duration])

def get_login_summary(username, csv_filename):
    try:
        result = subprocess.run(['last', '-w'], check=True, stdout=subprocess.PIPE, text=True)
        logins = result.stdout.split('\n')

        login_count_last_24_hours = 0
        currently_logged_in_since = None
        now = datetime.now()

        for login in logins:
            if username in login:
                login_time = parse_login_time(login)
                if login_time:
                    if 'still logged in' in login:
                        currently_logged_in_since = now - login_time
                    elif login_time > now - timedelta(days=1):
                        login_count_last_24_hours += 1

        if currently_logged_in_since:
            hours_logged_in = currently_logged_in_since.seconds // 3600
            minutes_logged_in = (currently_logged_in_since.seconds % 3600) // 60
            currently_logged_in_duration = f'{hours_logged_in} hours and {minutes_logged_in} minutes'
        else:
            currently_logged_in_duration = 'Not currently logged in'

        login_date = datetime.now().strftime('%Y-%m-%d')
        append_to_csv(csv_filename, login_date, username, login_count_last_24_hours, currently_logged_in_duration)

        print(f'{username} logged in {login_count_last_24_hours} times in the past 24 hours.')
        if currently_logged_in_since:
            print(f'{username} session time is {hours_logged_in} hours and {minutes_logged_in} minutes.')
        else:
            print(f'{username} is not currently logged in.')

    except subprocess.CalledProcessError as e:
        print(f"Error executing last command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    csv_filename = 'replace_with_your_desired_destination'
    get_login_summary('aaron', csv_filename)
