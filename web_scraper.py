from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from datetime import date

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

    def drops_for_today(self):
        self.today = date.today().day

        page_source = self.__fetch_site_html()
        # with open('pagesource2.html', 'r') as file:
            # page_source = file.read()

        drops_information = self.__drops_information_from_page_source(
            page_source=page_source)

        self.driver.close()

        return drops_information

    def __fetch_site_html(self):
        """Use selenium to fetch the information from the CNFT calendar site.

        This function returns the html source code of the fetched web page.
        """
        self.driver.get(self.website)

        print('Searching for today\'s drops information.')
        try:
            WebDriverWait(self.driver, self.delay).until(
                EC.element_to_be_clickable(
                    (By.CLASS_NAME, 'calendar-list-event'))
            )
            print('Information found!')
        except TimeoutException:
            print('Loading took to much time')
            self.driver.quit()
            return

        # click on the div to get all the information on the drop
        for elem in self.driver.find_elements(By.CLASS_NAME, 'calendar-list-event'):
            elem.click()

        # with open('pagesource2.html', 'w') as file:
            # file.write(self.driver.page_source)

        return self.driver.page_source

    def __drops_information_from_page_source(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        drops = []

        for div in soup.find_all('div', {'class': 'calendar-list-event__header'}):

            day = div.find_next(
                'div',
                {'class': 'calendar-list-event__date__day'}
            ).get_text().strip()

            if self.__check_drop_day(day):
                drops.append(self.__retrieve_drop_information(div))

        return drops

    def __check_drop_day(self, day):
        try:
            return int(day) == self.today
        except Exception:
            return False
    
    def __retrieve_drop_information(self, drop):
        name = drop.find_next(
            'div',
            {'class': 'calendar-list-event__name'}
        ).get_text().strip()

        twitter = drop.find_next(
            'div',
            {'class': 'calendar-list-event__properties'}
        ).find_next(
            'div',
            {'class': 'eca-flex'}
        ).get_text().strip()[14:]

        time = drop.find_next(
            'span',
            {'class' : 'calendar-list-event__time'}
        ).find_next('span').get_text().strip()

        long_description = drop.find_next(
            'div',
            {'class': 'calendar-event-details__long-description'}
        )

        paragraphs = long_description.find_all('p')

        # try to parse the standar way (with <p>)
        #
        # sometimes the description comes with <br />, that's
        # the reason behing the except
        try:
            supply = paragraphs[2].get_text().split(' ')[1].strip()
            price = paragraphs[3].get_text().strip()[7:]
            website = paragraphs[5].get_text().strip()[9:]
            discord = paragraphs[6].get_text().strip()[9:]
        except Exception:
            supply, price, website, discord = self.__find_long_description_attr(
                long_description
            )

        return {
            'name': name,
            'twitter': twitter,
            'time': time,
            'supply': supply,
            'price': price,
            'website': website,
            'discord': discord
        }

    def __find_long_description_attr(self, long_description):
        long_description_text = long_description.get_text().strip()

        positions = [
            long_description_text.find('Supply'),
            long_description_text.find('Price'),
            long_description_text.find('Website'),
            long_description_text.find('Discord')
        ]

        # TODO sometimes some fields may not be available
        # treat that type of situation

        supply = long_description_text[positions[0]+8:positions[1]]
        price = long_description_text[positions[1]+7:positions[2]]
        website = long_description_text[positions[2]+9:positions[3]]
        discord = long_description_text[positions[3]+9:]

        return (supply, price, website, discord)
    

if __name__ == '__main__':
    app = WebScraper()

    try:
        drops = app.drops_for_today()
        print(drops)
    finally:
        print('Bye bye!')
        app.driver.quit()
