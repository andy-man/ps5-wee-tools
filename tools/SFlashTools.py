#==============================================================
# PS4 Nor Tools
# part of ps5 wee tools project
#==============================================================
import os, time
from lang._i18n_ import *
import utils.utils as Utils
import utils.sflash as SFlash
import utils.slb2 as BLS
import tools.Tools as Tools


def screenExtractNorDump(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_NOR_EXTRACT))
	
	with open(file, 'rb') as f:
		
		sn = SFlash.getNorData(f, 'SN', True)
		folder = os.path.dirname(file) + os.sep + sn + os.sep
		
		if not os.path.exists(folder):
			os.makedirs(folder)
		
		info = ''
		data = SFlash.getSFlashInfo(file)
		for key in data:
			info += '{} : {}\n'.format(key.ljust(12,' '),data[key])
		info += '\n'
		
		print(STR_EXTRACTING%sn+'\n')
		
		i = 0
		for k in SFlash.NOR_PARTITIONS:
			p = SFlash.NOR_PARTITIONS[k]
			i += 1
			print(' {:2d}: {:16s} > {}'.format(i, k, p['n']))
			info += '{:2d}: {:16s} > {}\n'.format(i, k, p['n'])
			
			with open(folder + p['n'], 'wb') as out:
				out.write(SFlash.getNorPartition(f, k))
		
		with open(folder + Utils.INFO_FILE_SFLASH, 'w') as txt:
			txt.write(info)
		
		print('\n'+STR_SAVED_TO%folder)
	
	print('\n'+STR_DONE)
	
	input(STR_BACK)



def screenBuildNorDump(folder):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_NOR_BUILD))
	
	if not os.path.exists(folder):
		print(STR_NO_FOLDER%(folder)+'\n\n'+STR_ABORT)
		input(STR_BACK)
		return
	
	print(STR_FILES_CHECK.format(folder)+'\n')
	
	found = 0
	
	i = 0
	for k in SFlash.NOR_PARTITIONS:
		p = SFlash.NOR_PARTITIONS[k]
		i += 1
		status = STR_OK
		
		file = folder+os.sep+p['n']
		if not os.path.exists(file):
			status = STR_NOT_FOUND
		elif os.stat(file).st_size != p['l']:
			status = STR_BAD_SIZE
		else:
			found += 1
		
		print(' {:2d}: {:20s} - {}'.format(i, p['n'], status))
	
	print()
	
	if found == len(SFlash.NOR_PARTITIONS):
		
		"""
		sn = '0'*17
		with open(folder+os.sep+SFlash.NOR_PARTITIONS['s0_nvs']['n'],'rb') as nvs:
			nvs.seek(0x4030)
			sn = nvs.read(17)
		"""
		
		fname = os.path.join(folder, 'sflash0.bin')
		
		print(STR_BUILDING%fname)
		
		out = open(fname,"wb")
		
		for k in SFlash.NOR_PARTITIONS:
			file = folder+os.sep+SFlash.NOR_PARTITIONS[k]['n']
			with open(file, 'rb') as f:
				out.write(f.read())
		
		out.close()
		
		print('\n'+STR_DONE)
	else:
		print(STR_ABORT)
	
	input(STR_BACK)



def screenFlagsToggler(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_WARNING))
	
	print(UI.warning(STR_PATCHES))
	
	print(UI.getTab(STR_NOR_FLAGS))
	
	with open(file, 'rb') as f:
		
		patches = [
			{'k':'MODEL',		'v':list(SFlash.PS_MODELS.keys()),	'd':list(SFlash.PS_MODELS.values())},
			{'k':'IDU',			'v':[b'\x00',b'\x01'],				'd':[STR_OFF,STR_ON]},
			{'k':'ACT_SLOT',	'v':[b'\x00',b'\x80'],				'd':['A','B']},
		]
		
		for i in range(len(patches)):
			name = SFlash.getNorAreaName(patches[i]['k'])
			val = SFlash.getNorData(f, patches[i]['k'])
			str = '['+Utils.hex(val,'')[:32]+']'
			for k in range(len(patches[i]['v'])):
				if val == patches[i]['v'][k]:
					str = patches[i]['d'][k]
			print(' {:2d}: {:24s}: {}'.format(i+1, name, str))
	
	print(UI.DIVIDER)
	
	print(' 0:'+STR_GO_BACK)
	
	UI.showStatus()
	
	try:
		choice = input(STR_CHOICE)
		num = int(choice)
	except:
		num = -1
	
	if num == 0:
		return
	elif num > 0 and num <= len(patches):
		toggleFlag(file, patches[num-1])
	
	screenFlagsToggler(file)



def toggleFlag(file, patch):
	with open(file, 'r+b') as f:
		
		cur = SFlash.getNorData(f, patch['k'])
		for i in range(0,len(patch['v'])):
			if cur == patch['v'][i]:
				break
		i = 0 if (i + 1) >= len(patch['v']) else i + 1
		val = patch['v'][i]
		
		SFlash.setNorData(f, patch['k'],  patch['v'][i])
		if 'b' in patch and patch['b'] == True:
			# Set flag in backup area
			SFlash.setNorDataB(f, patch['k'], patch['v'][i])
	
	UI.setStatus(STR_SET_TO%(SFlash.getNorAreaName(patch['k']), patch['d'][i]))



def screenPartitionsInfo(file):
	UI.clearScreen()
	print(TITLE+UI.getTab('Partitions info'))
	
	with open(file,'rb') as f:
		data = SFlash.getPartitionsInfo(f)
		slot = 'A' if data['slot'] == b'\x00' else 'B'
		print(' Active slot: %s [0x%02X]'%(slot, data['slot'][0]))
		print()
		for i in range(len(data['parts'])):
			p = data['parts'][i]
			print(UI.highlight(' #%d %s'%(i+1, p['name'])))
			UI.showTable({
				'Offset':'%8d [0x%x]'%(p['offset'],p['offset']),
				'Size':'%8d [0x%x]'%(p['size'],p['size']),
				'Type':'%8d [0x%x]'%(p['type'],p['type']),
			})
			print()
	
	choice = input(STR_CHOICE)



def screenValidate(file):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_NOR_VALIDATOR))
	
	with open(file,'rb') as f:
		data = f.read()
		fw = SFlash.getNorFW(f, 4)['c']
		slot = 'A' if SFlash.getNorData(f, 'ACT_SLOT')[0] == 0x00 else 'B'
		
		print(STR_FW_VERSION%(fw,slot)+'\n')
		
		magics = {}
		for k in SFlash.MAGICS:
			magics[k] = STR_OK if SFlash.checkMagic(data, k) else STR_DIFF
		
		print(UI.highlight(STR_MAGICS_CHECK)+'\n')
		UI.showTable(magics,10)
		print()
		
		print(UI.highlight(STR_PARTITIONS_CHECK)+'\n')
		
		bls_parts = ['emc_ipl_a', 'emc_ipl_b', 'usb_pdc_a', 'usb_pdc_b']
		for i, k in enumerate(bls_parts):
			print(UI.cyan(' #%d %s'%(i,k)))
			data = SFlash.getNorPartition(f, k)
			head = BLS.getGet2BLSInfo(data)['header']
			md5 = Utils.getMD5(data)
			hash_list = SFlash.getDataByPartition(k)
			info = {
				'Magic'		: STR_OK if 'magic' in head else STR_FAIL,
				'MD5'		: '%s | %s'%(md5, STR_OK if md5 in hash_list else UI.warning('??')),
				'Size'		: '%d bytes'%head['size'] if 'size' in head else STR_FAIL,
				'Entries'	: head['entries'] if 'entries' in head else STR_FAIL,
			}
			UI.showTable(info)
			print()
	
	print(UI.highlight(STR_ENTROPY)+'\n')
	#stats = {'ent':0,'ff':0,'00':0}
	stats = Utils.entropy(file)
	print('\r',end='')
	
	info = {
		
		'Entropy'	: '{:.5f}'.format(stats['ent']),
		'0xFF'		: '{:.2f}%'.format(stats['ff']*100),
		'0x00'		: '{:.2f}%'.format(stats['00']*100),
		'Other'		: '{:.2f}%'.format((1 - stats['ff'] - stats['00'])*100),
	}
	
	UI.showTable(info,10)
	
	input(STR_BACK)



def screenSFlashTools(file):
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_NOR_INFO))
	
	info = SFlash.getSFlashInfo(file)
	if info:
		info['Board ID'] = UI.highlight(info['Board ID'])
		UI.showTable(info)
	else:
		return Tools.screenFileSelect(file)
	
	print(UI.getTab(STR_ACTIONS))
	
	UI.showMenu(MENU_NOR_ACTIONS,1)
	print(UI.DIVIDER)
	UI.showMenu(MENU_EXTRA)
	
	UI.showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '1':
	    screenFlagsToggler(file)
	elif choice == '2':
	    screenExtractNorDump(file)
	elif choice == '3':
	    screenBuildNorDump(os.path.dirname(file) + os.sep + SFlash.getNorData(file, 'SN', True))
	elif choice == '4':
	    screenValidate(file)
	
	elif choice == 's':
	    return Tools.screenFileSelect(file)
	elif choice == 'f':
		return Tools.screenNorFlasher(file)
	elif choice == 'm':
	    return Tools.screenMainMenu()
	
	screenSFlashTools(file)
