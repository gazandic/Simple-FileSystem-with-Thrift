import glob
import sys
import os
import os.path
import getopt
sys.path.append('gen-py')
# sys.path.insert(0, glob.glob('../../lib/py/build/lib*')[0])

from filesharing.ttypes import File, Directory, FileNotFoundException, DirectoryNotFoundException
from filesharing.FileSharing import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class FileSharingHandler:
    pathFirst = "/home/gazandic/Tingkat 4/PAT/Tugas 2/server";
    def __init__(self, string):
        self.pathFirst = string;
        print('Starting the server at'+self.pathFirst)

    def getDirectory(self, path):
        print('getDir')
        # Open a file
        paths = self.pathFirst + path
        dirs = os.listdir(paths)
        # This would print all the files and directories
        return dirs

    def createDir(self, path, namaDir):
        print('createDir')
        paths = self.pathFirst + path + "/" + namaDir
        if os.path.isdir(paths):
            print("error udah ada filenya")
            raise DirectoryNotFoundException("sudah ada")
        else:
            os.mkdir( paths, 0755 )
            return "create file success"

    def getFile(self, path, namaFile):
        print('getFile')
        fileloc = self.pathFirst + path + "/" + namaFile
        try:
            f = open(fileloc, 'r')
            lis = bytearray()
            byte = f.read(1)
            lis.append(byte)
            while byte != "":
                # Do stuff with byte.
                byte = f.read(1)
                lis.append(byte)

        except (OSError, IOError) as e:
            print('DirectoryNotFoundException: %r' % e)
            raise FileNotFoundException("ga ada filenya")

        finally:
            f.close()
            return lis

    def putFile(self, path, dataFile, namaFile):
        print('putFile')
        try:
            pathloc = self.pathFirst + path
            if not os.path.isdir(pathloc):
                os.mkdir( pathloc, 0755 )
            fileloc = pathloc + "/" + namaFile
            target = open(fileloc, 'w')
            for bit in dataFile:
                ri = chr(bit)
                target.write(ri)

        finally:
            target.close()
            return "success to create file"

        return "failed to create file"

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:],"hg:c:p:d:",["getDirectory=","createDir=","putFile=","getFile="])
    if len(sys.argv) > 1:
        print(sys.argv[1])
    else:
        print 'server.py <path>'
        sys.exit(2)
    dir_path = os.path.dirname(os.path.realpath(__file__))+"/server/"
    if not os.path.isdir(dir_path):
        os.mkdir( dir_path, 0755 )
    dir_path += args[0]
    handler = FileSharingHandler(dir_path)
    processor = Processor(handler)
    transport = TSocket.TServerSocket(port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(
        processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)
    server.serve()
    print('done.')
