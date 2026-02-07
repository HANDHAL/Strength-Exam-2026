import streamlit as st
import pandas as pd
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="جامعة النهرين - قسم الهندسة المدنية", layout="centered")

# --- الترويسة النصية الرسمية (بدون شعار) ---
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
        uploaded_q_image = st.file_uploader("ارفع صورة المسألة (أحمال، أبعاد...):", type=['png', 'jpg', 'jpeg'])
        if uploaded_q_image:
            st.session_state['exam_image'] = uploaded_q_image
        
        if st.button("تحديث الاختبار للطلاب"):
            st.toast("تم تحديث محتوى الاختبار بنجاح!")

# --- واجهة الطالب ---
if st.session_state['exam_text'] or st.session_state['exam_image']:
    st.warning(f"📝 السؤال الحالي: {st.session_state['active_topic']}")
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
st.subheader("📐 أدوات الحل")
shape = st.selectbox("اختر شكل المقطع العرضي للمسألة:", 
                     ["Rectangle", "Solid Circle", "Hollow Circle", "I-Section", "C-Channel"])

# عرض صور توضيحية للمقاطع المختارة
if shape == "I-Section":
    
elif shape == "C-Channel":
    
elif shape == "Hollow Circle":
    

# حقول إدخال النتائج
st.write("---")
st.write("**النواتج النهائية لردود الأفعال والحسابات:**")
r1, r2 = st.columns(2)
st_ra = r1.number_input("Reaction at A (kN)")
st_rb = r2.number_input("Reaction at B (kN)")

if st.session_state['active_topic'] == "Shear Stress":
    
    sc1, sc2, sc3 = st.columns(3)
    area = sc1.number_input("Area A (mm²)")
    thickness = sc2.number_input("Thickness t (mm)")
    product = sc3.number_input("Result of (A * t)")
    shear_final = st.number_input("Final Shear Stress (MPa)")

elif st.session_state['active_topic'] == "Torsion":
    
    tc1, tc2 = st.columns(2)
    st_j = tc1.number_input("Polar Moment J (mm⁴)")
    st_angle = tc2.number_input("Angle of Twist (rad)")

else: # Bending
    
    bc1, bc2 = st.columns(2)
    st_i = bc1.number_input("Moment of Inertia I (mm⁴)")
    st_bending = bc2.number_input("Max Bending Stress (MPa)")

st.divider()
student_file = st.file_uploader("ارفع ملف الحل الورقي")

if st.button("إرسال الإجابة النهائية للقسم"):
    if student_name and student_id:
        st.success(f"تم بنجاح استلام إجابة الطالب: {student_name}")
        st.balloons()
    else:
        st.error("الرجاء إدخال الاسم والرقم الجامعي")

st.markdown("<p style='text-align: center; color: #999; font-size: 12px;'>قسم الهندسة المدنية - جامعة النهرين © 2026</p>", unsafe_allow_html=True)