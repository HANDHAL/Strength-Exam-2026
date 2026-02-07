import streamlit as st
import pandas as pd
import math

# --- إعدادات الصفحة ---
st.set_page_config(page_title="جامعة النهرين - نظام الاختبار الذكي", layout="centered")

# --- الترويسة ---
st.markdown("""
<div style="text-align: right; dir: rtl; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-right: 5px solid #1f77b4;">
    <h2 style="margin: 0; color: #1f77b4;">جامعة النهرين - كلية الهندسة</h2>
    <h3 style="margin: 0; color: #333;">قسم الهندسة المدنية</h3>
    <p style="margin: 0; color: #666;">مادة مقاومة المواد - اختبار الالتواء (Torsion)</p>
</div>
<br>
""", unsafe_allow_html=True)

# --- إدارة الحالة (بيانات المسألة المرفوعة) ---
if 'exam_text' not in st.session_state:
    st.session_state['exam_text'] = """Find $T_2$ that causes no rotation at C when $T_1$ is applied at B.
    Given:
    - $G_s = 12 \times 10^6$ psi
    - $G_c = 6 \times 10^6$ psi
    - Outer Diameter $D = 2$ in, Inner Diameter $d = 1.5$ in"""

# --- لوحة المسؤول (المخفية) ---
with st.sidebar:
    st.header("🔐 لوحة الإدارة")
    admin_key = st.text_input("رمز الدخول", type="password")
    if admin_key == "prof2026":
        st.success("وضع الإدارة مفعل")
        st.session_state['active_topic'] = "Torsion"
        st.session_state['exam_text'] = st.text_area("نص السؤال:", value=st.session_state['exam_text'])
        # هنا يتم تخزين الحل الصحيح للمقارنة لاحقاً
        st.number_input("الجواب الصحيح لـ T2 (للتحقق التلقائي)", value=0.0, key="correct_ans")

# --- عرض السؤال للطالب ---
st.info("### 📝 السؤال المطروح")
st.write(st.session_state['exam_text'])
# يمكنك استبدال الرابط أدناه برابط الصورة المرفوعة أو المسار المحلي
st.image("https://example.com/torsion_problem.png", caption="الشكل التوضيحي للمسألة (Torsion Example)")

st.divider()

# --- بيانات الطالب ---
with st.container():
    c1, c2 = st.columns(2)
    student_name = c1.text_input("الاسم الثلاثي")
    student_id = c2.text_input("الرقم الجامعي")

# --- جزء الحسابات الهندسية (التفاعلي) ---
st.subheader("📐 خطوات الحل والحسابات")

col_a, col_b = st.columns(2)

with col_a:
    st.write("**1. خصائص المقطع (Section Properties)**")
    d_outer = st.number_input("القطر الخارجي D (in)", value=2.0)
    d_inner = st.number_input("القطر الداخلي d (in)", value=1.5)
    
    # حساب J تلقائياً لتعزيز ذكاء التطبيق
    j_val = (math.pi / 32) * (d_outer**4 - d_inner**4)
    st.caption(f"قيمة $J$ المحسوبة للمقطع: {j_val:.4f} $in^4$")

with col_b:
    st.write("**2. القيم المدخلة للحل**")
    st_t1 = st.number_input("قيمة $T_1$ المعطاة (lb.in)", value=0.0)
    st_t2_ans = st.number_input("قيمة $T_2$ النهائية (lb.in)", value=0.0)

# --- التحقق النهائي ---
st.divider()
if st.button("إرسال الإجابة النهائية"):
    if not student_name or not student_id:
        st.error("الرجاء إكمال البيانات الأساسية قبل الإرسال")
    else:
        # منطق التحقق (Simple Check)
        st.balloons()
        st.success(f"تم استلام إجابة الطالب: {student_name}")
        
        # عرض ملخص سريع للطالب
        with st.expander("استعراض ملخص الحل المرسل"):
            st.write(f"القطر الخارجي: {d_outer} in")
            st.write(f"عزم القصور الذاتي القطبي (J): {j_val:.4f} in⁴")
            st.write(f"قيمة T2 التي أدخلتها: {st_t2_ans}")

st.markdown("<p style='text-align: center; color: #999; font-size: 12px;'>قسم الهندسة المدنية - جامعة النهرين © 2026</p>", unsafe_allow_html=True)