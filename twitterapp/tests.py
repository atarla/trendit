from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySeleniumTests(StaticLiveServerTestCase):
    #fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver(executable_path='C:/selenium/chromedriver.exe')
        cls.selenium.implicitly_wait(10)
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls.selenium.quit()
    #     super(MySeleniumTests, cls).tearDownClass()

    def test_search(self):
        self.selenium.maximize_window()
        self.selenium.get('%s%s' % (self.live_server_url, '/'))

        search_term = self.selenium.find_element_by_name('searchterm')
        search_term.send_keys('tuesdaymotivation')
        self.selenium.find_element_by_name('search').click()
        #WebDriverWait(self.selenium,5).until(lambda driver: driver.find_element_by_tag_name('body'))
            #.until(self.selenium.page_source)
        WebDriverWait(self.selenium, 5).until(EC.new_window_is_opened)

    def test_surprise(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.maximize_window()
        self.selenium.find_element_by_name('surprise').click()
        #WebDriverWait(self.selenium,6).until(lambda driver: driver.find_element_by_tag_name('body'))
        WebDriverWait(self.selenium, 5).until(EC.new_window_is_opened)

    # def test_disc(self):
    #     self.selenium.get('%s%s' % (self.live_server_url, '/login'))
    #     self.selenium.maximize_window()
    #     self.selenium.find_element_by_name('username').send_keys('atarla90')
    #     self.selenium.find_element_by_name('password').send_keys('qwerty')
    #     self.selenium.find_element_by_name('login').click()
    #     self.selenium.get('%s%s' % (self.live_server_url, '/details'))
    #     WebDriverWait(self.selenium, 5).until(EC.new_window_is_opened)