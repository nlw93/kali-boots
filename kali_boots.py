# This script is an attempt at boostrapping my kali instance for the OSCP
# I've had so many issues and needed to rebuild so many times.
# this is a list of scripts/tools I always need to install
import paramiko
import time

sleeptime = 0.001

class KALI():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

    def connect(self, input):
        # ssh with ls /home
        result = self.ssh_command(command='ls /home')
        return result

    def ssh_command(self, command):  
        try:
            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print('creating connection')
                ssh.connect(self.host, username=self.username, password=self.password)

                if command.startswith('sudo'):  # Re-enter password if sudo command.
                    session = ssh.get_transport().open_session()
                    session.set_combine_stderr(True)
                    session.get_pty()
                    command = command.replace('sudo ', '')
                    session.exec_command("sudo bash -c \"" + command + "\"")
                    outdata, errdata = '', ''
                    stdin = session.makefile('wb', -1)
                    stdout = session.makefile('rb', -1)
                    stdin.write(self.password + '\n')
                    while True:
                        while session.recv_ready():
                            current_data = session.recv(1000).decode('utf8')
                            print(current_data)
                            outdata += current_data
                        while session.recv_stderr_ready():
                            errdata += str(session.recv_stderr(1000))
                        if session.exit_status_ready():
                            break
                        time.sleep(sleeptime)
                    retcode = session.recv_exit_status()
                    stdin.flush()
                    return outdata
                else:       # Non-sudo command
                    stdin, stdout, _stderr = ssh.exec_command(command)
                    return stdout.read().decode('utf8')
        finally:
            print('closing connection')
            ssh.close()
            print('closed')

if __name__ == '__main__':
    kali = KALI(host='192.168.1.186', username='kali',password='kali')
    
    commands = (

    # AutoRecon - https://github.com/Tib3rius/AutoRecon
#        'sudo apt install seclists curl enum4linux feroxbuster gobuster impacket-scripts nbtscan nikto nmap onesixtyone oscanner redis-tools smbclient smbmap snmp sslscan sipvicious tnscmd10g whatweb wkhtmltopdf -y',

        'sudo apt install python3 -y',
        'sudo apt install python3-pip -y',
        'sudo apt install python3-venv -y',
        'python3 -m pip install --user pipx',
        'python3 -m pipx ensurepath',
        'python3 -m pipx install git+https://github.com/Tib3rius/AutoRecon.git',
    
    # Rustscan - https://github.com/RustScan/RustScan
        'sudo apt install docker.io -y',
        'sudo systemctl enable docker --now',
        'sudo docker pull rustscan/rustscan:2.0.0',
        'echo "alias rustscan=\'sudo docker run -it --rm --name rustscan rustscan/rustscan:2.0.0\'" >> .zshrc',

    # Windows-Exploit-Suggester
        'sudo git clone https://github.com/Pwnistry/Windows-Exploit-Suggester-python3.git /opt/Windows-Exploit-Suggester',
        'sudo /opt/windows-exploit-suggester.py -u',

    # Windows-Kernel-Exploits
        'sudo git clone https://github.com/SecWiki/windows-kernel-exploits.git /opt/windows-kernel-exploits',

    # WinPEAS
        'sudo wget https://github.com/carlospolop/PEASS-ng/releases/download/20220424/linpeas.sh /opt/linpeas.sh',
        'sudo wget https://github.com/carlospolop/PEASS-ng/releases/download/20220424/winPEAS.bat /opt/winPEAS.bat',
        'sudo wget https://github.com/carlospolop/PEASS-ng/releases/download/20220424/winPEASx64.exe /opt/winPEASx64.exe',
        'sudo wget https://github.com/carlospolop/PEASS-ng/releases/download/20220424/winPEASx86.exe /opt/winPEASx86.exe',

        
        'sudo apt install xrdp -y',
    # RDP
        'sudo systemctl enable xrdp'
        'sudy systemctl statr xrdp',
        
        'echo DONE!'
    )

    for current_command in commands:
        print('executing: ' + current_command)
        kali.ssh_command(command=current_command)