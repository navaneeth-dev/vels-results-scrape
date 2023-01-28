import csv
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import os
load_dotenv()

driver = Chrome()
all_results = []


def scrape(admission_number):
    driver.get("http://184.95.52.42/examresults/online/report/onlineResult.jsp")
    admission_number_input = driver.find_element(By.ID, "txtRegisterno")
    admission_number_input.send_keys(admission_number)

    # find the submit button and click it
    submit_button = driver.find_element(By.CLASS_NAME, "submitButton")
    submit_button.click()

    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.find_element(
        By.ID, "divResult").text.strip() != '')

    try:
        if driver.find_element(By.CSS_SELECTOR, "font[color=red]"):
            all_results.append([admission_number, "-", "-",
                                "-", "-", "-", "-", "-", "-", "-"])
    except NoSuchElementException:
        name = driver.find_element(
            By.XPATH, "/html/body/form/table[2]/tbody/tr[2]/td/div/table[1]/tbody/tr[1]/td[2]")
        result = [admission_number, name.text]

        table = driver.find_element(By.ID, "table1")
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]

        # iterate through each row and get the 4th <td> and last <td> text
        for row in rows:
            cells = row.find_elements(By.XPATH, "td")

            # result.append(cells[3].text)
            result.append(cells[-1].text)

        all_results.append(result)


admission_number_starting = os.getenv("ADMISSION_NUMBER")
for admission_last_digits in range(1, 56):
    scrape(f"{admission_number_starting}{admission_last_digits:02}")

driver.quit()

with open('data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["ADMISSION NUMBER", "NAME", "COMMUNICATION SKILLS", "MATHEMATICS", "PROGRAMMING IN C", "WEB TECHNOLOGY",
                       "ENGLISH PAPER", "FRENCH PAPER", "PRACTICAL - PROGRAMMING IN C", "PRACTICAL - WEB TECHNOLOGY"])
    csvwriter.writerows(all_results)
