import sys, os, numpy
from xml.etree import ElementTree

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
    
    for atype in tree.findall('constraint'):
        print(atype.text)
      
    """    
    for atype in tree.findall('bound'): # this has more data, will require more work
        for btype in atype:
            print(btype.tag)
    """
    for bound in tree.iter('bound'):
        varname = bound.find('var').text
        low = bound.find('min').text
        high = bound.find('max').text
        print varname, low, high
        
        
    for atype in tree.findall('energy'):
        print(atype.text)
        
    for atype in tree.findall('minimax'):
        print(atype.text)
    
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