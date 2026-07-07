"""
Reboots Compal GW7557CE router using Selenium
"""

import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

log_file = open(
    os.path.join(os.path.dirname(__file__), "log.txt"), "a", encoding="utf-8"
)
log_file.write(f"[{datetime.now()}]\n")

if len(sys.argv) < 2:
    log_file.write("Usage: python gw7557ce_selenium_reboot.py <password>\n")
    sys.exit(1)
password = sys.argv[1]

log_file.write("Uruchamianie webdrivera.\n")
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

try:
    driver.get("http://192.168.0.1")
    log_file.write("Webdriver uruchomiony.\n")

    wait = WebDriverWait(driver, 10)
    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"), "Zaloguj się, aby uzyskać dostęp"
        ),
        "Nie można znaleźć strony logowania do routera. Sprawdź połączenie z routerem.",
    )

    wait.until(
        EC.presence_of_element_located((By.ID, "loginPassword")),
        "Nie można znaleźć pola hasła do logowania.",
    ).send_keys(password)

    wait.until(
        EC.element_to_be_clickable((By.ID, "c_88")),
        "Nie można znaleźć przycisku logowania.",
    ).click()

    try:
        logged_in_page = wait.until(
            EC.any_of(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"), "Przegląd statusu routera"
                ),
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, "body"),
                    "Mogą występować problemy z działaniem usługi",
                ),
            ),
            "Nie można znaleźć strony głównej routera po zalogowaniu.",
        )
    except TimeoutException as e:
        log_file.write(f"Błąd podczas przetwarzania: {str(e.msg)}\n")
        if "Zablokowano dostęp do panelu administracyjnego" in driver.page_source:
            raise TimeoutException(
                "Zablokowano dostęp do panelu administracyjnego."
            ) from e
        if "Podane hasło jest niepoprawne" in driver.page_source:
            raise TimeoutException("Podane hasło jest niepoprawne.") from e
        raise TimeoutException("Powód nieznany.") from e

    wait.until(
        EC.element_to_be_clickable((By.ID, "c_mu25")),
        "Nie można znaleźć narzędzi administratora.",
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.ID, "c_mu27")),
        "Nie można znaleźć menu `przeładuj i zrestartuj`.",
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.ID, "c_rr14")),
        "Nie można znaleźć przycisku `Uruchom ponownie`.",
    ).click()

    wait.until(
        EC.element_to_be_clickable((By.ID, "c_st28")),
        "Nie można znaleźć przycisku `Zatwierdź ponowne uruchomienie`.",
    ).click()

except TimeoutException as e:
    log_file.write(f"Błąd podczas przetwarzania: {str(e.msg)}\n")
except Exception as e:
    log_file.write(f"Nieznany błąd: {str(e)}\n")
finally:
    driver.quit()
    log_file.close()
