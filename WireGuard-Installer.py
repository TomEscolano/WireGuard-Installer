#!/usr/bin/python3
#encoding : utf8

import os
import sys

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
print("\rWireGuard Installer v0.1 - Tom ESCOLANO www.tomescolano.fr")

if(os.geteuid() != 0):
	sys.exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

print("-----| Welcome to WireGuard installer! |-----")
print("[*] Updating your computer")
os.system("apt-get update && apt-get upgrade")

if(not os.path.exists("/etc/wireguard/")):

	print("[*] Installing WireGuard")
	os.system("echo 'deb http://deb.debian.org/debian/ unstable main' > /etc/apt/sources.list.d/unstable.list")
	os.system("printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' > /etc/apt/preferences.d/limit-unstable")
	os.system("apt update -y")
	os.system("apt install wireguard -y")

print("[*] Creating private & public keys for the server")
os.system("umask 077")
os.system("wg genkey | tee privatekey | wg pubkey > publickey")

print("[*] Generating configuration file")
os.system("echo '[Interface]' > /etc/wireguard/wg0.conf")
os.system("echo 'Address = 192.168.9.1' >> /etc/wireguard/wg0.conf")
os.system("echo 'PrivateKey = " + open("privatekey",'r') + "' >> /etc/wireguard/wg0.conf")
os.system("echo 'ListenPort = 51820' >> /etc/wireguard/wg0.conf")

interface = ""
while interface == "":
	interface = input("[*] What interface do you want the traffic to be routed to ?\n> ")

os.system("echo 'PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o " + str(interface) + " -j MASQUERADE' >> /etc/wireguard/wg0.conf")
os.system("echo 'PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o " + str(interface) + " -j MASQUERADE' >> /etc/wireguard/wg0.conf")

choice = ""
while choice == "":
	choice = input("[*] Do you want to generate a connection profile for a client ? [y/n]\n> ")

if(choice == "Y" || choice == "y"):
	os.system("mkdir -p WireGuardInstaller")
	os.chdir("WireGuardInstaller/")
	print("[*] Creating private & public keys for the client")
	os.system("wg genkey | tee privatekeyClient | wg pubkey > publickeyClient")
	print("[*] Creating config profile for the client")
	os.system("echo '[Peer]' >> ./configClient.conf")
	os.system("echo 'PublicKey = " + open("privatekeyClient",'r') + "' >> ./configClient.conf")
	ip = input("[*] Please specify the IP adress of your server: ")
	os.system("echo 'Endpoint = " + str(ip) + ":51820' >> ./configClient.conf")
	os.system("echo 'AllowedIPs = 192.168.9.2/24' >> ./configClient.conf")
	print("[*] Configuration file created under ./WireGuardInstaller/configClient.conf !")
	print("[*] Adding client to server configuration")
	os.system("echo '\n[Peer]' >> /etc/wireguard/wg0.conf")
	os.system("echo 'PublicKey = " + open("privatekeyClient",'r') + "' >> /etc/wireguard/wg0.conf")
	os.system("echo 'AllowedIPs = 192.168.9.2/32' >> /etc/wireguard/wg0.conf")
	os.chdir("..")


print("[*] Starting wireguard ... (suspens)")
if (os.system("wg-quick up wg0") == 0):
	print("[*] Server started successfully !")
else:
	print("[*] Server failed to start...")

startup = ""
while startup != "Y" && startup != "y" && startup != "n" && startup != "N":
	startup = input("[*] Do you want WireGuard to start on startup ? [y/n]\n> ")
if(startup == "Y" || startup == "y"):
	os.system("systemctl enable wg-quick@wg0")
	print("[*] WireGuard added on startup")

print("[*] WireGuard installer finished his job. Quitting.")
exit(0)
