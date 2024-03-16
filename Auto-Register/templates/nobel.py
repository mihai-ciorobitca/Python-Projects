from imports import *

class Nobel:
    def __init__(self):
        print("Creating bot...")

        self.driver = Chrome()
        self.waiter = WebDriverWait(self.driver, 10)
        self.urls = [
            "https://nobelcareers.talentlyft.com/jobs/billing-and-collections-specialist-GOU/new"
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
        self.driver.maximize_window()
        for index in self.applicants:
            for url in self.urls:
                self.driver.get(url)
                try:
                    applicant = self.applicants[index]
                    self.fill_form(applicant, index, url)   
                except Exception as e:
                    sleep(1)
                    print(f"Error with {e}")
                    return
        self.driver.quit()

    def fill_form(self, applicant, index, url):
        print(f"Filling application {index}")
        
        firstname = self.waiter.until(EC.presence_of_element_located((By.NAME, self.selectors["firstname"])))
        firstname.send_keys(applicant["firstname"])
        sleep(1)
        
        lastname = self.waiter.until(EC.presence_of_element_located((By.NAME, self.selectors["lastname"])))
        lastname.send_keys(applicant["lastname"])
        sleep(1)

        email = self.waiter.until(EC.presence_of_element_located((By.NAME, self.selectors["email"])))
        email.send_keys("email@gmail.com")
        sleep(1)

        resume = self.waiter.until(EC.presence_of_element_located((By.NAME, self.selectors["resume"])))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", resume)
        self.driver.execute_script("arguments[0].click();", resume)
        sleep(1)
        typewrite("resume.pdf")
        press('enter')
        sleep(1)

        gdpr = self.waiter.until(EC.presence_of_element_located((By.NAME, self.selectors["gdpr"])))
        gdpr.click()
        
        submit = self.waiter.until(EC.element_to_be_clickable((By.ID, self.selectors["submit"])))
        submit.click()
        print("Submited")

        self.waiter.until(EC.url_changes(url))
        sleep(1)
        print(f"Application {index} done!")