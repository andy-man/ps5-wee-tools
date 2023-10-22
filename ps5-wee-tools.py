#==============================================================
# PS5 Wee Tools
# app entry point
#==============================================================
import sys
import tools.Tools as Tools
import tools.SFlashTools as SFlashTools
from lang._i18n_ import UI



def main(args):
    
    UI.setTitle()
    
    args.pop(0)
    
    if len(args) >= 2:
    	if args[0].replace('-', '', 2) == 'parts':
    		SFlashTools.screenPartitionsInfo(args[1])
    	else:
    		Tools.screenCompareFiles(args)
    elif len(args) == 1:
    	if args[0].replace('-', '', 2) in ['help','h','?']:
    		Tools.screenHelp()
    	elif not Tools.launchTool(args[0]):
    		Tools.screenFileSelect(args[0])
    else:
    	Tools.screenMainMenu()



main(sys.argv)