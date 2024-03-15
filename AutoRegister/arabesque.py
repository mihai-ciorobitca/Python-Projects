# Achivement Access denied

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
    ""
]
url = "https://cariere.arabesque.ro/jobs/job/?oras=Toate&categorie=Vanzari&job_id=328"

with open("names.json", "r", encoding="utf-8") as f:
    names = load(f)

driver.maximize_window()

driver.get(url)

for index in names:
    print(index)
    user = names[index]
    try:
        firstname = waiter.until(EC.presence_of_element_located((By.NAME, "arabesque_aplica_nume")))
        firstname.send_keys(user["name"])
        sleep(1)
        
        lastname = waiter.until(EC.presence_of_element_located((By.NAME, "arabesque_aplica_prenume")))
        lastname.send_keys(user["surname"])
        sleep(1)
        
        phone = waiter.until(EC.presence_of_element_located((By.NAME, "arabesque_aplica_telefon")))
        phone.send_keys("0725497858")
        sleep(1)

        email = waiter.until(EC.presence_of_element_located((By.NAME, "arabesque_aplica_email")))
        email.send_keys("mihai.ciorobitca@student.tuiasi.ro")
        sleep(1)

        gdpr = waiter.until(EC.presence_of_element_located((By.NAME, "arabesque_aplica_agreement")))
        gdpr.click()
        
        submit = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wpcf7-f266-o1 > form > div.arabesque_aplica_camp_trimite_cv > p > input")))

        resume = waiter.until(EC.presence_of_element_located((By.NAME, "your-file")))
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

input()
driver.quit()

