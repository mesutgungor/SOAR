#This script uses a jump windows scvmm console installed to query vm description by ip by using winrm protocol 
import winrm
from winrm.protocol import Protocol
from getpass import getpass
user = getpass("username:")
passw = getpass("vmm_pass:")
ip_address = "ASSET_IP_ADRES"
p = Protocol(
		endpoint='http://VMM_JUMP_SERVER:5985/wsman',
        transport='credssp',
        kerberos_delegation=True,
    		username=user,
    		password=passw,
        server_cert_validation='ignore')
shell_id = p.open_shell()
#Here we find name of the vm which has the ip address "ip_address" 
command_id = p.run_command(shell_id, 'powershell "Get-SCVirtualMachine | Get-SCVirtualNetworkAdapter | ? IPv4Addresses -eq "'+ip_address+'"|Select-Object -ExpandProperty Name"')
std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
p.cleanup_command(shell_id, command_id)
p.close_shell(shell_id)
shell_id2 = p.open_shell()
#Here we fetch the description using the vm name we have found in the previous powershell call output. 
command_id2 = p.run_command(shell_id2, 'powershell "Get-SCVirtualMachine -Name "'+std_out.strip()+'"|Select -ExpandProperty Description"')
std_out2, std_err2, status_code2 = p.get_command_output(shell_id2, command_id2)
p.cleanup_command(shell_id2, command_id2)
p.close_shell(shell_id2)
descr = std_out2.decode("utf-8","replace")
username_list=descr.split(" ")

print username_list[0]
