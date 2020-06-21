import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import scipy.optimize as sp

# ********** Read data ********************************************************

# Read data from disk
data_ssg24_45 = pd.read_csv("data/ssg24_45.csv", skiprows = 2)
data_ssg24_30 = pd.read_csv("data/ssg24_30.csv", skiprows = 2)
data_krytac_30 = pd.read_csv("data/krytac_30.csv", skiprows = 2)
data_krytac_25 = pd.read_csv("data/krytac_25.csv", skiprows = 2)
data_hk416_30 = pd.read_csv("data/hk416_30.csv", skiprows = 2)

# Add setName as metadata
data_ssg24_45.setName  = "ssg24_45"
data_ssg24_30.setName  = "ssg24_30"
data_krytac_30.setName = "krytac_30"
data_krytac_25.setName = "krytac_25"
data_hk416_30.setName  = "hk416_30"

# Add setWeight in kg as metedata
data_ssg24_45.setWeight  = 45 / 100000
data_ssg24_30.setWeight  = 30 / 100000
data_krytac_30.setWeight = 30 / 100000
data_krytac_25.setWeight = 25 / 100000
data_hk416_30.setWeight  = 30 / 100000

# Create macros for accessing specific subsets of the dataFrames
colNames_values = ["Value_1", "Value_2", "Value_3", "Value_4", "Value_5"]

# Collect the dataFrames in one object for easier handling
data = [
    data_ssg24_45,
    data_ssg24_30,
    data_krytac_30,
    data_krytac_25,
    data_hk416_30]

# ********** Compute means ****************************************************

for df in data:
    df["mean"] = df[colNames_values].mean(axis=1)

# ********** Fit exponential model to data ************************************

# Known constants
density = 1.184 # kg/m^3 (1.225 kg/m^3, 15 degC, 1 atm), (1.184 kg/m^3, 25 degC, 1 atm)
characteristicLength = 0.006 # m (diameter of projectile)
area = np.pi * (characteristicLength/2)**2 # m^2
dragCoefficientGuess = 0.5 # unitless

# Model exponential functions to fit
def func0(x, c):
    return data[0]["mean"][0] * np.exp(- 0.5 * c * density * area / data[0].setWeight * x)
def func1(x, c):
    return data[1]["mean"][0] * np.exp(- 0.5 * c * density * area / data[1].setWeight * x)
def func2(x, c):
    return data[2]["mean"][0] * np.exp(- 0.5 * c * density * area / data[2].setWeight * x)
def func3(x, c):
    return data[3]["mean"][0] * np.exp(- 0.5 * c * density * area / data[3].setWeight * x)
def func4(x, c):
    return data[4]["mean"][0] * np.exp(- 0.5 * c * density * area / data[4].setWeight * x)

func = [func0, func1, func2, func3, func4]

# Curve fitting
dragCoefficients = []
pcovs = []
perr = []
for i in range(len(data)):
    popt, pcov = sp.curve_fit(func[i], data[i]["Distance"], data[i]["mean"], dragCoefficientGuess)
    dragCoefficients.append(popt[0])
    pcovs.append(pcov[0][0])
    perr.append(np.sqrt(pcov[0][0]))

# ********** Combine results and compute fit error ****************************

# Combine the different drag coefficient to one value with more evidence.
# The combined distributions mean is the average of means weighed by precision
# and the combined variance is the harmonic sum of variances.
# ref: https://stats.stackexchange.com/questions/193987/how-to-combine-two-measurements-of-the-same-quantity-with-different-confidences

dragCoefficientVariance = 0
for v in pcovs:
    dragCoefficientVariance = dragCoefficientVariance + 1 / v**2
dragCoefficientVariance = 1 / dragCoefficientVariance

dragCoefficientMean = 0
for i in range(len(pcovs)):
    dragCoefficientMean = dragCoefficientMean + dragCoefficients[i] / pcovs[i]**2
dragCoefficientMean = dragCoefficientMean * dragCoefficientVariance

dragCoefficientStandardDeviation = np.sqrt(dragCoefficientVariance)

# ********** Compute model mean square error *********************************

modelError = []
for i_set in range(len(data)):
    for i_dist in range(len(data[i_set]["Distance"])):
        modelError.append((data[i_set]["mean"][i_dist] - func[i_set](data[i_set]["Distance"][i_dist], dragCoefficientMean))**2)
modelError = np.sqrt(np.mean(modelError))

# ********** Print results ****************************************************

print("Drag coefficients: " + str(dragCoefficients))
print("Mean drag coefficient: " + str(np.mean(dragCoefficients)))
print("Weighted mean drag coefficient: " + str(dragCoefficientMean))
print("Standard deviations: " + str(perr))
print("Combined standard deviation: " + str(dragCoefficientStandardDeviation))
print("Final result, drag coefficient: {:.5f} +- {:f}".format(dragCoefficientMean, dragCoefficientStandardDeviation))
print("Model prediction mean square error: {:1.3f} m/s".format(modelError))

file = open("output/dataAnalyzerOutput.txt", "w")
file.write("Drag coefficients: " + str(dragCoefficients) + "\n")
file.write("Mean drag coefficient: " + str(np.mean(dragCoefficients)) + "\n")
file.write("Weighted mean drag coefficient: " + str(dragCoefficientMean) + "\n")
file.write("Standard deviations: " + str(perr) + "\n")
file.write("Combined standard deviation: " + str(dragCoefficientStandardDeviation) + "\n")
file.write("Final result, drag coefficient: {:.5f} +- {:f}".format(dragCoefficientMean, dragCoefficientStandardDeviation) + "\n")
file.write("Model prediction mean square error: {:1.3f} m/s".format(modelError) + "\n")
file.close()

# ********** Plot model prediction and data ***********************************

# x values to compute predictions for
xrange = np.linspace(0, data[0]["Distance"].max())

# color per measurement set
data[0].setColor = 'b'
data[1].setColor = 'g'
data[2].setColor = 'r'
data[3].setColor = 'c'
data[4].setColor = 'm'

# plot predictions
axis = plt.gca()
for f in func:
    plt.plot(xrange, f(xrange, dragCoefficientMean), "k--")

# plot data
for df in data:
    plt.plot(df["Distance"], df[colNames_values], "D", color=df.setColor, label=df.setName)

# remove redundant legend labels
handles, labels = plt.gca().get_legend_handles_labels()
i =1
while i<len(labels):
    if labels[i] in labels[:i]:
        del(labels[i])
        del(handles[i])
    else:
        i +=1
plt.legend(handles, labels)

# configure plot settings
axis.grid()
axis.set_xlabel("Distance [m]")
axis.set_ylabel("Velocity [m/s]")
axis.set_title("Exponential decay model compared with measurements")
plt.show()