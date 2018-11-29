from selenium import webdriver
import time
import re
from datetime import datetime
from config.settings import CHROME_DRIVER
from reservations.models import Movie
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome(CHROME_DRIVER)
time.sleep(5)
driver.get('https://www.cgv.co.kr/movies/')
driver.find_element_by_css_selector('div.nowshow input').click()
time.sleep(1)
driver.find_element_by_class_name('btn-more-fontbold').click()
time.sleep(20)
url_list = driver.find_elements_by_xpath("//ol/li/div[@class='box-image']/a")
detail_urls = [url.get_attribute("href") for url in url_list]
time.sleep(2)

for url in detail_urls:
    driver.get(url)
    time.sleep(5)
    try:
        driver.find_element_by_class_name('sect-error')
    except NoSuchElementException:
        driver.get(url)
        time.sleep(5)
        try:
            title = driver.find_element_by_css_selector('div.title strong').text
            spec = driver.find_elements_by_css_selector('div.spec dd')
            clean_spec = [dd.text for dd in spec]
            director = clean_spec[0]
            actor = clean_spec[2]
            genre = re.split(':', driver.find_elements_by_css_selector('div.spec dt')[2].text)[1]
            running_time = int(re.search(r'[0-9]+', clean_spec[4].split(',')[1]).group())
            opening_date = clean_spec[5]
            story = driver.find_element_by_css_selector('div.sect-story-movie div').text.strip().replace('\n', '<br>')
            image = driver.find_element_by_css_selector('div.box-image a').get_attribute("href")
            driver.find_elements_by_css_selector('ul.tab-menu li a')[2].click()
            time.sleep(2)
            still_cut = driver.find_elements_by_css_selector('div#stillcut_list img')
            still_cut_list = ', '.join([img.get_attribute("src") for img in still_cut][:5])
            Movie.objects.create(
                title=title,
                director=director,
                cast=actor,
                duration_min=running_time,
                opening_date=datetime.strptime(opening_date, '%Y.%m.%d').date(),
                description=story,
                genre=genre,
                main_img=image,
                stillcut_img=still_cut_list,
            )
            time.sleep(2)
        except NoSuchElementException:
            pass
            time.sleep(1)