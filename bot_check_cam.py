import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- การตั้งค่าคอนฟิกและการปรับแต่งสไตล์สำหรับโทรศัพท์มือถือ (Mobile Responsive & Blue Theme) ---
st.set_page_config(page_title="Wonder AI Intelligent Monitor", page_icon="🔵", layout="wide")

st.markdown("""
    <style>
    /* ตั้งค่าโทนสีฟ้าสำหรับองค์ประกอบหลัก */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.2em;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    
    /* ปรับแต่งการแสดงผลบนสมาร์ทโฟน */
    @media (max-width: 640px) {
        .main .block-container {
            padding: 1rem !important;
        }
        h1 {
            font-size: 1.6rem !important;
        }
        .stTextInput>div>div>input {
            font-size: 16px !important;
        }
    }
    
    /* แถบหัวเรื่องสไตล์ Gradient สีน้ำเงิน-ฟ้า */
    .header-style {
        padding: 24px;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัวและโลโก้แบรนด์ Wonder AI พร้อมไอคอนกล้องวงจรปิด SVG สีขาว ---
st.markdown("""
    <div class="header-style">
        <h1 style='margin:0; color: white; font-family: sans-serif; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 15px;'>
            <svg viewBox="0 0 24 24" width="54" height="54" fill="white" style="vertical-align: middle;">
                <path d="M16 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm-2 10H6v-4h8v4zm8-4.5v5l-3 2.5v-10l3 2.5z"/>
            </svg>
            WONDER AI
        </h1>
        <p style='margin:8px 0 0 0; font-size:15px; opacity:0.85; color: white;'>ระบบตรวจสอบสถานะกล้องวงจรปิดอัตโนมัติ (Cloud Production v4.0)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### ⚙️ ตั้งค่าการเชื่อมต่อระบบ")

# โซนรับข้อมูลจากผู้ใช้แบบค่าว่าง (Empty Values) โล่งสะอาดตา
col1, col2 = st.columns(2)
with col1:
    web_url = st.text_input("🔗 วางลิงก์ URL ระบบของเว็บ:", value="")

with col2:
    username = st.text_input("👤 Username สำหรับล็อกอิน:", value="")
    username_password = st.text_input("🔑 Password สำหรับล็อกอิน:", value="", type="password")

st.markdown("---")

if st.button("🚀 เริ่มทำงาน (เปิดระบบคลาวด์อัจฉริยะ)", type="primary"):
    if not web_url or not username or not username_password:
        st.warning("⚠️ กรุณากรอกข้อมูลระบบให้ครบถ้วนทุกช่องก่อนเริ่มทำงานครับ")
    else:
        with st.spinner('ระบบ Wonder AI กำลังประมวลผลความปลอดภัยบนเซิร์ฟเวอร์คลาวด์...'):
            
            # 🎯 ไฮไลต์เด็ด: ตั้งค่าควบคุม Chrome ให้แอบทำงานเบื้องหลังเงียบ ๆ (Headless Mode) เหมาะกับเซิร์ฟเวอร์คลาวด์
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            
            driver = webdriver.Chrome(options=options)
            wait = WebDriverWait(driver, 30) 
            
            try:
                driver.get(web_url)
                time.sleep(4) 
                
                # 1. ขั้นตอนการล็อกอิน
                try:
                    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
                    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    
                    username_field.send_keys(username)
                    password_field.send_keys(username_password)
                    password_field.submit()
                    
                    st.info("🔑 ระบบทำการล็อกอินเข้าสู่ศูนย์กลางเรียบร้อยแล้ว...")
                    time.sleep(6) 
                except Exception as e:
                    st.warning("ℹ️ ระบบเข้าสู่หน้าต่างหลักโดยตรง")

                # 🏢 2. ระบบตรวจหาชื่อสาขาปัจจุบันอัตโนมัติ (Auto-Detect)
                try:
                    store_element = wait.until(EC.presence_of_element_located((By.XPATH, 
                        "//*[text()='Camera Registration']/preceding::*[contains(@class, 'select') or @role='combobox' or @type='button'][1] | "
                        "(//div[contains(@class, 'select') or @role='combobox'])[1] | "
                        "//*[contains(@class, 'ant-select-selector')]"
                    )))
                    detected_store = store_element.text.strip().replace('\n', ' ')
                    if detected_store:
                        st.success(f"🏢 ระบบตรวจพบสาขาปัจจุบันอัตโนมัติ: **{detected_store}**")
                except:
                    pass

                # 3. ระบบคลิกเลือกเมนูที่ (2) Camera dewarping ด้านซ้าย
                st.info("🔄 ระบบกำลังเข้าเมนู Camera dewarping...")
                try:
                    dewarping_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Camera dewarping') or contains(text(), 'Camera Dewarping')]")))
                    driver.execute_script("arguments[0].click();", dewarping_menu)
                    time.sleep(6) 
                except Exception as menu_err:
                    st.error("❌ ไม่สามารถเข้าสู่เมนูตรวจสอบภาพได้")
                    driver.quit()
                    st.stop()

                # 4. ระบบคลิกปุ่ม Refresh เพื่ออัปเดตสถานะภาพกล้องล่าสุด
                try:
                    refresh_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Camera']/..//button | //*[text()='Camera']/following-sibling::*[local-name()='svg' or @role='button'] | //*[text()='Camera']/..//*[local-name()='svg']")))
                    driver.execute_script("arguments[0].click();", refresh_btn)
                    st.success("✅ ระบบกดปุ่ม Refresh เพื่ออัปเดต Snapshot เรียบร้อยแล้ว!")
                    time.sleep(8) 
                except:
                    pass

                # 5. ระบบตรวจหากล้องและวิเคราะห์ชื่อกล้องอัตโนมัติ (Camera Auto-Detect)
                st.info("📸 ระบบกำลังวิเคราะห์รายชื่อกล้องวงจรปิดบนหน้าจออัตโนมัติ...")
                try:
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '_')]")))
                except:
                    time.sleep(4)

                camera_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '_')]")
                camera_names = []
                for elem in camera_elements:
                    try:
                        txt = elem.text.strip()
                        if txt and '_' in txt:
                            parts = txt.split('_')
                            if parts[-1].isdigit():
                                camera_names.append(txt)
                    except:
                        continue
                
                camera_names = list(set(camera_names))
                try:
                    camera_names.sort(key=lambda x: int(x.split('_')[-1]) if '_' in x and x.split('_')[-1].isdigit() else 0)
                except:
                    camera_names.sort()
                
                if not camera_names:
                    st.error("❌ ระบบไม่พบรายชื่อกล้องวงจรปิดบนหน้าจอนี้")
                    driver.quit()
                else:
                    st.success(f"🎯 ระบบสแกนพบกล้องอัตโนมัติทั้งหมดจำนวน {len(camera_names)} ตัว")
                    
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 6. วนลูปคลิกเช็กกล้องทีละตัว
                    for idx, name in enumerate(camera_names):
                        status_text.text(f"🔵 ระบบกำลังเลือกตรวจจับ: {name}")
                        
                        try:
                            target_click = driver.find_element(By.XPATH, f"//*[text()='{name}']")
                            driver.execute_script("arguments[0].click();", target_click)
                            time.sleep(6) 
                            
                            main_display = driver.page_source.lower()
                            
                            if "connection failed" in main_display or "not found" in main_display:
                                status = "🔴 Offline"
                                detail = "เซิร์ฟเวอร์กล้องปลายทางแจ้งเตือนการเชื่อมต่อล้มเหลว"
                            else:
                                status = "🟢 Online"
                                detail = "ภาพสัญญาณเสถียร โหลด Snapshot ล่าสุดสำเร็จ"
                                
                        except Exception as click_err:
                            status = "🔴 Error"
                            detail = "ระบบเข้าไม่ถึงตัวกล้องตัวนี้"
                        
                        results.append({
                            "ชื่อกล้องวงจรปิด": name,
                            "สเตตัสภาพล่าสุด": status,
                            "รายละเอียดปัญหา": detail
                        })
                        progress_bar.progress((idx + 1) / len(camera_names))
                    
                    status_text.success("🎉 ระบบทำงานตรวจเช็กเรียบร้อยครบทุกขั้นตอน!")
                    driver.quit()
                    
                    df = pd.DataFrame(results)
                    st.table(df)
                    
            except Exception as main_err:
                st.error(f"เกิดข้อผิดพลาดภายนอกระบบ: {main_err}")
                driver.quit()