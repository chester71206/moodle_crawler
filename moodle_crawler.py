user_name = ""  # 你的帳號
user_password = ""  # 你的密碼

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import os
import requests
from urllib.parse import unquote
from pathlib import Path
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import shutil
import chardet
import certifi
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC



desktop_path = Path.home() / "Desktop"

# 要創建的資料夾名稱
base_folder_name = "moodle備份"
base_folder_path = desktop_path / base_folder_name

# 檢查資料夾是否存在，如果不存在就創建
if not base_folder_path.exists():
    try:
        os.mkdir(base_folder_path)
        print(f"資料夾 '{base_folder_name}' 已成功創建於桌面。")
    except OSError as e:
        print(f"創建資料夾時出現錯誤: {e}")
else:
    print(f"資料夾 '{base_folder_name}' 已經存在於桌面。")

# 配置 WebDriver
chrome_options = Options()
prefs = {
    "download.default_directory": str(base_folder_path),  # 指定下載目錄
    "download.prompt_for_download": False,  # 不提示下載
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

#driver_wait = WebDriverWait(driver, 2) # 設置driver等待時間
try:
    driver.get('https://i.nccu.edu.tw/Login.aspx?app=moodle&ReturnUrl=%2fsso_app%2fMoodleSSO.aspx')

    # 填寫用戶名和密碼
    username_input = driver.find_element(By.ID, 'captcha_Login1_UserName')
    password_input = driver.find_element(By.ID, 'captcha_Login1_Password')
    username_input.send_keys(user_name)  # 替換成你的帳號
    password_input.send_keys(user_password)  # 替換成你的密碼

    # 點擊登錄按鈕
    login_button = driver.find_element(By.ID, 'captcha_Login1_LoginButton')
    login_button.click()

    # 等待登錄後的頁面加載
    driver.implicitly_wait(20)  # 最多等待20秒

    # 確認登錄是否成功
    current_url = driver.current_url
    if current_url == 'https://moodle.nccu.edu.tw/my/':
        print("成功登錄")
    else:
        print("登錄失敗或需要進一步驗證")

    # 在這裡可以繼續使用 Selenium 進行後續操作，如點擊連結、下載文件等
    # 例如，找到目標連結並點擊

    original_window = driver.current_window_handle
    Target_classes = driver.find_elements(By.CSS_SELECTOR, '.column.c1')

    for i in range(len(Target_classes)):
        try:
            target_classes = driver.find_elements(By.CSS_SELECTOR, '.column.c1')
            target_class = target_classes[i].find_element(By.TAG_NAME, 'a')  # 表示幾個課程

            div_element = driver.find_elements(By.XPATH, '//div[@class="column c1"]')

            # 獲取 div 元素內的文字內容
            text_content = div_element[i].text
            if '/' in text_content:
                text_content = text_content.split('/')[1]
            if ':' in text_content:
                text_content = text_content.split(':')[0]

            sub_folder_name = text_content
            sub_folder_path = base_folder_path / sub_folder_name

            if not sub_folder_path.exists():
                try:
                    os.mkdir(sub_folder_path)
                    print(f"資料夾 '{sub_folder_name}' 已成功創建於 '{base_folder_name}' 資料夾內。")
                except OSError as e:
                    print(f"創建資料夾時出現錯誤: {e}")
            else:
                print(f"資料夾 '{sub_folder_name}' 已經存在於 '{base_folder_name}' 資料夾內。")
                continue # 如果資料夾已經存在就跳過

            time.sleep(1)
            target_class.click()  # 進入到每一個 class 的頁面
            time.sleep(1)

            # 記錄訪問過的 URL
            visited_urls = []

            cookies = driver.get_cookies()  # 從 Selenium 中獲取 Cookies
            session = requests.Session()
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            
            Target_divs =driver.find_elements(By.CSS_SELECTOR, '.activityinstance')
            for j in range(len(Target_divs)):
                try:
                    target_divs =driver.find_elements(By.CSS_SELECTOR, '.activityinstance')
                    target_div = target_divs[j]

                    actions = ActionChains(driver)
                    actions.move_to_element(target_div).perform()

                    link = target_div.find_element(By.TAG_NAME, 'a')
                    link_text = link.find_element(By.CLASS_NAME, 'instancename').text  # 紀錄檔案名稱用
                    link_url = link.get_attribute('href')
                    visited_urls.append(driver.current_url)
                    link.click()
                    time.sleep(1)

                    all_windows = driver.window_handles
                    if len(all_windows) > 1:
                        new_window = [window for window in all_windows if window != original_window][0]
                        driver.switch_to.window(new_window)
                        print(f"彈跳式連結: {driver.current_url}")

                        try:
                           response = requests.get(driver.current_url, verify=certifi.where())
                           if response.status_code == 200:
                               filename = link_text.replace('/', '_').replace(':', '_')
                               file_path = sub_folder_path / f"{filename}.txt"
                               counter = 1
                               while file_path.exists():
                                   file_path = sub_folder_path / f"{filename} ({counter}).txt"
                                   counter += 1
                               with open(file_path, 'w', encoding='utf-8') as file:
                                   file.write(driver.current_url)
                                   print(f"內容已保存到: {file_path}")
                           else:
                              print(f"無法下載內容，狀態碼：{response.status_code}")
                        except requests.exceptions.SSLError:
                             # 處理SSL證書驗證錯誤
                             print(f"處理 Target_divs 錯誤: SSL證書驗證失敗，請檢查證書設置或略過驗證")

                        driver.close()
                        driver.switch_to.window(original_window)
                    else:
                        print(f"非彈跳式連結: {link_url}")
                        content_type = driver.execute_script("return document.contentType")
                        if content_type == "application/pdf":
                            try:
                                response = session.get(driver.current_url, timeout=10)
                                if response.status_code == 200:
                                    content_disposition = response.headers.get('content-disposition')
                                    if content_disposition:
                                        filename = content_disposition.split('filename=')[1].strip('" ')
                                        filename = unquote(filename)
                                        # 檢測文件名的編碼並進行解碼
                                        detected_encoding = chardet.detect(filename.encode())['encoding']
                                        if detected_encoding:
                                            filename = filename.encode('latin1').decode(detected_encoding)
                                        else:
                                            filename = filename.encode('latin1').decode('utf-8')
                                    else:
                                        filename = 'downloaded.pdf'
                                    i = 1
                                    original_filename = filename
                                    while os.path.exists(os.path.join(sub_folder_path, filename)):
                                        filename = f"{os.path.splitext(original_filename)[0]} ({i}){os.path.splitext(original_filename)[1]}"
                                        i += 1
                                    pdf_path = os.path.join(sub_folder_path, filename)
                                    with open(pdf_path, 'wb') as f:
                                        f.write(response.content)
                                    print(f"PDF 文件已保存到: {pdf_path}")
                                else:
                                    print(f"無法下載 PDF 文件，狀態碼：{response.status_code}")
                            except requests.exceptions.RequestException as e:
                                print(f"下載 PDF 文件時出錯: {e}")
                            driver.back()
                        else:
                            driver.implicitly_wait(0.2) #Implicit Wait:查找元素前的等待時間
                            try:
                               # 嘗試尋找目標元素
                               Target_docs = driver.find_elements(By.CSS_SELECTOR, '.ygtvcell.ygtvhtml.ygtvcontent')
                            except NoSuchElementException:
                               Target_docs = []
                            for k in range(len(Target_docs)):
                                try:
                                    target_docs = driver.find_elements(By.CSS_SELECTOR, '.ygtvcell.ygtvhtml.ygtvcontent')
                                    target_doc = target_docs[k]

                                    actions = ActionChains(driver)
                                    actions.move_to_element(target_doc).perform()

                                    link = target_doc.find_element(By.TAG_NAME, 'a')
                                    link.click()
                                    time.sleep(2)

                                    downloaded_files = [f for f in base_folder_path.iterdir() if f.is_file()]
                                    print(f"Downloaded files: {downloaded_files}")
                                    for file in downloaded_files:
                                        shutil.move(str(file), str(sub_folder_path / file.name))
                                        print(f"Moved {file} to {sub_folder_path / file.name}")
                                except Exception as e:
                                    print(f"處理 Target_docs 錯誤: {e}")

                    time.sleep(1)
                    driver.get(visited_urls.pop())
                except NoSuchElementException as e:
                    print(f"找不到元素: {e}")
                except Exception as e:
                    print(f"處理 Target_divs 錯誤: {e}")
                    if len(all_windows) > 1:
                        driver.close()
                        driver.switch_to.window(original_window) #讓他回到原本的頁面
        except NoSuchElementException as e:
            print(f"找不到元素: {e}")
        except Exception as e:
            print(f"處理 Target_classes 錯誤: {e}")
        driver.get("https://moodle.nccu.edu.tw/my/index.php")

except Exception as e:
    print(f"總體錯誤: {e}")

finally:
    driver.quit()
