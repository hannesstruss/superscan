import argparse
import subprocess
import sys
import os
import tempfile


def scan_pages(num_pages, filename):
    if not filename.endswith('.png'):
        filename = filename + ".png"

    folder = tempfile.mkdtemp()
    filename = os.path.join(folder, filename)

    all_files = []

    for page in range(num_pages):
        page_name = filename.replace(".png", "_{:0>4}.png".format(page + 1))
        print "scanning %s..." % page_name
        scanimage = subprocess.Popen(('scanimage', '--resolution', '300', '--source',
            'Automatic Document Feeder'), stdout=subprocess.PIPE)
        convert = subprocess.Popen(('convert', '-', page_name), stdin=scanimage.stdout,
            stdout=sys.stdout)
        scanimage.wait()
        convert.wait()

        all_files.append(page_name)

    return all_files


def make_pdf(files, outfile):
    cmd = ['convert'] + files + [outfile]
    subprocess.call(cmd)


def main():
    parser = argparse.ArgumentParser(description='''Don't-forget-the-values-wrapper around scanimage''')
    parser.add_argument('--pages', type=int, help='Scan that many pages')
    parser.add_argument('--filename', type=str, help='Use that as the filename')
    args = parser.parse_args()
    
    pages = scan_pages(args.pages, args.filename)
    make_pdf(pages, args.filename + ".pdf")
    # map(os.remove, pages)


if __name__ == '__main__':
    main()
