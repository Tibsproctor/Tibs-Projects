from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from lxml.html import fromstring
import time, os, psutil, threading,csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


class BeenVerifiedScraping():
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--profile-directory=Default")
        self.chrome_options.add_argument("--ignore-certificate-errors")
        self.chrome_options.add_argument("--disable-plugins-discovery")
        self.chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")

    def startChrome(self):
        return os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222')

    def closeBrowser(self):
        try:
            PROCNAME = "chromedriver.exe"
            userName = os.getlogin()
            for proc in psutil.process_iter():
                # check whether the process name matches

                if proc.name() == PROCNAME or proc.name() == 'chrome.exe':
                    if str(userName) in str(proc.username()):
                        print(str(proc.name()))
                        print(proc.username())
                        proc.kill()
        except Exception as ex:
            print(str(ex))


    def startScraping(self):
        path = chromedriver_autoinstaller.install(cwd=True)
        print(path)
        time.sleep(2)

        self.closeBrowser()
        time.sleep(2)

        th = threading.Thread(target=self.startChrome, args=())
        th.daemon = True
        th.start()
        
        time.sleep(6)
        driver = webdriver.Chrome(options=self.chrome_options)


    
        with open('highly_relevant_amazon.csv',encoding='utf-8') as fr:
            product_links = fr.readlines()
            for url in product_links:
                query_url = url.split(',')[0]
                driver.get(query_url.strip())
                
                print(f'Getting-Links: {query_url} - {driver.title}')
                HTMLSource = fromstring(driver.page_source, 'lxml')
                try:stock = driver.find_element(By.XPATH,'//div[@id="availability"]//span[contains(text(),"In Stock")]').text.strip()
                except:stock = 'Not Avilable'
                prod_titleTag = HTMLSource.xpath('//h1/span[@id="productTitle"]')
                prod_title = prod_titleTag[0].text.strip() if prod_titleTag else None
                # review_tag = HTMLSource.xpath('//span[@id="acrPopover"]//i/span[@class="a-icon-alt"]')
                # prod_reviews = review_tag[0].text if review_tag else 'none'
                ratting_tag = HTMLSource.xpath('//div[@id="averageCustomerReviews_feature_div"]//span[@class="a-icon-alt"]')
                prod_rattings = ratting_tag[0].text_content().strip().split(' ')[0] if ratting_tag else 'None'
                prcTag = HTMLSource.xpath('//span[@id="acrCustomerReviewText"]')
                prod_price = prcTag[0].text_content().strip() if prcTag else 'None'
                # currency = 'USD'
                # main_imageTag = HTMLSource.xpath('//div[@id="imgTagWrapperId"]/img[@id="landingImage"]')
                # main_image = main_imageTag[0].get('src') if main_imageTag else None
                # img_container = HTMLSource.xpath('//ul[contains(@class, "a-unordered-list")]//li[contains(@class, "item imageThumbnail")]//img')
                # prod_imgs = ', '.join([img.get('src') for img in img_container])
                # categoryTag = HTMLSource.xpath('//div[@id="wayfinding-breadcrumbs_feature_div"]//ul/li/span/a')
                # prod_category = ' > '.join([cate.text.strip() for cate in categoryTag])
                # desc_tag = HTMLSource.xpath('//div[@id="productDescription"]//p/span')
                # product_desc = desc_tag[0].text if desc_tag else None
                # product_url = url.replace('amazon.com','amazon.de')
                # asin_number = url.replace('amazon.com','amazon.de').split('ref=')[0].split('dp/')[-1].replace('/', '')
                # try:pack = driver.find_element(By.XPATH,'//li[@class="a-spacing-mini"]//span[@class="a-list-item"][contains(text(), "Pack ")]').text.strip() 
                # except:pack = ''
                # try:brand = driver.find_element(By.XPATH,'//div[@id="productOverview_feature_div"]//tr[contains(@class,"a-spacing-small")][1]').text.strip().replace('\n',' : ') 
                # except:brand = ''
                # try:ram = driver.find_element(By.XPATH,'//div[@id="productOverview_feature_div"]//tr[contains(@class,"a-spacing-small")][2]').text.strip().replace('\n',' : ') 
                # except:ram = ''
                # try:ramType = driver.find_element(By.XPATH,'//div[@id="productOverview_feature_div"]//tr[contains(@class,"a-spacing-small")][3]').text.strip().replace('\n',' : ') 
                # except:ramType = ''
                # try:memoryspeed = driver.find_element(By.XPATH,'//div[@id="productOverview_feature_div"]//tr[contains(@class,"a-spacing-small")][4]').text.strip().replace('\n',' : ') 
                # except:memoryspeed = ''
                # try:voltage = driver.find_element(By.XPATH,'//div[@id="productOverview_feature_div"]//tr[contains(@class,"a-spacing-small")][5]').text.strip().replace('\n',' : ') 
                # except:voltage = ''
                row = [query_url.split('.com/dp/')[1].split('?')[0].strip(),query_url.strip(),prod_title,prod_rattings,prod_price,stock]
                print(row)
                with open('Details.csv','a',newline='',encoding='utf-8') as fo:
                    csv.writer(fo).writerow(row)


if __name__ == '__main__':
    beenVerified=BeenVerifiedScraping()
    beenVerified.startScraping()