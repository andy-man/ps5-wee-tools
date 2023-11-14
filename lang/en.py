#==========================================================
# Default language [EN]
# part of ps5 wee tools project
#==========================================================

MENU_FLASHER = [
	'Read all',
	'Read area',
	'Read block',
	'Write all',
	'Write area',
	'Write block',
	'Verify all',
	'Verify area',
	'Verify block',
	'Erase all',
	'Erase area',
	'Erase block',
]

MENU_SERIAL_MONITOR = {
	'Ctrl+Q':'quit monitor',
	'Ctrl+R':'restart monitor',
	'Ctrl+E':'toggle EMC cmd mode',
	'Ctrl+B':'show bytecodes < 0x20',
	'Ctrl+L':'log to file',
}

MENU_TOOL_SELECTION = [
	'File browser',
	'Terminal (UART)',
	'sFlash r/w (SPIway by Judges)',
	'Exit',
]

MENU_FILE_SELECTION = {
	'a':'Show all files / Toggle filters [bin,pup]',
	'f':'Build sflash0 dump',
	'b':'Build 2BLS/PUP',
	'c':'Compare files in current folder',
	'm':'Go to [Main menu]',
}

MENU_EXTRA_FLASHER = {
	's':'Select file',
	'f':'Launch Tool for this file',
	'm':'Open Main menu',
}

MENU_EXTRA = {
	's':'Select another file',
	'f':'Flash this file (full/parts) back to console',
	'm':'Open Main menu',
}

MENU_NOR_ACTIONS = [
	'Flags (IDU, Model, etc)',
	'Extract sFlash\'s partitions',
	'Build dump from extracted files',
	'Base validation and entropy stats',
]

MENU_SPW_ACTS = {
	'read':		'Reading',
	'write':	'Writing',
	'verify':	'Verifying',
	'erase':	'Erasing',
}

STR_SECONDS				= '%0.0f seconds'
STR_PORTS_LIST			= 'Serial ports'
STR_MAIN_MENU			= 'Main menu'
STR_FILE_LIST			= 'Files list'
STR_NOR_INFO			= 'NOR dump info'
STR_ADDITIONAL			= 'Additional tools'
STR_COMPARE				= 'Compare'
STR_HELP				= 'Help'
STR_ACTIONS				= 'Actions'
STR_SYSFLAGS			= 'System flags'
STR_NOR_VALIDATOR		= 'NOR validator'
STR_NOR_FLAGS			= 'NOR flags'
STR_NOR_EXTRACT			= 'NOR extractor'
STR_NOR_BUILD			= 'NOR builder'
STR_HDD_KEY				= 'HDD eap key'
STR_2BLS_BUILDER		= '2BLS builder'
STR_UNPACK_2BLS			= '2BLS unpacker'
STR_EAP_KEYS			= 'EAP keys'
STR_SC_BOOT_MODES		= 'Bootmode records'
STR_INFO				= 'Info'
STR_SPIWAY				= 'SPIway by Judges & Abkarino'

STR_EQUAL				= 'Equal'
STR_NOT_EQUAL			= 'Not equal'
STR_NO_INFO				= '- No info -'
STR_OFF					= 'Off'
STR_ON					= 'On'
STR_WARNING				= 'Warning'
STR_HELP				= 'Help'
STR_UNKNOWN				= '- Unknown -'
STR_YES					= 'Yes'
STR_NO					= 'No'
STR_PROBABLY			= 'Probably'
STR_NOT_SURE			= 'not sure'
STR_DIFF				= 'Different'
STR_NOT_FOUND			= 'not found'
STR_BAD_SIZE			= 'bad size'
STR_OK					= 'OK'
STR_FAIL				= 'Fail'
STR_CANCEL				= 'Cancel'
STR_IS_PART_VALID		= '[%s] %s FW %s'
STR_SERIAL_MONITOR		= 'Terminal'

STR_NO_PORTS			= ' No one serial port was found'
STR_PORT_UNAVAILABLE	= ' Selected port is unavailable'
STR_PORT_CLOSED			= ' Port is closed'
STR_STOP_MONITORING		= ' Monitoring was stopped by user'

STR_DECRYPTING			= ' Decrypting'
STR_ENCRYPTING			= ' Encrypting'
STR_PATCHING			= ' Patching'
STR_EXPERIMENTAL		= ' * - experimental functions'
STR_PERFORMED			= ' Performed action: '

STR_EMPTY_FILE_LIST		= ' File list is empty'
STR_NO_FOLDER			= ' Folder %s doesn\'t exists'
STR_EXTRACTING			= ' Extracting sflash to %s folder'
STR_FILES_CHECK			= ' Checking files'
STR_BUILDING			= ' Building file %s'

STR_DONE				= ' All done'
STR_PROGRESS			= ' Progress %2d%% '
STR_PROGRESS_KB			= ' Progress: %dKB / %dKB'
STR_WAIT				= ' Please wait...'
STR_WAITING				= ' Waiting...'
STR_SET_TO				= ' %s was set to [%s]'
STR_ABORT				= ' Action was aborted'
STR_FILENAME			= ' Filename: '

STR_NIY					= ' Function is not implemented yet'
STR_CLEAN_FLAGS			= ' Clean all system flags'
STR_UNK_FILE_TYPE		= ' Unknown file type'
STR_UNK_CONTENT			= ' Unknown content'
STR_UART				= ' UART is set to '

STR_DIFF_SLOT_VALUES	= ' Values in slots are different!'
STR_SYSFLAGS_CLEAN		= ' Sys flags were cleared. Tip: turn on UART'

STR_CHOICE				= ' Make choice: '
STR_BACK				= ' Press [ENTER] to go back'

STR_UNPATCHABLE			= ' Can\'t patch!'
STR_PARTITIONS_CHECK	= ' Checking partitions'
STR_ENTROPY				= ' Entropy statistics'
STR_MAGICS_CHECK		= ' Checking magics'

STR_FW_VERSION			= ' FW version %s / Active slot %s'

STR_INCORRECT_SIZE		= ' %s - incorrect dump size!'
STR_FILE_NOT_EXISTS		= ' File %s doesn\'t exist!'
STR_ERROR_FILE_REQ		= ' You need to select file first'
STR_SAVED_TO			= ' Saved to %s'
STR_ERROR_INPUT			= ' Incorrect input'
STR_ERROR_DEF_VAL		= ' Setting default values'
STR_ERROR_CHOICE		= ' Invalid choice'
STR_OUT_OF_RANGE		= ' Value is out of range!'
STR_FILES_MATCH			= ' Files are equal'
STR_FILES_MISMATCH		= ' Files mismatch'
STR_SIZES_MISMATCH		= ' Sizes mismatch!'

STR_CHOOSE_AREA			= ' Choose area: '
STR_INPUT_BLOCK			= ' Input start block [count]: '
STR_INPUT_SAVE_IM		= ' Save all intermediate files? [y] '
STR_USE_NEWBLOBS		= ' Use new key blobs? [y] '
STR_CONFIRM_SEPARATE	= ' Save as separate file? [y] '
STR_CONFIRM				= ' Input [y] to continue: '
STR_CURRENT				= ' Current: '
STR_GO_BACK				= ' Go back'
STR_FLASH_PATCHED		= ' Flash patched to console (SPIway)? [y] '

STR_EMC_CMD_MODE		= 'Turning EMC cmd mode: [%s]'
STR_SHOW_BYTECODES		= 'Show byte codes < 0x20: [%s]'
STR_MONITOR_STATUS		= 'RX/TX: %d/%d (bytes) Elapsed: %d (sec)'

STR_CHIP_CONFIG			= ' Chip config'
STR_FILE_INFO			= ' File info'
STR_VERIFY				= ' Verify'

STR_SPW_PROGRESS		= 'Block %03d [%d KB / %d KB] %d%% %s '
STR_SPW_ERROR_CHIP		= 'Unsupported chip!'
STR_SPW_ERROR_VERSION	= 'Unsupported version! (v%d.%02d required)'
STR_SPW_ERROR_ERASE		= 'Error erasing chip!'
STR_SPW_ERROR_ERASE_BLK	= 'Block %d - error erasing block'
STR_SPW_ERROR_DATA_SIZE	= 'Incorrent data size %d'
STR_SPW_ERROR_LENGTH	= 'Incorrect length %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Error! Block verification failed (block=%d)'
STR_SPW_ERROR_WRITE		= 'Error while writing!'
STR_SPW_ERROR_READ		= 'Teensy receive buffer timeout! Disconnect and reconnect Teensy!'
STR_SPW_ERROR_VERIFY	= 'Verification error!'
STR_SPW_ERROR_PROTECTED	= 'Device is write-protected!'
STR_SPW_ERROR_UNKNOWN	= 'Received unknown error!'
STR_SPW_ERROR_UNK_STATUS= 'Unknown status code!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Expecting file size to be a multiplication of block size: %d'
STR_SPW_ERR_DATA_SIZE	= 'Data is %d bytes long (expected %d)!'
STR_SPW_ERR_OVERFLOW	= 'Chip has %d blocks. Writing outside the chip\'s capacity!'

STR_CANT_USE			= 'Can\'t use this'
STR_DIFF_SN				= 'Serial numbers are different!'

STR_INFO_FLASH_TOOLS = ''\
' Flash tools (spiway & syscon flasher) are experimental! Be careful.'\

STR_ABOUT_SPIWAY = 'About SPIway'
STR_INFO_SPIWAY = ''\
' SPIway - sflash r/w with random block access support (Teensy++ 2.0)\n'\
' Look at </assets/hw/spiway> folder for diagrams and Teensy\'s FW\n'\
' More info at PSDevWiki: '

STR_IMMEDIATLY = ''\
' Be careful: All patches are applied immediatly to the file!'

STR_PATCHES = STR_IMMEDIATLY + '\n'\
' Will switch value between available values for chosen option'

STR_APP_HELP = ''\
' Usage: ps5-wee-tools [params] \n'\
'\n'\
' Params: \n\n'\
'  <file>              : load appropriate tool for supplied file\n'\
'  <folder>            : build dump with files from supplied folder\n'\
'  <file1> <file2> ... : compare files (with MD5 info)\n'\
'  --parts <file>      : show partitions info\n'\
'  --help              : show this help screen\n'\
'\n'\
' Home: '
