import pandas as pd

def export_to_excel(df, bestandsnaam="OK_berekening.xlsx"):
    df.to_excel(bestandsnaam, index=False)
    return bestandsnaam
