#!/usr/bin/env python3

import os
import shutil

class Messages():
    symbol = '[PYCOMMANDER]'

    error_messages = {
    'folder_not_found': f'{symbol} - Folder not found!',
    'unknown_command': f'{symbol} - Unknown command!',
    'folder_exists': f'{symbol} - Folder already exists!',
    'src_not_found': f'{symbol} - Source not found!',
    'dest_exists': f'{symbol} - Destination name already exists!',
    'dest_not_exists': f'{symbol} - Destination file does not exists!',
    }

    system_messages = {
    'exit': f'{symbol} - Logout...'
    }


class Viewer():
    messages = Messages()

    def list_files(self, *args):
        if len(args) >= 1:
            if os.path.exists(args[0]):
                target_dir = args[0]
            else:
                print(self.messages.error_messages['folder_not_found'])
                return
        else:
            target_dir = os.curdir
        last_dir = os.getcwd()
        os.chdir(target_dir)
        file_list = os.listdir(os.curdir)
        print('{:<20} {:<15} {:<10}'.format('Filename', 'Type', 'Size (bytes)'))
        for file in file_list:
            if os.path.isdir(file):
                type = 'D'
            elif os.path.isfile(file):
                type = 'F'
            elif os.path.islink(file):
                type = 'L'
            elif os.path.ismount(file):
                type = 'M'
            print('{:<20} |{:<15} |{:<10}'.format(
                file, type, os.path.getsize(file)))
        os.chdir(last_dir)

    def change_current_directory(self, *args):
        path = ' '.join(args)
        if os.path.exists(path):
            os.chdir(path)
        else:
            print(self.messages.error_messages['folder_not_found'])

    def clear(self,):
        print(chr(27) + "[2J")

    def exit(self,):
        print(self.messages.system_messages['exit'])
        exit()

    def default(self, *_args):
        print(self.messages.error_messages['unknown_command'])


class Editor():
    messages = Messages()

    def mkdir(self, *args):
        path = ' '.join(args)
        if os.path.exists(path):
            print(self.messages.error_messages['folder_exists'])
        else:
            os.makedirs(path)
            print(f'+ [DIR] {path}')

    def rmdir(self, *args):
        path = ' '.join(args)
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f'- [DIR] {path}')
        else:
            print(self.messages.error_messages['folder_not_found'])

    def rename(self, *args):
        if os.path.exists(args[0]):
            src = args[0]
        else:
            print(self.messages.error_messages['src_not_found'])
            return
        if os.path.exists(args[1]):
            print(self.messages.error_messages['dest_exists'])
            return
        else:
            dst = args[1]
        os.rename(src, dst)
        print(f'{src} -> {dst}')

    def rm(self, *args):
        path = ' '.join(args)
        if os.path.exists(path):
            os.remove(path)
            print(f'- [FILE] {os.path.basename(path)}')
        else:
            print(self.messages.error_messages['dest_not_exists'])
            return


viewer = Viewer()
editor = Editor()

command_list = {
    'ccd': viewer.change_current_directory,
    'lf': viewer.list_files,
    'exit': viewer.exit,
    'clear': viewer.clear,
    'mkdir': editor.mkdir,
    'rmdir': editor.rmdir,
    'rename': editor.rename,
    'rm': editor.rm,
}

while True:
    current_directory = os.getcwd()
    input_prefix = f'{current_directory} $> '
    try:
        command, *attrs = input(input_prefix).split()
    except ValueError:
        continue
    call_program = command_list.get(command, viewer.default)
    call_program(*attrs)
