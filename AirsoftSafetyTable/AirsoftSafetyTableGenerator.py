import numpy as np
import TableFormatter as tf

def getTable(masses, distances, energiesMuzzle, energiesImpact, classNames, dragCoefficient = 0.477):
    """
    Parameters
    ----------
    masses : np.array
        The projectile masses form the columns of the table. Unit: kg.
    distances : np.array
        The safety distances form the rows of the table. Unit: m
    energiesMuzzle : np.array
        The maximum allowed energy by the muzzle. Unit: J
    energiesImpact : np.array
        The maximum allowed energy by the safety distance. Unit: J
    classNames: str array
        Names of the different classes (as defined by the distances).

    The number of distances, impact energies, muzzle energies and classNames must match!
    """
    # ********** Validate inputs **********************************************
    if distances.size != energiesMuzzle.size and \
       distances.size != energiesImpact.size and \
       distances.size != len(classNames):
        print("Number of distances, impact energies, muzzle energies and class names does not match!")

    # ********** Output ***********************************************************
    muzzleVelocities = np.array(np.ones([distances.size, masses.size])); # m/s

    # ********** Parameters *******************************************************
    density = 1.225 # kg/m^3 (15 degC, 1 atm)
    characteristicLength = 0.006 # m (diameter of projectile)
    area = np.pi * (characteristicLength/2)**2 # m^2
    #dragCoefficient = 0.477 # unitless

    constant = 0.5 * dragCoefficient * density * area

    # ********** Energy computation functions *************************************
    def velocityFromEnergyWithDrag(m, x, E, k):
        return np.sqrt(2*E/m)*np.exp(k*x/m)

    def velocityFromEnergy(m, E):
        return np.sqrt(2*E/m)

    def velocityMax(mass, distance, Eimpact, Emax, const):
        vFromDrag = velocityFromEnergyWithDrag(mass, distance, Eimpact, const)
        vMuzzleMax = velocityFromEnergy(mass, Emax)
        return np.min([vFromDrag, vMuzzleMax])

    # ********** Population of the table ******************************************
    for i_class in range(distances.size):
        for i_mass in range(masses.size):
            mass = masses[i_mass]
            distance = distances[i_class]
            energyMuzzle = energiesMuzzle[i_class]
            energyImpact = energiesImpact[i_class]
            muzzleVelocities[i_class, i_mass] = \
                velocityMax(mass, distance, energyImpact, energyMuzzle, constant)

    # ********** Print output *****************************************************
    np.set_printoptions(linewidth=100)
    print(np.array2string(muzzleVelocities, precision=1))

    tf.formatLatexTable(masses, distances, muzzleVelocities, classNames, "output/latexTable.txt")

    tf.formatHtmlTable(masses, distances, muzzleVelocities, classNames, "output/htmlTable.html", False)

    # ********** Return the results ***********************************************
    return masses, distances, muzzleVelocities, constant

def getVsaf2019Table():
    # ********** Define table *****************************************************
    masses = np.array([20, 25, 28, 30, 34, 36, 40, 43, 45])/100000 # kg
    distances = np.array([0, 5, 10, 20, 20, 30, 40]) # m
    muzzleVelocities = np.array([[100.0,  89.4,  84.5,  81.6,  76.7,  74.2,  70.4,  68.0,  66.6],
                                 [115.8, 103.6,  97.9,  94.6,  88.8,  86.3,  81.9,  79.0,  77.2],
                                 [132.6, 118.6, 112.1, 108.3, 101.7,  98.6,  93.5,  90.4,  88.4],
                                 [145.0, 129.6, 122.5, 118.3, 111.1, 108.0, 102.5,  98.8,  96.6],
                                 [158.5, 141.8, 134.0, 129.4, 121.6, 118.1, 112.0, 108.1, 105.7],
                                 [182.9, 163.6, 154.6, 149.3, 140.3, 136.2, 129.2, 124.7, 121.9],
                                 [213.4, 190.8, 180.3, 174.2, 163.6, 159.0, 150.8, 145.5, 142.2]]); # m/s
    classNames = ["CQB\t", "AutoA", "AutoB", "HMG", "Semi", "BoltA", "BoltB"]
    dummyConstant = 0

    # ********** Print output *****************************************************
    np.set_printoptions(linewidth=100)
    print(np.array2string(muzzleVelocities, precision=1))

    print(tf.formatLatexTable(masses, distances, muzzleVelocities, \
       "output/latexTable.txt", classNames))
    
    # ********** Return the results ***********************************************
    return masses, distances, muzzleVelocities, dummyConstant

def getVsaf2020Table():
    masses = np.array([20, 25, 28, 30, 32, 34, 36, 40, 43, 45, 46, 48, 50, 58])/100000 # kg
    #masses = np.array([20, 25, 28, 30, 34, 36, 40, 43, 45, 48, 50])/100000 # kg
    #masses = np.array([20, 25, 28, 30, 34, 36, 40, 43, 45])/100000 # kg
    distances = np.array([0, 5, 10, 20, 20, 30, 40]) # m
    energiesMuzzle = np.array([1, 1.34, 1.76, 2.11, 2.51, 3.34, 4.55]) # J (max energy at muzzle)
    energiesImpact = np.array([1, 1, 1, 1.08, 1.16, 1.16, 1.16]) # J (max energy at safety distance)
    classNames = ["CQB\t", "AutoA", "AutoB", "HMG", "Semi", "BoltA", "BoltB"]
    return getTable(masses, distances, energiesMuzzle, energiesImpact, classNames)

def get2020Table():
    masses = np.array([20, 25, 28, 30, 34, 36, 40, 43, 45, 48, 50])/100000 # kg
    distances = np.array([0, 5, 10, 20, 20, 30, 40]) # m
    energiesMuzzle = np.array([1.2, 1.45, 1.7, 2.2, 2.2, 3, 4]) # J (max energy at muzzle)
    energiesImpact = np.array([1, 1, 1, 1, 1, 1, 1]) * 1.2 # J (max energy at safety distance)
    classNames = ["CQB 2\t", "Assault 1", "Assault 2", "Support 3", "DMR", "Sniper 1", "Sniper 2"]
    return getTable(masses, distances, energiesMuzzle, energiesImpact, classNames)

def get2020TableDragCoeff04():
    masses = np.array([20, 25, 28, 30, 34, 36, 40, 43, 45, 48, 50])/100000 # kg
    distances = np.array([0, 5, 10, 20, 20, 30, 40]) # m
    energiesMuzzle = np.array([1.2, 1.45, 1.7, 2.2, 2.2, 3, 4]) # J (max energy at muzzle)
    energiesImpact = np.array([1, 1, 1, 1, 1, 1, 1]) * 1.2 # J (max energy at safety distance)
    classNames = ["CQB 2\t", "Assault 1", "Assault 2", "Support 3", "DMR", "Sniper 1", "Sniper 2"]
    return getTable(masses, distances, energiesMuzzle, energiesImpact, classNames, 0.4)

getVsaf2020Table()