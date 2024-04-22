import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pyautogui
import csv
from datetime import datetime
from datetime import datetime, timedelta

data_folder = "./dataFolder"
users = []
firstNames = []
lastNames = []

# fill user information
with open(f'{data_folder}/users.txt', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        users.append(row[0])
        firstNames.append(row[1])
        lastNames.append(row[2])

# fill time slots
with open(f'{data_folder}/times.txt', 'r') as file:
    times = [line.strip() for line in file.readlines()]

roomName = 'Anschutz 203L'

if (roomName == 'Anschutz 203L'):
    url = "https://calendar.lib.ku.edu/space/147403"

elif (roomName == 'Anschutz 203K'):
    url = "https://calendar.lib.ku.edu/space/147402"

browser = webdriver.Chrome()


browser.get(url)

pyautogui.click(x=780, y=465)
pageSource = browser.page_source

today = datetime.today()

days_until_next_tuesday = (1 - today.weekday()) % 7  # Calculate the number of days until next Tuesday
next_tuesday = today + timedelta(days=days_until_next_tuesday)
next_tuesday_formatted = next_tuesday.strftime("%B %-d, %Y")

days_until_next_thursday = (3 - today.weekday()) % 7  # Calculate the number of days until next Thursday
next_thursday = today + timedelta(days=days_until_next_thursday)
next_thursday_formatted = next_thursday.strftime("%B %-d, %Y")


mapped_data = zip(times, users, firstNames, lastNames)
for data in mapped_data:
    print(data)



time.sleep(2)

current_date = datetime.now()
day_of_week = current_date.weekday()
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_day = days_of_week[day_of_week]

clickOnNextWeek = False


for i in range(len(times)):
    print(f'================== iteration {i} =====================')
    if (i < 5):
        element_attributes = {
            "class": "fc-timegrid-event fc-v-event fc-timegrid-event-short fc-event fc-event-start fc-event-end fc-event-future s-lc-eq-avail",
            "title": f"{times[i]} Tuesday, {next_tuesday_formatted} - {roomName} - Available",
            "aria-label": f"{times[i]} Tuesday, {next_tuesday_formatted} - {roomName} - Available"
        }

        unavailable_element_attributes = {
            "class": "fc-timegrid-event fc-v-event fc-timegrid-event-short fc-event fc-event-start fc-event-end fc-event-future s-lc-eq-checkout s-lc-eq-checkout",
            "title": f"{times[i]} Tuesday, {next_tuesday_formatted} - {roomName} - Unavailable/Padding",
            "aria-label": f"{times[i]} Tuesday, {next_tuesday_formatted} - {roomName} - Unavailable/Padding"
        }
        day = f'{next_tuesday_formatted} - Tuesday'
        

    
    else:
        element_attributes = {
            "class": "fc-timegrid-event fc-v-event fc-timegrid-event-short fc-event fc-event-start fc-event-end fc-event-future s-lc-eq-avail",
            "title": f"{times[i]} Thursday, {next_thursday_formatted} - {roomName} - Available",
            "aria-label": f"{times[i]} Thursday, {next_thursday_formatted} - {roomName} - Available"
        }

        unavailable_element_attributes = {
            "class": "fc-timegrid-event fc-v-event fc-timegrid-event-short fc-event fc-event-start fc-event-end fc-event-future s-lc-eq-checkout s-lc-eq-checkout",
            "title": f"{times[i]} Thursday, {next_thursday_formatted} - {roomName} - Unavailable/Padding",
            "aria-label": f"{times[i]} Thursday, {next_thursday_formatted} - {roomName} - Unavailable/Padding"
        }
        
        day = f'{next_thursday_formatted} - Thursday'

    try:
        
        element = browser.find_element(
            By.CSS_SELECTOR,
            f'a[class="{element_attributes["class"]}"][title="{element_attributes["title"]}"][aria-label="{element_attributes["aria-label"]}"]'
        )

        
        element.click()
        print(f"Booking for: {times[i]}, {day} - {roomName}")
        print(f"Using {firstNames[i]} {lastNames[i]}'s username: {users[i]}")


    except NoSuchElementException:
        try:
            element = browser.find_element(
                By.CSS_SELECTOR,
                f'a[class="{unavailable_element_attributes["class"]}"][title="{unavailable_element_attributes["title"]}"][aria-label="{unavailable_element_attributes["aria-label"]}"]'
            )
            print(f"WARNING: The time slot ({times[i]})")
            print(f'        on ({day})') 
            print(f'        at {roomName}) is not available')

        except NoSuchElementException:
            print("WARNING: Element does not exist anywhere")
        
        print('Exiting program...')
        time.sleep(5)
        exit()



    time.sleep(3)
    # clicks on submit times
    pyautogui.click(x=500, y=685)

    time.sleep(2)
    # clicks on continue
    pyautogui.click(x=150, y=885)

    time.sleep(2)
    # clicks on first name
    pyautogui.click(x=430, y=230)
    # writes first name
    pyautogui.write(firstNames[i], interval = 0.1)

    # clicks on last name
    pyautogui.click(x=600, y=230)
    # writes last name
    pyautogui.write(lastNames[i], interval=0.1)

    # clicks on email
    pyautogui.click(x=630, y=270)
    # writes email
    pyautogui.write(users[i], interval=0.1)

    # submits booking
    pyautogui.press('enter')

    time.sleep(2)
    pyautogui.click(x=200, y=300)
    time.sleep(2)
    pyautogui.click(x=780, y=465)
    time.sleep(3)

    if (clickOnNextWeek):
        pyautogui.click(x=255,y=465)


import subprocess

command = 'pkill Discord'
time.sleep(2)

try:
    subprocess.run(command, shell=True)
    print('Discord process terminated')

except subprocess.CalledProcessError as e:
    print(f'Error: {e}')


discord_executable_path = "/usr/bin/discord"

try:
    subprocess.Popen([discord_executable_path])
    print("Discord is opening...")
except Exception as e:
    print(f"Error: {e}")

time.sleep(10)

pyautogui.hotkey('ctrl', 'k')
channelName = '#active-house'
pyautogui.write(channelName)
pyautogui.press('enter')
text1 = '@Active Study Room Bookings:'
text2 = f'{next_tuesday_formatted} (Tuesday): {roomName} from {times[0]} - 8:00pm'
text3 = f'{next_thursday_formatted} (Thursday): {roomName} from {times[0]} - 8:00pm'
pyautogui.write(text1)
pyautogui.hotkey('shift', 'enter')
pyautogui.write(text2)
pyautogui.hotkey('shift', 'enter')
pyautogui.write(text3)
pyautogui.press('enter')





time.sleep(4000) 
