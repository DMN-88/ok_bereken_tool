def bereken_luchtdebiet(opp, hoogte, luchtwisselingen):
    volume = opp * hoogte
    luchtdebiet = volume * luchtwisselingen
    return volume, luchtdebiet

def bereken_warmtevermogen(pers, apparatuur, verlichting):
    warmte_persoon = pers * 120  # W
    totaal_watt = warmte_persoon + apparatuur + verlichting
    return totaal_watt / 1000  # kW

def bereken_bevochtiging(luchtdebiet, rv_gewenst, rv_buiten, temp):
    bevochtiging = (rv_gewenst - rv_buiten) * luchtdebiet * 0.001
    return max(bevochtiging, 0)

def bereken_conditioneringsvermogen(luchtdebiet_m3h, delta_T):
    rho = 1.2  # kg/m³
    c = 1005   # J/kg·K
    V_m3s = luchtdebiet_m3h / 3600
    Q_watt = rho * V_m3s * c * delta_T
    return round(Q_watt / 1000, 2)  # kW
