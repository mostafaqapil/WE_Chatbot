from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path  # pip install chromedriver-py
import os, time

# ---------------------------
# 1️⃣ إعداد المسارات والمجلدات
# ---------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = os.path.join(BASE_DIR, "data", "html_pages")
TXT_DIR = os.path.join(BASE_DIR, "data", "clean_text")
os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(TXT_DIR, exist_ok=True)

# ---------------------------
# 2️⃣ إعداد Selenium Chrome
# ---------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--log-level=3")

service = Service(binary_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# ---------------------------
# 3️⃣ قائمة URLs الأساسية والجديدة
# ---------------------------
urls = {
    "Home": "https://www.te.eg",
    "Mobile_Services": "https://www.te.eg/wps/portal/te/Personal/Mobile/Services",
    "Internet_Services": "https://www.te.eg/wps/portal/te/Personal/Internet/Services",
    "Billing": "https://www.te.eg/wps/portal/te/Billing/Personal",
    "Customer_Support": "https://www.te.eg/wps/portal/te/Support/CustomerSupport",
    "FAQ": "https://www.te.eg/wps/portal/te/Personal/FAQ",
    # URLs الجديدة المفيدة
    "Nitro_Mobile_Internet": "https://te.eg/wps/portal/te/Personal/Mobile/Nitro-mobile-internet",
    "WE_Internet": "https://te.eg/wps/portal/te/Personal/WEInternet",
    "International_Roaming": "https://www.te.eg/wps/portal/te/Personal/Mobile/International-Roaming",
    "WE_Pay": "https://te.eg/wps/portal/te/Personal/?1dmy&urile=wcm%3apath%3a%2Fte%2Fresidential%2Fmobile%2Bmodule%2Fservices%2Fother-services%2Fwe%2Bpay%2Fwe_pay"
}

# ---------------------------
# 4️⃣ Scraper
# ---------------------------
for name, url in urls.items():
    try:
        driver.get(url)
        time.sleep(20)  # انتظار تحميل الصفحة بالكامل

        # جلب النص الرئيسي فقط
        try:
            main_text = driver.find_element(By.CSS_SELECTOR, "body").text
            # يمكن تعديل selector لو وجدت class محدد للمحتوى المهم
        except:
            main_text = driver.page_source  # fallback في حال لم نجد النص

        # إزالة النصوص غير المفيدة (إعلانات، footer، download app، follow us)
        unwanted_phrases = [
            "Download our App", "FOLLOW US", "© 2025 Telecom Egypt",
            "Chat with us", "Not registered? Sign up"
        ]
        for phrase in unwanted_phrases:
            main_text = main_text.replace(phrase, "")

        # حفظ النصوص
        txt_path = os.path.join(TXT_DIR, f"{name}.txt")
        html_path = os.path.join(HTML_DIR, f"{name}.html")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(main_text)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        print(f" Scraped: {name} → {txt_path}")

    except Exception as e:
        print(f" Failed: {name} — {e}")

driver.quit()
print(" Extraction Completed! Clean text files are ready.")
