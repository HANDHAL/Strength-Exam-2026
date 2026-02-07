import streamlit as st
import pandas as pd
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="جامعة النهرين - قسم الهندسة المدنية", layout="centered")

# --- الترويسة النصية الرسمية ---
st.markdown("""
<div style="text-align: right; dir: rtl; line-height: 1.2; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-right: 5px solid #1f77b4;">
    <h2 style="margin: 0; color: #1f77b4;">جامعة النهرين - كلية الهندسة</h2>
    <h3 style="margin: 0; color: #333;">قسم الهندسة المدنية</h3>
    <p style="margin: 0; font-size: 16px; color: #666;">نظام الاختبارات الإلكتروني الذكي</p>
</div>
<br>
""", unsafe_allow_html=True)

# --- إدارة الحالة (لوحة التحكم) ---
if 'exam_image' not in st.session_state: st.session_state['exam_image'] = None
if 'exam_text' not in st.session_state: st.session_state['exam_text'] = ""
if 'active_topic' not in st.session_state: st.session_state['active_topic'] = "Bending Stress"

with st.sidebar:
    st.header("🔐 لوحة إدارة الاختبار")
    admin_key = st.text_input("رمز الدخول للمسؤول", type="password")
    
    if admin_key == "prof2026":
        st.success("وضع الإدارة مفعل")
        st.session_state['active_topic'] = st.selectbox("اختر الموضوع:", ["Bending Stress", "Torsion", "Shear Stress"])
        
        st.write("---")
        st.write("**تجهيز محتوى السؤال:**")
        st.session_state['exam_text'] = st.text_area("اكتب نص السؤال هنا:", value=st.session_state['exam_text'])
        uploaded_q_image = st.file_uploader("ارفع صورة المسألة:", type=['png', 'jpg', 'jpeg'])
        if uploaded_q_image:
            st.session_state['exam_image'] = uploaded_q_image
        
        if st.button("تحديث الاختبار للطلاب"):
            st.toast("تم تحديث محتوى الاختبار بنجاح!")

# --- واجهة الطالب ---
if st.session_state['exam_text'] or st.session_state['exam_image']:
    st.warning(f"📝 الموضوع الحالي: {st.session_state['active_topic']}")
    if st.session_state['exam_text']:
        st.info(st.session_state['exam_text'])
    if st.session_state['exam_image']:
        st.image(st.session_state['exam_image'], caption="رسم توضيحي للمسألة")

st.divider()

# بيانات الطالب
c_s1, c_s2 = st.columns(2)
student_name = c_s1.text_input("الاسم الثلاثي للطالب")
student_id = c_s2.text_input("الرقم الجامعي")

# اختيار المقطع
st.subheader("📐 أبعاد المقطع العرضي المختارة")
shape = st.selectbox("اختر شكل المقطع العرضي:", 
                     ["Rectangle", "Solid Circle", "Hollow Circle", "I-Section", "C-Channel"])

# حقول إدخال الأبعاد بناءً على الشكل المختار (هذا الجزء أصلح الخطأ)
sc1, sc2, sc3 = st.columns(3)
if shape == "Rectangle":
    
    b_dim = sc1.number_input("العرض b (mm)", value=0.0)
    h_dim = sc2.number_input("الارتفاع h (mm)", value=0.0)
elif shape == "I-Section":
    
    bf = sc1.number_input("Flange Width (mm)", value=0.0)
    tf = sc2.number_input("Flange Thickness (mm)", value=0.0)
    hw = sc3.number_input("Web Height (mm)", value=0.0)
elif shape == "C-Channel":
    
    bc = sc1.number_input("Channel Width (mm)", value=0.0)
    hc = sc2.number_input("Total Height (mm)", value=0.0)
    tc = sc3.number_input("Thickness (mm)", value=0.0)
elif shape == "Hollow Circle":
    
    do = sc1.number_input("Outer Diameter (mm)", value=0.0)
    di = sc2.number_input("Inner Diameter (mm)", value=0.0)
elif shape == "Solid Circle":
    
    ds = sc1.number_input("Diameter D (mm)", value=0.0)

# حقول إدخال النتائج الهندسية
st.write("---")
st.write("**النواتج النهائية (Reactions & Results):**")
r1, r2 = st.columns(2)
st_ra = r1.number_input("Reaction at A (kN)", format="%.2f")
st_rb = r2.number_input("Reaction at B (kN)", format="%.2f")

if st.session_state['active_topic'] == "Shear Stress":
    
    res_c1, res_c2, res_c3 = st.columns(3)
    area = res_c1.number_input("Area A (mm²)")
    thickness = res_c2.number_input("Thickness t (mm)")
    product = res_c3.number_input("Product (A * t)")
    shear_res = st.number_input("Final Shear Stress (MPa)")
elif st.session_state['active_topic'] == "Torsion":
    
    t1, t2 = st.columns(2)
    st_j = t1.number_input("Polar Moment J (mm⁴)")
    st_angle = t2.number_input("Angle of Twist (rad)")
else: # Bending
    
    b1, b2 = st.columns(2)
    st_i = b1.number_input("Moment of Inertia I (mm⁴)")
    st_bend = b2.number_input("Max Bending Stress (MPa)")

st.divider()
student_file = st.file_uploader("ارفع ملف الحل الورقي")

if st.button("إرسال الإجابة النهائية"):
    if student_name and student_id:
        st.success(f"تم الإرسال بنجاح للطالب: {student_name}")
        st.balloons()
    else:
        st.error("الرجاء إدخال الاسم والرقم الجامعي")

st.markdown("<p style='text-align: center; color: #999; font-size: 12px;'>قسم الهندسة المدنية - جامعة النهرين © 2026</p>", unsafe_allow_html=True)