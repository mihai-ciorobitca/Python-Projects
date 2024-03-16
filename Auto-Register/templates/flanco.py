# Achivement: Flanco removed like 10  jobs from the job carrer page, maybe because they got scarred

from imports import *


class Flanco:
    def __init__(self):
        print("Creating bot...")

        self.driver = Chrome()
        self.self.waiter = WebDriverWait(self.driver, 10)
        self.urls = [
            "https://www.flanco.ro/cariere/vacantpositions/apply/id/9/",
            "https://www.flanco.ro/cariere/vacantpositions/apply/id/8/",
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

        firstname = self.waiter.until(
            EC.presence_of_element_located((By.ID, "first_name"))
        )
        firstname.send_keys("firstname")
        sleep(1)

        lastname = self.waiter.until(
            EC.presence_of_element_located((By.ID, "last_name"))
        )
        lastname.send_keys("lastname")
        sleep(1)

        phone = self.waiter.until(
            EC.presence_of_element_located((By.ID, "phone_number"))
        )
        phone.send_keys("0725497858")
        sleep(1)

        resume = self.waiter.until(EC.presence_of_element_located((By.ID, "pdf_file")))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", resume)
        self.driver.execute_script("arguments[0].click();", resume)
        sleep(1)
        typewrite("resume.pdf")
        press("enter")
        sleep(1)

        self.driver.execute_script(
            "document.getElementById('terms_and_conditions').click();"
        )

        submit = self.waiter.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#maincontent > div.columns > div > div.form-container.container-960 > div.load-pdf > form > div.form-group.buttons > button",
                )
            )
        )
        submit.click()
        print("Submited")

        self.waiter.until(EC.url_changes(url))
        sleep(1)
        print(index)
        print(url)

        print(f"Application {index} done!")
