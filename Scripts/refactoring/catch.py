import time
import json
import os
# import main

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def init(dir: str = None, filename: str = None,company_name: str = None,company_id: int = None,for_one_company = False):
    year_list = [i for i in range(92, 108)]
    if(not for_one_company): 
        if(dir != None and filename != None):
            path = '../' + dir + '/' + filename
            with open(path, 'r') as f:
                twse_dictionary = json.loads(f.read())
        else:
            print('請輸入資料夾名稱與清單檔案名稱')
            exit()
    else:
        if(company_name != None and company_id != None):
            twse_dictionary = {}
            twse_dictionary[company_name] = company_id
        else:
            print('請輸入公司名稱與代碼')
            exit()
    return year_list, twse_dictionary

def driver_open():
    browser = webdriver.Chrome()
    browser.get('http://mops.twse.com.tw/mops/web/t05st01')
    return browser

def driver_close(browser):
    browser.quit()

def input_text(index, xpath):
    inputbox = browser.find_element_by_xpath(xpath)
    inputbox.clear()
    inputbox.send_keys(str(index) + Keys.RETURN)

def ChangeToPopUpWindow(index):
    browser.find_element_by_xpath('//*[@id="t05st01_fm"]/table/tbody/tr[' + str(index) + ']/td[6]/input').click()
    window_after = browser.window_handles[1] #獲取彈出視窗資訊
    browser.switch_to_window(window_after) #焦點切換到彈出視窗

def BackToSourceWindow(window_before):
    browser.close() #關閉彈出視窗
    browser.switch_to_window(window_before) #將焦點切回原先視窗

def WebWaitXpath(xpath):
    try:
        wait = WebDriverWait(browser, 10)
        wait.until(ec.visibility_of_element_located((By.XPATH, xpath)))
        return True
    except Exception as e:
        print(e)

def ListToDict(length, l_title, l_content):
    d_details = {}
    for i in range(0, length):
        d_details[l_title[i]] = l_content[i]
    return d_details

def get_data():
    try:
        time.sleep(10) #等待5s 再次點擊
        WebWaitXpath('//*[@id="table01"]/table[2]/tbody/tr[1]/td/b') #等待元件讀取
        l_title = []
        l_content = []
        table_path = '//*[@id="table01"]/table[3]/tbody'
        col_path = browser.find_elements_by_xpath(table_path + '/tr') #欄位置
        for i in range(1, len(col_path) + 1):
            row_path = browser.find_elements_by_xpath(table_path + '/tr[' + str(i) + ']/td') #列位置
            for j in range(1, len(row_path) + 1):
                if not (j % 2 == 0):
                    title = browser.find_element_by_xpath(table_path + '/tr[' + str(i) + ']/td[' + str(j) + ']').text #標題
                    l_title.append(title)
                elif(i == len(col_path) and j == len(row_path)):
                    content = browser.find_element_by_xpath(table_path + '/tr[' + str(i) + ']/td[' + str(j) + ']').text.split('\n') #說明部分切割成List
                    for k in content:
                        k.lstrip().rstrip()
                    l_content.append(content)
                else:
                    content = browser.find_element_by_xpath(table_path + '/tr[' + str(i) + ']/td[' + str(j) + ']').text.lstrip().rstrip() #內容 去左右空白
                    l_content.append(content)
        return ListToDict(len(l_title), l_title, l_content)
    except:
        print('Get Data Error!')
        return False

def get_year_message():
    company_keys = stock_Id_TWSE_Dictionaryed.keys()
    for company in company_keys:
        path = company+str(year_range_list[0])+'-'+str(year_range_list[-1])
        if not os.path.isdir(path):
            os.mkdir(path)
        input_text(stock_Id_TWSE_Dictionaryed[company], '//*[@id="co_id"]') #公司代號或簡稱
        for j in year_range_list:
            input_text(j, '//*[@id="year"]') #年度
            print('id: %s\tyear: %s' % (stock_Id_TWSE_Dictionaryed[company], j))
            btn_search = browser.find_element_by_xpath("//input[@type='button' and @value=' 查詢 ']") #查詢按鈕
            btn_search.click()
            time.sleep(3) #等待3s
            again = True
            while(again):
                if(WebWaitXpath('//*[@id="t05st01_fm"]/table/tbody/tr[2]/td[3]')): #等待元件讀取
                    again = False
                    window_before = browser.window_handles[0] #獲取來源網頁資訊
                    btn_details = browser.find_elements_by_xpath('//*[@id="t05st01_fm"]/table/tbody/tr') #詳細資料按鈕
                    for k in range(2, len(btn_details) + 1): #迭代每則重大消息按鈕 
                        print('第' + str(k - 1) + '個按鈕')
                        again_data = True
                        while(again_data):
                            ChangeToPopUpWindow(k) #改變視窗焦點
                            if(get_data() == False):
                                BackToSourceWindow(window_before)
                            else:
                                print('Get Data OK!')
                                again_data = False
                                d_details = get_data()
                                # print(d_details)
                                BackToSourceWindow(window_before)
                        #=========================
                        with open(path+'/'+company+'('+str(stock_Id_TWSE_Dictionaryed[company])+')-'+ str(j)+'-'+str(k - 1)+'.log', 'w') as f:
                                f.writelines(json.dumps(d_details)+'\n')
                        time.sleep(2) #等待2s 再次搜尋下一年
                        #===========================    
                else:
                    if (browser.find_elements_by_xpath('//*[@id="table01"]/center/h3')):
                        print('該 %s 公開發行公司不繼續公開發行！' % company)
                        break
                    else:
                        time.sleep(10) #等待10s
                        browser.refresh() #刷新網頁



if __name__ == '__main__':
    # main.check_browser_driver_available()
    browser = driver_open()

    # year_range_list, stock_Id_TWSE_Dictionaryed = init(dir = 'Listed-company', filename = 'information.txt')
    year_range_list, stock_Id_TWSE_Dictionaryed = init(company_name = '聯電',company_id = 2303,for_one_company = True)
    
    print(stock_Id_TWSE_Dictionaryed)
    get_year_message()
    driver_close(browser)