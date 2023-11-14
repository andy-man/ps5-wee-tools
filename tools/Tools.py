#==============================================================
# Common Tools
# part of ps5 wee tools project
#==============================================================
import os, sys, time, datetime
from lang._i18n_ import *
from utils.serial import WeeSerial
from utils.spiway import SpiFlasher
import utils.utils as Utils
import utils.slb2 as BLS
import utils.sflash as SFlash
import tools.SFlashTools as SFlashTools



def screenNorFlasher(path = '', port = '', act = '', mode = False):
	
	port = port if port else screenChoosePort()
	if not port:
		UI.setStatus(STR_NO_PORTS)
		return
	
	flasher = SpiFlasher(port)
	flasher.reset()
	
	UI.clearScreen()
	print(TITLE+UI.getTab(STR_ABOUT_SPIWAY))
	print(UI.warning(STR_INFO_SPIWAY))
	print(UI.getTab(STR_SPIWAY))
	
	if flasher.err or flasher.sp.is_open == False:
		print(UI.warning(STR_PORT_UNAVAILABLE))
		print(UI.warning(flasher.err))
		flasher.close()
		input(STR_BACK)
		return
	
	ping = flasher.ping()
	ver_maj, ver_min = ping['VER']
	UI.showTable({
		'Version':'%d.%02d'%(ver_maj, ver_min),
		'Memory':'%d bytes'%ping['RAM'],
	})
	print()
	
	if ping['VER'] != flasher.VERSION:
		flasher.close()
		input(STR_BACK)
		return
	
	info = flasher.getChipInfo()
	
	if flasher.Config.IC_ID == 0:
		UI.showTable({
			'Device ID': '0x%02X'%flasher.Config.VENDOR_ID,
			'Vendor ID': '0x%04X'%flasher.Config.DEVICE_ID,
		})
		input(STR_BACK)
		return
	
	print(UI.highlight(STR_CHIP_CONFIG)+':\n')
	UI.showTable(info)
	print()
	
	# Show current file info
	if act != 'read' and path and os.path.isfile(path):
		print(UI.highlight(STR_FILE_INFO)+':\n')
		UI.showTable({
			'File':		os.path.basename(path),
			'MD5':		Utils.getFileMD5(path),
			'Size':		'%d MB'%(os.stat(path).st_size // (1024**2)),
		})
		print(end=('\n' if act else ''))
	
	# Perform action
	
	cfg = flasher.Config
	
	if act:
		print(' '+UI.highlight(MENU_SPW_ACTS[act] if act in MENU_SPW_ACTS else STR_UNKNOWN)+'\n')
		block, count = chooseBNC(mode, cfg.BLOCK_SIZE)
	
	if act == 'read':
		sfx = '_full' if block == 0 and count == 0 else '_b%d-%d'%(block,block+count)
		path = os.path.join(os.getcwd(), 'dump_' + datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + sfx + '.bin')
		data = flasher.readChip(block, count)
		print()
		if data:
			with open(path, "wb") as file:
				file.seek(cfg.TOTAL_SIZE - 1)
				file.write(b'\x00')
				file.seek(cfg.BLOCK_SIZE * block)
				file.write(data)
		else:
			path = ''
	
	elif act == 'write':
		if path and os.path.isfile(path):
			with open(path,"rb") as file:
				file.seek(cfg.BLOCK_SIZE * block)
				data = file.read(cfg.BLOCK_SIZE * (count if count > 0 else cfg.BLOCK_COUNT))
				flasher.writeChip(data, False, block, count)
				print()
		else:
			UI.setStatus(STR_FILE_NOT_EXISTS%path)
	
	elif act == 'verify':
		if path and os.path.isfile(path):
			with open(path,"rb") as file:
				file.seek(cfg.BLOCK_SIZE * block)
				data = file.read(cfg.BLOCK_SIZE * (count if count else cfg.BLOCK_COUNT))
				vdata = flasher.readChip(block, count)
				print('\n'+STR_VERIFY+': '+(STR_OK if data == vdata else STR_FAIL)+'\n')
		else:
			UI.setStatus(STR_FILE_NOT_EXISTS%path)
	
	elif act == 'erase':
		flasher.eraseChip(block, count)
		print()
	
	if act:
		print(STR_DONE)
	
	flasher.close()
	
	# Show file info after read action
	if act == 'read' and path and os.path.isfile(path):
		print('\n'+UI.highlight(STR_FILE_INFO)+':\n')
		UI.showTable({
			'File': os.path.basename(path),
			'MD5': Utils.getFileMD5(path),
			'Size': '%d MB'%(os.stat(path).st_size // 1024**2),
		})
	
	# Action done
	
	print(UI.getTab(STR_ACTIONS))
	UI.showTableEx(UI.getMenu(MENU_FLASHER,1), 4, 17)
	print(UI.DIVIDER)
	UI.showMenu(MENU_EXTRA_FLASHER)
	
	UI.showStatus()
	
	act = ''
	mode = False
	
	choice = input(STR_CHOICE)
	
	if choice == '0':
		return
	elif choice in ['1','2','3']:
		act = 'read'
		mode = int(choice) - 1
	elif choice in ['4','5','6']:
		act = 'write'
		mode = int(choice) - 4
	elif choice in ['7','8','9']:
		act = 'verify'
		mode = int(choice) - 7
	elif choice in ['10','11','12']:
		act = 'erase'
		mode = int(choice) - 10
		
	elif choice == 's':
	    path = screenFileSelect(path, False, True)
	elif choice == 'f':
		if path and os.path.isfile(path):
			return SFlashTools.screenSFlashTools(path)
		else:
			UI.setStatus(STR_FILE_NOT_EXISTS%path)
	elif choice == 'm':
	    return screenMainMenu()
	
	screenNorFlasher(path, port, act, mode)



def screenSerialMonitor(port = '', emc_mode = False):
	
	port = port if port else screenChoosePort()
	if not port:
		UI.setStatus(STR_NO_PORTS)
		return
	
	serial = WeeSerial(port)
	
	UI.clearScreen()
	print(TITLE + UI.getTab(serial.getPortInfo()))
	UI.showTableEx(UI.getMenu(MENU_SERIAL_MONITOR), 2)
	
	print(UI.getTab(STR_SERIAL_MONITOR))
	
	if serial.err or serial.sp.is_open == False:
		print(UI.warning(STR_PORT_UNAVAILABLE))
		print(UI.warning(serial.err))
		input(STR_BACK)
		return
	
	serial.startMonitor()
	#serial.testPatterns('../uart.txt')
	while serial.sp.is_open and serial.alive:
		txt = input()
		if not len(txt):
			continue
		elif Utils.checkCtrl(txt[0],'L'):
			UI.clearInput()
			serial.LOG = False if serial.LOG else datetime.datetime.now().strftime('uart_%Y-%m-%d_%H-%M-%S.txt')
			print('\n' + UI.highlight('UART log: {}'.format(serial.LOG if serial.LOG else STR_OFF)) + '\n')
			continue
		elif Utils.checkCtrl(txt[0],'R'):
			serial.sp.close()
			UI.clearScreen()
			time.sleep(0.1) # port open/close need some delay
			return screenSerialMonitor(port)
		elif Utils.checkCtrl(txt[0],'Q'):
			serial.sp.close()
			UI.clearInput()
			print('\n' + UI.highlight(STR_STOP_MONITORING))
			break
		elif Utils.checkCtrl(txt[0],'E'):
			UI.clearInput()
			emc_mode = False if emc_mode else True
			print('\n' + UI.highlight(STR_EMC_CMD_MODE%(STR_ON if emc_mode else STR_OFF)))
			continue
		elif Utils.checkCtrl(txt[0],'B'):
			UI.clearInput()
			serial.SHOWCODES = False if serial.SHOWCODES else True
			print('\n' + UI.highlight(STR_SHOW_BYTECODES%(STR_ON if serial.SHOWCODES else STR_OFF)))
			continue
		elif emc_mode:
			txt = Utils.getEmcCmd(txt)
			UI.clearInput()
			print(txt)
			
		serial.sendText(txt)
	if serial.err:
		print(' '+UI.error(serial.err))
	input(STR_BACK)



def screenChoosePort():
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_PORTS_LIST))
	
	ports = WeeSerial.getPortList()
	
	for i in range(len(ports)):
		port = ports[i]
		print(' % 2s: %s - %s'%(i+1, port['port'].ljust(6), port['desc']))
    
	if not len(ports):
		print(UI.warning(STR_NO_PORTS))
		input(STR_BACK)
		return ''
    
	UI.showStatus()
	
	try:
		c = input(STR_CHOICE)
		
		if c == '':
			return
		
		c = int(c)
		
		if c > 0 and c <= len(ports):
			return ports[c-1]['port']
		else:
			UI.setStatus(STR_ERROR_INPUT)
	except:
		UI.setStatus(STR_ERROR_INPUT)
	
	return screenChoosePort()



def screenMainMenu():
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_MAIN_MENU))
	
	UI.showMenu(MENU_TOOL_SELECTION,1)
	
	UI.showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == '1':
		screenFileSelect()
	elif choice == '2':
		screenSerialMonitor()
	elif choice == '3':
		screenNorFlasher()
	elif choice == '4':
		return quit()
	else:
		UI.setStatus(STR_ERROR_CHOICE)
		
	screenMainMenu()



def screenFileSelect(path = False, all = False, ret = False):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_FILE_LIST+' '+('[all]' if all else '[bin, pup]')))
	
	path = path if path and os.path.exists(path) else os.getcwd()
	path = path if os.path.isdir(path) else os.path.dirname(path)
	
	print(Clr.fg.l_grey+(' %s\n'%path)+Clr.reset)
	
	list = [os.path.dirname(path)]
	print('  0: '+os.sep+'..')
	
	dirs = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
	files = [x for x in os.listdir(path) if not os.path.isdir(os.path.join(path, x))]
	
	dirs.sort()
	files.sort()
	
	for d in dirs:
		list.append(os.path.join(path, d))
		print((' %2d: '+os.sep+'%s'+os.sep)%(len(list)-1,d))
	
	for f in files:
		if all or f.lower().endswith('.bin') or f.lower().endswith('.pup'):
			list.append(os.path.join(path, f))
			print(' %2d: %s'%(len(list)-1,f))
	
	print(UI.DIVIDER)
	UI.showMenu(MENU_FILE_SELECTION)
	UI.showStatus()
	
	choice = input(STR_CHOICE)
	
	if choice == 'a':
		all = False if all else True
	elif choice == 'f':
		AdvSFlashTools.screenBuildNorDump(path)
	elif choice == 'b':
		screenBuild2BLS(path)
	elif choice == 'c':
		file_list = [os.path.join(path, x) for x in files] # Force bin only: if x.lower().endswith('.bin')
		screenCompareFiles(file_list)
	elif choice == 'm':
		return screenMainMenu()
	elif choice != '':
		try:
			ind = int(choice)
			if ind >= 0 and ind < len(list):
				path = list[ind]
				if not os.path.isdir(path):
					if ret:
						return path
					else:
						launchTool(path)
			else:
				UI.setStatus(STR_ERROR_CHOICE)
		except Exception as error:
			UI.setStatus(' %s'%error)
	
	screenFileSelect(path, all)



def screenCompareFiles(list):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_COMPARE))
	
	if len(list) == 0:
		print(STR_EMPTY_FILE_LIST)
		input(STR_BACK)
		return
	
	res = True
	hashes = []
	for i, file in enumerate(list):
		if not file or not os.path.isfile(file):
			print(STR_FILE_NOT_EXISTS%file)
			continue
		else:
			md5 = Utils.getFileMD5(file)
			if not md5 in hashes:
				hashes.append(md5)
			print((' {: 2}: [{}] {}').format(i+1, md5,  os.path.basename(file)))
	
	print(UI.DIVIDER)
	UI.showTable({
		'Result':STR_OK if len(hashes) == 1 else STR_FAIL,
		'Hashes count':len(hashes),
	})
	input(STR_BACK)
	
	screenFileSelect()



def screenUnpack2BLS(path):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_UNPACK_2BLS))
	
	with open(path,'rb') as f:
		data = f.read()
	
	fname = os.path.splitext(os.path.basename(path))[0]
	folder = os.path.join(os.path.dirname(path), fname+'_2bls')	
	
	info = BLS.getGet2BLSInfo(data)
	
	print(UI.highlight(' Header'))
	head = '\n'.join(UI.getTable(info['header'], 16))
	txt_info = 'Header:\n\n' + head + '\n'
	print(head)
	
	if not os.path.isdir(folder):
		os.makedirs(folder)
	
	entries = info['entries']
	txt_info += '\nEntries:\n\n'
	
	for key in range(len(entries)):
		entry = entries[key]
		
		print(UI.highlight('\n Entry %s'%key))
		e_info = '\n'.join(UI.getTable(entry,16))
		txt_info += e_info + '\n'
		print(e_info)
		
		with open(os.path.join(folder, entry['name']),'wb') as out:
			out.write(data[entry['offset']:entry['offset'] + entry['size']])
	
	with open(os.path.join(folder, Utils.INFO_FILE_2BLS),'w') as txt:
		txt.write(txt_info)
	
	print('\n'+STR_SAVED_TO%folder)
	
	input(STR_BACK)



def screenBuild2BLS(path):
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_2BLS_BUILDER))
	
	name = os.path.basename(path).replace('_2bls','')+ '.2bls'
	file = os.path.join(os.path.dirname(path),name)
	
	files = [os.path.join(path,x) for x in os.listdir(path) if os.path.isfile(os.path.join(path, x)) and x != Utils.INFO_FILE_2BLS]
	
	if len(files) == 0:
		print(STR_EMPTY_FILE_LIST)
		input(STR_BACK)
		return
	
	data = BLS.build2BLS(files)
	
	with open(file, 'wb') as out:
		out.write(data)
	
	info = BLS.getGet2BLSInfo(data)
	
	print(UI.highlight(' Header'))
	UI.showTable(info['header'])
	
	entries = info['entries']
	for key in range(len(entries)):
		entry = entries[key]
		
		print(UI.highlight('\n Entry %s'%key))
		UI.showTable(entry)
	
	
	print('\n'+STR_SAVED_TO%file)
	
	input(STR_BACK)



def screenHelp():
	UI.clearScreen()
	print(TITLE + UI.getTab(STR_HELP))
	print(STR_APP_HELP)
	
	UI.showStatus()
	
	input(STR_BACK)



def chooseBNC(mode = 0, block_size = 0, syscon = False):
	
	block = 0
	count = 0
	
	if mode == 1:
		areas = [
			{'n':'PS5 Full dump',	'o':0,	'l':SFlash.DUMP_SIZE},
		]
		for i in range(len(areas)):
			areas[i]['b'] = areas[i]['o'] // block_size
			areas[i]['c'] = areas[i]['l'] // block_size + (1 if areas[i]['l'] % block_size else 0)
		
		UI.showMenu(['[%03d %03d] %s'%(areas[i]['b'], areas[i]['c'], areas[i]['n']) for i in range(len(areas))])
		num = input(UI.DIVIDER+STR_CHOOSE_AREA)
		print()
		try:
			num = int(num)
			if num < len(areas):
				block = areas[num]['b']
				count = areas[num]['c']
		except:
			num = 0
	
	if mode == 2:
		str = input(STR_INPUT_BLOCK)
		print()
		try:
			num = str.split()
			block = int(num[0])
			count = int(num[1]) if len(num) > 1 else 1
		except:
			count = 1
	
	return [block, count]



def launchTool(path):
	
	if not os.path.exists(path):
		return 0
	
	if os.path.isdir(path):
		if os.path.exists(os.path.join(path, Utils.INFO_FILE_SFLASH)):
			return Tools.screenBuildNorDump(path)
		elif os.path.exists(os.path.join(path, Utils.INFO_FILE_2BLS)):
			return screenBuild2BLS(path)
		else:
			#TODO: maybe open SPIway?
			UI.setStatus(STR_UNK_CONTENT + ' {}'.format(path))
			return 0
	
	f_size = os.stat(path).st_size
	with open(path,'rb') as f:
		header = f.read(0x10)
	
	if f_size == SFlash.DUMP_SIZE:
		return SFlashTools.screenSFlashTools(path)
	elif header[0:len(BLS.SLB2_MAGIC)] == BLS.SLB2_MAGIC:
		return screenUnpack2BLS(path)
	else:
		UI.setStatus(STR_UNK_FILE_TYPE + ' {}'.format(path))
