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
from export import export_to_excel

st.set_page_config(page_title="OK Bereken Tool", layout="wide")
st.title("🧾 OK-complex Lucht- & Klimaatberekening (V2)")

ruimte_types = list(ruimte_classificatie_normen.keys())
buitencondities = {
    "Zomer": {"temp": 28, "rv": 60},
    "Winter": {"temp": -5, "rv": 35},
    "Voorjaar / Najaar": {"temp": 15, "rv": 45}
}

ruimte_data = []
seizoen = st.selectbox("Selecteer seizoen (voor buitencondities)", buitencondities.keys())
buiten_rv = buitencondities[seizoen]["rv"]
buiten_temp = buitencondities[seizoen]["temp"]

st.markdown(f"**Buitenconditie:** {seizoen} - {buiten_temp}°C / {buiten_rv}% RV")

aantal_ruimtes = st.number_input("Aantal ruimtes", min_value=1, value=3)

for i in range(aantal_ruimtes):
    st.subheader(f"🧱 Ruimte {i+1}")
    ruimte_naam = st.text_input(f"Naam ruimte {i+1}", value=f"Ruimte {i+1}", key=f"naam_{i}")

    col1, col2, col3 = st.columns(3)

    with col1:
        ruimte_type = st.selectbox(f"Type ruimte {i+1}", ruimte_types, key=f"type_{i}")
        opp = st.number_input(f"Oppervlakte (m²)", value=40.0, key=f"opp_{i}")
        hoogte = st.number_input(f"Hoogte (m)", value=3.0, key=f"hoogte_{i}")

    with col2:
        pers = st.number_input(f"Personen aanwezig", value=4, key=f"pers_{i}")
        apparatuur = st.number_input(f"Apparatuur (W)", value=1000, key=f"apparatuur_{i}")
        verlichting = st.number_input(f"Verlichting (W)", value=500, key=f"licht_{i}")

    with col3:
        klimaatklasse = st.selectbox("Klimaatklasse", ["Klasse A", "Klasse B", "Klasse C"], key=f"klimaat_{i}")
        rv_gewenst = st.slider("Gewenste RV (%)", 40, 65, 50, key=f"rvg_{i}")
        temp = st.slider("Gewenste temperatuur (°C)", 16, 24, 20, key=f"temp_{i}")

    ruimte_klassen = ruimte_classificatie_normen.get(ruimte_type, {})
    classificatie = "-"
    iso_klasse = "-"

    if ruimte_klassen:
        classificatie = st.selectbox(
            f"Classificatie voor {ruimte_type}",
            options=list(ruimte_klassen.keys()),
            key=f"classificatie_{i}"
        )
        gegevens = ruimte_klassen[classificatie]
        luchtwisselingen = gegevens["luchtwisselingen"]
        iso_klasse = gegevens.get("iso_klasse", "-")
        st.info(f"{ruimte_type} ({classificatie}) → {luchtwisselingen} luchtwisselingen/uur | ISO: {iso_klasse}")
    else:
        classificatie = st.text_input(f"Classificatie (optioneel)", value="-", key=f"class_{i}")
        luchtwisselingen = st.number_input(
            f"Luchtwisselingen per uur (geen norm)", value=6, key=f"wisselingen_{i}"
        )

    delta_T_koeling = st.number_input("ΔT voor koelen (°C)", value=8, key=f"delta_koel_{i}")
    delta_T_verwarming = st.number_input("ΔT voor verwarmen (°C)", value=12, key=f"delta_warm_{i}")

    volume, luchtdebiet = bereken_luchtdebiet(opp, hoogte, luchtwisselingen)
    warmte_kw = bereken_warmtevermogen(pers, apparatuur, verlichting)
    bevochtiging = bereken_bevochtiging(luchtdebiet, rv_gewenst, buiten_rv, temp)
    vermogen_koelen = bereken_conditioneringsvermogen(luchtdebiet, delta_T_koeling)
    vermogen_verwarmen = bereken_conditioneringsvermogen(luchtdebiet, delta_T_verwarming)
    hersteltijd = bereken_hersteltijd(luchtwisselingen)

    ruimte_data.append({
        "Ruimtenaam": ruimte_naam,
        "Ruimte": ruimte_type,
        "Classificatie": classificatie,
        "ISO-klasse": iso_klasse,
        "Klimaatklasse": klimaatklasse,
        "Opp. (m²)": opp,
        "Hoogte (m)": hoogte,
        "Volume (m³)": round(volume, 1),
        "Luchtwisselingen": luchtwisselingen,
        "Luchtdebiet (m³/h)": round(luchtdebiet),
        "Hersteltijd (min)": hersteltijd,
        "Warmte intern (kW)": round(warmte_kw, 2),
        "Bevochtiging (kg/h)": round(bevochtiging, 2),
        "Koelvermogen (kW)": vermogen_koelen,
        "Verwarmingsvermogen (kW)": vermogen_verwarmen
    })

df = pd.DataFrame(ruimte_data)
st.dataframe(df, use_container_width=True)

totaal_luchtdebiet = df["Luchtdebiet (m³/h)"].sum()
totaal_volume = df["Volume (m³)"].sum()
totaal_koelvermogen = df["Koelvermogen (kW)"].sum()
totaal_warmtevermogen = df["Verwarmingsvermogen (kW)"].sum()

st.markdown("### 🧾 Samenvatting totaal")
col1, col2 = st.columns(2)
with col1:
    st.metric("Totaal luchtdebiet (m³/h)", f"{totaal_luchtdebiet:,.0f}")
    st.metric("Totaal koelvermogen (kW)", f"{totaal_koelvermogen:.1f}")
with col2:
    st.metric("Totaal volume (m³)", f"{totaal_volume:.1f}")
    st.metric("Totaal verwarmingsvermogen (kW)", f"{totaal_warmtevermogen:.1f}")

if st.checkbox("Toon grafiek luchtdebiet per ruimte"):
    fig, ax = plt.subplots()
    ax.bar(df["Ruimtenaam"], df["Luchtdebiet (m³/h)"])
    plt.xticks(rotation=45)
    ax.set_ylabel("Luchtdebiet (m³/h)")
    st.pyplot(fig)

if st.button("📄 Exporteer naar Excel"):
    bestand = export_to_excel(df)
    with open(bestand, "rb") as f:
        st.download_button("Download Excel", data=f, file_name=bestand)
