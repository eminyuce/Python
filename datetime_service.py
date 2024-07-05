from datetime import datetime

# Get the current date and time
now = datetime.now()

# Format the datetime object to a string
formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

print("Formatted date and time:", formatted_date)

# Example of different formatting options
formatted_date1 = now.strftime("%A, %B %d, %Y")
formatted_date2 = now.strftime("%I:%M %p")
formatted_date3 = now.strftime("%d/%m/%Y")

print("Formatted date 1:", formatted_date1)
print("Formatted date 2:", formatted_date2)
print("Formatted date 3:", formatted_date3)