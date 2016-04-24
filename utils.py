#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko
import socket
import stat
import pwd
import grp
import os
import os.path
import shlex
import subprocess
import sys

def test_connection(host, port, username, passwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=username, password=passwd)
        print 'Connection verified'
        ssh.close()
    except paramiko.AuthenticationException:
        print 'Authentication failed'
    except paramiko.SSHException:
        print 'SSHException error'
    except socket.error as se:
        print se
    except:
        print 'Generic error'
    finally:
        ssh.close()


def gethostbyname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
        print 'Unknown hostname'
        return
    except:
        print 'Generic error'
        return


def chkdir_remote(path):
    try:
        t = paramiko.Transport((host, port))
        t.connect(username=username, password=passwd)
        sftp = paramiko.SFTPClient.from_transport(t)

        try:
            attrs = sftp.stat(path)
            if (attrs.st_mode & stat.S_IFDIR):
                print path + ' is a directory'
            else:
                print path + ' is not a directory'
        except:
            print 'Destination does not exist'

        t.close()

    except paramiko.AuthenticationException:
        print 'Authentication failed'
    except paramiko.SSHException:
        print 'SSHException error'
    except socket.error as se:
        print se
    #except:
    #    print 'Generic error'
    finally:
        t.close()


def chksource_local(path):
    if not os.path.exists(source):
        print 'Path does not exist'


def get_file_attrs_local(path):
    """ Returns dictionary with attributes of a local *path* file """

    st = os.stat(path)
    attributes = {}
    attributes['type'] = 'file'
    attributes['hash'] = get_hash_local(path)
    attributes['size'] = st.st_size
    attributes['uid'] = pwd.getpwuid(st.st_uid)
    attributes['gid'] = grp.getgrgid(st.st_gid)

    return attributes


def get_file_attrs_remote(sftp, ssh, path):
    """ Returns dictionary with attributes of a remote *path* file """

    st = sftp.stat(path)
    attributes = {}
    attributes['type'] = 'file'
    attributes['hash'] = get_hash_remote(ssh, path)
    attributes['size'] = st.st_size
    attributes['uid'] = st.st_uid
    attributes['gid'] = st.st_gid

    return attributes


def get_dir_content_remote(sftp, ssh, path):
    """ Returns content of a remote *path* directory """

    st = sftp.stat(path)
    attributes = {}
    attributes['type'] = 'directory'
    attributes['uid'] = st.st_uid
    attributes['gid'] = st.st_gid
    content = {}
    attributes['content'] = content

    for filename in sftp.listdir(path):
        try:
            file = os.path.join(path, filename)
            attrs = sftp.stat(file)
            if (attrs.st_mode & stat.S_IFDIR):
                content[file] = get_dir_content_remote(sftp, ssh, file)
            elif (attrs.st_mode & stat.S_IFREG):
                content[file] = get_file_attrs_remote(sftp, ssh, file)
        except Exception as ex:
            print ex
            print 'Destination {0} does not exist'.format(file)
            sys.exit(1)

    return attributes


def get_dir_content_local(path):
    """ Returns content of a local *path* directory """

    st = os.stat(path)
    attributes = {}
    attributes['type'] = 'directory'
    attributes['uid'] = pwd.getpwuid(st.st_uid)
    attributes['gid'] = grp.getgrgid(st.st_gid)
    content = {}
    attributes['content'] = content
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        if os.path.isfile(file):
            content[file] = get_file_attrs_local(file)
        elif os.path.isdir(file):
            content[file] = get_dir_content_local(file)
        # Test for soft link

    return attributes


def get_content_local(path):
    """ Returns content of a local *path* directory """

    content = {}
    if os.path.isfile(path):
        content[path] = get_file_attrs_local(path)        
    elif os.path.isdir(path):
        content[path] = get_dir_content_local(path)

    content = flatten(content)

    return content


def flatten(input, output=None):
    """ Flattens out nested dictionary """

    if not output:
        output = {}

    for key in input.keys():
        output[key] = input[key]
        if input[key]['type'] == 'directory':
            flatten(input[key]['content'], output)
            output[key].pop('content')

    return output


def get_content_remote(sftp, ssh, path):
    """ Returns content of a remote *path* directory """

    content = {}
    content[path] = get_dir_content_remote(sftp, ssh, path)

    content = flatten(content)

    return content


def establish_sftp_conn(host, port, username, password):
    """ Establishes sFTP connection to host:post using username and password """

    t = paramiko.Transport((host, port))
    t.connect(username=username, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(t)

    return sftp


def establish_ssh_conn(host, port, username, passwd):
    """ Estabishes SSH connection to host:post using username and password """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=passwd)

    return ssh


def get_hash_local(path):
    """ Gets hash of a local *path* file """

    cmd = shlex.split("md5sum " + path)
    ps = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ps.stdout.read().split()[0]


def get_hash_remote(ssh, path):
    """ Gets hash of a remote *path* file """

    stdin, stdout, stderr = ssh.exec_command("md5sum " + path)
    return stdout.read().split()[0]


def files_to_sync(source_content, source_path, dest_content, dest_path):
    """ Returns a list of files and directories to be synchronized """

    if os.path.isdir(source_path):
        source_content.pop(source_path)

    source_keys = [key.replace(source_path, '') for key in source_content.keys()]
    dest_keys = [key.replace(dest_path, '') for key in dest_content.keys()]
    diff = [os.path.normpath(source_path+'/'+key) for key in list(set(source_keys).difference(set(dest_keys)))]
    to_sync = {key:source_content[key] for key in diff}

    return to_sync


def create_dirs(sftp, source_tree, source, dest):
    """ Creates directories that need to be synched (missing in *dest*) """

    L = []
    for key in source_tree.keys():
        if os.path.isdir(key):
            L.append(key)
    L = [item.replace(source, dest) for item in L]
    sorted(L, key=lambda item: len(item.split('/')))

    for dir in L:
        print 'Creating directory {}'.format(dir)
        sftp.mkdir(dir)


def sync_files(source_tree, source, dest, host):
    """ Creates a tuple of (source, dest) files to be syncronized.
        Calls rsync to make synchronization """

    source_files = []
    for key in source_tree.keys():
        if os.path.isfile(key):
            source_files.append(key)

    dest_files = []
    for file in source_files:
        destination = '{0}@{1}:{2}'.format(username, host, file.replace(source, dest))
        dest_files.append(destination)
    
    for src, dst in zip(source_files, dest_files):
        rsync(0, src, dst)


def rsync(options, source, dest):
    """ rsync wrapper function """

    cmd = shlex.split('rsync {} {}'.format(source, dest))
    print cmd
    subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
