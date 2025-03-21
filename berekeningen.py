def bereken_luchtdebiet(opp, hoogte, luchtwisselingen):
    volume = opp * hoogte
    luchtdebiet = volume * luchtwisselingen
    return volume, luchtdebiet

def bereken_warmtevermogen(pers, apparatuur, verlichting):
    warmte_persoon = pers * 120  # W per persoon
    totaal_watt = warmte_persoon + apparatuur + verlichting
    return totaal_watt / 1000  # kW

def bereken_bevochtiging(luchtdebiet, rv_gewenst, rv_buiten, temp):
    bevochtiging = (rv_gewenst - rv_buiten) * luchtdebiet * 0.001
    return max(bevochtiging, 0)
