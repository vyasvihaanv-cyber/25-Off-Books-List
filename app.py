import streamlit as st
import pandas as pd
import urllib.parse
import os


# =========================
# HEADER (LOGO + TITLE)
# =========================
col1, col2 = st.columns([1,6])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=800)

with col2:
    st.markdown("<h2 style='margin-bottom:0;'>📚 राजहंस पुस्तक पेठ , पुणे ०३८</h2>", unsafe_allow_html=True)
    st.markdown("<small>🎉 ऑफर कालावधी : १६ एप्रिल ते १९ एप्रिल २०२६</small>", unsafe_allow_html=True)
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Book Store", layout="wide")

# =========================
# CSS (Professional UI)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER (LOGO + TITLE)
# =========================
col1, col2 = st.columns([1,6])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)

with col2:
    st.markdown("<h2>📚 राजहंस पुस्तक पेठ , पुणे ०३८</h2>", unsafe_allow_html=True)
    st.caption("🎉 ऑफर कालावधी : १६ एप्रिल ते १९ एप्रिल २०२६")

# =========================
# LOAD DATA
# =========================
if os.path.exists("books_marathi.csv"):
    df = pd.read_csv("books_marathi.csv")
else:
    st.error("❌ books_marathi.csv file नाही")
    st.stop()

# =========================
# SEARCH
# =========================
search = st.text_input("🔍 पुस्तक शोधा")

filtered_df = df.copy()
if search:
    filtered_df = filtered_df[
        filtered_df["पुस्तकाचे नाव"].str.contains(search, case=False)
    ]

# =========================
# SESSION STATE CART
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = {}

# =========================
# BOOK GRID
# =========================
st.markdown("## 📚 पुस्तके")

cols = st.columns(3)

for i, (_, row) in enumerate(filtered_df.iterrows()):
    col = cols[i % 3]

    book = row["पुस्तकाचे नाव"]
    author = row["लेखक"]
    publisher = row["प्रकाशक"]
    price = row["किंमत"]
    discount = row["सवलतीत किंमत"]


    with col:
        st.markdown(f"""
        <div class="card">
        <h4>{book}</h4>
        <p>✍️ {author}</p>
        <p style="color:green;font-weight:bold;">₹{price}</p>
        </div>
        """, unsafe_allow_html=True)

        # Initialize qty
        if book not in st.session_state.cart:
            st.session_state.cart[book] = {"qty": 0, "price": price}

        c1, c2, c3 = st.columns([1,1,1])

        # ➖
        with c1:
            if st.button("➖", key=f"minus_{i}"):
                if st.session_state.cart[book]["qty"] > 0:
                    st.session_state.cart[book]["qty"] -= 1

        # Qty display
        with c2:
            st.markdown(
                f"<h4 style='text-align:center'>{st.session_state.cart[book]['qty']}</h4>",
                unsafe_allow_html=True
            )

        # ➕
        with c3:
            if st.button("➕", key=f"plus_{i}"):
                st.session_state.cart[book]["qty"] += 1

# =========================
# CART DISPLAY
# =========================
st.markdown("## 🛒 Cart")

total = 0
has_items = False

for book, item in st.session_state.cart.items():
    if item["qty"] > 0:
        has_items = True
        item_total = item["qty"] * item["price"]
        total += item_total

        st.write(f"📚 {book} | Qty: {item['qty']} | ₹{item_total}")

if not has_items:
    st.info("Cart रिकामा आहे")

st.markdown(f"### 💰 Total: ₹{total}")

# =========================
# CUSTOMER INFO
# =========================
st.markdown("## 👤 तुमची माहिती")

col3, col4 = st.columns(2)

with col3:
    name = st.text_input("नाव")

with col4:
    mobile = st.text_input("मोबाईल नंबर")

# =========================
# WHATSAPP ORDER
# =========================
if st.button("🟢 WhatsApp वर ऑर्डर करा"):

    if not has_items:
        st.warning("Cart रिकामा आहे")
    elif name == "" or mobile == "":
        st.warning("कृपया नाव आणि मोबाईल नंबर भरा")
    else:
        message = "नमस्कार 🙏\n\nमला खालील पुस्तके हवी आहेत:\n\n"

        for book, item in st.session_state.cart.items():
            if item["qty"] > 0:
                amt = item["qty"] * item["price"]
                message += f"📚 {book} (Qty: {item['qty']}) - ₹{amt}\n"

        message += f"\n💰 Total: ₹{total}"
        message += f"\n👤 नाव: {name}"
        message += f"\n📞 मोबाईल: {mobile}"

        phone = "919322630703"
        url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"

        st.success("👇 WhatsApp वर ऑर्डर पाठवा")
        st.markdown(f"[📲 WhatsApp वर क्लिक करा]({url})")

# =========================
# CLEAR CART
# =========================
if st.button("🗑️ Clear Cart"):
    st.session_state.cart = {}
    st.rerun()
