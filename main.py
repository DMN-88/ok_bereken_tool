import streamlit as st
import pandas as pd
from normen import vccn_normen
from berekeningen import bereken_luchtdebiet, bereken_warmtevermogen, bereken_bevochtiging
from export import export_to_excel

st.set_page_config(page_title="OK Bereken Tool", layout="wide")
st.title("🧮 OK-complex Lucht- & Klimaatberekening (VCCN)")

ruimte_types = list(vccn_normen.keys())
ruimte_data = []

aantal_ruimtes = st.number_input("Aantal ruimtes", min_value=1, value=3)

for i in range(aantal_ruimtes):
    st.subheader(f"🧱 Ruimte {i+1}")
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
        rv_gewenst = st.slider("Gewenste RV (%)", 30, 60, 40, key=f"rvg_{i}")
        rv_buiten = st.slider("Buiten RV (%)", 0, 100, 30, key=f"rvb_{i}")
        temp = st.slider("Temperatuur (°C)", 16, 24, 20, key=f"temp_{i}")

    luchtwisselingen = vccn_normen[ruimte_type]
    volume, luchtdebiet = bereken_luchtdebiet(opp, hoogte, luchtwisselingen)
    warmte_kw = bereken_warmtevermogen(pers, apparatuur, verlichting)
    bevochtiging = bereken_bevochtiging(luchtdebiet, rv_gewenst, rv_buiten, temp)

    ruimte_data.append({
        "Ruimte": ruimte_type,
        "Opp. (m²)": opp,
        "Hoogte (m)": hoogte,
        "Volume (m³)": volume,
        "Luchtwisselingen": luchtwisselingen,
        "Luchtdebiet (m³/h)": round(luchtdebiet),
        "Warmte (kW)": round(warmte_kw, 2),
        "Bevochtiging (kg/h)": round(bevochtiging, 2)
    })

df = pd.DataFrame(ruimte_data)
st.dataframe(df, use_container_width=True)

if st.button("📤 Exporteer naar Excel"):
    bestand = export_to_excel(df)
    with open(bestand, "rb") as f:
        st.download_button("Download Excel", data=f, file_name=bestand)
        
# Totaal luchtdebiet voor LBK
totaal_luchtdebiet = df["Luchtdebiet (m³/h)"].sum()
totaal_volume = df["Volume (m³)"].sum()

st.markdown("### 🧮 Samenvatting")
col1, col2 = st.columns(2)
with col1:
    st.metric("Totaal luchtdebiet (m³/h)", f"{totaal_luchtdebiet:,.0f}")
with col2:
    st.metric("Totaal volume (m³)", f"{totaal_volume:,.1f}")
