# 財經新聞重大消息爬蟲使用說明

## 下載及安裝

| 軟體名稱 | 下載連結 |
| --- | --- |
| Visual Studio Code | [Visual Studio Code] |
| uv | [uv] |
| Python 3.14 | 由 uv 自動安裝（目前鎖定 3.14.7） |

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

### uv 與 Python 3.14 安裝流程

本專案使用 [uv] 管理 Python 版本與套件。請先安裝最新版 uv，再於專案目錄同步環境。

macOS / Linux：

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows（PowerShell）：

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安裝完成後，於專案根目錄執行：

```cmd
uv sync
uv run playwright install chromium
```

`uv sync` 會依 `.python-version` 自動安裝 Python 3.14，並依 `uv.lock` 安裝已鎖定的套件版本。`playwright install chromium` 會下載 Playwright 所需的 Chromium 瀏覽器。

驗證 Python 版本：

```cmd
uv run python --version
```

預期輸出類似：

```cmd
Python 3.14.7
```
---

## Python 模組安裝

專案依賴由 `pyproject.toml` 與 `uv.lock` 管理。請使用 uv，不要再用 pip 逐一套件安裝。

```cmd
uv sync
uv run playwright install chromium
```

若只需執行環境、不含開發工具（pylint、isort）：

```cmd
uv sync --no-dev
uv run playwright install chromium
```

執行腳本範例：

```cmd
uv run python Scripts/refactoring/catch.py
```

公開資訊觀測站新版網站（`mops.twse.com.tw`）已改為 SPA。本爬蟲改抓仍提供舊版頁面的 `https://mopsov.twse.com.tw/mops/web/t05st01`。

## 選項設定說明
---
1. 13行可設定抓取年分(單位為民國年)，數字區間為 ```期望開始年份``` 與 ```期望結束年份+1``` 以下範例區間為92~109年

```python
year_list = [i for i in range(92, 110)]
```

2. 150行若未設定for_one_company選項，預設功能為抓取清單內所有公司，需給予 ```dir(清單放置資料夾)``` 與 ```filename(清單檔名)``` 參數
```python
year_range_list, stock_Id_TWSE_Dictionaryed = init(dir = 'Listed-company', filename = 'information.txt')#清單批次抓取
```

3. 151行若設定for_one_company選項為True，功能為抓取單一公司，需給予 ```company_name(公司名稱，中英皆可)``` 與 ```company_id(股票代碼)``` 參數
```python
year_range_list, stock_Id_TWSE_Dictionaryed = init(company_name = '聯電',company_id = '2303',for_one_company = True)
```

4. ```2.、3.``` 擇一使用即可

License
----
MIT

   [Visual Studio Code]: <https://code.visualstudio.com/>
   [uv]: <https://docs.astral.sh/uv/getting-started/installation/>
   [Tortoisegit]: <https://tortoisegit.org/>
   [Git]: <https://gitforwindows.org/>
