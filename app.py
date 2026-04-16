import streamlit as st
import pandas as pd
import pickle

# =========================
# Load Data
# =========================
df = pd.read_csv("books_marathi.csv")

# Clean column names if needed
df.columns = df.columns.str.strip()

# =========================
# Load Model
# =========================
with open("model.pkl", "rb") as f:
    model, version = pickle.load(f)

st.title("📚 Marathi Book Store App")
st.markdown(f"Model Version: **{version}**")

# =========================
# Sidebar - Book Selection
# =========================
st.sidebar.header("🛒 Order Book")

book_name = st.sidebar.selectbox("पुस्तक निवडा", df["पुस्तकाचे नाव"].unique())

selected_book = df[df["पुस्तकाचे नाव"] == book_name].iloc[0]

author = selected_book["लेखक"]
publisher = selected_book["प्रकाशक"]
price = selected_book["किंमत"]
discount_price = selected_book["सवलतीत किंमत"]

quantity = st.sidebar.number_input("Quantity", min_value=1, value=1)

# =========================
# Prediction (ML Model)
# =========================
# Prepare input same as training
input_df = pd.DataFrame({
    "पुस्तकाचे नाव": [book_name],
    "लेखक": [author],
    "प्रकाशक": [publisher]
})

input_encoded = pd.get_dummies(input_df)

# NOTE: Training columns match करणे आवश्यक
# Dummy alignment (important)
model_features = model.get_booster().feature_names
input_encoded = input_encoded.reindex(columns=model_features, fill_value=0)

predicted_price = model.predict(input_encoded)[0]

# =========================
# Display Book Info
# =========================
st.subheader("📖 Book Details")

st.write(f"**पुस्तक:** {book_name}")
st.write(f"**लेखक:** {author}")
st.write(f"**प्रकाशक:** {publisher}")

st.write(f"💰 Original Price: ₹{price}")
st.write(f"🔥 Discount Price: ₹{discount_price}")

st.write(f"🤖 Predicted Price (ML): ₹{round(predicted_price, 2)}")

# =========================
# Order Calculation
# =========================
total_price = discount_price * quantity

st.subheader("🧾 Order Summary")

st.write(f"Quantity: {quantity}")
st.write(f"Total Amount: ₹{total_price}")

# =========================
# Place Order Button
# =========================
if st.button("✅ Place Order"):
    st.success("🎉 Order Placed Successfully!")

    order_data = pd.DataFrame({
        "Book": [book_name],
        "Author": [author],
        "Publisher": [publisher],
        "Quantity": [quantity],
        "Unit Price": [discount_price],
        "Total": [total_price]
    })

    st.dataframe(order_data)

    # Download CSV
    csv = order_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Bill",
        data=csv,
        file_name="order_bill.csv",
        mime="text/csv"
    )


st.title("📚 राजहंस पुस्तक पेठ , पुणे ०३८")

st.markdown("### 🎉 ऑफर कालावधी : १६ एप्रिल ते १९ एप्रिल २०२६ पर्यन्त")
st.markdown("📲 WhatsApp Order Available")


import urllib.parse

if st.button("🟢 Order via WhatsApp"):

    phone_number = "919322630703"  # 91 + number (India)

    message = f"""
नमस्कार,

मला खालील पुस्तक ऑर्डर करायचे आहे:

📖 पुस्तक: {book_name}
✍️ लेखक: {author}
🏢 प्रकाशक: {publisher}

🔢 Quantity: {quantity}
💰 एकूण किंमत: ₹{total_price}

कृपया ऑर्डर कन्फर्म करा.
"""

    encoded_message = urllib.parse.quote(message)

    whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"

    st.success("👉 Click below to send order on WhatsApp")

    st.markdown(f"[📲 WhatsApp वर ऑर्डर करा]({whatsapp_url})", unsafe_allow_html=True)



st.markdown("""
<style>
.big-button {
    background-color: #25D366;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

customer_name = st.text_input("तुमचे नाव")

    address = st.text_area("पत्ता")


