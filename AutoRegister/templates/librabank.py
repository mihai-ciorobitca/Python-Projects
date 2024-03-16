# Achivement: Librabank removed job application forms from carrer page
# You can now only appy by sending email with your CV
# Obs.: they have a terrible captcha system

from imports import *

options = ["Nu", "Da"]

class Librabank:
    def __init__(self):
        print("Creating bot...")

        self.driver = Chrome()
        self.waiter = WebDriverWait(self.driver, 10)
        self.urls = [
            'https://www.librabank.ro/jobs/aplica/1099'
        ]
        self.selectors = {
            "firstname": "FirstName",
            "lastname": "LastName",
            "submit": "btnSubmit",
            "gdpr": "PrivacyPolicyConsent",
            "resume": "Resume",
            "email": "Email"
        }
        with open("info.json", encoding="utf-8") as reader:
            self.applicants = load(reader)

    def run_bot(self):
        print("Running bot...")
        self.self.driver.maximize_window()
        for index in self.applicants:
            for url in self.urls:
                self.self.driver.get(url)
                try:
                    applicant = self.applicants[index]
                    self.fill_form(applicant, index, url)   
                except Exception as e:
                    sleep(1)
                    print(f"Error with {e}")
                    return
        self.self.driver.quit()

    def fill_form(self, applicant, index, url):
        print(f"Filling application {index}")
        
        cookie = self.waiter.until(EC.element_to_be_clickable((By.CLASS_NAME, "cookie-consent-btn-action-preview.cookie-consent-block")))
        cookie.click()
            
        firstname = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantNume")))
        firstname.send_keys(applicant["firstname"])

        lastname = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantPrenume")))
        lastname.send_keys(applicant["lastname"]) 
        
        email = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantEmail")))
        email.send_keys("email@gmail.com")
        
        phone = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantTelefon")))
        phone.send_keys("1234567890")

        city = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantOras")))
        phone.send_keys("city")

        work = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantLucrezi")))
        work.send_keys("work")

        position = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantFunctia")))
        position.send_keys("positions")
        
        employer = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantLastJob")))
        employer.send_keys("employer")

        faculty = self.waiter.until(EC.presence_of_element_located((By.NAME, "data[JobAplicant][raspunsuri_facultate_specializare]")))
        faculty.send_keys("faculty")

        university = self.waiter.until(EC.presence_of_element_located((By.NAME, "data[JobAplicant][raspunsuri_facultate]")))
        university.send_keys("university")

        self.driver.execute_script("arguments[0].scrollIntoView(true);", work)
        select = Select(work)
        select.select_by_visible_text(choice(options))

        resume = self.waiter.until(EC.presence_of_element_located((By.ID, "JobAplicantCvLink")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", resume)
        self.driver.execute_script("arguments[0].click();", resume)
        sleep(1)
        typewrite("resume.pdf")
        press('enter')
        sleep(1)
        
        gdpr = self.waiter.until(EC.element_to_be_clickable((By.ID, "gdpr")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", gdpr)
        self.driver.execute_script("arguments[0].click();", gdpr)

        word = self.waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#JobAplicaForm > div:nth-child(4) > label > span")))
        word = word.text
        number = words[word]
        images = [self.waiter.until(EC.presence_of_element_located((By.CLASS_NAME, f"image{i}"))) for i in range(5)]
        sources = [(image.get_attribute('src'), image.get_attribute('class')) for image in images]
    
        for source in sources:
            if source[0].endswith(number):
                image = self.waiter.until(EC.presence_of_element_located((By.ID, "img"+source[1][-1])))
                self.driver.execute_script("arguments[0].click()", image)
                break
        
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit)
        self.driver.execute_script("arguments[0].click();", submit)
        submit = self.waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#JobAplicaForm > div:nth-child(6) > button")))
        print("Submited")

        self.waiter.until(EC.url_changes(url))
        sleep(1)

        print(f"Application {index} done!")


with open("words.json", "r", encoding="utf-8") as f:
    words = load(f)
