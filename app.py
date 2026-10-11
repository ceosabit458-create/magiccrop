import streamlit as st
import datetime
from PIL import Image
from rembg import remove

# ১. পেজ সেটআপ
st.set_page_config(page_title="MagicCrop - AI Background Remover", page_icon="✂️")

# ২. ইউজারের স্টেট ও লিমিট ট্র্যাকিং (Session State)
if 'is_premium' not in st.session_state:
    st.session_state.is_premium = False
if 'photos_count' not in st.session_state:
    st.session_state.photos_count = 0
if 'last_reset' not in st.session_state:
    st.session_state.last_reset = datetime.datetime.now()

# ২৪ ঘণ্টা পর কাউন্টার রিসেট করার লজিক
now = datetime.datetime.now()
if (now - st.session_state.last_reset).total_seconds() > 86400:
    st.session_state.photos_count = 0
    st.session_state.last_reset = now

# ৩. সাইডবার: প্রিমিয়াম পেমেন্ট ও স্ট্যাটাস
st.sidebar.title("👑 MagicCrop Premium")

if st.session_state.is_premium:
    st.sidebar.success("🎉 আপনার প্রিমিয়াম এক্সেস চালু আছে (Unlimited)")
else:
    st.sidebar.warning(f"📊 ফ্রি ইউজার: আজকের ব্যবহার {st.session_state.photos_count}/6")
    st.sidebar.markdown("---")
    st.sidebar.subheader("মাত্র ৯৯ টাকায় ১ মাস আনলিমিটেড!")
    st.sidebar.write("Nagad (Send Money): **01963320934**")
    
    trx_id = st.sidebar.text_input("TrxID (ট্রানজেকশন আইডি) লিখুন:")
    if st.sidebar.button("ভেরিফাই ও প্রিমিয়াম অ্যাক্টিভ করুন"):
        if len(trx_id) >= 6:
            st.session_state.is_premium = True
            st.sidebar.success("অভিনন্দন! আপনার প্রিমিয়াম প্ল্যান চালু হয়েছে।")
            st.rerun()
        else:
            st.sidebar.error("সঠিক TrxID প্রদান করুন।")

# ৪. মেইন অ্যাপ হেডার
st.title("✂️ MagicCrop - AI Background Remover")

# ৫. ফ্রি ইউজারদের জন্য এডভারটাইজমেন্ট (Ad Banner)
if not st.session_state.is_premium:
    st.components.v1.html(
        """
        <div style="background-color: #f9f9f9; padding: 12px; text-align: center; border: 1px dashed #bbb; border-radius: 8px;">
            <p style="color: #666; margin: 0; font-size: 14px;">[ Google Ads / Advertisement Banner ]</p>
        </div>
        """,
        height=65
    )

st.markdown("---")

# ৬. ছবি আপলোড ও প্রসেসিং
uploaded_file = st.file_uploader("আপনার ছবি নির্বাচন করুন (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # লিমিট চেক (ফ্রি ইউজার ৬টি পার করলে ব্লক করবে)
    if not st.session_state.is_premium and st.session_state.photos_count >= 6:
        st.error("⚠️ আপনার আজকের ২৪ ঘণ্টার ফ্রি সীমা (৬/৬) শেষ হয়ে গেছে!")
        st.info("💡 আনলিমিটেড ছবি প্রসেস করতে বামপাশের সাইডবার থেকে ৯৯ টাকায় প্রিমিয়াম এক্সেস নিন।")
    else:
        if st.button("ব্যাকগ্রাউন্ড রিমুভ করুন"):
            with st.spinner("AI ব্যাকগ্রাউন্ড রিমুভ করছে..."):
                # রিমুভাল কাজ সম্পন্ন
                image = Image.open(uploaded_file)
                output_image = remove(image)
                
                # রেজাল্ট প্রদর্শন
                st.image(output_image, caption="ব্যাকগ্রাউন্ড রিমুভ করা ছবি", use_column_width=True)
                
                # ফ্রি ইউজার হলে কাউন্ট ১ বাড়ানো
                if not st.session_state.is_premium:
                    st.session_state.photos_count += 1
                    remaining = 6 - st.session_state.photos_count
                    st.success(f"সফল হয়েছে! আজকের বাকি ফ্রি সীমা: {remaining}/6")
        
