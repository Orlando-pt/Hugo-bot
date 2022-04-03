from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

"""

For this code to work the GECKODRIVER needs
to be installed.

Also, it needs to be on one of the $PATH directories, so
one option is to copy the GECKODRIVER to /usr/local/bin.
"""
class WebScraper:

    def __init__(self):
        self.website = 'https://www.cnftcalendar.com/'
        self.delay = 7
        
        firefox_options = Options()
        firefox_options.headless = True
        self.driver = webdriver.Firefox(options=firefox_options)
        
    def today_dops(self):
        self.driver.get(self.website)
        
        print('Finding drop information...')
        try:
            WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'calendar-list-event'))
            )
            print('Necessary information found!')
        except TimeoutException:
            print('Loading took to much time')
            self.driver.quit()
            return

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        for drop in soup.find_all('span', {'class': 'calendar-list-event__time'}):
            drop_time = drop.find('span').get_text().strip()

            print(drop_time)
        
        self.driver.close()

if __name__ == '__main__':
    app = WebScraper()

    try:
        app.today_dops()
    finally:
        print('Bye bye!')
        app.driver.quit()
