import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import defaultdict

# Path to the CSV file
csv_filename = 'where_you_exported_your_data.csv'

# Structure to hold the data by user
login_data_by_user = defaultdict(list)

# Reading the data from the CSV file
with open(csv_filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) < 4:  
            continue
        try:
            user = row[1]
            date = np.datetime64(row[0])
            login_count = int(row[2])
            login_data_by_user[user].append((date, login_count))
        except ValueError:
            continue  

# Plotting
plt.figure(figsize=(10, 6))

for user, data in login_data_by_user.items():
    dates, login_counts = zip(*data)  
    plt.bar(dates, login_counts, label=user)

plt.xlabel('Date')
plt.ylabel('Number of Logins')
plt.title('Login Activity Over Time')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()
