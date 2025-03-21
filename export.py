# export.py

import pandas as pd
from fpdf import FPDF
from datetime import datetime

def export_to_excel(df, bestandsnaam="OK_berekening.xlsx"):
    totaal_lucht = df["Luchtdebiet (m³/h)"].sum()
    totaal_volume = df["Volume (m³)"].sum()
    totaal_koel = df["Koelvermogen (kW)"].sum()
    totaal_warm = df["Verwarmingsvermogen (kW)"].sum()

    with pd.ExcelWriter(bestandsnaam) as writer:
        df.to_excel(writer, index=False, sheet_name="Berekening")
        summary = pd.DataFrame({
            "Omschrijving": [
                "Totaal luchtdebiet (m³/h)",
                "Totaal volume (m³)",
                "Totaal koelvermogen (kW)",
                "Totaal verwarmingsvermogen (kW)"
            ],
            "Waarde": [
                totaal_lucht,
                totaal_volume,
                totaal_koel,
                totaal_warm
            ]
        })
        summary.to_excel(writer, index=False, sheet_name="Samenvatting")

    return bestandsnaam

def export_to_pdf(df, bestandsnaam="OK_berekening.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="OK Berekeningsoverzicht", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Datum: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True, align="C")
    pdf.ln(10)

    # Tabelkop
    kolommen = ["Ruimtenaam", "Ruimte", "Volume (m³)", "Luchtdebiet (m³/h)", "Koelvermogen (kW)", "Verwarmingsvermogen (kW)"]
    for kol in kolommen:
        pdf.cell(40, 10, kol[:18], border=1)
    pdf.ln()

    # Data
    for _, row in df.iterrows():
        for kol in kolommen:
            pdf.cell(40, 10, str(row.get(kol, ""))[:18], border=1)
        pdf.ln()

    # Opslaan
    pdf.output(bestandsnaam)
    return bestandsnaam
