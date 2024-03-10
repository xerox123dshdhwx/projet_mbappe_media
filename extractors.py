from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Media import Media


def extract_news_text(media: Media):
    media_url = media.get_media_login_url()
    article_div = media.get_article_div()
    cookie_div = media.get_cookie_div()
    media_login_url = media.get_media_login_url()
    username = media.get_username()
    password = media.get_password()
    username_id_tag = media.get_username_id_tag()
    password_id_tag = media.get_password_id_tag()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(media_url)

    driver.implicitly_wait(10)

    if (cookie_div):
        driver.find_element(By.ID, cookie_div).click()

    if media_login_url and username and password:
        driver.get(media_login_url)

        driver.find_element(By.CSS_SELECTOR, f"input[id='{username_id_tag}']").send_keys(username)
        password_field = driver.find_element(By.CSS_SELECTOR, f"input[id='{password_id_tag}']")

        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    all_cookies = driver.get_cookies()

    driver.implicitly_wait(10)

    for cookie in all_cookies:
        driver.add_cookie(cookie)

    driver.get(media_url)

    article_text = driver.find_element(By.CSS_SELECTOR, f"div.{article_div}").text

    driver.quit()
    return article_text
