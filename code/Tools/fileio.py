import sys, os, numpy
from xml.etree import ElementTree
#from model import Constraint, Decision, Objective #TODO - make a "model" class that has all of this.

# Helper methods
def filelist(txt, filetype, filepath):
    path = filepath       
    files = [f for f in os.listdir(path) if f.endswith('.'+ filetype) & (txt in f)]
    return files

def readdata(filename): # this was originally intended for bulk input of files, but it now only does one.  Watch for things I forgot to fix.
    if '.xml' in filename:
        data = xml_reader(filename)
    else:
        data = csv_reader(filename)
    return data

def xml_reader(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    
    return tree
        
def csv_reader(filenames):
    data = numpy.genfromtxt(
        filenames,
        names = True, #  If `names` is True, the field names are read from the first valid line
        comments = '#', # Skip characters after #
        delimiter = ',', # comma separated values
        dtype = None)  # guess the dtype of each column
    return data
        
def read(txt, filetype, filepath='.'):
    files = filelist(txt, filetype, filepath)
    for f in files:
        return readdata(f)
        
def easyread(fname):
    data = numpy.genfromtxt(
    fname,
    names = True, #  If `names` is True, the field names are read from the first valid line
    comments = '#', # Skip characters after #
    delimiter = ',', # comma separated values
    dtype = None)  # guess the dtype of each column
    print data.dtype.names

# Helper methods

def read_data(filename): 
    xmltree = read(filename, 'xml')
    decisions = [] 
    objectives = []
    constraints = []
    
    
    for cin in xmltree.findall('constraint'):
        constraints.append(Constraint(cin.text))
        
    for bound in xmltree.iter('bound'):
        varname = bound.find('var').text
        low = bound.find('min').text
        high = bound.find('max').text
        decisions.append(Decision(varname, low, high))
        
    for ener in xmltree.iter('energy'):
        varname = ener.find('function').text
        func = varname
        minimize = ener.find('minimize').text
        objectives.append(Objective(varname, func, minimize))
    print(decisions, objectives, constraints)    
    return decisions, objectives, constraints
    
def objective_data(xmltree):
    res = []
    for cin in xmltree.findall('energy'):
        res.append(cin.text, cin.text)
    return res
    
def constraint_data(xmltree):
    res = []
    for cin in xmltree.findall('constraint'):
        res.append(Constraint(cin.text))
    return res
    
def decision_data(xmltree):
    res = []
    for bound in xmltree.iter('bound'):
        varname = bound.find('var').text
        low = bound.find('min').text
        high = bound.find('max').text
        res.append(Decision(varname, low, high))
    return res