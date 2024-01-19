"""
Reboots Compal GW7557CE router using Selenium
"""
import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

logged_in = False

log_file = open(os.path.join(os.path.dirname(__file__), "log.txt"), "a")
log_file.write(f"\n [{datetime.now()}]")

if len(sys.argv) < 2:
    log_file.write("Usage: python gw7557ce_selenium_reboot.py <password>\n")
    sys.exit(1)
password = sys.argv[1]

log_file.write("Uruchamianie webdrivera\n")
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("http://192.168.0.1")
log_file.write("Webdriver uruchomiony\n")

while True:
    if "Witaj" in driver.page_source:
        log_file.write("Logowanie\n")
        password_input = driver.find_element(By.ID, "loginPassword")
        password_input.send_keys(password)
        login_button = driver.find_element(By.ID, "c_36")
        login_button.click()
        time.sleep(1)

    if (
        "Istnieje inna aktywna sesja zarządzania ustawieniami urządzenia"
        in driver.page_source
    ):
        log_file.write("Istnieje inna aktywna sesja zarządzania ustawieniami urządzenia\n")
        log_file.write("Spróbuj ponownie później\n")
        driver.close()
        log_file.close()
        sys.exit(1)

    if "Podane hasło jest niepoprawne" in driver.page_source:
        log_file.write("Podane hasło jest niepoprawne\n")
        log_file.write("Użyj poprawnego hasła\n")
        driver.close()
        log_file.close()
        sys.exit(1)

    if "Mogą występować problemy z działaniem usługi" in driver.page_source:
        log_file.write("Słabe połączenie z routerem, ponowna próba logowania\n")
        try_again_button = driver.find_element(By.ID, "c_61")
        try_again_button.click()
        continue

    if "Witamy" in driver.page_source:
        log_file.write("Zalogowano\n")
        logged_in = True
        break

log_file.write("Znajdowanie narzędzi administratora\n")
admin_settings_menu = driver.find_element(By.ID, "c_mu25")
admin_settings_menu.click()

log_file.write("Szukanie menu `przeładuj i zrestartuj`\n")
restart_menu = driver.find_element(By.ID, "c_mu27")
restart_menu.click()

log_file.write("Szukanie przycisku `Uruchom ponownie`\n")
restart_button = driver.find_element(By.ID, "c_rr14")
restart_button.click()

log_file.write("Zatwierdzanie ponownego uruchomienia\n")
restart_confirmation_button = driver.find_element(By.ID, "c_st28")
restart_confirmation_button.click()

if logged_in:
    log_file.write("Wylogowywanie\n")
    logout_button = driver.find_element(By.ID, "c_mu30")
    logout_button.click()
    time.sleep(1)
    log_file.write("Wylogowano\n")

driver.close()
log_file.close()
