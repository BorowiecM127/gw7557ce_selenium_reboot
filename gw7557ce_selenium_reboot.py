"""
Reboots Compal GW7557CE router using Selenium
"""

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

if len(sys.argv) < 2:
    print("Usage: python gw7557ce_selenium_reboot.py <password>")
    sys.exit(1)
password = sys.argv[1]

print("Uruchamianie webdrivera.")
options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

try:
    print("Otwieranie strony logowania do routera.")
    driver.get("http://192.168.0.1")

    wait = WebDriverWait(driver, 30)
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
        print(f"Błąd podczas przetwarzania: {str(e.msg)}")
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

    print("Router został pomyślnie zrestartowany.")

except TimeoutException as e:
    print(f"Błąd podczas przetwarzania: {str(e.msg)}")
except Exception as e:
    print(f"Nieznany błąd: {str(e)}")
finally:
    driver.quit()
