import sys
import os
import platform

colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() # Get current version of OS
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed in mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')   # Enables the ANSI
if not colors:
    N = R = W = G = Y = run = bad = good = info = que = ''
else:
    N = '\033[0m'
    W = '\033[1;37m' 
    B = '\033[1;34m' 
    M = '\033[1;35m' 
    R = '\033[1;31m' 
    G = '\033[1;32m' 
    Y = '\033[1;33m' 
    C = '\033[1;36m' 
    underline = "\033[4m"
    back = '\033[7;91m'
    info = '\033[93m[!]\033[0m'
    que = '\033[94m[?]\033[0m'
    bad = '\033[91m[-]\033[0m'
    good = '\033[92m[+]\033[0m'
    run = '\033[97m[~]\033[0m'




logo = G+r"""

                ──▐─▌──▐─▌────────────────────────────────────────
                ─▐▌─▐▌▐▌─▐▌───────────────────────────────────────
                ─█▄▀▄██▄▀▄█────__  ______ ____ ───────────────────
                ──▄──██▌─▄──   \ \/ / ___/ ___|  ___ __ _ _ __────
                ▄▀─█▀██▀█─▀▄    \  /\___ \___ \ / __/ _` | '_ \───
                ▐▌▐▌─▐▌─▐▌▐▌────/  \ ___) |__) | (_| (_| | | | |──
                ─▐─█────█─▌────/_/\_\____/____/ \___\__,_|_| |_|──
                ────▌──▐──────────────────────────────────────────
                
"""
