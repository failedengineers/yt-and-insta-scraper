from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def instagram_scraper(url, username, password):
    
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (without opening a browser window)
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--no-sandbox")  # Disable sandboxing

    # Specify the path to chromedriver
    driver_path = r'C:\Users\gcmad\.cache\selenium\chromedriver\win64\132.0.6834.110\chromedriver.exe'
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.instagram.com")
        time.sleep(2)

        # Log in to Instagram
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(5)

        driver.get(url)# Go to the provided URL
        
        time.sleep(5)

        # Extract follower and following counts
        try:
            followers_element = driver.find_element(By.XPATH, '//a[contains(@href, "/followers/")]/span')
            followers = followers_element.get_attribute('title')
            
        except Exception as e:
            followers = f"Error retrieving followers: {e}"

  

        result = {
            'followers': followers,
            'AT TIME':datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            
            }

    except Exception as e:
        result = {
            'error': f"An error occurred: {e}",
        }

    finally:
        driver.quit()
        return result

if __name__ == "__main__":
    url = 'https://www.instagram.com/dr.rakshitasingh/#'
    username = "temppp85"
    password = "kalash@12"
    data = instagram_scraper(url, username, password)
    print(data)
