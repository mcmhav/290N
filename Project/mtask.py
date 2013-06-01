#!/usr/bin/python
#
# Script to do the same task on multiple servers
# Author: Vegar Engen
#
#

import base64
from binascii import hexlify
import getpass
import os
import select
import socket
import sys
import time
import traceback

import argparse

import paramiko


def agent_auth(transport, username):
    """
    Attempt to authenticate to the given transport using any of the private
    keys available from an SSH agent.
    """
    try:
        key = paramiko.RSAKey.from_private_key_file(args.key_file)
    except paramiko.PasswordRequiredException:
        password = getpass.getpass('RSA key password: ')
        key = paramiko.RSAKey.from_private_key_file(args.key_file, password)

    print 'Trying ssh-agent key %s' % hexlify(key.get_fingerprint()),
    try:
        transport.auth_publickey(username, key)
        print '... success!'
        return
    except paramiko.SSHException:
        print '... nope.'


def manual_auth(username, hostname):
    default_auth = 'p'
    auth = raw_input('Auth by (p)assword, (r)sa key? [%s] ' % default_auth)
    if len(auth) == 0:
        auth = default_auth

    if auth == 'r':
        default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
        path = raw_input('RSA key [%s]: ' % default_path)
        if len(path) == 0:
            path = default_path
        try:
            key = paramiko.RSAKey.from_private_key_file(path)
        except paramiko.PasswordRequiredException:
            password = getpass.getpass('RSA key password: ')
            key = paramiko.RSAKey.from_private_key_file(path, password)
        t.auth_publickey(username, key)
    else:
        pw = getpass.getpass('Password for %s@%s: ' % (username, hostname))
        t.auth_password(username, pw)

#
# Main
#


parser = argparse.ArgumentParser(prog = 'Multiple task', description = 'Do the same task on multiple servers')
parser.add_argument('-f', '--foo', help='foo help')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-i', '--identity', nargs='?', help = 'Specify rsa key to use', dest='key_file', default=os.path.join(os.environ['HOME'], '.ssh', 'id_rsa'))
parser.add_argument('-t', '--hosts', nargs='?', help = 'File with list of hosts', dest='hosts_file', default='hosts.txt')
parser.add_argument('-s', '--script', nargs='?', help = 'Specifies the script to run on each host', dest='script', default='scripy.sh')
parser.add_argument('-o', '--options', nargs=2, action="append", help= 'Add an option to be sent as argument for the script')
parser.add_argument('--as-array', nargs=2, action="append", help= 'Adds an option to the script and converts a file to an array of strings' )
args = parser.parse_args()
print args


script_args = ''

if args.as_array:
    for option in args.as_array:
        script_args += " -%s "% option[0]
        with open(option[1]) as f:
            lines = f.readlines()

        o = "'"

        for line in lines:
            o += " %s"% line

        o += "'"
        script_args = script_args + o.replace("\n", "")


if args.options:
    for op in args.options:
        script_args += " -%s %s "%(op[0], op[1])


# setup logging
paramiko.util.log_to_file('test.log')

with open(args.hosts_file) as f:
    hosts = f.readlines()

print args.key_file

for host in hosts:
    host = host.replace("\n", "")
    username = ''
    if host.find('@') >= 0:
        username, hostname = host.split('@')

    if len(hostname) == 0:
        print '*** Hostname required.'
        sys.exit(1)
    port = 22
    if hostname.find(':') >= 0: 
        hostname, portstr = hostname.split(':')
        port = int(portstr)

    print "USERNAME: %s \nHOSTNAME: %s\nPORT: %d"%(username, hostname, port) 

    # now connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
    except Exception, e:
        print '*** Connect failed: ' + str(e)
        traceback.print_exc()
        sys.exit(1)

    try:
        t = paramiko.Transport(sock)

        try:
            t.start_client()
        except paramiko.SSHException:
            print '*** SSH negotiation failed.'
            sys.exit(1)

        try:
            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print '*** Unable to open host keys file'
                keys = {}


        # check server's host key -- this is important.
        key = t.get_remote_server_key()
        if not keys.has_key(hostname):
            print '*** WARNING: Unknown host key!'
        elif not keys[hostname].has_key(key.get_name()):
            print '*** WARNING: Unknown host key!'
        elif keys[hostname][key.get_name()] != key:
            print '*** WARNING: Host key has changed!!!'
            sys.exit(1)
        else:
            print '*** Host key OK.'

        # get username
        if username == '':
            default_username = getpass.getuser()
            username = raw_input('Username [%s]: ' % default_username)
            if len(username) == 0:
                username = default_username

        agent_auth(t, username)
        if not t.is_authenticated():
            manual_auth(username, hostname)
        if not t.is_authenticated():
            print '*** Authentication failed. :('
            t.close()
            sys.exit(1)

        
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(args.script, args.script)


        print '*** Here we go!'
        print 
        chan = t.open_session()
        chan.exec_command("chmod +x %s; ./%s %s ;rm %s"%(args.script, args.script, script_args, args.script))

        t.close()


    except Exception, e:
        print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
        traceback.print_exc()
        try:
            t.close()
        except:
            pass
        sys.exit(1)
