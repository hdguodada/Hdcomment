from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapy.selector import Selector


# # 进入浏览器设置
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
start_url = 'http://hotels.ctrip.com/hotel/D1096_755/p1'



def next_page(page_number):
    '获得下一页'
    try:
        browser.get(start_url)
        browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage"
            )
        time.sleep(1)
        # 页数框
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#txtpage'))
        )
        # 确定按钮
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#page_info > div.c_pagevalue > input.c_page_submit'))
        )
        input.clear() # 清除输入框内的内容
        time.sleep(1)
        input.send_keys(page_number) # 输入page_number
        submit.click()
        time.sleep(1)
    except TimeoutError:
        return next_page(page_number)


if __name__ == '__main__':
    for page in range(2, 9):
        next_page(page)

