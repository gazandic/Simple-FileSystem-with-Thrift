/*
 * filesharing.thrift
 *
 * @author Gazandi Cahyadarma <gazandi@urbanindo.com>
 *
 * This file contains thrift definitions for File and directory.
 */

struct File {

    1: required string name;

    2: required list<byte> data;

}

struct Directory {

    1: required string name;

    2: required string path;

    3: optional list<File> listFiles;

    4: optional list<string> listDirectories;

}

exception DirectoryNotFoundException {

    1: optional string message;

}

exception FileNotFoundException {

    1: optional string message;

}

service FileSharing {

    list<string> getDirectory(1: string path);

    string createDir(1: string path, 2: string namaDir) throws (1: DirectoryNotFoundException dirException) ;

    list<byte> getFile(1: string path, 2: string namaFile) throws (1: FileNotFoundException dirException);

    string putFile (1: string path, 2: list<byte> dataFile, 3: string namaFile) throws (1: FileNotFoundException dirException);

}
