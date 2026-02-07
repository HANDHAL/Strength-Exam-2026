import streamlit as st
import pandas as pd
import os

# --- دالة الحسابات الهندسية ---
def calculate_results(L, b, h, P, e_type, load_type):
    b_m, h_m = b/1000, h/1000
    I = (b_m * h_m**3) / 12
    y = h_m / 2
    M_max = 0
    
    if e_type == "Cantilever":
        if "Point" in load_type: M_max = P * 1000 * L
        elif "UDL" in load_type: M_max = (P * 1000 * L**2) / 2
        else: M_max = (P * 1000 * L**2) / 6 # Triangular
    else: # Simply Supported
        if "Point" in load_type: M_max = (P * 1000 * L) / 4
        elif "UDL" in load_type: M_max = (P * 1000 * L**2) / 8
        else: M_max = (P * 1000 * L**2) / 12 # Triangular
        
    stress = (M_max * y / I) / 10**6
    return I, M_max, stress

# --- الواجهة ---
st.set_page_config(page_title="Strength Exam", layout="wide")
st.title("🏗️ اختبار مقاومة المواد - المرحلة الثانية")

# كلمة مرور بسيطة للطلاب
if "authenticated" not in st.session_state:
    password = st.text_input("أدخل رمز الدخول للاختبار:", type="password")
    if password == "1234": # يمكنك تغيير الرمز هنا
        st.session_state["authenticated"] = True
        st.rerun()
    else:
        st.stop()

# بيانات الطالب
with st.sidebar:
    st.header("بيانات الطالب")
    name = st.text_input("الاسم الثلاثي")
    st_id = st.text_input("الرقم الجامعي")

# اختيار معطيات السؤال
col1, col2 = st.columns(2)
with col1:
    e_type = st.selectbox("نوع العتبة", ["Cantilever", "Simply Supported"])
    load_type = st.selectbox("نوع الحمل", ["Point Load", "UDL (موزع)", "Triangular (مثلثي)"])
    P = st.selectbox("قيمة الحمل P (kN)", [10, 20, 50])
with col2:
    L = st.slider("طول العتبة L (m)", 2, 10, 5)
    b = st.number_input("العرض b (mm)", value=150)
    h = st.number_input("الارتفاع h (mm)", value=300)

st.divider()

# حقول الإجابة
st.subheader("✍️ أدخل نتائج حساباتك:")
c1, c2, c3 = st.columns(3)
st_I = c1.number_input("قيمة I (m^4)")
st_M = c2.number_input("قيمة M max (N.m)")
st_S = c3.number_input("قيمة الإجهاد (MPa)")

theory_q = st.text_area("سؤال نظري: ما تأثير زيادة ارتفاع المقطع (h) على الإجهاد؟")
file = st.file_uploader("ارفع صورة الحل الورقي")

if st.button("إرسال الإجابة وحفظها"):
    if name and st_id:
        I_ref, M_ref, S_ref = calculate_results(L, b, h, P, e_type, load_type)
        
        data = {
            "الاسم": [name], "الرقم": [st_id], "نوع الحمل": [load_type],
            "إجهاد الطالب": [st_S], "الإجهاد الصحيح": [round(S_ref, 2)],
            "النتيجة": ["صح" if abs(st_S-S_ref) < 1 else "خطأ"]
        }
        df_new = pd.DataFrame(data)
        
        # حفظ في إكسل
        fname = "results.xlsx"
        if os.path.exists(fname):
            df_old = pd.read_excel(fname)
            df_final = pd.concat([df_old, df_new]).sort_values(by="الاسم")
        else:
            df_final = df_new
        
        df_final.to_excel(fname, index=False)
        st.success("تم الحفظ بنجاح!")
        st.balloons()
    else:
        st.error("يرجى ملء الاسم والرقم الجامعي")