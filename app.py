import streamlit as st
import pandas as pd
import urllib.parse
import os

import os

col1, col2 = st.columns([1,5])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)

with col2:
    st.markdown("<h2>राजहंस पुस्तक पेठ , पुणे ०३८</h2>", unsafe_allow_html=True)
    st.markdown("🎉 ऑफर कालावधी : १६ एप्रिल ते १९ एप्रिल २०२६ पर्यन्त")
    
# =========================
# SHOP INFO
# =========================
st.title("📚 राजहंस पुस्तक पेठ , पुणे ०३८")
st.markdown("### 🎉 ऑफर कालावधी : १६ एप्रिल ते १९ एप्रिल २०२६ पर्यन्त")
st.markdown("📲 WhatsApp वरून थेट ऑर्डर करा")

# =========================
# LOAD DATA (SAFE)
# =========================
if os.path.exists("books_marathi.csv"):
    df = pd.read_csv("books_marathi.csv")
else:
    st.error("❌ books_marathi.csv file नाही")
    st.stop()

# =========================
# USER INPUT
# =========================
st.header("🛒 ऑर्डर करा")

book_name = st.selectbox("पुस्तक निवडा", df["पुस्तकाचे नाव"])

selected = df[df["पुस्तकाचे नाव"] == book_name].iloc[0]

author = selected["लेखक"]
publisher = selected["प्रकाशक"]
price = selected["किंमत"]
discount = selected["सवलतीत किंमत"]

quantity = st.number_input("Quantity", 1, 10, 1)

# =========================
# DISPLAY BOOK
# =========================
st.subheader("📖 पुस्तक माहिती")

st.write(f"**पुस्तक:** {book_name}")
st.write(f"**लेखक:** {author}")
st.write(f"**प्रकाशक:** {publisher}")

st.write(f"💰 मूळ किंमत: ₹{price}")
st.write(f"🔥 सवलतीत: ₹{discount}")

# =========================
# TOTAL
# =========================
total = discount * quantity

st.subheader("🧾 एकूण")

st.write(f"Quantity: {quantity}")
st.write(f"Total: ₹{total}")

# =========================
# CUSTOMER INFO
# =========================
st.subheader("👤 तुमची माहिती")

name = st.text_input("नाव")
mobile = st.text_input("मोबाईल नंबर WhatsApp")
address = st.text_input("पत्ता")
# =========================
# WHATSAPP ORDER
# =========================
if st.button("🟢 WhatsApp वर ऑर्डर करा"):

    if name == "" or mobile == "":
        st.warning("कृपया नाव आणि मोबाईल नंबर भरा")
    else:
        phone = "919322630703"

        message = f"""
नमस्कार 🙏

मी {name} बोलत आहे.

📚 ऑर्डर तपशील:
पुस्तक: {book_name}
लेखक: {author}
प्रकाशक: {publisher}

संख्या: {quantity}
एकूण रक्कम: ₹{total}

📞 मोबाईल: {mobile}

कृपया ऑर्डर कन्फर्म करा. 
धन्यवाद 🙏

"""

        url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

        st.success("👇 खाली क्लिक करा आणि WhatsApp वर ऑर्डर पाठवा")

        st.markdown(f"[📲 WhatsApp वर ऑर्डर पाठवा]({url})")



# Save order to CSV
order_data = pd.DataFrame([{
    "Name": name,
    "Mobile": mobile,
    "Book": book_name,
    "Author": author,
    "Publisher": publisher,
    "Quantity": quantity,
    "Total": total
}])

if os.path.exists("orders.csv"):
    order_data.to_csv("orders.csv", mode='a', header=False, index=False)
else:
    order_data.to_csv("orders.csv", index=False)



