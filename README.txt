#introduction
  Ethical hacking & Security application- contain various tool to do hacking & pentesting
 


#Main requirements
  python 3.9.2 or above

       1.(clone the tool from GitHub) clone the tool using below git clone                               https://github.com/ankushlakhani3/lazyhackes.git 
        or
       1.Unzip the downloaded zip file
       2.Go to the the directory where you extracted your file
       3.Install dependencies from requirements.txt directly by using below command
        pip install -r requirements.txt 
       4.Run mainfile.py with admin privileges
     

#How to use
  After running LazyHacks.py choose tool wisely according to which attack you want to perform on your target.
  
  1)scan_target using Port scan 
	1. Provide the IP address or Hostname of your target
	2. Specify ports or scan default 0-1024 ports

  2)scan_target using ARP scan 
    (To run this attack, you may need super user permissions otherwise run as root)
	1. Provide interface using option(1,2,3)
	2. Specify IP range of your network

  3)Man In The Middle attack
	1. Specify the IP of your Target
	2. Specify IP address of your Router/Gateway

  4)Slowloris Attack (DoS)
	1. Specify number of threads (You can skip this, default threads are 200)
	2. Specify target's IP or Hostname
	3. Target-port : 80 - default (You can skip this)
  
  5)Synflood Attack (DDoS) && Requests Attack (DoS)
	1. Specify the target IP or Hostname
	2. Number of threads: 1000 - default (You can skip this)
  
  6)Advance Backdoor
	1. Change host_ip="192.168.2.6" to attacker IP, uncomment it and save Backdoor.py
	2. Send Backdoor.exe to your target
 	3. Run the Backdoor file into target machine
	4. now hit scan start butoon to get connected to target
	5.now select the function to access the target's machine

  7)XSS 
	1. Provide the IP address or Hostname of your target
	2. Specify crawl level and the payload although it is optional

  8)CSRF 
	1. Provide the IP address or Hostname of your target
	2. Specify crawl level and the payload although it is optional
	

 
