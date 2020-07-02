import numpy as np
import TableComparator
import AirsoftSafetyTableGenerator

# ********** Load *************************************************************
massesOld, distancesOld, velocitiesOld, constant = AirsoftSafetyTableGenerator.get2020Table()
massesNew, distancesNew, velocitiesNew, constant = AirsoftSafetyTableGenerator.getVsaf2020Table()

# ********** Compute **********************************************************
impactEnergyOld = TableComparator.impactEnergyFromMuzzleVelocities(velocitiesOld, massesOld, distancesOld, constant)
impactEnergyNew = TableComparator.impactEnergyFromMuzzleVelocities(velocitiesNew, massesNew, distancesNew, constant)
muzzleEnergyOld = TableComparator.muzzleEnergyFromMuzzleVelocities(velocitiesOld, massesOld)
muzzleEnergyNew = TableComparator.muzzleEnergyFromMuzzleVelocities(velocitiesNew, massesNew)

muzzleVelocityDiff = TableComparator.compareMuzzleVelocities(velocitiesOld, velocitiesNew)
muzzleEnergyDiff = TableComparator.compareMuzzleEnergies(velocitiesOld, massesOld, velocitiesNew, massesNew)
impactEnergyDiff = TableComparator.compareImpactEnergies(velocitiesOld, massesOld, distancesOld, velocitiesNew, massesNew, distancesNew, constant)

# ********** Print ************************************************************
np.set_printoptions(linewidth=100, suppress=True)

print("Masses", np.array2string(massesOld*1000, prefix="Masses ", separator=', ', precision=2))
print("Distances", np.array2string(distancesOld, prefix="Distances ", separator=', ', precision=1))
print("MuzzleVelocitiesOld", np.array2string(velocitiesOld, prefix="MuzzleVelocitiesOld ", separator=', ', precision=1))
print("MuzzleVelocitiesNew", np.array2string(velocitiesNew, prefix="MuzzleVelocitiesNew ", separator=', ', precision=1))
print("MuzzleVelocityDiff", np.array2string(muzzleVelocityDiff, prefix="MuzzleVelocityDiff ", separator=', ', precision=1))
print("MuzzleEnergyOld", np.array2string(muzzleEnergyOld, prefix="MuzzleEnergyOld ", separator=', ', precision=3))
print("MuzzleEnergyNew", np.array2string(muzzleEnergyNew, prefix="MuzzleEnergyNew ", separator=', ', precision=3))
print("MuzzleEnergyDiff", np.array2string(muzzleEnergyDiff, prefix="MuzzleEnergyDiff ", separator=', ', precision=3))
print("ImpactEnergyOld", np.array2string(impactEnergyOld, prefix="ImpactEnergyOld ", separator=', ', precision=3))
print("ImpactEnergyNew", np.array2string(impactEnergyNew, prefix="ImpactEnergyNew ", separator=', ', precision=3))
print("ImpactEnergyDiff", np.array2string(impactEnergyDiff, prefix="ImpactEnergyDiff ", separator=', ', precision=3))

# ********** Write ************************************************************
file = open("output/tableAnalyzerOutput.txt", "w")
file.write("Masses " + np.array2string(massesOld*1000, prefix="Masses ", separator=', ', precision=2) + "\n")
file.write("Distances " + np.array2string(distancesOld, prefix="Distances ", separator=', ', precision=1) + "\n")
file.write("MuzzleVelocitiesOld " + np.array2string(velocitiesOld, prefix="MuzzleVelocitiesOld ", separator=', ', precision=1) + "\n")
file.write("MuzzleVelocitiesNew " + np.array2string(velocitiesNew, prefix="MuzzleVelocitiesNew ", separator=', ', precision=1) + "\n")
file.write("MuzzleVelocityDiff " + np.array2string(muzzleVelocityDiff, prefix="MuzzleVelocityDiff ", separator=', ', precision=1) + "\n")
file.write("MuzzleEnergyOld " + np.array2string(muzzleEnergyOld, prefix="MuzzleEnergyOld ", separator=', ', precision=3) + "\n")
file.write("MuzzleEnergyNew " + np.array2string(muzzleEnergyNew, prefix="MuzzleEnergyNew ", separator=', ', precision=3) + "\n")
file.write("MuzzleEnergyDiff " + np.array2string(muzzleEnergyDiff, prefix="MuzzleEnergyDiff ", separator=', ', precision=3) + "\n")
file.write("ImpactEnergyOld " + np.array2string(impactEnergyOld, prefix="ImpactEnergyOld ", separator=', ', precision=3) + "\n")
file.write("ImpactEnergyNew " + np.array2string(impactEnergyNew, prefix="ImpactEnergyNew ", separator=', ', precision=3) + "\n")
file.write("ImpactEnergyDiff " + np.array2string(impactEnergyDiff, prefix="ImpactEnergyDiff ", separator=', ', precision=3) + "\n")
file.close()