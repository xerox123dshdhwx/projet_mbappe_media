from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from contextlib import contextmanager
from Media import Media


class NewsExtractor:
    def __init__(self, media: Media):
        self.media = media

    @contextmanager
    def _get_webdriver(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        driver = webdriver.Chrome(options=chrome_options)
        try:
            yield driver
        finally:
            driver.quit()

    def _login(self, driver):
        try:
            driver.get(self.media.get_media_login_url)
            driver.find_element(By.CSS_SELECTOR, f"input[id='{self.media.get_username_id_tag()}']").send_keys(
                self.media.get_username())
            password_field = driver.find_element(By.CSS_SELECTOR, f"input[id='{self.media.get_password_id_tag()}']")
            password_field.send_keys(self.media.get_password())
            password_field.send_keys(Keys.RETURN)
        except WebDriverException as e:
            print(f"Login error: {e}")

    def handle_cookie_consent(self, driver):
        cookie_div_id = self.media.get_cookie_div()

        try:
            # Try to find the cookie div by ID
            cookie_element = driver.find_element(By.ID, cookie_div_id)
        except NoSuchElementException:
            # If not found by ID, try finding it by tag name 'div'
            cookie_element = driver.find_element(By.TAG_NAME, 'div')

        if cookie_element:
            cookie_element.click()
        else:
            print("Cookie consent element not found.")

    def extract_news_text(self):
        with self._get_webdriver() as driver:
            driver.get(self.media.get_article_to_reduce_url())
            driver.implicitly_wait(10)
            print("connecté to the driver")

            if self.media.get_cookie_div():
                print("cookie div trouvé")
                self.handle_cookie_consent(driver)
            #                driver.find_element(By.ID, self.media.get_cookie_div()).click()

            if all([self.media.get_media_login_url(), self.media.get_username(), self.media.get_password()]):
                self._login(driver)

            driver.get(self.media.get_article_to_reduce_url())
            driver.implicitly_wait(10)
            return driver.find_element(By.CSS_SELECTOR, f"div.{self.media.get_article_div()}").text
