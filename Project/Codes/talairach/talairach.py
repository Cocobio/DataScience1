import os
import sys
import numpy as np
import ctypes

try:
	_c_funcs = ctypes.cdll.LoadLibrary("./talairach/functions.so")
except:
	_c_funcs = ctypes.cdll.LoadLibrary("./functions.so")

_readBundleFile = _c_funcs.readBundleFile
_readBundleFile.argtypes = (ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int)

_applyMatrix = _c_funcs.applyMatrix
_applyMatrix.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p)

_saveBundlesData = _c_funcs.saveBundlesData
_saveBundlesData.argtypes = (ctypes.c_char_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int)

class Bundle:
	def __init__(self, file_path):
		self.path = file_path
		self.points = None
		self.fiberSizes = None

		self.bundlesName = None
		self.bundleStart = None
		self.curvescount = 0

		self.readFibers()

	def readFibers(self):
		datafile = self.path + 'data'
		dataSize = os.path.getsize(datafile)

		ns = dict()
		with open(self.path) as f:
			exec(f.read(), ns)

		bundlescount = ns['attributes']['bundles']
		self.curvescount = ns['attributes']['curves_count']

		self.bundlesName = bundlescount[::2]
		self.bundlesStart = bundlescount[1::2]

		self.points = np.empty(dataSize//4-self.curvescount, dtype=np.float32)
		self.fiberSizes = np.empty(self.curvescount, dtype=np.int32)

		_readBundleFile(
			datafile.encode('utf-8'),
			self.points.ctypes.data,
			self.fiberSizes.ctypes.data,
			self.curvescount)

	def saveBundle(self, out_file):
		# wrtie minf file
		minf = """attributes = {\n    'binary' : 1,\n    'bundles' : %s,\n    'byte_order' : 'DCBA',\n    'curves_count' : %s,\n    'data_file_name' : '*.bundlesdata',\n    'format' : 'bundles_1.0',\n    'space_dimension' : 3\n  }\n"""

		bundlesstr = []
		for name, offset in zip(self.bundlesName, self.bundlesStart):
			bundlesstr.append(name)
			bundlesstr.append(offset)
		
		bundlesstr = str(bundlesstr)
		bundlesstr = bundlesstr[0] + ' ' + bundlesstr[1:-1] + ' ' + bundlesstr[-1]

		with open(out_file, 'w') as f:
			f.write( minf % (bundlesstr, self.curvescount))

		_saveBundlesData(
			(out_file+"data").encode('utf-8'),
			self.points.ctypes.data,
			self.fiberSizes.ctypes.data,
			self.curvescount)


def loadTrmMatrix(trmFile):
	transform = np.zeros(16,dtype=np.float32)

	with open(trmFile) as f:
		lines = f.readlines()
		translate = lines[0].split(' ')

		transform[0:3] = [float(x) for x in lines[1].split(' ')]
		transform[3] = float(translate[0])
		
		transform[4:7] = [float(x) for x in lines[2].split(' ')]
		transform[7] = float(translate[1])
		
		transform[8:11] = [float(x) for x in lines[3].split(' ')]
		transform[11] = float(translate[2])

		transform[15] = 1.0

	return transform

def applyMatrix(data, transform):
	_applyMatrix(
		data.ctypes.data,
		data.size,
		transform.ctypes.data)

if len(sys.argv) != 4:
 	sys.exit('Argument error. Correct syntax: "python3 ' + sys.argv[0] + ' input_bundle.bundles output_bundle.bundles trm_matrix_file.trm"');

fiber_file = sys.argv[1]
fiber_out_file = sys.argv[2]
matrix_file = sys.argv[3]

matrix = loadTrmMatrix(matrix_file)

bundle = Bundle(fiber_file)
applyMatrix(bundle.points, matrix)

bundle.saveBundle(fiber_out_file)