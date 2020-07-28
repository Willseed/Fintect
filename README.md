# 財經新聞重大消息爬蟲使用說明

## 下載及安裝

| 軟體名稱 | 下載連結 |
| --- | --- |
| Visual Studio Code | [Visual Studio Code] |
| Python 3.6.8 | [Python 3.6.8] |

> 以上軟體都下載最新版本即可
---

### Visual Studio Code 安裝流程
1. 點選 <我接受合約>
2. 點選 <下一步>
3. **使用預設值** 或 **選擇安裝的路徑** ```例如：C:\VS Code``` 
4. 點選 <下一步>
5. 點選 <下一步>
6. 將所有選項打勾
7. 點選 <下一步>
8. 點選 <安裝>
9. 點選 <完成> 打開 Visual Studio Code
---

### Python 3.6.8 安裝流程

1. 將 ```Add Python 3.6 To PATH``` 打勾
2. 點選 \<Install Now\>
3. **若有跳出需要管理員權限，點選<是>**

安裝完成後 ```⊞Win鍵``` + ```R鍵```打開執行視窗輸入```cmd```打開命令提示字元。

打開命令提示字元後，輸入```python``` 若出現以下畫面即為安裝成功
```cmd
Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
---

## Python模組安裝
### 檢查pip版本是否為最新
---
輸入指令

```cmd
pip list
```

若出現 WARNING

```cmd
Package    Version
---------- -------
pip        18.1
setuptools 41.2.0
WARNING: You are using pip version 18.1, however version 20.1.1 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.
```

請執行以下指令進行更新

```cmd
python -m pip install --upgrade pip
```

安裝相關模組
```cmd
pip install selenium
```

## 選項設定說明
---
1. 13行可設定抓取年分(單位為民國年)，數字區間為 ```*期望開始年份*``` 與 ```**期望結束年份+1**``` 以下範例區間為92~109年

```python
year_list = [i for i in range(92, 110)]
```

2. 150行若未設定for_one_company選項，預設功能為抓取清單內所有公司，需給予 ```**dir(清單放置資料夾)**``` 與 ```**filename(清單檔名)**``` 參數
```python
year_range_list, stock_Id_TWSE_Dictionaryed = init(dir = 'Listed-company', filename = 'information.txt')#清單批次抓取
```

3. 151行若設定for_one_company選項為True，功能為抓取單一公司，需給予 ```**company_name(公司名稱，中英皆可)**``` 與 ```**company_id(股票代碼)**``` 參數
```python
year_range_list, stock_Id_TWSE_Dictionaryed = init(company_name = '聯電',company_id = 2303,for_one_company = True)
```

4. ```**2.、3.**``` 擇一使用即可

License
----
MIT

   [Visual Studio Code]: <https://code.visualstudio.com/>
   [Python 3.6.8]: <https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe>
   [Tortoisegit]: <https://tortoisegit.org/>
   [Git]: <https://gitforwindows.org/>
