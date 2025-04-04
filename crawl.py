from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from datetime import datetime, timedelta
import time
import random
import requests
import json

profile_path = "/home/sudoppo/snap/firefox/common/.mozilla/firefox/ge47pdqr.sudoppo"
# Configure Firefox options for headless mode
firefox_options = Options()
firefox_options.add_argument("--headless")# Run in headless mode
firefox_options.add_argument(f"--profile {profile_path}")

# Set up the Firefox driver
service = Service('/usr/local/bin/geckodriver')  # Path to GeckoDriver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Flags
stop_program = False
is_lesson_occurring = False

time_chart = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
possible_top_values = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640]

current_day_lessons = []

# Já foi testada e está a funcionar
def crawl_page():
    try:
        driver.get("https://gisem.dei.estg.ipleiria.pt/horarios")

        if driver.title == "Login":
            print("Login credentials required!")
            print("Initianting login process...")
            login_process()

        else:
            print("Page loaded successfully")

            driver.get("https://gisem.dei.estg.ipleiria.pt/obterAulasMarcarPresenca")

            if driver.title == "Horários":
                print("Presença not opened yet")
            else:
                marcar_title = driver.find_element(By.CSS_SELECTOR, "h1")

                if marcar_title.text == "Marcar Presenças":
                    print("Presença opened")
                    marcar_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.col-xs-12")
                    button_id = marcar_button.get_attribute("id")

                    if button_id is not None:
                        marcar_button.click()
                        print(f"Presença marked for {marcar_button.text}")

                        try:
                            WebDriverWait(driver, 2).until(EC.alert_is_present())
                            alert = Alert(driver)

                            print(f"Alert text: {alert.text}")

                            alert.accept()
                            print("Alert accepted")
                            driver.quit()
                        except:
                            print("No alert found")
                    else:
                        print("Presença button does not have an id")

                else:
                    print("Didn't find the h1 title")



    except Exception as e:
        print(f"Error: {e}")

def login_process():
    try:
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        remember_input = driver.find_element(By.NAME, "remember")
        submit_input = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        username_input.send_keys("2231175")

        f = open("password.txt", "r")
        password = f.read()
        
        if password is not None:
                password_input.send_keys(password)
                remember_input.click()
                submit_input.click()

                if (driver.title == "Horários"):
                    print("Login process completed")
        else:
            print("Password not found")
            return
        
        f.close()
    except Exception as e: 
        print(f"Error: {e}")

def find_lecture():
    try:
        driver.get("https://gisem.dei.estg.ipleiria.pt/horariosAluno")

        # Format and display the week range
        week_number = datetime.now().isocalendar()[1]
        first_day_of_week = datetime.strptime(f'{datetime.now().year}-W{week_number - 1}-1', "%Y-W%U-%w")
        last_day_of_week = first_day_of_week + timedelta(days=4)
        formatted_last_date = last_day_of_week.strftime(f"%d/%m/%Y")
        formatted_first_date = first_day_of_week.strftime(f"%d/%m/%Y")

        current_week_gisem = f"S{week_number} ({formatted_first_date} - {formatted_last_date})"
        print(f"Current week: {current_week_gisem}")

        # Check every td with class="wc-day-column" and specific class day-x
        current_weekDay = f"day-{datetime.now().isoweekday()}"

        # Wait for the lessons divs to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "wc-cal-event"))
        )

        tds = driver.find_elements(By.CLASS_NAME, "wc-day-column")
        for td in tds:
            if current_weekDay in td.get_attribute("class"):
                td_divs = td.find_elements(By.CLASS_NAME, "wc-cal-event")
                print(f"Found {len(td_divs)} event divs")
                for td_div in td_divs:
                    top_value = td_div.value_of_css_property("top")
                    top_valueToInt = int(top_value.replace('px', ''))
                    
                    if top_valueToInt in possible_top_values:
                        lecture_title = lecture_name_finder(td_div)
                        timechart_search(top_valueToInt, td_div, lecture_title)
                            
            
        # x value is the day of the week (1-monday to 6-saturday)

        print(f"Crawl instance: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    except Exception as e:
        print(f"Error: {e}")

def timechart_search(int_value, lecture_div, lecture_title):
    # Type 0: Top Value
    # Type 1: Height Value

    # Get the index from the top value
    index = possible_top_values.index(int_value)

    # Get the time string according to the index
    initial_time = time_chart[index]
    print("\n========================")
    print(f"\n{lecture_title}")
    print(f"\nStarts: {initial_time}")

    lesson = {
        "title": lecture_title,
        "start_time": initial_time,
        "end_time": "",
    }
    lesson["start_time"] = initial_time
    
    # Get the height value
    height_value = lecture_div.value_of_css_property("height")

    # Convert the height value to int and cut out the px
    height_valueToInt = int(height_value.replace('px', ''))

    # A height value that is a multiple of 40 indicates a full-hour lesson (e.g., 9:00-10:00), 
    # while non-multiples suggest lessons with half-hour increments (e.g., 9:30-10:30).

    # Find if the height value is multiple of 40
    if height_valueToInt % 40 == 0:
        multiplier = height_valueToInt // 40

        # The end time index on time_chart will be equal to the initial_time index plus the multiplier
        # The difference between these indexes indicate how much time does a lesson take
        end_time_index = index + multiplier
        end_time = time_chart[end_time_index]
        lesson["end_time"] = end_time
        current_day_lessons.append(lesson)

        print(f"Ends: {end_time}")
        print("\n========================")
    else:

        # For height values that are not multiples of 40, subtract 20 to align with the nearest multiple.
        # Subtracting 20 from the height value accounts for half-hour increments in lessons, 
        # ensuring the correct time string is calculated for non-multiples of 40.
        # The height value must substracted by 20 to find the closest mutiple to the right time string

        converted_height = height_valueToInt - 20

        # Same process as before for multiples
        multiplier = converted_height // 40
        end_time_index = index + multiplier
        end_time = time_chart[end_time_index]

        # There are only 2 time strings where there are 2 chars before the char we want to replace with 3
        # To change a specific char in a string on Python, you can't modify it directly
        # I decided to use the list method and convert the string to lists
        if end_time_index < 2:
            end_time_list = list(end_time)
            end_time_list[2] = "3"
            converted_end_time = "".join(end_time_list)
            lesson["end_time"] = converted_end_time
            current_day_lessons.append(lesson)

            print(f"Ends {converted_end_time}")
            print("\n========================")
   
        else:
            end_time_list = list(end_time)
            end_time_list[3] = "3"
            converted_end_time = "".join(end_time_list)
            lesson["end_time"] = converted_end_time
            current_day_lessons.append(lesson)

            print(f"Ends: {converted_end_time}")
            print("\n========================")
    
def lecture_name_finder(lecture_div):
    lecture_titles = lecture_div.find_elements(By.TAG_NAME, "big")
    if lecture_titles:
        return lecture_titles[0].text
    
def is_lesson_occurring():
    current_time = datetime.now().strftime("%H:%M")
    for lesson in current_day_lessons:
        if lesson["start_time"] <= current_time <= lesson["end_time"]:
            return True
    return False

    

while True:

    if len(current_day_lessons) == 0:
        find_lecture()

    if is_lesson_occurring():
        crawl_page()
        time.sleep(random.uniform(10, 20))

driver.quit()