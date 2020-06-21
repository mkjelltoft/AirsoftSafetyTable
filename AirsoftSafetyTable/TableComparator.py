import numpy as np

# ********** Energy computation functions *************************************
def impactEnergyFromMuzzleVelocity(m, x, u, k):
    return m*u*u*0.5*np.exp(-2*k*x/m)

def impactEnergyFromMuzzleVelocities(velocitiesMuzzle, masses, distances, constant):
    energiesImpact = np.zeros(velocitiesMuzzle.shape)
    for i_class in range(velocitiesMuzzle.shape[0]):
        for i_mass in range(velocitiesMuzzle.shape[1]):
            mass = masses[i_mass]
            distance = distances[i_class]
            velocityMuzzle = velocitiesMuzzle[i_class, i_mass]
            energiesImpact[i_class, i_mass] = \
                impactEnergyFromMuzzleVelocity(mass, distance, velocityMuzzle, constant)
    return energiesImpact

def muzzleEnergyFromMuzzleVelocities(velocitiesMuzzle, masses):
    distances = np.zeros(velocitiesMuzzle.shape[0])
    constant = 1
    return impactEnergyFromMuzzleVelocities(velocitiesMuzzle, masses, distances, constant)

# ********** Comparing functions **********************************************
"""
:return: TableB - TableA
"""
def compareMuzzleVelocities(velocitiesMuzzleA, velocitiesMuzzleB):
    return velocitiesMuzzleB - velocitiesMuzzleA

"""
:return: TableB - TableA
"""
def compareMuzzleEnergies(velocitiesMuzzleA, massesA, velocitiesMuzzleB, massesB):
    muzzleEnergiesA = muzzleEnergyFromMuzzleVelocities(velocitiesMuzzleA, massesA)
    muzzleEnergiesB = muzzleEnergyFromMuzzleVelocities(velocitiesMuzzleB, massesB)
    return muzzleEnergiesB - muzzleEnergiesA

"""
:return: TableB - TableA
"""
def compareImpactEnergies(velocitiesMuzzleA, massesA, distancesA, velocitiesMuzzleB, massesB, distancesB, constant):
    impactEnergiesA = impactEnergyFromMuzzleVelocities(velocitiesMuzzleA, massesA, distancesA, constant)
    impactEnergiesB = impactEnergyFromMuzzleVelocities(velocitiesMuzzleB, massesB, distancesB, constant)
    return impactEnergiesB - impactEnergiesA