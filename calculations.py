"""
Project Aero-Seed - Calculation Framework
This script provides the foundational mathematical scaffolding for simulating atmospheric ablation,
albedo-driven thermal shifts, and biological proliferation of the Martian terraforming vectors.
"""

import math

def calculate_ice_ablation_rate(entry_velocity, atmospheric_density):
    """
    Calculates the thickness of the cryogenic ice shell consumed during atmospheric entry.
    Uses the cold-wall ablation approximation where kinetic energy transfers to sublimation heat.
    """
    if entry_velocity <= 0 or atmospheric_density <= 0:
        return 0.0
        
    # Chulon (lämmönsiirtokerroin aerodynaamisessa kuumenemisessa, arvioitu 0.01)
    heat_transfer_coefficient = 0.01
    
    # Jään sublimaatiolämpö (J/kg) – energia, joka tarvitaan jään muuttamiseen suoraan kaasuksi
    latent_heat_sublimation = 2.83e6 
    
    # Jään tiheys (kg/m^3)
    ice_density = 917.0
    
    # Aerodynaaminen lämpövuo (Q = 0.5 * rho * v^3 * C_h)
    heat_flux = 0.5 * atmospheric_density * (entry_velocity ** 3) * heat_transfer_coefficient
    
    # Ablaation nopeus metreinä sekunnissa (m/s)
    ablation_rate_m_per_s = heat_flux / (latent_heat_sublimation * ice_density)
    
    # Arvioidaan tyypillinen kriittinen ilmakehän läpäisyaika (esim. 30 sekuntia intensiivistä kuumenemista)
    entry_duration_seconds = 30.0
    
    required_thickness = ablation_rate_m_per_s * entry_duration_seconds
    return round(required_thickness, 4)


def model_albedo_thermal_gain(mat_surface_area_km2, base_albedo=0.25, algae_albedo=0.08):
    """
    Models the local temperature increase caused by the expansion of dark algae mats.
    Calculates the net thermal energy gain using the solar constant at Mars.
    """
    # Marsin keskimääräinen aurinkovakio (Solar Irradiance) ilmakehän pinnalla (W/m^2)
    mars_solar_constant = 590.0 
    
    # Albedon muutos (kuinka paljon enemmän valoa imeytyy heijastumisen sijaan)
    albedo_delta = base_albedo - algae_albedo
    
    # Nettoenergian lisäys per neliömetri (W/m^2)
    net_thermal_gain_per_m2 = mars_solar_constant * albedo_delta
    
    return round(net_thermal_gain_per_m2, 2)


def simulate_biological_growth(initial_biomass_npk, water_volume_liters):
    """
    Tracks the replication rate of cyanobacteria based on available organic waste 
    nutrients and liquid water derived from the melted teardrop shell.
    Uses a modified logistic growth curve model.
    """
    if initial_biomass_npk <= 0 or water_volume_liters <= 0:
        return 0.0
        
    # Maksimikantokyky (Carrying capacity) grammoina, jota sulanut vesi ja NPK-ravinteet voivat ylläpitää
    carrying_capacity = water_volume_liters * 50.0 * (initial_biomass_npk / 10.0)
    
    # Kasvunopeuskerroin (Marsin kylmissä oloissa hidas, esim. 0.15 per sykli)
    growth_rate = 0.15
    
    # Simuloitu aika (esim. 48 kasvukautta/sykliä Marsin kesässä)
    time_cycles = 48
    
    # Logistisen kasvun kaava: N(t) = K / (1 + ((K - N0) / N0) * e^(-r*t))
    n0 = initial_biomass_npk  # Alkuperäinen biomassa lähtöpisteenä
    
    exponent = math.exp(-growth_rate * time_cycles)
    final_biomass = carrying_capacity / (1 + ((carrying_capacity - n0) / n0) * exponent)
    
    return round(final_biomass, 2)


if __name__ == "__main__":
    print("--- Project Aero-Seed: Calculation Framework ---")
    
    # Testiajo tyypillisillä Mars-arvoilla:
    # V entry = 5500 m/s, Marsin ilmakehän tiheys alhaalla = 0.02 kg/m^3
    thickness = calculate_ice_ablation_rate(5500, 0.02)
    print(f"1. Required Ice Shield Thickness: {thickness} meters")
    
    # Energian nousu kun albedo tippuu 0.25 -> 0.08
    thermal_gain = model_albedo_thermal_gain(1.0)
    print(f"2. Net Thermal Energy Gain: {thermal_gain} W/m^2")
    
    # Kasvusimulaatio 10g NPK-alustalla ja 6L vedellä (kuten one-drop-oasis kipsipallot)
    biomass = simulate_biological_growth(10.0, 6.0)
    print(f"3. Simulated Final Cyanobacteria Biomass: {biomass} grams")
