import os                  # For working with file paths
import pathlib             # Modern way to handle file paths
import unittest            # Python's built-in testing tool

# Import Selenium — a tool to control a real browser automatically
from selenium import webdriver
from selenium.webdriver.common.by import By

# Helper function — converts a file name to a web address (file:///...)
def file_uri(filename):
    # os.path.abspath = get full path to file (e.g. C:\folder\counter.html)
    # pathlib.Path = modern path object
    # .as_uri() = turn it into "file:///C:/folder/counter.html"
    return pathlib.Path(os.path.abspath(filename)).as_uri()

# Start a real Chrome browser (Selenium opens Chrome for us)
# This browser will be controlled by the tests
driver = webdriver.Chrome()

# Create a test class — all tests go inside
class WebpageTests(unittest.TestCase):
    def test_title(self):
        driver.get(file_uri("counter.html"))
        self.assertEqual(driver.title, "Counter")

    def test_increase(self):
        driver.get(file_uri("counter.html"))
        #increase = driver.find_element_by_id("increase")
        increase = driver.find_element(By.ID, "increase")
        increase.click()
        #self.assertEqual(driver.find_element_by_tag_name("h1"), "1")
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "1")

    def test_decrease(self):
        driver.get(file_uri("counter.html"))
        #decrease = driver.find_element_by_id("decrease")
        decrease = driver.find_element(By.ID, "decrease")
        decrease.click()
        #self.assertEqual(driver.find_element_by_tag_name("h1", "-1"))
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "-1")

    def test_multiple_increase(self):
        driver.get(file_uri("counter.html"))
        #increase = driver.find_element_by_id("increase")
        increase = driver.find_element(By.ID, "increase")
        for i in range(3):
            increase.click()
        #self.assertEqual(driver.find_element_by_tag_name("h1"), "3")
        self.assertEqual(driver.find_element(By.TAG_NAME, "h1").text, "3")

# This part runs the tests when you execute the file
if __name__ == "__main__":
    unittest.main()
            