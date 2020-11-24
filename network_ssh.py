import paramiko
import time
import datetime

t = datetime.datetime.now().strftime('%Y_%m_%d-%H:%M:%S')

commands = ['show version\n', 'show run\n']

max_buffer = 65535

devices = {
   'hostanme': {
      'ip': '',
      'username': '',
      'password': '',
      },
   'hostname': {
      'ip': '',
      'username': '',
      'password': '',
      }
   }

def get_connection(hostname, username, password):
   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   ssh.connect(hostname=hostname,username=username, password=password, port=22, look_for_keys=False, allow_agent=False)
   return ssh

def clear_buffer(connection):
    if connection.recv_ready():
        return connection.recv(max_buffer)

for device in devices.keys(): 
    outputfilename = device + '_' + t
    connection = get_connection(hostname=devices[device]['ip'], username=devices[device]['username'], password=devices[device]['password'])
    new_connection = connection.invoke_shell()
    clear_buffer(new_connection)
    new_connection.send("terminal length 0\n")
    time.sleep(1)
    clear_buffer(new_connection)
    with open(outputfilename, 'wb') as f:
        for command in commands:
           print(f"Executing command {command}")
           new_connection.send(command)
           time.sleep(2)
           output = new_connection.recv(max_buffer)
           f.write(output)
    
    new_connection.close()

