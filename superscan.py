from __future__ import print_function

import argparse
import subprocess
import sys
import os
import re
import tempfile


class SuperScanner(object):
    def __init__(self):
        self.tmp_folder = tempfile.mkdtemp()
        self.scanned_files = []

    def get_next_index(self):
        return len(self.scanned_files) + 1

    def scan_page(self):
        page_name = os.path.join(self.tmp_folder, "scan_%d.png" % self.get_next_index())

        scanimage = subprocess.Popen(('scanimage', '--resolution', '300', '--source',
            'Automatic Document Feeder'), stdout=subprocess.PIPE)
        convert = subprocess.Popen(('convert', '-', page_name), stdin=scanimage.stdout,
            stdout=sys.stdout)
        scanimage.wait()
        convert.wait()

        self.scanned_files.append(page_name)

    def make_pdf(self, filename):
        cmd = ['convert'] + self.scanned_files + [filename]
        subprocess.call(cmd)


class ScannerUI(object):
    INTRX = re.compile(r'^\d+$')
    MENU = """\
1. Enter an integer to scan N pages
2. Enter 'pdf' to generate the PDF"""

    def __init__(self):
        self.scanner = SuperScanner()

    def start(self):
        self.running = True

        print("\nGreetings, sir! What project will we be working on today?")
        self.filename = self.get_filename()

        print("\n%s, very well! And what can I do for you?" % self.filename)
        self.menu()

    def get_filename(self):
        name = self.prompt()
        if not name.endswith('.pdf'):
            name += '.pdf'
        return name

    def prompt(self):
        return raw_input("> ")

    def menu(self):
        print(self.MENU)
        while self.running:
            cmd = self.prompt()
            if self.INTRX.match(cmd):
                print()
                for n in range(int(cmd)):
                    print("Page %d in the works, sir!" %
                        self.scanner.get_next_index())
                    self.scanner.scan_page()
                print("\nAlright! What now?")
                print(self.MENU)
            elif cmd == "kthx":
                self.running = False
                print("Have a nice day, sir!\n\n")
            elif cmd == 'pdf':
                print("\nRight away, sir, just one moment!")
                self.scanner.make_pdf(self.filename)
                print("There you go, sir, fresh and warm!\n")
                self.running = False
            else:
                print("\nI'm sorry, what?")


def main():
    ScannerUI().start()


if __name__ == '__main__':
    main()
