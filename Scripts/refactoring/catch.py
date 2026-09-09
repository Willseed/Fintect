import time
import json
import os

from playwright.sync_api import sync_playwright


def init(dir: str = None, filename: str = None,company_name: str = None,company_id: str = None,for_one_company = False):
    year_list = [i for i in range(110, 111)]
    if(not for_one_company): 
        print('清單抓取開始')
        if(dir != None and filename != None):
            path = '../' + dir + '/' + filename
            with open(path, 'r') as f:
                twse_dictionary = json.loads(f.read())
        else:
            print('請輸入資料夾名稱或清單檔案名稱')
            driver_close(browser)
            exit()
    else:
        print('單一公司抓取開始')
        if(company_name != None and company_id != None):
            twse_dictionary = {}
            twse_dictionary[company_name] = company_id
        else:
            print('請輸入公司名稱或代碼')
            driver_close(browser)
            exit()
    return year_list, twse_dictionary

playwright_runtime = None
browser = None
page = None
popup = None

def current_page():
    return popup if popup is not None else page

def driver_open():
    global playwright_runtime, browser, page, popup
    playwright_runtime = sync_playwright().start()
    browser = playwright_runtime.chromium.launch(headless=True)
    page = browser.new_page()
    popup = None
    page.goto('https://mopsov.twse.com.tw/mops/web/t05st01')
    return page

def driver_close(browser_arg=None):
    global playwright_runtime, browser, page, popup
    if browser is not None:
        browser.close()
    if playwright_runtime is not None:
        playwright_runtime.stop()
    playwright_runtime = None
    browser = None
    page = None
    popup = None
    print('瀏覽器已關閉')

def input_text(index, xpath):
    inputbox = page.locator('xpath=' + xpath)
    inputbox.fill(str(index))
    inputbox.press('Enter')

def ChangeToPopUpWindow(index):
    global popup
    with page.expect_popup() as popup_info:
        page.locator('xpath=//*[@id="t05st01_fm"]/table/tbody/tr[' + str(index) + ']/td[6]/input').click()
    popup = popup_info.value

def BackToSourceWindow(window_before):
    global popup
    if popup is not None:
        popup.close()
        popup = None

def WebWaitXpath(xpath):
    try:
        current_page().locator('xpath=' + xpath).first.wait_for(state='visible', timeout=10000)
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
        WebWaitXpath('//*[@id="table01"]//table[contains(@class,"hasBorder")]') #等待元件讀取
        l_title = []
        l_content = []
        table_path = '//*[@id="table01"]//table[contains(@class,"hasBorder")]/tbody'
        target = current_page()
        col_path = target.locator('xpath=' + table_path + '/tr') #欄位置
        for i in range(1, col_path.count() + 1):
            row_path = target.locator('xpath=' + table_path + '/tr[' + str(i) + ']/td') #列位置
            print('%s%s' % ('\n', '-' * 50))
            for j in range(1, row_path.count() + 1):
                cell = target.locator('xpath=' + table_path + '/tr[' + str(i) + ']/td[' + str(j) + ']')
                if not (j % 2 == 0):
                    title = cell.inner_text() # 標題
                    print('title = %s' % title)
                    l_title.append(title)
                elif(i == col_path.count() and j == row_path.count()):
                    content = cell.inner_text() # 說明部分切割成List
                    print('content 1 = %s' % content)
                    l_content.append(content)
                else:
                    content = cell.inner_text().lstrip().rstrip() # 內容 去左右空白
                    print('content 2 = %s' % content)
                    l_content.append(content)
            print('%s' % ('=' * 50))
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
            btn_search = page.locator("xpath=//input[@type='button' and @value=' 查詢 ']") #查詢按鈕
            btn_search.click()
            time.sleep(3) #等待3s
            again = True
            while(again):
                if(WebWaitXpath('//*[@id="t05st01_fm"]/table/tbody/tr[2]/td[3]')): #等待元件讀取
                    again = False
                    window_before = page #獲取來源網頁資訊
                    btn_details = page.locator('xpath=//*[@id="t05st01_fm"]/table/tbody/tr').all() #詳細資料按鈕
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
                        with open(path+'/'+company+'('+str(stock_Id_TWSE_Dictionaryed[company])+')-'+ str(j)+'-'+str(k - 1)+'.log', 'w', encoding='utf-8') as f:
                                f.writelines(json.dumps(d_details, ensure_ascii=False)+'\n')
                        time.sleep(2) #等待2s 再次搜尋下一年
                        #===========================    
                else:
                    if (page.locator('xpath=//*[@id="table01"]/center/h3').count()):
                        print('該 %s 公開發行公司不繼續公開發行！' % company)
                        break
                    else:
                        time.sleep(10) #等待10s
                        page.reload() #刷新網頁



if __name__ == '__main__':
    driver_open()

    #以下兩行則一開啟使用

    # year_range_list, stock_Id_TWSE_Dictionaryed = init(dir = 'Listed-company', filename = 'information.txt')#清單批次抓取
    year_range_list, stock_Id_TWSE_Dictionaryed = init(company_name = '台積電', company_id = '2330', for_one_company = True)#單一公司抓取 

    get_year_message()
    driver_close(browser)
    print('爬蟲完成')