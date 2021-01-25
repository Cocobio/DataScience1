import ctypes
import numpy as np

try:
    _c_funcs = ctypes.cdll.LoadLibrary("./talairach/functions.so")
except:
    _c_funcs = ctypes.cdll.LoadLibrary("./functions.so")
    
_saveBundlesData = _c_funcs.saveBundlesData
_saveBundlesData.argtypes = (ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int)



def saveBundle(points, fiberSizes, bundlesName, bundlesStart, curvescount, out_file):
# wrtie minf file
    minf = """attributes = {\n    'binary' : 1,\n    'bundles' : %s,\n    'byte_order' : 'DCBA',\n    'curves_count' : %s,\n    'data_file_name' : '*.bundlesdata',\n    'format' : 'bundles_1.0',\n    'space_dimension' : 3\n  }\n"""

    bundlesstr = []
    for name, offset in zip(bundlesName, bundlesStart):
        bundlesstr.append(name)
        bundlesstr.append(offset)
        
    bundlesstr = str(bundlesstr)
    bundlesstr = bundlesstr[0] + ' ' + bundlesstr[1:-1] + ' ' + bundlesstr[-1]

    with open(out_file, 'w') as f:
        f.write( minf % (bundlesstr, curvescount))

    _saveBundlesData(
        (out_file+"data").encode('utf-8'),
        points.ctypes.data,
        fiberSizes.ctypes.data,
        curvescount)