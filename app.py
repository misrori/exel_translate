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

    # Oszlopválasztó: csak szöveges típusú oszlopokat ajánl fel
    text_cols = [col for col in df.columns if df[col].dtype == object]
    selected_cols = st.multiselect(
        "Válaszd ki, mely oszlopokat fordítsa le (csak szöveges oszlopok):",
        options=text_cols,
        default=text_cols
    )

    if st.button("🔁 Fordítás oroszra"):
        translator = Translator()

        # Fejléc fordítása
        def translate_header(header):
            try:
                return translator.translate(header, src='hu', dest='ru').text
            except:
                return header

        new_columns = [translate_header(col) for col in df.columns]

        # Csak a kiválasztott oszlopokat fordítja le cellánként
        translated_df = df.copy()
        for col in selected_cols:
            translated_df[col] = translated_df[col].apply(
                lambda x: translator.translate(x, src='hu', dest='ru').text if isinstance(x, str) else x
            )
        translated_df.columns = new_columns

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
