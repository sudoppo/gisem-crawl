<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from datetime import datetime, timedelta
import time
import requests
import json

profile_path = "/home/sudoppo/snap/firefox/common/.mozilla/firefox/ge47pdqr.sudoppo"
# Configure Firefox options for headless mode
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode
firefox_options.add_argument(f"--profile {profile_path}")

# Set up the Firefox driver
service = Service('/usr/local/bin/geckodriver')  # Path to GeckoDriver
driver = webdriver.Firefox(service=service, options=firefox_options)

# Flag to control the loop
stop_program = False

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

            # find_lecture()

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
        weekday_identifier = [1, 2, 3, 4, 5, 6]

        # Wait for the lessons divs to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "wc-cal-event"))
        )

        possible_top_values = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640]
        top_index_string = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

        tds = driver.find_elements(By.CLASS_NAME, "wc-day-column")
        for td in tds:
            if current_weekDay in td.get_attribute("class"):
                td_divs = td.find_elements(By.CLASS_NAME, "wc-cal-event")
                print(f"Found {len(td_divs)} event divs")

                for td_div in td_divs:
                    top_value = td_div.value_of_css_property("top")
                    top_valueToInt = int(top_value.replace('px', ''))
                    
                    if top_value == top_valueToInt:
                        horaInicio = "9:00"
                    
                
            
        # x value is the day of the week (1-monday to 6-saturday)

        print(f"Crawl instance: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    except Exception as e:
        print(f"Error: {e}")
while True:
    crawl_page()
    time.sleep(15)

=======
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import sys

# Linux
# profile_path = "/home/sudoppo/snap/firefox/common/.mozilla/firefox/ge47pdqr.sudoppo"

# Windows
profile_path = r"C:\Users\Vasco\AppData\Roaming\Mozilla\Firefox\Profiles\khok110j.sudoppo"

# Configure Firefox options for headless mode
firefox_options = Options()
#firefox_options.add_argument("--headless")  # Run in headless mode
firefox_options.add_argument(f"--profile {profile_path}")

# Set up the Firefox driver
# linux path /usr/local/bin/geckodriver
# windows path C:/geckodriver.exe
service = Service(r"C:\geckodriver\geckodriver.exe")  # Path to GeckoDriver
driver = webdriver.Firefox(service=service, options=firefox_options)

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

            find_lecture()

            if driver.title == "Horários":
                print("Presença not opened yet")
            else:
                marcar_title = driver.find_element(By.CSS_SELECTOR, "h1")
                if marcar_title.text == "Marcar Presenças":
                    print("Presença opened")
                    marcar_button = driver.find_element(By.CSS_SELECTOR, "button")
                    button_id = marcar_button.get_attribute("id")

                    if button_id is not None:
                        marcar_button.click()
                        print(f"Presença marked for {marcar_button.text}")
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

all_lectures = []

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

        # Check every day_column with class="wc-day-column" and specific class day-x
        current_weekDay = f"day-{datetime.now().isoweekday()}"
        weekday_identifier = [1, 2, 3, 4, 5, 6]

        # Wait for the lessons divs to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "wc-cal-event"))
        )

        possible_top_values = [0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640]
        top_index_string = ["8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]

        # Get all the day_columns with the wc-day-column class
        day_columns = driver.find_elements(By.CLASS_NAME, "wc-day-column")

        # Iterate over the day_columns to find the lectures of the current day
        for day_column in day_columns:
            columnClass = day_column.get_attribute("class")
            lecturesALL = day_column.find_elements(By.CLASS_NAME, "wc-cal-event")

            store_all_lectures(lecturesALL)

            # Check if the current day_column is the current day
            if current_weekDay in columnClass:
                
                # Get all the lectures for the current day
                lectures = day_column.find_elements(By.CLASS_NAME, "wc-cal-event")
                print(f"Found {len(lectures)} lectures for today")

                # Iterate over the lectures to get the lecture name and date
                for lecture in lectures:

                    # It is necessary to get the top value of the lecture div to determine the time of the lecture
                    top_value = lecture.value_of_css_property("top")
                    lecture_name = lecture.find_element(By.TAG_NAME, "big")

                    # Remove the px from the top value and convert it to an integer
                    top_valueToInt = int(top_value.replace('px', ''))
                    
                    # Check if the top value is in the possible top values
                    if top_valueToInt in possible_top_values:
                        try:
                            index = possible_top_values.index(top_valueToInt)
                            print("===================================")
                            print(f"\nAula: {lecture_name.text}\nHora: {top_index_string[index]}")
                            print("\n===================================")
                        except ValueError:
                            index = -1
        # x value is the day of the week (1-monday to 6-saturday)
        print(f"Crawl instance: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    except Exception as e:
        print(f"Error: {e}")

def store_all_lectures(lectures):
    print(lectures.text)

def loading_animation(loadingDone):
    dots = ["", ".", "..", "..."]

    while loadingDone == False:
        for dot in dots:
            sys.stdout.write(f"\rLoading{dot}")
            sys.stdout.flush()
            time.sleep(0.5)
    
    sys.stdout.write("\rLoading complete!\n")
    sys.stdout.flush()

while True:
    crawl_page()
    time.sleep(15)

>>>>>>> 5023d11 (Working on find lecture)
driver.quit()