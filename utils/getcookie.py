from selenium import webdriver
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, TimeoutException

def getCookie(showCookie):
    # initialize webdriver
    driver = webdriver.Chrome()

    # send user to login
    driver.get('https://student.algebra.hr/digitalnareferada/#/login')

    # initiate login
    try:
        # wait for user to login
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'header-nav-user-actions'))
        )
        print("User has logged in!")

        # fetch the cookie
        cookies = driver.get_cookies()
        cookie_values = [cookie['value'] for cookie in cookies]
        ieCookie = ''.join(cookie_values)
        if showCookie:
            print("Your cookie is: " + ieCookie)

        return { 'PHPSESSID': ieCookie }

    except NoSuchWindowException:
        print("The browser window was closed before authentication!")
        sys.exit("Terminating program due to user closing the browser.")

    except TimeoutException:
        print("User did not log in within the time limit!")
        sys.exit("Terminating program due to authentication timeout.")

    finally:
        # quit the browser
        driver.quit()
