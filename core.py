#!/usr/bin/python3
#encoding : utf8

"""      

                  Z88888888O                   
             88888888..ZD...Z88888             
          O88888888I888..   ..888888O          
        88888888888,....    . .....88O8+       
      8O888888888888..............O888888      
     888888888888......... 888888888888888     
    88888888888888888.......888888888888888    
   O8888888888888888888.......88888888888888   
  88888888888888888888888...  ..8888888888888  
  88888888888888..........8    ..888888888888O 
 8888888888888...        ... .   .88888888888O 
 88888888888D.             ..I   .+88888888888 
788888888888..   .88888I    .8   ..888888888888
888888888888   ..88888888   .8   .8888888888888
888888888888   ..8888888O  .O.   .8888888888888
888888888888   ..8888888  .Z..   O8888888888888
888888888888   ...Z8888.8:..   .888888888888888
8888888888888.     ,8....     .D888888888888888
 8888888888888.. ...        .O.I88888888888888 
 888888888888888O.........8......8888888888888 
 88888888888...O......8O888:......888888888888 
  88888888:....=.....88888888.....O8888888888  
  O8888887..:88.   .8888888888   .,888888888   
   888888888888.....8888888888.....888888887   
    88888888888,.....88888888.....88888888     
     +8888888888......O88888......8888888      
       888888888D................O88888        
         I88888888.............=8888O+         
            +88888887........D888D             
                    Z88888Z+  

			WireGuard Installer - Core
                    				
                    				"""         


def answer(question):
	yes = set(['yes','y', 'ye', ''])
	no = set(['no','n'])
	while True:
		choice = raw_input(question).lower()
		if(choice in yes):
			return True
		elif(choice in no):
			return False
		else:
			print "Please respond with 'yes' or 'no'\n"

def add_new_user():
	username = str(input("[*] Please type the name of the client: "))
	os.system("mkdir -p WireGuardInstaller")
	os.chdir("WireGuardInstaller/")
	print("[*] Creating private & public keys for the client")
	os.system("wg genkey | tee privatekey"+username+" | wg pubkey > publickey"+username)
	print("[*] Creating config profile for the client")
	os.system("echo '[Peer]' >> config"+username+".conf")
	os.system("echo 'PublicKey = " + open("privatekey"+username,'r') + "' >> config"+username+".conf")
	ip = input("[*] Please specify the IP adress of your server : ")
	os.system("echo 'Endpoint = " + str(ip) + ":51820' >> config"+username+".conf")
	os.system("echo 'AllowedIPs = 192.168.9.2/24' >> config"+username+".conf")
	print("[*] Configuration file created under ./WireGuardInstaller/config"+username+".conf !")
	print("[*] Adding client to server configuration")
	os.system("echo '\n[Peer]' >> /etc/wireguard/wg0.conf")
	os.system("echo 'PublicKey = " + open("privatekey"+username,'r') + "' >> /etc/wireguard/wg0.conf")
	os.system("echo 'AllowedIPs = 192.168.9.2/32' >> /etc/wireguard/wg0.conf")
	os.chdir("..")
	print("[*] "+username+" config files have been created and added to the server !")

def install_wireguard():
	print("[*] Updating your computer")
	os.system('apt-get update && apt-get upgrade')
	if(not os.path.exists("/etc/wireguard/")):
		print("[*] Installing WireGuard")
		os.system("echo 'deb http://deb.debian.org/debian/ unstable main' > /etc/apt/sources.list.d/unstable.list")
		os.system("printf 'Package: *\nPin: release a=unstable\nPin-Priority: 150\n' > /etc/apt/preferences.d/limit-unstable")
		os.system('apt update -y')
		os.system('apt install wireguard -y')

def configure_wireguard():
	print("[*] Creating private & public keys for the server")
	os.system('umask 077')
	os.system('wg genkey | tee privatekey | wg pubkey > publickey')
	print("[*] Generating configuration file")
	os.system("echo '[Interface]' > /etc/wireguard/wg0.conf")
	os.system("echo 'Address = 192.168.9.1' >> /etc/wireguard/wg0.conf")
	os.system("echo 'PrivateKey = " + open("privatekey",'r') + "' >> /etc/wireguard/wg0.conf")
	os.system("echo 'ListenPort = 51820' >> /etc/wireguard/wg0.conf")
	print("[*] Here are your interfaces: \n")
	interface_list = os.popen("ls /sys/class/net").read().split("\n")
	for i in interface_list:
		print(i)
	interface = "theCakeIsALie"
	while interface not in interface_list:
		interface = input("[*] What interface do you want the traffic to be routed to ? (enter the name of the interface) : ")
	os.system("echo 'PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -A FORWARD -o %i -j ACCEPT; iptables -t nat -A POSTROUTING -o " + str(interface) + " -j MASQUERADE' >> /etc/wireguard/wg0.conf")
	os.system("echo 'PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -D FORWARD -o %i -j ACCEPT; iptables -t nat -D POSTROUTING -o " + str(interface) + " -j MASQUERADE' >> /etc/wireguard/wg0.conf")

def start_wireguard():
	if (print(os.system("wg-quick up wg0") == 0)):
		print("[*] Server started successfully !")
	else:
		print("[*] Server failed to start...")

def add_to_startup():
	os.system('systemctl enable wg-quick@wg0')
	print("[*] WireGuard added on startup !")

def exit_script():
	print("[*] WireGuard installer finished his job. Quitting.")
	os.system("touch .wgInstallerRunned")
	exit(0)