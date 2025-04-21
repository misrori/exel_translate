import streamlit as st
import pandas as pd
from googletrans import Translator
from io import BytesIO

st.set_page_config(page_title="Excel Fordító", layout="centered")
st.title("📄 Excel Fordító magyar → orosz")

uploaded_file = st.file_uploader("Tölts fel egy Excel fájlt (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 Eredeti táblázat")
    st.dataframe(df)

    if st.button("🔁 Fordítás oroszra"):
        translator = Translator()

        def translate_cell(x):
            try:
                return translator.translate(x, src='hu', dest='ru').text if isinstance(x, str) else x
            except:
                return x  # Hiba esetén hagyja eredetiben

        translated_df = df.applymap(translate_cell)

        st.subheader("🌐 Lefordított táblázat")
        st.dataframe(translated_df)

        # Letölthető fájl előkészítése
        output = BytesIO()
        translated_df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)

        st.download_button(
            label="📥 Letöltés orosz Excel fájl",
            data=output,
            file_name="forditott_igazolas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
