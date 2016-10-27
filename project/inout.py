from xml.etree import ElementTree
from structures import Constraint, Objective, Decision

"""Helper methods for io
"""
def read_data(filename):
    """Takes tree returned from xml_reader and builds the model from that data
    """
    xmltree = readdata(filename)
    decisions = []
    objectives = []
    constraints = []

    for cin in xmltree.findall('constraint'):
        constraints.append(Constraint(cin.text))

    for bound in xmltree.iter('bound'):
        varname = bound.find('var').text
        low = float(bound.find('min').text)
        high = float(bound.find('max').text)
        decisions.append(Decision(varname, low, high))

    for ener in xmltree.iter('energy'):
        varname = ener.find('function').text
        func = varname
        minimize = ener.find('minimize').text
        objectives.append(Objective(varname, func, minimize))
    
    earlyout = eval(xmltree.find('omax').text)

    return decisions, objectives, constraints, earlyout

def xml_reader(filename):
    """Reads an xml file into a tree that can be parsed.
    Here the model is created as an xml document, this reads in the model
    Future versions will have all the I/O abstracted into an I/O class
    """
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    return tree


def readdata(filename):  
    """Generic reader that acts as a quarterback to different file-specific I/O operations
    """
    if '.xml' in filename:
        data = xml_reader(filename)
    else:
        print("need to get csv reader")
    return data


