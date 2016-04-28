from utils import *
from parser import Parser
import os


def main():
    """ Entry point of the program """

    parser = Parser()
    sources = []
    destinations = []
    sources, destinations = check_args(parser)
    sources = [os.path.normpath(os.getcwd() + '/' + item) for item in sources]

    for source in sources:
        for dest in destinations:
            match = chk_dest_format(dest, DEST_PATTERN)
            host = match.group(4)
            port = int(match.group(3))
            username = match.group(1)
            remote_dir = match.group(5)
            passwd = parser.args.passwd

            sftp = establish_sftp_conn(host, port, username, passwd)
            ssh = establish_ssh_conn(host, port, username, passwd)

            content_local = get_content_local(source)
            content_remote = get_content_remote(sftp, ssh, remote_dir)

            to_sync = files_to_sync(content_local, source, content_remote, remote_dir)
            create_dirs(sftp, to_sync, source, remote_dir)
            sync_files(to_sync, source, remote_dir, host)


if __name__ == '__main__':
    main()
