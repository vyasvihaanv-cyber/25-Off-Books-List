import streamlit as st
import pandas as pd
import urllib.parse
import os

import os

col1, col2 = st.columns([1,5])

with col1:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=800)


    
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
      पत्ता: {address}
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



#step1

st.markdown("## 🔍 पुस्तके शोधा")

search = st.text_input("Search book...")

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["पुस्तकाचे नाव"].str.contains(search, case=False)
    ]

#step2



if "cart" not in st.session_state:
    st.session_state.cart = []

if "wishlist" not in st.session_state:
    st.session_state.wishlist = []



#step3

st.markdown("## 📚 पुस्तके")

cols = st.columns(3)  # 3 books per row

for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 3]

    with col:
        st.markdown(f"""
        <div style="background:white;padding:15px;border-radius:10px;
        box-shadow:0 4px 10px rgba(0,0,0,0.1);margin-bottom:15px">
        
        <h4>{row['पुस्तकाचे नाव']}</h4>
        <p>✍️ {row['लेखक']}</p>
        <p>🏢 {row['प्रकाशक']}</p>

        <p style="text-decoration:line-through;color:gray;">₹{row['किंमत']}</p>
        <p style="color:green;font-weight:bold;">₹{row['सवलतीत किंमत']}</p>

        </div>
        """, unsafe_allow_html=True)

        # Add to Cart
        if st.button(f"🛒 Add", key=f"cart_{i}"):
            st.session_state.cart.append(row.to_dict())

        # Wishlist
        if st.button(f"❤️ Wishlist", key=f"wish_{i}"):
            st.session_state.wishlist.append(row.to_dict())

#step4
st.markdown("## 🛒 Cart")

total = 0

if len(st.session_state.cart) == 0:
    st.info("Cart रिकामा आहे")
else:
    for item in st.session_state.cart:
        st.write(f"📚 {item['पुस्तकाचे नाव']} - ₹{item['सवलतीत किंमत']}")
        total += item["सवलतीत किंमत"]

    st.markdown(f"### 💰 Total: ₹{total}")

#step5
st.markdown("## ❤️ Wishlist")

if len(st.session_state.wishlist) == 0:
    st.info("Wishlist रिकामी आहे")
else:
    for item in st.session_state.wishlist:
        st.write(f"📚 {item['पुस्तकाचे नाव']}")

#step6
import urllib.parse

if st.button("🟢 WhatsApp Order (Cart)"):

    if len(st.session_state.cart) == 0:
        st.warning("Cart रिकामा आहे")
    else:
        message = "नमस्कार 🙏\n\nमला खालील पुस्तके हवी आहेत:\n\n"

        for item in st.session_state.cart:
            message += f"📚 {item['पुस्तकाचे नाव']} - ₹{item['सवलतीत किंमत']}\n"

        message += f"\n💰 Total: ₹{total}"

        phone = "919322630703"
        url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

        st.markdown(f"[📲 WhatsApp वर ऑर्डर करा]({url})")


#step7
if row['पुस्तकाचे नाव'] not in [x['पुस्तकाचे नाव'] for x in st.session_state.cart]:


$#if row['पुस्तकाचे नाव'] not in [x['पुस्तकाचे नाव'] for x in st.session_state.cart]:
