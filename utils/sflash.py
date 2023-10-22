#==========================================================
# NOR utils
# part of ps5 wee tools project
#==========================================================
import hashlib, os, math, sys, ctypes
from lang._i18n_ import *
import lang._i18n_ as Lang
import utils.utils as Utils
import data.data as Data


DUMP_SIZE = 0x200000
BACKUP_OFFSET = 0x3000
MBR_SIZE = 0x1000
BLOCK_SIZE = 0x200

PS_REGIONS = {
	'00':'Japan',
	'01':'US, Canada (North America)',
	'15':'US, Canada (North America)',
	'02':'Australia / New Zealand (Oceania)',
	'03':'U.K. / Ireland',
	'04':'Europe / Middle East / Africa',
	'16':'Europe / Middle East / Africa',
	'05':'Korea (South Korea)',
	'06':'Southeast Asia / Hong Kong',
	'07':'Taiwan',
	'08':'Russia, Ukraine, India, Central Asia',
	'09':'Mainland China',
	'11':'Mexico, Central America, South America',
	'14':'Mexico, Central America, South America',
}

# {'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
NOR_PARTITIONS = {
	"header"		: {"o": 0x000000,	"l": 0x1000,	"n":"head"},
	"active_slot"	: {"o": 0x001000,	"l": 0x1000,	"n":"act_slot"},
	"MBR1"			: {"o": 0x002000,	"l": 0x1000,	"n":"mbr1"},
	"MBR2"			: {"o": 0x003000,	"l": 0x1000,	"n":"mbr2"},
	"emc_ipl_a"		: {"o": 0x004000,	"l": 0x7E000,	"n":"emc_ipl_a"},
	"emc_ipl_b"		: {"o": 0x082000,	"l": 0x7E000,	"n":"emc_ipl_b"},
	"usb_pdc_a"		: {"o": 0x100000,	"l": 0x10000,	"n":"usb_pdc_a"},
	"usb_pdc_b"		: {"o": 0x110000,	"l": 0x10000,	"n":"usb_pdc_b"},
	"unk"			: {"o": 0x111000,	"l": 0xB3000,	"n":"unknown"},
	"nvs"			: {"o": 0x1C4000,	"l": 0x0C000,	"n":"nvs"},
	"reserved"		: {"o": 0x1D0000,	"l": 0x30000,	"n":"reserved"},
}

# 'KEY':{'o':<offset>, 'l':<length>, 't':<type>, 'n':<name>}
NOR_AREAS = {
	
	'ACT_SLOT':	{'o':0x001000,	'l':1,			't':'b',	'n':'Active slot'},		# 0x00 - A 0x80 - B
	
	'BOARD_ID':	{'o':0x1C4000,	'l':8,			't':'s',	'n':'Board id'},
	'MAC':		{'o':0x1C4020,	'l':6,			't':'b',	'n':'LAN MAC Address'},
	
	'MODEL':	{'o':0x1C7011,	'l':1,			't':'b',	'n':'Model variant'}, # 02 disc / 03 digital
	'MB_SN':	{'o':0x1C7200,	'l':16,			't':'s',	'n':'Motherboard Serial'},
	'SN':		{'o':0x1C7210,	'l':17,			't':'s',	'n':'Console Serial'},
	'SKU':		{'o':0x1C7230,	'l':13,			't':'s',	'n':'SKU Version'},
	'REGION':	{'o':0x1C7236,	'l':2,			't':'s',	'n':'Region code'}, # where is the region byte code?
	'KIBAN':	{'o':0x1C7250,	'l':13,			't':'s',	'n':'Kiban id'},
	'SOCUID':	{'o':0x1C7260,	'l':16,			't':'s',	'n':'Social UID?'},
	'MAC2':		{'o':0x1C73C0,	'l':6,			't':'b',	'n':'WiFi MAC Address'},
	
	'EAP_MGC':	{'o':0x1C75FC,	'l':4,			't':'b',	'n':b'\xE5\xE5\xE5\x01'},		# Eap key magic 1CB1FC - 1C81FC = 3000 | 1C81FC - 1C75FC = C00
	
	'FW_U':		{'o':0x1C8068,	'l':4,			't':'b',	'n':'Current FW upper'},		#B+
	
	'FW_F':		{'o':0x1C8C10,	'l':8,			't':'b',	'n':'Factory FW'},				#B+
	'FW_F_TS':	{'o':0x1C8C18,	'l':8,			't':'b',	'n':'Factory FW timestamp'},	#B+
	
	'FW_M':		{'o':0x1C8C20,	'l':8,			't':'b',	'n':'Minimum FW'},				#B+
	'FW_M_TS':	{'o':0x1C8C28,	'l':8,			't':'b',	'n':'Minimum FW timestamp'},	#B+
	
	'FW':		{'o':0x1C8C30,	'l':8,			't':'b',	'n':'Current FW'}, 				#B+
	
	'IDU':		{'o':0x1C9600,	'l':1,			't':'b',	'n':'IDU (Kiosk mode)'},		#B+ | On(01), Off(00/FF)
}

PS_MODELS = {b'\x02':'Disc edition', b'\x03':'Digital edition'}

MAGICS = {
	"MBR"		: {"o": 0x00,		"v":b'SONY COMPUTER ENTERTAINMENT INC.'},
	"MBR1"		: {"o": 0x2000,		"v":b'Sony Computer Entertainment Inc.'},
	"MBR2"		: {"o": 0x3000,		"v":b'Sony Computer Entertainment Inc.'},
	"EAP1"		: {"o": 0x1C75FC,	"v":b'\xE5\xE5\xE5\x01'},
	"EAP2"		: {"o": 0x1C81FC,	"v":b'\xE5\xE5\xE5\x01'},
	"EAP3"		: {"o": 0x1CB1FC,	"v":b'\xE5\xE5\xE5\x01'},
}

# MBR parser

class Partition(ctypes.Structure):
	_pack_ = 1
	_fields_ = [
		("start_lba",	ctypes.c_uint32),
		("n_sectors",	ctypes.c_uint32),
		("type",		ctypes.c_uint8),		# part_id?
		("flag",		ctypes.c_uint8),
		("unknown",		ctypes.c_uint16),
		("padding",		ctypes.c_uint64)
	]
	
	def getName(self):
		code = self.type
		return PARTITIONS_TYPES[code] if code in PARTITIONS_TYPES else 'UNK_'+str(code)
	
	def getOffset(self):
		return self.start_lba * BLOCK_SIZE
	
	def getSize(self):
		return self.n_sectors * BLOCK_SIZE

class MBR_v1(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic", 		ctypes.c_uint8 * 0x20),	# SONY COMPUTER ENTERTAINMENT INC.
        ("version", 	ctypes.c_uint32),		# 1
        ("mbr1_start",	ctypes.c_uint32),		# ex: 0x10
        ("mbr2_start",	ctypes.c_uint32),		# ex: 0x18
        ("unk",			ctypes.c_uint32 * 4),	# ex: (1, 1, 8, 1)
        ("reserved",	ctypes.c_uint32),
        ("unused",		ctypes.c_uint8 * 0x1C0)
    ]

class MBR_v4(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("magic",		ctypes.c_uint8 * 0x20),	# Sony Computer Entertainment Inc.
        ("version",		ctypes.c_uint32),		# 4
        ("n_sectors",	ctypes.c_uint32),
        ("reserved",	ctypes.c_uint64),
        ("loader_start",ctypes.c_uint32),		# ex: 0x11, 0x309
        ("loader_count",ctypes.c_uint32),		# ex: 0x267
        ("reserved2",	ctypes.c_uint64),
        ("partitions",	Partition * 16)
	]

PARTITIONS_TYPES = {
	0:"empty",
	1:"idstorage",
	2:"sam_ipl",
	3:"core_os",
	6:"bd_hrl",
	13:"emc_ipl",
	14:"eap_kbl",
	32:"emc_ipl",
	33:"eap_kbl",
	34:"nvs",
	38:"wifi",
	39:"vtrm",
	40:"empty",
	41:"C0050100",
}

# Functions ===============================================

def getConsoleRegion(file):
	code = getNorData(file, 'REGION', True)
	desc = PS_REGIONS[code] if code in PS_REGIONS else STR_UNKNOWN
	return [code, desc]



def getPartitionName(code):
	return PARTITIONS_TYPES[code] if code in PARTITIONS_TYPES else 'Unk_'+str(code)



def getNorPartition(f, name):
	if not name in NOR_PARTITIONS:
		return ''
	return Utils.getData(f, NOR_PARTITIONS[name]['o'], NOR_PARTITIONS[name]['l'])



def getNorPartitionMD5(f, name):
	data = getNorPartition(f, name)
	if len(data) > 0:
		return hashlib.md5(data).hexdigest()
	return ''



def getDataByPartition(name):
	
	if not name:
		return False
	elif name.find('emc_ipl') >= 0:
		return Data.EMC_IPL_MD5
	elif name.find('usb_pdc') >= 0:
		return Data.USB_PDC_MD5
	
	return False



def checkMagic(data, key):
	if len(data) <= 0:
		return False
	if key in MAGICS:
		offset = MAGICS[key]['o']
		length = offset + len(MAGICS[key]['v'])
		if data[offset:length] == MAGICS[key]['v']:
			return True
	return False



def getPartitionsInfo(f):
	# f - file in rb/r+b mode
	f.seek(MBR_SIZE)
	# active slot at 0x1000
	active = f.read(1)
	
	base = MBR_SIZE*2 if active == 0x00 else MBR_SIZE*3
	f.seek(base)
	mbr = MBR_v4()
	f.readinto(mbr)
	
	partitions = []
	
	for i in range(len(mbr.partitions)):
		p = mbr.partitions[i]
		if p.getSize() == 0:
			continue
		partitions.append({
			'name'		: p.getName(),
			'offset'	: p.getOffset() + base,
			'size'		: p.getSize(),
			'type'		: p.type,
		})
	
	return {'slot':active, 'base':base, 'parts':partitions}



def getNorFW(f, full = True):
	fw = getNorData(f, 'FW')[::-1]
	fw_m = getNorData(f, 'FW_M')[::-1]
	fw_f = getNorData(f, 'FW_F')[::-1]
	
	if full:
		return {'c':fw, 'f':fw_f, 'm':fw_m}
	else:
		return {'c':'%d.%02d'%(fw[0],fw[1]), 'f':'%d.%02d'%(fw_f[0],fw_f[1]), 'm':'%d.%02d'%(fw_m[0],fw_m[1])}



# NOR Areas data utils

def getNorAreaName(key):
	if key in NOR_AREAS:
		return NOR_AREAS[key]['n']
	return STR_UNKNOWN



def setNorData(file, key, val):
	if not key in NOR_AREAS:
		return False
	return Utils.setData(file, NOR_AREAS[key]['o'], val)


def getNorDataByPath(path, key, decode = False):
	with open(path, 'rb') as f:
		data = getNorData(f, key, decode)
	return data



def setNorDataB(file, key, val):
	if not key in NOR_AREAS:
		return False
	return Utils.setData(file, NOR_AREAS[key]['o'] + BACKUP_OFFSET, val)



def getNorData(file, key, decode = False):
	if not key in NOR_AREAS:
		return 'False' if decode else False
	data = Utils.getData(file, NOR_AREAS[key]['o'], NOR_AREAS[key]['l'])
	return data.decode('utf-8','ignore').strip('\x00') if decode else data



def getNorDataB(file, key, decode = False):
	if not key in NOR_AREAS:
		return 'False' if decode else False
	data = Utils.getData(file, NOR_AREAS[key]['o'] + BACKUP_OFFSET, NOR_AREAS[key]['l'])
	return data.decode('utf-8','ignore').strip('\x00') if decode else data



def getSFlashInfo(file = '-'):
	with open(file, 'rb') as f:
		
		active_slot = 'A' if getNorData(f, 'ACT_SLOT')[0] == 0x00 else 'B'
		model = getNorData(f, 'MODEL')
		region = getConsoleRegion(f)
		fw = getNorFW(f, False)
		
		info = {
			'FILE'			: os.path.basename(file),
			'MD5'			: Utils.getFileMD5(file),
			'Board ID'		: Utils.hex(getNorData(f, 'BOARD_ID'),':'),
			'Model'			: PS_MODELS[model] if model in PS_MODELS else STR_UNKNOWN,
			'SKU / Slot'	: getNorData(f, 'SKU', True) + ' / [%s]'%active_slot,
			'Region'		: '[{}] {}'.format(region[0], region[1]),
			'SN / Mobo SN'	: getNorData(f, 'SN', True)+' / '+getNorData(f, 'MB_SN', True),
			'Kiban ID'		: getNorData(f, 'KIBAN', True),
			'FW (current)'	: fw['c'],
			'FW (min/fac)'	: fw['m'] + ' / ' + fw['f'],
			'MAC LAN'		: Utils.hex(getNorData(f, 'MAC'),':'),
			'MAC WiFi'		: Utils.hex(getNorData(f, 'MAC2'),':'),
		}
	
	return info
