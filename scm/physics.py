from dataclasses import dataclass
R=8.31446261815324
N_A=6.02214076e23
K_B=1.380649e-23
C_LIGHT=299792458.0
@dataclass(frozen=True)
class GasState:
    pressure_pa:float
    volume_m3:float
    amount_mol:float
    temperature_k:float
def ideal_gas_pressure(volume_m3,amount_mol,temperature_k):
    if min(volume_m3,amount_mol,temperature_k)<=0: raise ValueError('inputs must be positive')
    return amount_mol*R*temperature_k/volume_m3
def ideal_gas_volume(pressure_pa,amount_mol,temperature_k):
    if min(pressure_pa,amount_mol,temperature_k)<=0: raise ValueError('inputs must be positive')
    return amount_mol*R*temperature_k/pressure_pa
