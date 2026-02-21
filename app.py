import streamlit as st
import cohere
import os

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="Khoy AlDarb | خوي الدرب", page_icon=None)# إخفاء الأسهم والقائمة الجانبية تماماً
st.markdown("""
    <style>
    [data-testid="collapsedControl"] { display: none; }
    section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. اللوجو والتحكم بالثيم (محمي من خطأ NoneType)
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    st.image("khdrblogo.jpg", use_container_width=True)
    
    # اختيار الثيم بشكل مباشر
   # اختيار الثيم بشكل مباشر
    theme_choice = st.segmented_control(
        "اختر جوك يالذيب:",
        options=["🌙 وضع الليل", "☀️ وضع النهار"],
        default="🌙 وضع الليل"
    )
    
    # التأكد من عدم وجود قيمة فارغة
    if theme_choice is None:
        theme_choice = "🌙 وضع الليل"
        
    # تعريف المتغير (تأكد أن هذا السطر موجود قبل سطر if dark_mode)
    dark_mode = True if "🌙" in theme_choice else False

# 3. إعدادات الألوان (هنا سطر 34 اللي فيه المشكلة)
if dark_mode:
    bg_color = "#0f172a"
    # ... بقية الكود
        

# 3. إعدادات الألوان
if dark_mode:
    bg_color = "#0f172a"
    text_color = "#ffffff"
    chat_bg = "#1e293b"
    chat_text = "#f8fafc"
else:
    bg_color = "#f8fafc"
    text_color = "#0f172a"
    chat_bg = "#ffffff"
    chat_text = "#1e293b"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="st-"] {{ font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }}
    .stApp {{ background-color: {bg_color}; color: {text_color}; }}
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {{ display: none !important; }}
    .main-header {{ background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); padding: 1rem; border-radius: 20px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px; }}
    [data-testid="stChatMessage"] {{ background-color: {chat_bg} !important; border: 1px solid rgba(0,0,0,0.1); border-radius: 15px !important; margin-bottom: 10px; }}
    [data-testid="stChatMessageContent"] p {{ color: {chat_text} !important; font-size: 1.1rem; font-weight: 500; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>⛺ خوي الدرب</h1><p>تطوير: مازن الشمري</p></div>', unsafe_allow_html=True)

# 4. ربط API Cohere
api_key = "Zb5IsbR1FgG0MW2mDnIXdieerAkoSNRUPe4JUFgC"
co = cohere.ClientV2(api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# دالة الرد (هنا التعديل ليصبح عالمياً)
def call_cohere(prompt):
    try:
        response = co.chat(
            model="command-r-08-2024",
            messages=[
                {
                    "role": "system", 
                    "content": "أنت 'خوي الدرب'، خبير سياحي عالمي ملم بكل دول العالم ووجهاتها. رد على المستخدم بلهجة سعودية بيضاء وفزعة، وناده دائماً بلقب 'الذيب'. قدم له نصائح دقيقة عن السفر، الفنادق، والفعاليات في أي دولة يطلبها (سواء داخل السعودية أو في أوروبا، آسيا، أمريكا، إلخ)."
                },
                {"role": "user", "content": prompt}
            ]
        )
        return response.message.content[0].text
    except Exception as e:
        return f"يا ذيبان، السيرفر يبي له تشييك: {str(e)}"

# 6. التفاعل
if prompt := st.chat_input("وين نوينا يالذيب؟ (اكتب أي مكان بالعالم)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("خوي الدرب يلف العالم عشانك..."):
            res = call_cohere(prompt)
            st.markdown(res)

            st.session_state.messages.append({"role": "assistant", "content": res})




