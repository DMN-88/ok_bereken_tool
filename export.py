# export.py

import pandas as pd

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
