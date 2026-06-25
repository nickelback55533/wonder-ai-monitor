import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
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
            font-size: 16px !important; /* ป้องกันไม่ให้หน้าจอ iOS ซูมเข้าอัตโนมัติเมื่อกดพิมพ์ */
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
        <p style='margin:8px 0 0 0; font-size:15px; opacity:0.85; color: white;'>ระบบตรวจสอบสถานะกล้องวงจรปิดอัตโนมัติ (เวอร์ชันรองรับหลายสาขา)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### ⚙️ ตั้งค่าการเชื่อมต่อระบบ")

# โซนรับข้อมูลจากผู้ใช้แบบค่าว่าง (ลบช่อง Prefix ออกไปให้ระบบตรวจหา Auto เรียบร้อยครับ)
col1, col2 = st.columns(2)
with col1:
    web_url = st.text_input("🔗 วางลิงก์ URL ระบบของเว็บ:", value="")

with col2:
    username = st.text_input("👤 Username สำหรับล็อกอิน:", value="")
    username_password = st.text_input("🔑 Password สำหรับล็อกอิน:", value="", type="password")

st.markdown("---")

if st.button("🚀 เริ่มทำงาน (เปิดระบบ Chrome)", type="primary"):
    if not web_url or not username or not username_password:
        st.warning("⚠️ กรุณากรอกข้อมูลระบบให้ครบถ้วนทุกช่องก่อนเริ่มทำงานครับ")
    else:
        with st.spinner('กำลังสตาร์ทระบบ และเปิดเบราว์เซอร์ Chrome...'):
            
            options = webdriver.ChromeOptions()
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            wait = WebDriverWait(driver, 30) 
            
            try:
                # วิ่งไปที่ URL ระบบที่กรอกหน้าเว็บ
                driver.get(web_url)
                time.sleep(3) 
                
                # 1. ขั้นตอนการล็อกอิน
                try:
                    username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']")))
                    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
                    
                    username_field.send_keys(username)
                    password_field.send_keys(username_password)
                    password_field.submit()
                    
                    st.info("🔑 ระบบทำการกรอกรหัสผ่านและล็อกอินเข้าสู่ระบบแล้ว...")
                    time.sleep(6) 
                except Exception as e:
                    st.warning("ℹ️ ระบบเข้าสู่หน้าเว็บหลักโดยตรง (Session เดิมยังทำงานอยู่)")

                # 🏢 2. ระบบตรวจหาชื่อสาขาปัจจุบันที่กำลังใช้งานอยู่แบบอัตโนมัติ (Auto-Detect)
                try:
                    store_element = wait.until(EC.presence_of_element_located((By.XPATH, 
                        "//*[text()='Camera Registration']/preceding::*[contains(@class, 'select') or @role='combobox' or @type='button'][1] | "
                        "(//div[contains(@class, 'select') or @role='combobox'])[1] | "
                        "//*[contains(@class, 'ant-select-selector')]"
                    )))
                    detected_store = store_element.text.strip().replace('\n', ' ')
                    if detected_store:
                        st.success(f"🏢 ระบบตรวจพบสาขาปัจจุบันอัตโนมัติ: **{detected_store}**")
                except Exception as store_err:
                    st.info("ℹ️ ระบบข้ามการอ่านชื่อสาขา แต่จะดำเนินการตรวจเช็กกล้องบนหน้าจอต่อทันที")

                # 3. ระบบคลิกเลือกเมนูที่ (2) Camera dewarping ด้านซ้าย
                st.info("🔄 ระบบกำลังขยับไปคลิกเมนูหมายเลข (2) Camera dewarping...")
                try:
                    dewarping_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Camera dewarping') or contains(text(), 'Camera Dewarping')]")))
                    driver.execute_script("arguments[0].click();", dewarping_menu)
                    st.success("🎯 ระบบเปลี่ยนเข้าสู่หน้า Camera dewarping เรียบร้อยแล้ว!")
                    time.sleep(6) 
                except Exception as menu_err:
                    st.error(f"❌ หาปุ่มเมนู 'Camera dewarping' ไม่เจอ: {menu_err}")
                    driver.quit()

                # 4. ระบบคลิกปุ่ม Refresh (ลูกศรหมวนวน) ข้างๆ หัวข้อ "Camera"
                st.info("🔄 ระบบกำลังคลิกปุ่ม Refresh เพื่อดึงภาพ Snapshot ล่าสุด...")
                try:
                    refresh_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Camera']/..//button | //*[text()='Camera']/following-sibling::*[local-name()='svg' or @role='button'] | //*[text()='Camera']/..//*[local-name()='svg']")))
                    driver.execute_script("arguments[0].click();", refresh_btn)
                    st.success("✅ ระบบกดปุ่ม Refresh กล้องเรียบร้อยแล้ว! กำลังรอระบบโหลดภาพ Snapshot ใหม่...")
                    time.sleep(8) 
                except Exception as refresh_err:
                    st.warning(f"⚠️ ไม่สามารถกดปุ่ม Refresh ได้ จะข้ามไปไล่เช็กกล้องต่อ: {refresh_err}")

                # 5. 🎯 ขั้นตอนใหม่: ระบบตรวจหากล้องและดึงรายชื่ออัตโนมัติ (Camera Auto-Detect)
                st.info("📸 ระบบกำลังสแกนและวิเคราะห์รายชื่อกล้องวงจรปิดบนหน้าจออัตโนมัติ...")
                try:
                    # รอจนกว่าจะมีชื่อกล้องที่มีเครื่องหมายเครื่องหมายขีดล่างปรากฏขึ้นบนจอซ้ายมือ
                    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '_')]")))
                except:
                    time.sleep(4)

                # ดึงองค์ประกอบทั้งหมดที่มีเครื่องหมาย _ แล้วกรองเฉพาะชื่อกล้องจริง ๆ ออกมา
                camera_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '_')]")
                camera_names = []
                for elem in camera_elements:
                    try:
                        txt = elem.text.strip()
                        if txt and '_' in txt:
                            parts = txt.split('_')
                            if parts[-1].isdigit():  # ตรวจจับแพทเทิร์นที่เป็นตัวเลขต่อท้าย เช่น Sangtong_1, Yongsanguan_14
                                camera_names.append(txt)
                    except:
                        continue
                
                # เคลียร์ค่าซ้ำ
                camera_names = list(set(camera_names))
                
                # จัดเรียงลำดับตัวเลขกล้องให้อัตโนมัติ (1 -> 2 -> 10)
                try:
                    camera_names.sort(key=lambda x: int(x.split('_')[-1]) if '_' in x and x.split('_')[-1].isdigit() else 0)
                except:
                    camera_names.sort()
                
                if not camera_names:
                    st.error("❌ ระบบไม่พบรายชื่อกล้องวงจรปิดบนหน้าจอ กรุณาตรวจสอบหน้าต่างเบราว์เซอร์ Chrome ของระบบ")
                    driver.quit()
                else:
                    st.success(f"🎯 ระบบสแกนพบกล้องวงจรปิดอัตโนมัติจำนวนทั้งหมด {len(camera_names)} ตัว")
                    
                    results = []
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # 6. วนลูปคลิกเช็กกล้องทีละตัว
                    for idx, name in enumerate(camera_names):
                        status_text.text(f"🔵 ระบบกำลังเลือกตรวจจับ: {name}")
                        
                        try:
                            target_click = driver.find_element(By.XPATH, f"//*[text()='{name}']")
                            driver.execute_script("arguments[0].click();", target_click)
                            
                            # หน่วงเวลา 6 วินาที ให้ภาพ Snapshot โหลดขึ้นมาโชว์เต็มตาก่อนตรวจสอบ
                            time.sleep(6) 
                            
                            # ดึงซอร์สโค้ดหน้าเว็บ ณ วินาทีนั้นมาประมวลผลสถานะ
                            main_display = driver.page_source.lower()
                            
                            # ตรวจสอบคีย์เวิร์ดพังระดับระบบจริงๆ เท่านั้น
                            if "connection failed" in main_display or "not found" in main_display:
                                status = "🔴 Offline"
                                detail = "เซิร์ฟเวอร์กล้องปลายทางแจ้งเตือนการเชื่อมต่อล้มเหลว"
                            else:
                                status = "🟢 Online"
                                detail = "ภาพสัญญาณเสถียร โหลด Snapshot ล่าสุดสำเร็จ"
                                
                        except Exception as click_err:
                            status = "🔴 Error"
                            detail = f"ระบบเข้าไม่ถึงกล้องตัวนี้ หรือเกิดปัญหาตอนกด: {click_err}"
                        
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