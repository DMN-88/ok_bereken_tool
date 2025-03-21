# main.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from normen import ruimte_classificatie_normen
from berekeningen import (
    bereken_luchtdebiet,
    bereken_warmtevermogen,
    bereken_bevochtiging,
    bereken_conditioneringsvermogen,
    bereken_hersteltijd
)
from export import export_to_excel, export_to_pdf

st.set_page_config(page_title="OK Bereken Tool", layout="wide")
st.title("📟 OK-complex Lucht- & Klimaatberekening")

keuze = st.sidebar.radio("Kies methode", ["🔹 Methode 1 – Basis", "🔸 Methode 2 – Geavanceerd"])

buitencondities = {
    "Zomer": {"temp": 28, "rv": 60},
    "Winter": {"temp": -5, "rv": 35},
    "Voorjaar / Najaar": {"temp": 15, "rv": 45}
}

ruimte_types = list(ruimte_classificatie_normen.keys())

# ========== METHODE 1 ==========
if keuze == "🔹 Methode 1 – Basis":
    st.subheader("🔹 Methode 1 – Basis luchtdebiet en vermogen")
    aantal_ruimtes = st.number_input("Aantal ruimtes", min_value=1, value=2)
    ruimte_data = []

    for i in range(aantal_ruimtes):
        st.markdown(f"#### Ruimte {i+1}")
        naam = st.text_input("Ruimtenaam", value=f"Ruimte {i+1}", key=f"naam_b_{i}")
        opp = st.number_input("Oppervlakte (m²)", value=30.0, key=f"opp_b_{i}")
        hoogte = st.number_input("Hoogte (m)", value=3.0, key=f"hoogte_b_{i}")
        wisselingen = st.number_input("Luchtwisselingen per uur", value=6, key=f"wissel_b_{i}")
        personen = st.number_input("Aantal personen", min_value=0, value=2, key=f"pers_b_{i}")

        volume, debiet_ruimte = bereken_luchtdebiet(opp, hoogte, wisselingen)
        debiet_personen = personen * 30  # 30 m³/h per persoon
        totaal_debiet = max(debiet_ruimte, debiet_personen)

        koelvermogen = bereken_conditioneringsvermogen(totaal_debiet, 8)
        warmvermogen = bereken_conditioneringsvermogen(totaal_debiet, 12)

        ruimte_data.append({
            "Ruimte": naam,
            "Opp (m²)": opp,
            "Hoogte (m)": hoogte,
            "Volume (m³)": round(volume, 1),
            "Luchtwisselingen": wisselingen,
            "Personen": personen,
            "Debiet ruimte (m³/h)": round(debiet_ruimte),
            "Debiet personen (m³/h)": round(debiet_personen),
            "Luchtdebiet totaal (m³/h)": round(totaal_debiet),
            "Koelvermogen (kW)": koelvermogen,
            "Warmtevermogen (kW)": warmvermogen
        })

    df = pd.DataFrame(ruimte_data)
    st.dataframe(df)

    totaal_lucht = df["Luchtdebiet totaal (m³/h)"].sum()
    totaal_koel = df["Koelvermogen (kW)"].sum()
    totaal_warm = df["Warmtevermogen (kW)"].sum()

    st.markdown("### 📊 Samenvatting totaal (LBK / Koeling / Verwarming)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Totaal luchtdebiet (m³/h)", f"{totaal_lucht:,.0f}")
    with col2:
        st.metric("Totaal koelvermogen (kW)", f"{totaal_koel:.2f}")
    with col3:
        st.metric("Totaal warmtevermogen (kW)", f"{totaal_warm:.2f}")

    if st.button("📄 Exporteer naar Excel (Basis)"):
        bestand = export_to_excel(df)
        with open(bestand, "rb") as f:
            st.download_button("Download Excel", data=f, file_name=bestand)

    if st.button("📥 Download PDF-rapport (Basis)"):
        bestand = export_to_pdf(df)
        with open(bestand, "rb") as f:
            st.download_button("Download PDF", data=f, file_name=bestand)

# ========== METHODE 2 ==========
else:
    st.subheader("🔸 Methode 2 – Geavanceerd (volledige versie volgt)")

    # Voorbeeld van seizoensselectie en weergave buitencondities
    seizoen = st.selectbox("Seizoen (voor buitencondities)", buitencondities.keys())
    buiten_rv = buitencondities[seizoen]["rv"]
    buiten_temp = buitencondities[seizoen]["temp"]

    st.markdown(f"**Buitenconditie:** {seizoen} – {buiten_temp}°C / {buiten_rv}% RV")

    # Hier kan Methode 2 verder worden geïmplementeerd
    st.info("De uitgebreide berekeningen, ISO-klassen, bevochtiging, grafieken en exports komen hier.")
