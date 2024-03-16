# Achivement: They implemented ReCaptcha v3, but can still submit application
# and get positive feedback that will be contacted

from imports import *


class Doramedical:
    def __init__(self):
        print("Creating bot...")

        self.driver = Chrome()
        self.waiter = WebDriverWait(self.driver, 10)
        self.urls = [
            "https://www.dornamedical.ro/cariere/reprezentant-medical/",
            "https://www.dornamedical.ro/cariere/manager-regional/",
            "https://www.dornamedical.ro/cariere/asistent-medical-generalist/",
            "https://www.dornamedical.ro/cariere/operator-call-center/",
            "https://www.dornamedical.ro/cariere/operator-ct/",
            "https://www.dornamedical.ro/cariere/medici-specialisti/",
            "https://www.dornamedical.ro/cariere/asistent-medical-radiolog/",
            "https://www.dornamedical.ro/cariere/infirmiera/",
        ]
        self.selectors = {
            "firstname": "FirstName",
            "lastname": "LastName",
            "submit": "btnSubmit",
            "gdpr": "PrivacyPolicyConsent",
            "resume": "Resume",
            "email": "Email",
        }
        with open("info.json", encoding="utf-8") as reader:
            self.applicants = load(reader)

    def run_bot(self):
        print("Running bot...")
        self.self.self.driver.maximize_window()
        for index in self.applicants:
            for url in self.urls:
                self.self.self.driver.get(url)
                try:
                    applicant = self.applicants[index]
                    self.fill_form(applicant, index, url)
                except Exception as e:
                    sleep(1)
                    print(f"Error with {e}")
                    return
        self.self.self.driver.quit()

    def fill_form(self, applicant, index, url):
        print(f"Filling application {index}")

        firstname = self.waiter.until(
            EC.presence_of_element_located((By.ID, "wpforms-354640-field_6"))
        )
        firstname.send_keys("firstname")
        sleep(1)

        lastname = self.waiter.until(
            EC.presence_of_element_located((By.ID, "wpforms-354640-field_7"))
        )
        lastname.send_keys("lastname")
        sleep(1)

        phone = self.waiter.until(
            EC.presence_of_element_located((By.ID, "wpforms-354640-field_8"))
        )
        phone.send_keys("0751234567")
        sleep(1)

        email = self.waiter.until(
            EC.presence_of_element_located((By.ID, "wpforms-354640-field_13"))
        )
        email.send_keys("email@gmail.com")
        sleep(1)

        submit = self.waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#wpforms-submit-354640"))
        )

        resume = self.waiter.until(
            EC.presence_of_element_located((By.CLASS_NAME, "dz-hidden-input"))
        )
        self.driver.execute_script("arguments[0].click();", resume)
        sleep(2)

        typewrite("resume.pdf")
        press("enter")
        sleep(2)

        while not submit.is_enabled():
            sleep(1)
        submit.click()
        print("Submited")

        self.waiter.until(EC.url_changes(url))
        sleep(1)
        print(url)
