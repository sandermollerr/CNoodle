import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import datetime

browser: any
session_cookies: any


def open_browser_with_driver():
    options = Options()
    # Set headless option for browser
    options.add_argument('--headless')

    # Apply options for web driver
    global browser
    browser = webdriver.Firefox(options=options)  # options=options
    browser.implicitly_wait(5)
    browser.get('https://moodle.ut.ee/login/index.php')
    browser.find_element_by_xpath("//a[@class='btn btn-secondary btn-block']").click()


def get_login_status(username, password):
    # Entering credentials to input fields
    browser.find_element_by_id("i0116").send_keys(username)
    browser.find_element_by_id("i0116").send_keys(Keys.ENTER)

    browser.find_element_by_id("i0118").send_keys(password)
    time.sleep(1)
    browser.find_element_by_id("i0118").send_keys(Keys.ENTER)
    time.sleep(3)

    # Returns status code
    return browser.get_cookies()[0]["name"]


def get_course_links():
    # Navigates to courses overview page
    browser.get("https://moodle.ut.ee/grade/report/overview/index.php?id=2880")
    time.sleep(1)

    # Finds all active courses hyperlinks and appends them to list
    courses = browser.find_elements_by_xpath("//table[@id='overview-grade']//tbody//tr[@class='']//a")
    course_links = []
    for course in courses:
        course_links.append(course.get_attribute("href"))

    # Storing session cookies for later use
    global session_cookies
    session_cookies = browser.get_cookies()
    browser.close()
    return course_links


def navigate_to_login_page():
    browser.get('https://moodle.ut.ee/login/index.php')
    browser.find_element_by_xpath("//a[@class='btn btn-secondary btn-block']").click()


def read_data_from_moodle_into_file(course_links):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

    # Sets up session details for requests session
    session = requests.session()
    session.headers.update(headers)

    # Syncs all cookies between selenium driver session and requests session
    for cookie in session_cookies:
        c = {cookie['name']: cookie['value']}
        session.cookies.update(c)

    # Gets datetime and replaces all invalid symbols
    file_name = str(datetime.datetime.now())
    file_name = file_name.strip().replace(" ", "_").replace("-", "_").replace(":", "_")[:file_name.index(".")]

    # Checks if history directory exists and if doesn't creates one
    if not os.path.isdir('./history'):
        os.mkdir('./history')

    with open("./history/{}.txt".format(file_name), "w", encoding="UTF-8") as output_file:

        # Iterates over all courses links
        for link in course_links:
            # Opens course link with session cookies
            page = session.get(link)
            # Parses website html
            soup = BeautifulSoup(page.content, "lxml")

            # Writes course header to file
            output_file.write("->{}\n".format(soup.tbody.tr.th.text))

            # Iterates all course tests
            for tr in soup.find("tbody").find_all("tr"):
                test_result = ""
                test_result_range = ""

                # Finds tests headers from different paths
                try:
                    test_title = tr.th.span.text
                except AttributeError:
                    try:
                        test_title = tr.th.a.text
                    except AttributeError:
                        continue

                try:
                    # Iterates over all table data elements to find test grade and grade range
                    for data_index in range(len(tr.find_all("td"))):
                        if tr.find_all("td")[data_index]["class"][-1] == "column-grade":
                            test_result = tr.find_all("td")[data_index].text
                            test_result_range = tr.find_all("td")[data_index + 1].text  # ["class"][-1]
                            break
                except IndexError:
                    continue
                except AttributeError:
                    continue

                output_file.write("=>{};{};{}\n".format(test_title, test_result, test_result_range))

    return file_name


def compare_files(newer_file, older_file):
    # Checks if result directory exists and if doesn't creates one
    if not os.path.isdir('./result'):
        os.mkdir('./result')

    # Creates and opens result.txt file for writing compared information
    with open(".\\result\\result.txt", "w", encoding="UTF-8") as output_file:
        # Opens two files to find their differences
        with open(newer_file, "r", encoding="UTF-8") as new, open(older_file, "r", encoding="UTF-8") as old:
            new_data = new.readlines()
            old_data = old.readlines()

            course_name_new = ""
            course_name_old = ""
            for new_value in new_data:
                # Checks if dealing with course heading
                if new_value[:2] == "->":
                    print(new_value.strip())
                    output_file.write(new_value.strip() + "\n")
                    course_name_new = new_value.strip()
                    continue
                new_value_data = new_value.strip().split(";")
                new_title, new_result, new_result_range = new_value_data[0], new_value_data[1], new_value_data[2]
                found_new_title = False
                for old_value in old_data:
                    if old_value[:2] == "->":
                        course_name_old = old_value.strip()
                        continue

                    # Statement prevents comparing tests with same name from different courses
                    if course_name_old == course_name_new:
                        old_value_data = old_value.strip().split(";")
                        old_title, old_result, old_result_range = old_value_data[0], old_value_data[1], old_value_data[
                            2]
                        if new_title == old_title:
                            found_new_title = True
                            if new_result != old_result:
                                print("{};{};{}".format(new_title, new_result, old_result))
                                output_file.write("{};{};{}\n".format(new_title, new_result, new_result_range))
                                break
                            break

                # If new test is found
                if not found_new_title:
                    print("{};{};{}".format(new_title, new_result, "-"))
                    output_file.write("{};{};{}\n".format(new_title, new_result, "-"))
