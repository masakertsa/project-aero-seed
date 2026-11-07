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
    
    Parameters:
    - entry_velocity (float): Entry speed in meters per second.
    - atmospheric_density (float): Density profile of the Martian atmosphere.
    
    Returns:
    - float: Required ice shield thickness in meters.
    """
    if entry_velocity <= 0 or atmospheric_density <= 0:
        return 0.0
        
    # Optimized aerodynamic heat transfer coefficient (Stanton number / Chulon) for a streamlined teardrop shape
    heat_transfer_coefficient = 0.003
    
    # Latent heat of sublimation for ice (J/kg) – energy required to turn ice directly into gas
    latent_heat_sublimation = 2.83e6 
    
    # Density of solid ice (kg/m^3)
    ice_density = 917.0
    
    # Aerodynamic heat flux calculation (Q = 0.5 * rho * v^3 * C_h)
    heat_flux = 0.5 * atmospheric_density * (entry_velocity ** 3) * heat_transfer_coefficient
    
    # Ablation velocity in meters per second (m/s)
    ablation_rate_m_per_s = heat_flux / (latent_heat_sublimation * ice_density)
    
    # Estimated critical duration of peak atmospheric heating in seconds
    entry_duration_seconds = 25.0
    
    required_thickness = ablation_rate_m_per_s * entry_duration_seconds
    return round(required_thickness, 4)


def model_albedo_thermal_gain(mat_surface_area_km2, base_albedo=0.25, algae_albedo=0.08):
    """
    Models the local temperature increase caused by the expansion of dark algae mats.
    Calculates the net thermal energy gain using the solar constant at Mars.
    
    Parameters:
    - mat_surface_area_km2 (float): Surface area covered by the expanding biological mat.
    - base_albedo (float): Native Martian regolith albedo (~0.25).
    - algae_albedo (float): Dense cyanobacteria mat albedo (~0.08).
    
    Returns:
    - float: Net thermal energy gain in Watts/meter^2.
    """
    # Average solar constant (Solar Irradiance) at the Martian orbital distance (W/m^2)
    mars_solar_constant = 590.0 
    
    # Delta albedo (amount of additional solar energy absorbed instead of reflected)
    albedo_delta = base_albedo - algae_albedo
    
    # Net thermal energy gain per square meter (W/m^2)
    net_thermal_gain_per_m2 = mars_solar_constant * albedo_delta
    
    return round(net_thermal_gain_per_m2, 2)


def simulate_biological_growth(initial_biomass_npk, water_volume_liters):
    """
    Tracks the replication rate of cyanobacteria based on available organic waste 
    nutrients and liquid water derived from the melted teardrop shell.
    Uses a modified logistic growth curve model adapted for Martian microclimates.
    
    Parameters:
    - initial_biomass_npk (float): Starting biomass acting as nutrient base in grams.
    - water_volume_liters (float): Available liquid water from the melted entry shell.
    
    Returns:
    - float: Final calculated cyanobacteria biomass in grams.
    """
    if initial_biomass_npk <= 0 or water_volume_liters <= 0:
        return 0.0
        
    # Environmental carrying capacity (K) in grams, sustained by available water and NPK nutrients
    carrying_capacity = water_volume_liters * 50.0 * (initial_biomass_npk / 10.0)
    
    # Intrinsic growth rate factor (slow due to cold Martian ambient baseline, e.g., 0.15 per cycle)
    growth_rate = 0.15
    
    # Simulated time horizons (e.g., 48 active growth cycles during Martian summer periods)
    time_cycles = 48
    
    # Logistic growth formula: N(t) = K / (1 + ((K - N0) / N0) * e^(-r*t))
    n0 = initial_biomass_npk  # Using initial biological biomass as the baseline N0
    
    exponent = math.exp(-growth_rate * time_cycles)
    final_biomass = carrying_capacity / (1 + ((carrying_capacity - n0) / n0) * exponent)
    
    return round(final_biomass, 2)


if __name__ == "__main__":
    print("--- Project Aero-Seed: Calculation Framework ---")
    
    # Test run using standardized Martian baseline variables:
    # V_entry = 5500 m/s, Average atmospheric density during descent profile = 0.0055 kg/m^3
    thickness = calculate_ice_ablation_rate(5500, 0.0055)
    print(f"1. Required Ice Shield Thickness: {thickness} meters ({thickness * 100:.1f} cm)")
    
    # Net radiation capture increase when surface albedo drops from 0.25 to 0.08
    thermal_gain = model_albedo_thermal_gain(1.0)
    print(f"2. Net Thermal Energy Gain: {thermal_gain} W/m^2")
    
    # Growth simulation using 10g NPK baseline substrate and 6L reservoir (matching one-drop-oasis parameters)
    biomass = simulate_biological_growth(10.0, 6.0)
    print(f"3. Simulated Final Cyanobacteria Biomass: {biomass} grams")
