import glob
import sys
import os
import os.path
import getopt
sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from filesharing.ttypes import File, Directory, FileNotFoundException, DirectoryNotFoundException
from filesharing.FileSharing import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

def main(argv):

    dir_path = os.path.dirname(os.path.realpath(__file__))+"/client/"
    if not os.path.isdir(dir_path):
        os.mkdir( dir_path, 0755 )
    localPath = ""
    namaFile = ""
    path = ""
    mode = 0
    try:
        opts, args = getopt.getopt(argv,"hg:c:p:d:",["getDirectory=","createDir=","putFile=","getFile="])
    except getopt.GetoptError:
        print 'client.py -g <path> | -c <path> <namaFile> | -d <path> <namaFile> <localPath> | -p <path> <namaFile> <localPath>'
        sys.exit(2)
    if len(sys.argv) < 2:
        print 'client.py -g <path> | -c <path> <namaFile> | -d <path> <namaFile> <localPath> | -p <path> <namaFile> <localPath>'
        sys.exit(2)
    i = 0
    for opt, arg in opts:
        if opt == '-h':
            print 'client.py -g <path> -c <path> <namaFile> -d <path> <namaFile> <localPath> -p <path> <namaFile> <localPath>'
            sys.exit()
        elif opt in ("-g", "--getDirectory"):
            path = arg
            mode = 1
        elif opt in ("-c", "--createDir"):
            path = arg
            namaFile = args[0]
            mode = 2
        elif opt in ("-d", "--getFile"):
            path = arg
            namaFile = args[0]
            localPath = dir_path + args[1]
            mode = 3
        elif opt in ("-p", "--putFile"):
            path = arg
            namaFile = args[0]
            localPath = dir_path + args[1]
            mode = 4
        i += 1
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Client(protocol)

    # Connect!
    transport.open()

    directory = Directory()
    if mode == 1:
        if path == '/':
            path = ""
        dirs = client.getDirectory(path)
        print("files :")
        for dires in dirs:
            print dires
    elif mode == 2:
        strs = client.createDir(path,namaFile)
        print(strs)
    elif mode == 3:
        bits = client.getFile(path,namaFile)
        print(bits)
        pathloc = localPath
        if not os.path.isdir(pathloc):
            os.mkdir( pathloc, 0755 )
        fileloc = pathloc + "/" + namaFile
        target = open(fileloc, 'w')
        for bit in bits:
            ri = unichr(bit)
            target.write(ri)
        target.close()
    elif mode == 4:
        fileloc = localPath + "/" + namaFile
        try:
            f = open(fileloc, 'r')
            lis = bytearray()
            byte = f.read(1)
            lis.append(byte)
            while byte != "":
                # Do stuff with byte.
                byte = f.read(1)
                lis.append(byte)

        except (OSError, IOError, ValueError) as e:
            print('FoundException: %r' % e)
            # raise FileNotFoundException("ga ada filenya")

        finally:
            f.close()
            stri = client.putFile(path, lis, namaFile)
            print(stri)
    # Close!
    transport.close()

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except Thrift.TException as tx:
        print('%s' % tx.message)
