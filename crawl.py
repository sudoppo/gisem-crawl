from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import time
import requests
import json

profile_path = "/home/sudoppo/snap/firefox/common/.mozilla/firefox/ge47pdqr.sudoppo"
# Configure Firefox options for headless mode
firefox_options = Options()
#firefox_options.add_argument("--headless")  # Run in headless mode
firefox_options.add_argument(f"--profile {profile_path}")

# Set up the Firefox driver
service = Service('/usr/local/bin/geckodriver')  # Path to GeckoDriver
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

driver.quit()