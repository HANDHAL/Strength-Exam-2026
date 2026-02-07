import streamlit as st
import pandas as pd
import math

# --- إعدادات الصفحة الرسمية ---
st.set_page_config(page_title="جامعة النهرين - كلية الهندسة", layout="centered")

# --- الترويسة الرسمية (تم تصحيح الكود هنا) ---
st.markdown("""
<div style="text-align: right; dir: rtl; line-height: 1.2; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-right: 5px solid #1f77b4;">
    <h2 style="margin: 0; color: #1f77b4;">جامعة النهرين</h2>
    <h3 style="margin: 0; color: #333;">كلية الهندسة</h3>
    <p style="margin: 0; font-size: 18px; color: #666;">قسم الهندسة المدنية</p>
</div>
<br>
""", unsafe_allow_html=True)

# --- إعدادات الحالة (Session State) لمنع الأخطاء ---
if 'active_shape' not in st.session_state:
    st.session_state['active_shape'] = ["Square/Rectangle"]
if 'active_topic' not in st.session_state:
    st.session_state['active_topic'] = "Bending Stress"

# --- واجهة التدريسي (لوحة التحكم في القائمة الجانبية) ---
with st.sidebar:
    st.header("⚙️ لوحة تحكم الأستاذ")
    admin_key = st.text_input("رمز الإدارة", type="password")
    if admin_key == "prof2026":
        st.success("تم تسجيل الدخول")
        st.session_state['active_topic'] = st.selectbox("الموضوع الحالي:", ["Bending Stress", "Torsion"])
        st.session_state['active_shape'] = st.multiselect(
            "تفعيل المقاطع للطلاب:", 
            ["Square/Rectangle", "Solid Cylinder", "Hollow Tube (Rectangular)", "Hollow Cylinder (Pipe)"],
            default=st.session_state['active_shape']
        )

# --- بيانات الطالب ---
st.subheader("📝 استمارة الاختبار الإلكتروني")
with st.container():
    c1, c2 = st.columns(2)
    student_name = c1.text_input("اسم الطالب الثلاثي")
    student_id = c2.text_input("الرقم الجامعي / المرحلة الثانية")

st.divider()

# --- اختيار شكل المقطع العرضي ---
st.subheader("📐 معطيات السؤال الهندسي")
# نستخدم القائمة المفعلة من قبل الأستاذ
selected_shape = st.selectbox("اختر شكل المقطع العرضي (Cross-section):", st.session_state['active_shape'])

# تخصيص المدخلات بناءً على الشكل المختار
sc1, sc2, sc3 = st.columns(3)
b, h, d_out, d_in, t = 0, 0, 0, 0, 0

if selected_shape == "Square/Rectangle":
    b = sc1.number_input("العرض b (mm)", value=150.0)
    h = sc2.number_input("الارتفاع h (mm)", value=300.0)
    

elif selected_shape == "Hollow Tube (Rectangular)":
    b = sc1.number_input("العرض الخارجي B (mm)", value=200.0)
    h = sc2.number_input("الارتفاع الخارجي H (mm)", value=400.0)
    t = sc3.number_input("سمك الجدار t (mm)", value=10.0)
    

elif selected_shape == "Solid Cylinder":
    d_out = sc1.number_input("القطر D (mm)", value=100.0)
    

elif selected_shape == "Hollow Cylinder (Pipe)":
    d_out = sc1.number_input("القطر الخارجي D_out (mm)", value=120.0)
    d_in = sc2.number_input("القطر الداخلي d_in (mm)", value=100.0)
    

# --- إدخال النتائج ---
st.divider()
st.subheader("📤 تسليم النتائج النهائية")
res1, res2, res3 = st.columns(3)
st_I = res1.number_input("عزم القصور I (mm^4)", format="%.2e")
st_stress = res2.number_input("الإجهاد الأقصى (MPa)")
st_y = res3.number_input("بعد الألياف القصوى y (mm)")

theory_ans = st.text_area("اشرح باختصار تأثير شكل المقطع على توزيع الإجهادات:")
uploaded_file = st.file_uploader("ارفع صورة الحل اليدوي")

if st.button("إرسال الإجابة النهائية"):
    if student_name and student_id:
        st.balloons()
        st.success(f"تم استلام إجابتك بنجاح يا {student_name}. سيتم تدقيق الحل من قبل القسم.")
    else:
        st.warning("يرجى إكمال الاسم والرقم الجامعي قبل الإرسال.")

# تذييل الصفحة
st.markdown("""
<br><hr>
<p style="text-align: center; color: gray; font-size: 12px;">© 2026 جامعة النهرين - كلية الهندسة - قسم الهندسة المدنية</p>
""", unsafe_allow_html=True)