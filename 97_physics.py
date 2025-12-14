import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random

class NuclearPhysicsSimulator:
    def __init__(self):
        self.avogadro = 6.022e23  # atoms per mole
        self.meV_to_J = 1.602e-13  # conversion factor
        self.amu_to_kg = 1.66054e-27  # atomic mass unit to kg
        
    def semi_empirical_mass_formula(self, Z, A):
        """
        Calculate nuclear binding energy using the semi-empirical mass formula
        Z: atomic number (protons)
        A: mass number (total nucleons)
        """
        N = A - Z  # number of neutrons
        
        # Constants (in MeV)
        a_v = 15.75  # volume term
        a_s = 17.8   # surface term
        a_c = 0.711  # Coulomb term
        a_a = 23.7   # asymmetry term
        a_p = 34.0   # pairing term
        
        # Calculate pairing term
        if Z % 2 == 0 and N % 2 == 0:
            pairing = a_p / A**(3/4)
        elif Z % 2 == 1 and N % 2 == 1:
            pairing = -a_p / A**(3/4)
        else:
            pairing = 0
        
        # Semi-empirical mass formula
        binding_energy = (a_v * A - a_s * A**(2/3) - a_c * Z**2 / A**(1/3) 
                         - a_a * (N - Z)**2 / A + pairing)
        
        return binding_energy
    
    def radioactive_decay(self, N0, lambda_, time_points):
        """
        Simulate radioactive decay using differential equations
        N0: initial number of nuclei
        lambda_: decay constant
        time_points: array of time points
        """
        def decay_equation(N, t):
            return -lambda_ * N
        
        solution = odeint(decay_equation, N0, time_points)
        return solution.flatten()
    
    def calculate_half_life(self, lambda_):
        """Calculate half-life from decay constant"""
        return np.log(2) / lambda_
    
    def nuclear_fission_simulation(self, initial_U235, neutron_multiplication_factor=2.4):
        """
        Simulate nuclear fission chain reaction
        initial_U235: initial number of U-235 nuclei
        neutron_multiplication_factor: average neutrons per fission
        """
        fission_events = []
        neutrons = 1  # start with one neutron
        generation = 0
        remaining_U235 = initial_U235
        
        while neutrons > 0 and remaining_U235 > 0 and generation < 10:
            # Number of fissions in this generation
            fissions = min(neutrons, remaining_U235)
            fission_events.append(fissions)
            
            # Update remaining U-235
            remaining_U235 -= fissions
            
            # Calculate neutrons for next generation
            neutrons = int(fissions * neutron_multiplication_factor * random.uniform(0.8, 1.2))
            generation += 1
            
        return fission_events, remaining_U235
    
    def plot_binding_energy_curve(self, Z_range=(1, 92)):
        """Plot binding energy per nucleon curve"""
        A_values = []
        BE_per_nucleon = []
        
        for Z in range(Z_range[0], Z_range[1] + 1):
            # Find most stable A for this Z
            A_stable = int(2 * Z)  # approximation
            if A_stable > 300:
                A_stable = 300
                
            BE = self.semi_empirical_mass_formula(Z, A_stable)
            A_values.append(A_stable)
            BE_per_nucleon.append(BE / A_stable)
        
        plt.figure(figsize=(10, 6))
        plt.plot(A_values, BE_per_nucleon, 'b-', linewidth=2)
        plt.xlabel('Mass Number (A)')
        plt.ylabel('Binding Energy per Nucleon (MeV)')
        plt.title('Nuclear Binding Energy Curve')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def simulate_decay_chain(self, initial_N, decay_constants, time_points):
        """
        Simulate radioactive decay chain (e.g., U-238 → Th-234 → Pa-234 → U-234)
        initial_N: initial number of parent nuclei
        decay_constants: list of decay constants for each nuclide
        time_points: array of time points
        """
        def decay_chain_equations(N, t):
            dN_dt = np.zeros(len(N))
            dN_dt[0] = -decay_constants[0] * N[0]  # parent decay
            
            for i in range(1, len(N)):
                production = decay_constants[i-1] * N[i-1]
                decay = -decay_constants[i] * N[i]
                dN_dt[i] = production + decay
                
            return dN_dt
        
        # Initial conditions (all nuclei start as parent)
        N0 = [initial_N] + [0] * (len(decay_constants) - 1)
        
        solution = odeint(decay_chain_equations, N0, time_points)
        return solution

def main():
    # Initialize simulator
    sim = NuclearPhysicsSimulator()
    
    print("=== NUCLEAR PHYSICS SIMULATOR ===\n")
    
    # 1. Calculate binding energies
    print("1. Binding Energy Calculations:")
    elements = [
        ("Helium-4", 2, 4),
        ("Carbon-12", 6, 12),
        ("Iron-56", 26, 56),
        ("Uranium-235", 92, 235),
        ("Uranium-238", 92, 238)
    ]
    
    for name, Z, A in elements:
        BE = sim.semi_empirical_mass_formula(Z, A)
        BE_per_nucleon = BE / A
        print(f"{name}: BE = {BE:.2f} MeV, BE/A = {BE_per_nucleon:.2f} MeV")
    
    # 2. Radioactive decay simulation
    print("\n2. Radioactive Decay Simulation:")
    N0 = 1e6  # initial nuclei
    half_life = 5.0  # years
    lambda_ = np.log(2) / half_life
    
    time_points = np.linspace(0, 20, 100)
    N_t = sim.radioactive_decay(N0, lambda_, time_points)
    
    print(f"Initial nuclei: {N0:.2e}")
    print(f"Half-life: {half_life:.2f} years")
    print(f"After 10 years: {N_t[50]:.2e} nuclei remaining")
    print(f"After 20 years: {N_t[-1]:.2e} nuclei remaining")
    
    # 3. Nuclear fission simulation
    print("\n3. Nuclear Fission Chain Reaction:")
    initial_U235 = 1000
    fission_events, remaining_U235 = sim.nuclear_fission_simulation(initial_U235)
    
    print(f"Initial U-235 nuclei: {initial_U235}")
    print(f"Fissions by generation: {fission_events}")
    print(f"Total fissions: {sum(fission_events)}")
    print(f"Remaining U-235: {remaining_U235}")
    
    # 4. Decay chain simulation
    print("\n4. Decay Chain Simulation (U-238 series):")
    # Simplified decay constants (in 1/year)
    decay_constants = [
        1.55e-10,  # U-238
        9.16e-3,   # Th-234
        3.33e-3,   # Pa-234
        2.81e-6    # U-234
    ]
    
    time_chain = np.linspace(0, 1e9, 100)  # 1 billion years
    chain_solution = sim.simulate_decay_chain(1e6, decay_constants, time_chain)
    
    print(f"Initial U-238: 1e6 nuclei")
    print(f"After 1 billion years:")
    print(f"  U-238 remaining: {chain_solution[-1, 0]:.2e}")
    print(f"  Th-234 produced: {chain_solution[-1, 1]:.2e}")
    print(f"  Pa-234 produced: {chain_solution[-1, 2]:.2e}")
    print(f"  U-234 produced: {chain_solution[-1, 3]:.2e}")
    
    # 5. Plot binding energy curve
    print("\n5. Generating binding energy curve...")
    sim.plot_binding_energy_curve()
    
    # 6. Calculate energy from fission
    print("\n6. Energy from Fission:")
    mass_defect = 0.2  # amu (typical for U-235 fission)
    energy_per_fission = mass_defect * 931.5  # MeV
    energy_per_fission_J = energy_per_fission * sim.meV_to_J
    
    print(f"Mass defect per fission: {mass_defect} amu")
    print(f"Energy per fission: {energy_per_fission:.1f} MeV")
    print(f"Energy per fission: {energy_per_fission_J:.2e} J")
    print(f"Energy from 1g U-235: {energy_per_fission_J * sim.avogadro / 235:.2e} J")
    
    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    main()
