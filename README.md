7/15號moodle即將更新，舊課程資料將會被清除，因此做了這個Moodle檔案爬蟲，可以爬取moodle裡面幾乎所有的檔案，包括作業、連結、課程講義，只有極少部分資料會無法被抓到，如果有重要文件請手動下載。
本程式需要的時間大致為兩小時到三小時，桌面有"moodle備份"這個資料夾建議進行改名，程式會從此資料夾開始存取，過程中請盡量不要中止程式碼，若是終止了程式碼，請將當前爬蟲的課程資料夾刪除(例如程式執行到微積分甲的課程，就將微積分甲課程的資料夾刪除即可，下次就會從微積分甲課程開始爬取)，程式執行前需要安裝以下套件:
```bash
!pip install selenium
```bash
!pip install requests
```bash
!pip install chardet
```bash
!pip install certifi
