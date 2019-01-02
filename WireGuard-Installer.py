#!/usr/bin/python3
#encoding : utf8

import os
import sys
import core

print("                                               ")
print("                  Z88888888O                   ")
print("             88888888..ZD...Z88888             ")
print("          O88888888I888..   ..888888O          ")
print("        88888888888,....    . .....88O8+       ")
print("      8O888888888888..............O888888      ")
print("     888888888888......... 888888888888888     ")
print("    88888888888888888.......888888888888888    ")
print("   O8888888888888888888.......88888888888888   ")
print("  88888888888888888888888...  ..8888888888888  ")
print("  88888888888888..........8    ..888888888888O ")
print(" 8888888888888...        ... .   .88888888888O ")
print(" 88888888888D.             ..I   .+88888888888 ")
print("788888888888..   .88888I    .8   ..888888888888")
print("888888888888   ..88888888   .8   .8888888888888")
print("888888888888   ..8888888O  .O.   .8888888888888")
print("888888888888   ..8888888  .Z..   O8888888888888")
print("888888888888   ...Z8888.8:..   .888888888888888")
print("8888888888888.     ,8....     .D888888888888888")
print(" 8888888888888.. ...        .O.I88888888888888 ")
print(" 888888888888888O.........8......8888888888888 ")
print(" 88888888888...O......8O888:......888888888888 ")
print("  88888888:....=.....88888888.....O8888888888  ")
print("  O8888887..:88.   .8888888888   .,888888888   ")
print("   888888888888.....8888888888.....888888887   ")
print("    88888888888,.....88888888.....88888888     ")
print("     +8888888888......O88888......8888888      ")
print("       888888888D................O88888        ")
print("         I88888888.............=8888O+         ")
print("            +88888887........D888D             ")
print("                    Z88888Z+                   ")
print("\rWireGuard Installer v0.2 - Tom ESCOLANO www.tomescolano.fr\n")

if(os.geteuid() != 0):
	sys.exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

print("-----| Welcome to WireGuard installer! |-----")
if(os.path.isfile(".wgInstallerRunned")):
	if(answer("[*] Do you want to add a new user ? (y/n) : ")):
		add_new_user()
		exit_script()

if(!answer("[*] Do you want to start the installation ? (y/n) : ")):
	exit_script()

install_wireguard()
configure_wireguard()

if(answer("[*] Do you want to add a new user ? (y/n) : ")):
	add_new_user()

print("[*] Starting wireguard ...")
start_wireguard()

if(answer("[*] Do you want WireGuard to start on startup ? (y/n) : ")):
	add_to_startup()

exit_script()