from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime
from TRIAL import instagram_scraper


def instagram_scraper(url, username, password):
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com")
    time.sleep(5)

    # Log in to Instagram
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(5)

    driver.get(url)  # Go to the provided URL
    time.sleep(5)

    try:
        if '/p/' in url or '/reel/' in url:  # Post Page
            # Try to find the likes element, but handle if it's hidden
            try:
                likes_text = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "likes")]'))
                ).text
                # Extract only the numeric part of the likes count
                likes = re.sub(r'[^0-9]', '', likes_text)  # Remove any non-numeric characters
                print(f"Likes: {likes}")
            except Exception:
                likes = "Hidden or not available"
                print("Likes not found")

           
            result = {
                'likes': likes,
                'AT TIME':datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                }

        else:
            instagram_scraper(url,username,password)
            
           

    except Exception as e:
        print(f"Error occurred: {e}")
        result = None

    driver.quit()
    return result


# Example usage
url = 'https://www.instagram.com/reel/DFNyK8ayTaU/'
username = "zi3jseuzz"
password = "kalash@12"
data = instagram_scraper(url, username, password)
print(data)

