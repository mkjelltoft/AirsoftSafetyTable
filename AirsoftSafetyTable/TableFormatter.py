import numpy as np

# ********** Define functions *************************************************
def toBold(string):
    return "{\\bf " + string + "}"

def toGram(kg):
    return ".{:.0f}".format(kg*100000)

def toms(ms):
    return "{:.1f}".format(ms)

def formatLatexTable(masses, \
                     distances, \
                     velocities, \
                     classNames = ["CQB\t", "Auto A", "Auto B", "Semi", "Bolt A", "Bolt B"], \
                     outputFile = "table.txt"):
    separator = "\t&\t"
    lineEnding = "\t\\\\"
    newline = "\n"
    hline = "\\hline\n"
    headerWords = ["Class", "Safety distance"]
    # Input validation
    if distances.size != len(classNames):
        return "Missmatch between class names ({:d}) and distances ({:d}).".format(len(classNames), distances.size)
    if velocities.shape[0] != distances.size:
        return "Missmatch between velocities and distances."
    if velocities.shape[1] != masses.size:
        return "Missmatch between velocities and masses."
    # Format header
    first = True
    header = ""
    for word in headerWords:
        header += toBold(word) if first else separator + toBold(word)
        first = False
    for mass in masses:
        header += separator + toBold(toGram(mass))
    header += lineEnding
    # Format rows
    rows = [""]*len(classNames)
    for i_class in range(len(classNames)):
        rows[i_class] = classNames[i_class] + separator + str(distances[i_class])
        for vel in velocities[i_class]:
            rows[i_class] += separator + toms(vel)
        rows[i_class] += lineEnding
    # Format final string
    tableString = hline + header + newline + hline + hline
    for row in rows:
        tableString += row + newline + hline
    # Write result
    file = open(outputFile, "w")
    file.write(tableString)
    file.close()
    return tableString

def formatHtmlTable(masses, \
                    distances, \
                    velocities, \
                    classNames = ["CQB\t", "Auto A", "Auto B", "Semi", "Bolt A", "Bolt B"], \
                    outputFile = "table.html",
                    fps = False):
    lineEnding = "</tr>"
    newline = "\n"
    headerWords = ["Klass", "S-avstånd"]
    rowColors = ['"#EEEEEE"', '"#CCCCCC"']
    mps2fps = 3.28084
    # Input validation
    if distances.size != len(classNames):
        return "Missmatch between class names ({:d}) and distances ({:d}).".format(len(classNames), distances.size)
    if velocities.shape[0] != distances.size:
        return "Missmatch between velocities and distances."
    if velocities.shape[1] != masses.size:
        return "Missmatch between velocities and masses."
    # Format table start
    tableStart = '<table style="border: 1px solid black; border-collapse: collapse; width: 100%; font-size: 100%;" border="1">\n'
    tableStart += '\t<tbody>\n'
    # Format title
    title = '\t\t<tr bgcolor='+rowColors[1]+'>\n'
    title += '\t\t\t<th style="font-size: 120%" align="left" colspan="' + str(len(masses)+2) + '">VSAF säkerhetstabell för airsoft ('
    if fps:
        title += 'fps'
    else:
        title += 'm/s'
    title += ')</th>\n'
    title += '\t\t</tr>\n'
    # Format header
    header = '\t\t<tr bgcolor='+rowColors[1]+'>\n'
    for word in headerWords:
        header += '\t\t\t<th>' + word + '</th>\n'
    for mass in masses:
        header += '\t\t\t<th>' + toGram(mass) + 'g</th>\n'
    header += '\t\t</tr>\n'
    # Format rows
    if (fps):
        velocities *= mps2fps
    rows = [""]*len(classNames)
    for i_class in range(len(classNames)):
        rows[i_class] = '\t\t<tr bgcolor=' + rowColors[i_class % 2] + '>\n'
        rows[i_class] += '\t\t\t<td>' + classNames[i_class] + '</td>\n'
        rows[i_class] += '\t\t\t<td>' + str(distances[i_class]) + 'm</td>\n'
        for vel in velocities[i_class]:
            rows[i_class] += '\t\t\t<td>' + toms(vel) + '</td>\n'
        rows[i_class] += '\t\t</tr>\n'
    # Format footer
    footer = '\t</tbody>\n'
    footer += '</table>\n'
    footer += '<p> </p>'
    # Format final string
    tableString = tableStart + title + header
    for row in rows:
        tableString += row
    tableString += footer
    # Write result
    file = open(outputFile, "w")
    file.write(tableString)
    file.close()
    return tableString

# ********** Test *************************************************************
#test_masses = np.array([20, 25, 28, 30, 34, 36, 40, 43, 45])/100000 # kg
#test_distances = np.array([0, 5, 10, 20, 30, 40]) # m
#test_velocities = np.array(np.ones([test_distances.size, test_masses.size])); # m/s
#formatLatexTable(test_masses, test_distances, test_velocities)