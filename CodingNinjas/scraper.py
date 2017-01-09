import os

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

from Utilities import cd

desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = user_agent
driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
cookies = {'domain': '.codingninjas.in', 'path': '/'}
cookie_string = input('Enter session cookie: ')
cookie_string = cookie_string.split('=')
for key, value in zip(['name', 'value'], cookie_string):
    cookies[key] = value

driver.add_cookie(cookies)
driver.get('http://codingninjas.in/students/assignments?show_details=PASS')
assignments = driver.find_elements_by_class_name('offeringName')
for i in range(len(assignments)):
    assignment = driver.find_elements_by_class_name('offeringName')[i]
    print(assignment.text)
    try:
        os.mkdir(assignment.text)
    except FileExistsError:
        pass
    with cd(assignment.text):
        assignment.find_element_by_class_name('customLink').click()
        problems = driver.find_elements_by_css_selector('.btn.blackButton')
        for j in range(len(problems)):
            problem = driver.find_elements_by_css_selector('.btn.blackButton')[j]
            problem.click()
            problem_name = driver.find_element_by_class_name('problemHeading').text
            driver.set_window_size('600', '1000')
            driver.save_screenshot('%s.png' % problem_name)
            driver.maximize_window()
            try:
                code_element = driver.find_element_by_link_text('View Submitted Code')
                driver.get(code_element.get_attribute('href'))
                with open('%s.cpp' % problem_name.replace(' ', ''), 'w', encoding='utf-8') as f:
                    f.write(driver.find_element_by_tag_name('body').text)
                driver.back()
            except NoSuchElementException:
                pass
            driver.back()
    driver.back()
