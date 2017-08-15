#!/usr/bin/python

# original source: http://voorloopnul.com/blog/a-python-netstat-in-less-than-100-lines-of-code/
# added support for tcp6 and filter for listening

# todo: formatting for ipv6 needs to be fixed

import pwd
import os
import re
import glob

PROC_TCP = "/proc/net/tcp"
PROC_TCP6 = "/proc/net/tcp6"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

def _load():
    ''' Read the table of tcp connections & remove header  '''
    content = []
    # ipv4 ports
    with open(PROC_TCP,'r') as f:
        tcp = []
        for row in f.readlines():
            tcp.append('tcp ' + row)
        tcp.pop(0)
        content += tcp
    # ipv6 ports
    with open(PROC_TCP6,'r') as f:
        tcp6=[]
        for row in f.readlines():
            tcp6.append('tcp6 ' + row)
        tcp6.pop(0)
        content += tcp6
    return content

def _hex2dec(s):
    return str(int(s,16))

def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)

def _remove_empty(array):
    return [x for x in array if x !='']

def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port)

def netstat():
    '''
    Function to return a list with status of tcp connections at linux systems
    To get pid of all network process running on system, you must run this script
    as superuser
    '''

    content=_load()
    result = []
    for line in content:
        line_array = _remove_empty(line.split(' '))     # Split lines and remove empty spaces.
        tcp_ver = line_array[0]
        l_host,l_port = _convert_ip_port(line_array[2]) # Convert ipaddress and port from hex to decimal.
        r_host,r_port = _convert_ip_port(line_array[3])
        tcp_id = line_array[1]
        state = STATE[line_array[4]]
        uid = pwd.getpwuid(int(line_array[8]))[0]       # Get user from UID.
        inode = line_array[10]                           # Need the inode to get process pid.
        pid = _get_pid_of_inode(inode)                  # Get pid prom inode.
        try:                                            # try read the process name.
            exe = os.readlink('/proc/'+pid+'/exe')
        except:
            exe = None

        nline = [tcp_ver, tcp_id, uid, l_host+':'+l_port, r_host+':'+r_port, state, pid, exe]
        result.append(nline)
    return result

def _get_pid_of_inode(inode):
    '''
    To retrieve the process pid, check every running process and look for one using
    the given inode.
    '''
    for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
        try:
            if re.search(inode,os.readlink(item)):
                return item.split('/')[2]
        except:
            pass
    return None

def filter_listen(l):
    return l[5] == 'LISTEN'

def only_listening():
    return filter(filter_listen, netstat())


if __name__ == '__main__':
    # for conn in netstat():
    #     print(conn)
    for conn in only_listening():
        print(conn)
