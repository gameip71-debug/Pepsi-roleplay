import streamlit as st
from anthropic import Anthropic

# 1. ตั้งค่าหน้าเว็บให้สวยงาม
st.set_page_config(page_title="Pepsi Sales Training AI", page_icon="🥤", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #004B87; text-align: center; }
    .sub-title { font-size: 18px; text-align: center; color: #555; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🥤 PepsiCo Sales Role-Play AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ด่านทดสอบ: ขจัดข้อโต้แย้ง "เฮียเส็ง ร้านโชห่วยสายเชียร์โค้ก"</p>', unsafe_allow_html=True)

# 2. แถบข้างสำหรับใส่ API Key
st.sidebar.header("⚙️ การตั้งค่าระบบ")
api_key = st.sidebar.text_input("ใส่ Anthropic API Key ของคุณ:", type="password")

# 3. กำหนด System Prompt (บทบาทเฮียเส็ง)
SYSTEM_PROMPT = """
คุณคือ 'เฮียเส็ง' เจ้าของร้านขายของชำขนาดใหญ่ (โชห่วย) ที่เปิดมานานกว่า 20 ปี
นิสัย: พูดจาตรงๆ ขวานผ่าซาก ขี้เหนียว เน้นกำไรและความสะดวกของตัวเองเป็นหลัก 

บริบทและทัศนคติของคุณ:
1. ร้านคุณขายดีทั้งคู่ แต่คุณสนิทกับเซลล์ 'โค้ก' มากกว่า เพราะเขามาหาบ่อย มีของแถมให้ตลอด
2. คุณมีความเชื่อว่า 'โค้ก' แบรนด์แข็งกว่า คนสั่ง "โค้ก" บ่อยกว่าสั่ง "เป๊ปซี่" 
3. คุณไม่อยากเพิ่มพื้นที่ตู้แช่ให้เป๊ปซี่ เพราะเปลืองไฟ และคิดว่าตู้เดิมที่มีก็พอแล้ว

ข้อโต้แย้งหลักที่คุณจะเอาไว้ใช้ไล่บี้เซลล์เป๊ปซี่ (หยิบมาใช้ทีละข้อตามความเหมาะสม):
- "โอ๊ย ไม่เอาเพิ่มหรอก ลูกค้ามาซื้อทีไรก็สั่งแต่โค้กๆๆ เป๊ปซี่เอามาก็จมทุน แช่เย็นก็เปลืองค่าไฟร้าน"
- "เซลล์โค้กเขาเพิ่งมาจัดโปรโมชั่นแถมของให้เฮียเนี่ย แล้วเป๊ปซี่มีอะไรให้บ้างล่ะ? ถ้าไม่มีข้อเสนอดีกว่าก็ไม่ต้องลง"
- "ตู้แช่ร้านเฮียเต็มหมดแล้ว ไม่มีที่ลงหรอก ไม่อยากได้ตู้แช่เป๊ปซี่เพิ่มด้วย เกะกะหน้าร้าน เปลืองไฟ"

เงื่อนไขการ Role Play:
1. สวมบทบาทเป็นเฮียเส็งอย่างเคร่งครัด ตอบโต้สั้นๆ สมจริง (ไม่เกิน 2 ประโยคต่อครั้ง) ภาษาไทยสไตล์คนไทยเชื้อสายจีนโชห่วย
2. เริ่มต้นบทสนทนาด้วยการปฏิเสธ หรือแสดงท่าทีไม่อยากคุยก่อน เช่น "อ้าว มาอีกแล้วเรรอ บอกแล้วไงว่าช่วงนี้ไม่ลงเพิ่ม โค้กยังเต็มตู้อยู่เลย"
3. หากเซลล์ยื่นข้อเสนอที่ปฏิเสธไม่ได้จริงๆ หรือโน้มน้าวใจได้ดี ถึงจะยอมใจอ่อนแบ่งพื้นที่ในตู้ให้ หรือยอมสั่งเพิ่ม
"""

if api_key:
    client = Anthropic(api_key=api_key)

    # สร้างคลังเก็บข้อมูลในหน้าเว็บ
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "evaluation" not in st.session_state:
        st.session_state.evaluation = ""

    # ปุ่มรีเซ็ตเริ่มคุยใหม่ และ ปุ่มกดตรวจคะแนน
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 เริ่มคุยใหม่"):
            st.session_state.messages = []
            st.session_state.evaluation = ""
            st.rerun()
    with col2:
        if st.button("📊 ประเมินผล"):
            if len(st.session_state.messages) > 1:
                with st.spinner("เฮียเส็งกำลังตรวจคำพูดคุณอยู่นะ..."):
                    # ส่งประวัติทั้งหมดไปให้ Claude วิเคราะห์คะแนน
                    eval_prompt = f"กรุณาประเมินผลการขายของเซลล์เป๊ปซี่จากประวัติการสนทนานี้ ให้คะแนนเต็ม 10 และวิเคราะห์จุดดี 3 ข้อ จุดที่ต้องปรับปรุง 3 ข้อ โดยอ้างอิงจากหลักการขจัดข้อโต้แย้งอย่างมืออาชีพ ประวัติการคุย: {str(st.session_state.messages)}"
                    eval_response = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=1500,
                        messages=[{"role": "user", "content": eval_prompt}]
                    )
                    st.session_state.evaluation = eval_response.content.text
            else:
                st.sidebar.warning("ต้องคุยกันอย่างน้อย 1 ประโยคก่อนเปิดตรวจคะแนนครับ")

    # แสดงผลรายงานการประเมินคะแนน (ถ้ามี)
    if st.session_state.evaluation:
        st.success("📝 ผลการประเมินการฝึกอบรมจาก AI")
        st.write(st.session_state.evaluation)
        st.markdown("---")

    # ทักทายประโยคแรกอัตโนมัติจากเฮียเส็ง
    if len(st.session_state.messages) == 0:
        initial_text = "ลื้อมาอีกแล้วเรรอเซลล์เป๊ปซี่? บอกแล้วไงว่าช่วงนี้ไม่ลงเพิ่ม โค้กยังเต็มตู้ขายดีอยู่เลย มีธุระอะไรอีกเนี่ย!"
        st.session_state.messages.append({"role": "assistant", "content": initial_text})

    # แสดงแชทบนหน้าจอ
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ช่องพิมพ์ข้อความตอบโต้ของเซลล์
    if user_input := st.chat_input("พิมพ์บทสนทนาโต้ตอบเฮียเส็งที่นี่..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # ส่งข้อความไปหา Claude ให้ตอบในบทเฮียเส็ง
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.7,
                system=SYSTEM_PROMPT,
                messages=api_messages
            )
            
            ai_response = response.content.text
            message_placeholder.markdown(ai_response)
            
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

else:
    st.info("💡 โปรดใส่ Anthropic API Key ของคุณที่แถบด้านซ้ายเพื่อเปิดใช้งานระบบบอท")
