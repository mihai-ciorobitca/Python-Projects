# Achivement: Flanco removed like 10  jobs from the job carrer page, maybe because they got scarred

from ..imports import *

driver = Chrome()
waiter = WebDriverWait(driver, 10)

urls = [
    "https://www.flanco.ro/cariere/vacantpositions/apply/id/9/",
    "https://www.flanco.ro/cariere/vacantpositions/apply/id/8/",
]

with open("names.json", "r", encoding="utf-8") as f:
    names = load(f)

driver.maximize_window()

for index in names:
    for url in urls:
        driver.get(url)
        try:
            firstname = waiter.until(EC.presence_of_element_located((By.ID, "first_name")))
            firstname.send_keys(names[index]["name"])
            sleep(1)
            
            lastname = waiter.until(EC.presence_of_element_located((By.ID, "last_name")))
            lastname.send_keys(names[index]["surname"])
            sleep(1)
            
            phone = waiter.until(EC.presence_of_element_located((By.ID, "phone_number")))
            phone.send_keys("0725497858")
            sleep(1)

            resume = waiter.until(EC.presence_of_element_located((By.ID, "pdf_file")))
            driver.execute_script("arguments[0].scrollIntoView(true);", resume)
            driver.execute_script("arguments[0].click();", resume)
            sleep(1)
            typewrite("resume.pdf")
            press('enter')
            sleep(1)

            driver.execute_script("document.getElementById('terms_and_conditions').click();")

            submit = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#maincontent > div.columns > div > div.form-container.container-960 > div.load-pdf > form > div.form-group.buttons > button")))
            submit.click()
            print("Submited")

            waiter.until(EC.url_changes(url))
            sleep(1)
            print(index)
            print(url)
            
        except Exception as e:
            sleep(1)
            print(e)

driver.quit()
