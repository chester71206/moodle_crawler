7/15號moodle即將更新，舊課程資料將會被清除，因此做了這個Moodle檔案爬蟲，可以爬取moodle裡面幾乎所有的檔案，包括作業、連結、課程講義。但是會有少部分格式不一樣的資料會無法被抓到，所以如果有重要文件請手動下載。

**程式碼的第一二行請輸入您的moodle帳號密碼**，本程式需要幾個小時的時間運行，建議在半夜且網路訊號良好的地方執行。桌面有"moodle備份"這個資料夾建議進行改名，程式會從此資料夾開始存入資料，過程中請盡量不要中止程式碼，**若是終止了程式碼，請將當前爬蟲的課程資料夾刪除**(例如程式執行到微積分甲的課程，就將微積分甲課程的資料夾刪除即可，下次就會從微積分甲課程開始爬取)，程式執行前需要安裝以下套件，以下提供兩種方法，皆默認使用者已有 python 環境：

1. 直接在終端環境下載以下套件

```bash
!pip install selenium
!pip install requests
!pip install chardet
!pip install certifi
```

2. 使用requirements.txt

a. 創建 python 虛擬環境，使環境分離

```bash
python3 -m venv 「替換成你想要的環境名字」
```

b. 啟動虛擬環境

```bash
source 環境名字/bin/activate
```

c. 下載所需套件

```bash
pip install -r requirements.txt
```

d. 下載完後執行爬蟲程式

```bash
python3 moodle_crawler.py
```

e. 爬蟲爬完將虛擬環境關閉
```bash
deactivate
```
