#==========================================================
# Common utils
# part of ps5 wee tools project
#==========================================================
import hashlib, os, math, random, datetime
from lang._i18n_ import *

# Common consts

INFO_FILE_SFLASH	= '_sflash0_.txt'
INFO_FILE_2BLS		= '_2bls_.txt'



def getEmcCmd(str):
	sum = 0
	for i in range(len(str)):
		sum += ord(str[i])
	return str + ':%02X'%(sum & 0xFF)


def ceil(a, b):
	return (a // b) + (1 if a % b else 0)


def checkCtrl(s, key):
	return ord(s) + 0x40 == ord(key)



def genRandBytes(size):
	return bytearray(random.getrandbits(8) for _ in range(size))



def getMemData(data, offset, lenght):
	if len(data) >= offset+lenght:
		return data[offset : offset+lenght]
	return b''



def getData(file, off, len):
	try:
		if isinstance(file, str):
			with open(file, 'rb') as f:
				f.seek(off)
				return f.read(len)
		else:
			file.seek(off)
			return file.read(len)
	except:
		return ''



def setData(file, off, val):
	try:
		if isinstance(file, str):
			with open(file, 'r+b') as f:
				f.seek(off)
				return f.write(val)
		else:
			file.seek(off)
			return file.write(val)
	except:
		return ''



def checkFileSize(file, size):
	if not file or not os.path.isfile(file):
		print(STR_FILE_NOT_EXISTS%file)
		input(STR_BACK)
		return False
	
	if os.stat(file).st_size != size:
		print(STR_INCORRECT_SIZE%file)
		input(STR_BACK)
		return False
	
	return True



def getFilePathWoExt(file, fix_spaces = False):
	name = os.path.splitext(os.path.basename(file))[0]
	name = name.replace(" ", "_") if fix_spaces else name
	return os.path.join(os.path.dirname(file),name)



def getFileMD5(file):
	with open(file, 'rb') as f:
		f.seek(0)
		d = f.read()
	return getMD5(d)



def getMD5(data):
	return hashlib.md5(data).hexdigest()


def getFileTime(path):
	ts = os.stat(path).st_mtime
	date = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
	return {'ts':ts, 'date':date}



def hex(buf,sep=' '):
	str = ""
	for c in buf:
		str += '{:02X}'.format(c)+sep
	return str[:len(str)-len(sep)]



def swapBytes(arr):
	res = [0]*len(arr)
	for i in range(0,len(arr),2):
		res[i] = arr[i+1]
		res[i+1] = arr[i]
	return bytes(res)



def getFileContents(path):
	with open(path, 'rb') as f:
		return f.read()



def savePatchData(path, data, patch = False):
	with open(path, 'wb') as f:
		f.write(data)
	if patch:
		patchFile(path, patch)



def patchFile(path, patch):
	with open(path, 'r+b') as f:
		for i in range(len(patch)):
			f.seek(patch[i]['o'],0)
			f.write(patch[i]['d'])



def entropy(file):
	
	with open(file, "rb") as f:
		data = f.read()
	
	vals = {byte: 0 for byte in range(2**8)}
	size = len(data)
	pp = size // 100
	
	for i in range(size):
		vals[data[i]] += 1
		if i % pp == 0:
			print('\r'+STR_PROGRESS%(i // pp),end='')
	
	probs = [val / size for val in vals.values()]
	entropy = -sum(prob * math.log2(prob) for prob in probs if prob > 0)
	
	return {'00':probs[0],'ff':probs[0xff],'ent':entropy}
