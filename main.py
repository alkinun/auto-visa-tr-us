import re
from datetime import datetime
from time import sleep
import time
import threading

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from request_tracker import RequestTracker
from msg import send_email
from settings import *

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkcalendar import DateEntry







root = tk.Tk()
root.title("Amerika Erken Randevu Botu")
root.geometry("512x690")

# Configure the grid
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

START_STATE = False

def start():
    global START_STATE
    if not START_STATE:
        global EMAIL_LOGIN, PASSWORD_LOGIN, CONSULATE_LOGIN, START_DATE, END_DATE, SEND_EMAIL, AUTO_RESCHEDULE, NOTIFICACION_EMAIL
        EMAIL_LOGIN = email_entry.get()
        PASSWORD_LOGIN = password_entry.get()
        CONSULATE_LOGIN = consulate_combobox.get()
        START_DATE = start_date.get_date()
        END_DATE = end_date.get_date()
        NOTIFICACION_EMAIL = notification_email_entry.get()

        if EMAIL_LOGIN == "" or PASSWORD_LOGIN == "" or CONSULATE_LOGIN == "" or START_DATE == "" or END_DATE == "" or NOTIFICACION_EMAIL == "":
            insert_log("Boş alan bırakmayın!")
            return

        insert_log("Program Başlatıldı")
        START_STATE = True

        session_count = 0
        while True:
            session_count += 1
            reschedule_and_send_mail_with_new_session()
            time.sleep(NEW_SESSION_DELAY)
    else:
        insert_log("Zaten başlatıldı")

def start_thread():
    thread = threading.Thread(target=start)
    thread.daemon = True
    thread.start()

# Title label
title_label = tk.Label(root, text="Amerika Erken Randevu Botu", font=("Arial", 16), pady=20, fg="darkred")
title_label.grid(row=0, column=0, columnspan=2)

# Ais E-posta
email_label = tk.Label(root, text="Ais E-posta")
email_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
email_entry = tk.Entry(root, width=46)
email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Ais Şifre
password_label = tk.Label(root, text="Ais Şifre")
password_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
password_entry = tk.Entry(root, show="*", width=46)
password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Konsolosluk
consulate_label = tk.Label(root, text="Konsolosluk")
consulate_label.grid(row=3, column=0, sticky="e", padx=10, pady=5)
consulate_combobox = ttk.Combobox(root, values=["Ankara", "Istanbul"], width=43)
consulate_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Başlangıç Tarihi
start_date_label = tk.Label(root, text="Başlangıç Tarihi")
start_date_label.grid(row=4, column=0, sticky="e", padx=10, pady=5)
start_date = DateEntry(root, date_pattern="yyyy-mm-dd", width=43)
start_date.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Bitiş Tarihi
end_date_label = tk.Label(root, text="Bitiş Tarihi")
end_date_label.grid(row=5, column=0, sticky="e", padx=10, pady=5)
end_date = DateEntry(root, date_pattern="yyyy-mm-dd", width=43)
end_date.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Bilgilendirme E-postası
notification_email_label = tk.Label(root, text="Bilgilendirme E-postası")
notification_email_label.grid(row=8, column=0, sticky="e", padx=10, pady=5)
notification_email_entry = tk.Entry(root, width=46)
notification_email_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")

# Divider
divider = ttk.Separator(root, orient="horizontal")
divider.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

# Mail Gönderilsin
send_mail_label = tk.Label(root, text="E-mail Gönderilsin")
send_mail_label.grid(row=10, column=0, sticky="e", padx=10)

SEND_EMAIL = tk.IntVar()
send_mail_btn = tk.Checkbutton(root, onvalue=1, offvalue=0, variable=SEND_EMAIL)
send_mail_btn.grid(row=10, column=1, padx=10)

# Otomatik Rezervasyon
auto_reschedule_label = tk.Label(root, text="Otomatik Rezervasyon")
auto_reschedule_label.grid(row=11, column=0, sticky="e", padx=10)

AUTO_RESCHEDULE = tk.IntVar()
auto_reschedule_btn = tk.Checkbutton(root, onvalue=1, offvalue=0, variable=AUTO_RESCHEDULE)
auto_reschedule_btn.grid(row=11, column=1, padx=10)

# Divider
divider = ttk.Separator(root, orient="horizontal")
divider.grid(row=12, column=0, columnspan=2, pady=10, sticky="ew")

# Başlat
button = tk.Button(root, text="Başlat", width=20, bg="lightgreen", command=start_thread)
button.grid(row=13, column=0, columnspan=2, pady=10)

# Divider
divider = ttk.Separator(root, orient="horizontal")
divider.grid(row=14, column=0, columnspan=2, pady=10, sticky="ew")

# Log
log = scrolledtext.ScrolledText(root, state="disabled", height=16)
log.grid(row=15, column=0, columnspan=2, pady=10)
log.configure(state="normal")
log.see("end")
log.configure(state="disabled")

def insert_log(text):
    log.configure(state="normal")
    log.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
    log.see("end")
    log.configure(state="disabled")





















































def get_chrome_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    if not SHOW_GUI:
        options.add_argument("headless")

    chrome_driver_path = ChromeDriverManager().install().replace("THIRD_PARTY_NOTICES.chromedriver", "chromedriver.exe")
    print("Corrected ChromeDriver path:", chrome_driver_path)

    driver = webdriver.Chrome(
        service=Service(chrome_driver_path), options=options
    )
    return driver


def login(driver: WebDriver) -> None:
    driver.get(LOGIN_URL)
    timeout = TIMEOUT

    sleep(.1)

    email_input = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "user_email"))
    )
    email_input.send_keys(EMAIL_LOGIN)

    sleep(.1)

    password_input = WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.ID, "user_password"))
    )
    password_input.send_keys(PASSWORD_LOGIN)

    sleep(.1)

    policy_checkbox = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "icheckbox"))
    )
    policy_checkbox.click()

    sleep(.1)

    login_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.NAME, "commit"))
    )
    login_button.click()


def reschedule(driver: WebDriver, date) -> None:
    timeout = TIMEOUT
    if CONSULATE_LOGIN == "Ankara":
        consular_input = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="appointments_consulate_appointment_facility_id"]/option[2]"""))
        )
    elif CONSULATE_LOGIN == "Istanbul":
        consular_input = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, """//*[@id="appointments_consulate_appointment_facility_id"]/option[3]"""))
        )
    consular_input.click()

    sleep(2)

    date_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="appointments_consulate_appointment_date"]"""))
    )
    driver.execute_script("arguments[0].value = arguments[1];", date_input, date.strftime("%Y-%m-%d"))
    date_input.send_keys(Keys.ENTER)

    sleep(8)

    time_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, f"""//*[@id="appointments_consulate_appointment_time"]"""))
    )
    driver.execute_script("arguments[0].click();", time_input)

    sleep(8)

    time_input = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, f"""//*[@id="appointments_consulate_appointment_time"]/option[2]"""))
    )
    time_input.click()

    sleep(8)

    reschedule_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="appointments_submit"]"""))
    )
    reschedule_button.click()

    if not TEST_MODE:
        time.sleep(6)
        confirm_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, """/html/body/div[6]/div/div/a[2]"""))
        )
        confirm_button.click()
    return


def get_appointment_page(driver: WebDriver) -> None:
    timeout = TIMEOUT
    continue_button = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Continue"))
    )
    continue_button.click()
    current_url = driver.current_url
    url_id = re.search(r"/(\d+)", current_url).group(1)
    appointment_url = APPOINTMENT_PAGE_URL.format(id=url_id)
    driver.get(appointment_url)


def get_available_dates(
    driver: WebDriver, request_tracker: RequestTracker
) -> list | None:
    request_tracker.log_retry()
    request_tracker.retry()
    current_url = driver.current_url
    if CONSULATE_LOGIN == "Istanbul":
        request_url = current_url + AVAILABLE_DATE_REQUEST_SUFFIX.format(consulate_id="125")
    elif CONSULATE_LOGIN == "Ankara":
        request_url = current_url + AVAILABLE_DATE_REQUEST_SUFFIX.format(consulate_id="124")
    request_header_cookie = "".join(
        [f"{cookie['name']}={cookie['value']};" for cookie in driver.get_cookies()]
    )
    request_headers = REQUEST_HEADERS.copy()
    request_headers["Cookie"] = request_header_cookie
    request_headers["User-Agent"] = driver.execute_script("return navigator.userAgent")
    sleep(10)
    try:
        response = requests.get(request_url, headers=request_headers)
    except Exception as e:
        print("Get available dates request failed: ", e)
        return None
    if response.status_code != 200:
        print(f"Failed with status code {response.status_code}")
        return None
    try:
        dates_json = response.json()
    except:
        print("Failed to decode json")
        return None
    dates = [datetime.strptime(item["date"], "%Y-%m-%d").date() for item in dates_json]
    print(dates)
    return dates


def reschedule_and_send_mail(driver: WebDriver) -> bool:
    date_request_tracker = RequestTracker(DATE_REQUEST_MAX_RETRY, DATE_REQUEST_MAX_TIME)
    while date_request_tracker.should_retry():
        dates = get_available_dates(driver, date_request_tracker)
        if not dates:
            sleep(DATE_REQUEST_DELAY)
            continue

        for date in dates:
            if START_DATE < date < END_DATE:
                try:
                    print(
                        f"{datetime.now().strftime('%H:%M:%S')} FOUND SLOT ON {date}!!!"
                    )
                    insert_log(f"Boş tarih bulundu: {date}")
                    if AUTO_RESCHEDULE.get():
                        reschedule(driver, date)
                        insert_log("Otomatik rezervasyon yapıldı")

                    if SEND_EMAIL.get():
                        send_email(SENDER_EMAIL, NOTIFICACION_EMAIL, "Ais E-Mail: " + EMAIL_LOGIN + "\nAçılan tarih: " + str(date), APP_KEY_GMAIL)
                        insert_log("Email gönderildi")
                    return
                except Exception as e:
                    print("Reschedule and send mail failed: ", e)
                    continue
        print(
            f"{datetime.now().strftime('%H:%M:%S')} Not found"
        )
        insert_log(f"Herhangi bir tarih istenen aralıkta bulunamadı")
        sleep(DATE_REQUEST_DELAY)
    return


def reschedule_and_send_mail_with_new_session() -> bool:
    driver = get_chrome_driver()
    session_failures = 0
    while session_failures < NEW_SESSION_AFTER_FAILURES:
        try:
            login(driver)
            sleep(20)
            get_appointment_page(driver)
            break
        except Exception as e:
            print("Unable to get appointment page: ", e)
            session_failures += 1
            sleep(FAIL_RETRY_DELAY)
            continue
    reschedule_and_send_mail(driver)
    driver.quit()
    return True




































root.mainloop()
import os
os.kill(os.getpid(), 9)