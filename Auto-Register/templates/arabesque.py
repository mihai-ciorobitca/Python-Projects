from imports import *

class Arabesque:
    def __init__(self):
        print("Creating bot...")

        self.driver = Chrome()
        self.waiter = WebDriverWait(self.driver, 10)
        self.urls = [
            "https://cariere.arabesque.ro/jobs/job/?oras=Toate&categorie=Vanzari&job_id=328"
        ]
        self.selectors = {
            "firstname": "arabesque_aplica_nume",
            "lastname": "arabesque_aplica_prenume",
            "phone": "arabesque_aplica_telefon",
            "email": "arabesque_aplica_email",
            "submit": "#wpcf7-f266-o1 > form > div.arabesque_aplica_camp_trimite_cv > p > input",
            "gdpr": "arabesque_aplica_agreement",
            "resume": "your-file",
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

        phone = self.waiter.until(EC.presence_of_element_located((By.NAME, self.selectors["phone"])))
        phone.send_keys("1234567890")
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