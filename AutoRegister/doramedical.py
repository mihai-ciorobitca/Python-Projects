# Achivement: They implemented ReCaptcha v3, but can still submit application
# and get positive feedback that will be contacted

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from json import load
from time import sleep
from pyautogui import typewrite, press

driver = Chrome()
waiter = WebDriverWait(driver, 10)

urls = [
    "https://www.dornamedical.ro/cariere/reprezentant-medical/",
    "https://www.dornamedical.ro/cariere/manager-regional/",
    "https://www.dornamedical.ro/cariere/asistent-medical-generalist/",
    "https://www.dornamedical.ro/cariere/operator-call-center/",
    "https://www.dornamedical.ro/cariere/operator-ct/",
    "https://www.dornamedical.ro/cariere/medici-specialisti/",
    "https://www.dornamedical.ro/cariere/asistent-medical-radiolog/",
    "https://www.dornamedical.ro/cariere/infirmiera/",
]

with open("names.json", "r", encoding="utf-8") as f:
    names = load(f)

driver.maximize_window()

for index in names:
    for url in urls:
        driver.get(url)
        user = names[index]
        print(index)
        try:
            firstname = waiter.until(EC.presence_of_element_located((By.ID, "wpforms-354640-field_6")))
            firstname.send_keys(user["name"])
            sleep(1)
            
            lastname = waiter.until(EC.presence_of_element_located((By.ID, "wpforms-354640-field_7")))
            lastname.send_keys(user["surname"])
            sleep(1)
            
            phone = waiter.until(EC.presence_of_element_located((By.ID, "wpforms-354640-field_8")))
            phone.send_keys("0751234567")
            sleep(1)

            email = waiter.until(EC.presence_of_element_located((By.ID, "wpforms-354640-field_13")))
            email.send_keys("email@gmail.com")
            sleep(1)

            submit = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wpforms-submit-354640")))

            resume = waiter.until(EC.presence_of_element_located((By.CLASS_NAME, "dz-hidden-input")))
            driver.execute_script("arguments[0].click();", resume)
            sleep(2)

            typewrite("resume.pdf")
            press('enter')
            sleep(2)

            while not submit.is_enabled():
                sleep(1)
            submit.click()
            print("Submited")

            waiter.until(EC.url_changes(url))
            sleep(1)
            print(url)
            
        except Exception as e:
            sleep(1)
            print(e)

driver.quit()
