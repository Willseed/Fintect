# 財經新聞重大消息爬蟲使用說明

## 下載及安裝

| 軟體名稱 | 下載連結 |
| --- | --- |
| Visual Studio Code | [Visual Studio Code] |
| Python 3.8.3 | [Python 3.8.3] |

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

### Python 3.8.3 安裝流程

1. 將 ```Add Python 3.8 To PATH``` 打勾
2. 點選 \<Install Now\>
3. **若有跳出需要管理員權限，點選<是>**

安裝完成後 ```⊞Win鍵``` + ```R鍵```打開執行視窗輸入```cmd```打開命令提示字元。

打開命令提示字元後，輸入```python``` 若出現以下畫面即為安裝成功
```cmd
Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:20:19) [MSC v.1925 32 bit (Intel)] on win32
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
pip        19.2.3
setuptools 41.2.0
WARNING: You are using pip version 19.2.3, however version 20.1.1 is available.
You should consider upgrading via the 'python -m pip install --upgrade pip' command.
```

請執行

```cmd
python -m pip install --upgrade pip
```

License
----
MIT

   [Visual Studio Code]: <https://code.visualstudio.com/>
   [Python 3.8.3]: <https://www.python.org/downloads/>
   [Tortoisegit]: <https://tortoisegit.org/>
   [Git]: <https://gitforwindows.org/>
