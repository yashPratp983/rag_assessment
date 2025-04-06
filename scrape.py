from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# Setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
driver = webdriver.Chrome(options=chrome_options)

# Store extracted data
data = []

# Helper to extract text or return empty string
def safe_get(by, value):
    try:
        return driver.find_element(by, value).text.strip()
    except NoSuchElementException:
        return ""

# Go to start page
# Go to start page

time.sleep(2)
def extract_label_data(label):
    try:
        return driver.find_element(By.XPATH, f"//h4[text()='{label}']/following-sibling::p").text.strip()
    except NoSuchElementException:
        return ""
i=0
# Loop through pages
while i<=372:
    driver.get(f"https://www.shl.com/solutions/products/product-catalog/?type=1&start={i}&type=1")
    print("Scraping catalog page:", driver.current_url)

    # Get all current links on the page
    links = driver.find_elements(By.CSS_SELECTOR, "td.custom__table-heading__title a")
    
    # Store link info (text + href) so we can safely come back and revisit
    assessments = []
    for link in links:
        assessments.append({
            "title": link.text.strip(),
            "href": link.get_attribute("href")
        })

    for assessment in assessments:
        print("  Visiting:", assessment["title"])
        driver.get(assessment["href"])
        time.sleep(1.5)

        # Extract details
        description = extract_label_data("Description")
        duration = extract_label_data("Assessment length")
        languages = extract_label_data("Languages")
        job_levels = extract_label_data("Job levels")


        data.append({
            "Title": assessment["title"],
            "URL": assessment["href"],
            "Description": description,
            "Job Levels": job_levels,
            "Languages": languages,
            "Assessment Length": duration,
        })

        driver.back()
        time.sleep(1.5)
        # print(data)

    i += 12

# Final save (in case loop exits via "disabled" logic)
df = pd.DataFrame(data)
df.to_csv("shl_assessments.csv", index=False)
df.to_json("shl_assessments.json", orient="records", indent=2)
print("Saved data to shl_assessments.csv and shl_assessments.json")
