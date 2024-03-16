# Achivement: Librabank removed job application forms from carrer page
# You can now only appy by sending email with your CV
# Obs.: they have a terrible captcha system

from ..imports import *

driver = Chrome()
url = 'https://www.librabank.ro/jobs/aplica/1099'
first = True
options = ["Nu", "Da"]

with open("words.json", "r", encoding="utf-8") as f:
    words = load(f)

with open("names.json", "r", encoding="utf-8") as f:
    names = load(f)
start = "217"
submiting = False

for index in names:

    if index == start:
        submiting = True

    if submiting:
        print("Application nr.", index)

        info = names[index]
        driver.get(url)
        driver.maximize_window()

        try:
            waiter = WebDriverWait(driver, 10)
            if first:
                cookie = waiter.until(EC.element_to_be_clickable((By.CLASS_NAME, "cookie-consent-btn-action-preview.cookie-consent-block")))
                cookie.click()
                first = False
            name = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantNume")))
            surname = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantPrenume")))
            email = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantEmail")))
            phone = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantTelefon")))
            city = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantOras")))
            work = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantLucrezi")))
            position = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantFunctia")))
            employer = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantLastJob")))
            faculty = waiter.until(EC.presence_of_element_located((By.NAME, "data[JobAplicant][raspunsuri_facultate_specializare]")))
            university = waiter.until(EC.presence_of_element_located((By.NAME, "data[JobAplicant][raspunsuri_facultate]")))
            resume = waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantCvLink")))
            gdpr = waiter.until(EC.element_to_be_clickable((By.ID, "gdpr")))
            submit = waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#JobAplicaForm > div:nth-child(6) > button")))
            word = waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#JobAplicaForm > div:nth-child(4) > label > span")))
            word = word.text
            number = words[word]
            images = [waiter.until(EC.presence_of_element_located((By.CLASS_NAME, f"image{i}"))) for i in range(5)]
            sources = [(image.get_attribute('src'), image.get_attribute('class')) for image in images]

            driver.execute_script("arguments[0].scrollIntoView(true);", name)
            name.send_keys(info["name"])
            print("Filled name field")

            driver.execute_script("arguments[0].scrollIntoView(true);", surname)
            surname.send_keys(info["surname"])
            print("Filled surname field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", email)
            email.send_keys(info["name"]+"."+info["surname"]+"@gmail.com")
            print("Filled email field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", phone)
            phone.send_keys("0725497858")
            print("Filled phone field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", city)
            city.send_keys(info["city"])
            print("Filled city field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", work)
            select = Select(work)
            select.select_by_visible_text(choice(options))
            print("Filled work field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", position)
            position.send_keys(info["position"])
            print("Filled position field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", employer)
            employer.send_keys(info["employer"])
            print("Filled employer field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", faculty)
            faculty.send_keys(info["faculty"])
            print("Filled faculty field")
            
            driver.execute_script("arguments[0].scrollIntoView(true);", university)
            university.send_keys(info["university"])
            print("Filled university field")

            driver.execute_script("arguments[0].scrollIntoView(true);", resume)
            driver.execute_script("arguments[0].click();", resume)
            sleep(1)
            typewrite("resume.pdf")
            press('enter')
            sleep(1)
            print("Filled resume field")

            driver.execute_script("arguments[0].scrollIntoView(true);", gdpr)
            driver.execute_script("arguments[0].click();", gdpr)
            print("Clicked GDPR checkbox")

            for source in sources:
                if source[0].endswith(number):
                    image = waiter.until(EC.presence_of_element_located((By.ID, "img"+source[1][-1])))
                    driver.execute_script("arguments[0].click()", image)
                    break
            
            driver.execute_script("arguments[0].scrollIntoView(true);", submit)
            driver.execute_script("arguments[0].click();", submit)
            print("Submited")

            waiter.until(EC.url_changes(url))
            sleep(1)
            
        except Exception as e:
            sleep(1)
            print(e)

driver.quit()
