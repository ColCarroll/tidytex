import os
import datetime
import pexpect
import tempfile
import shutil
import time
import click


@click.command()
@click.argument('texfile')
@click.option('--timeout', '-t', default=0.5, help="How frequently to check file for changes")
@click.option('--success/--no-success', '-s/-ns', default=True, help="Show message on successful compilation?")
def tidy(texfile, timeout, success):
    """
    Monitor a LaTeX file, and compile on save.  Pass in the path to the file.

    \b
    ex:
    $ tidytex ../path/to/texfile.tex
    """
    monitor_file(texfile, success, timeout)


def modification_date(filename):
    return os.path.getmtime(filename)


def monitor_file(filename, success, timeout):
    counter = pdf_tex(filename, success, 0)
    old_time = modification_date(filename)
    while True:
        new_time = modification_date(filename)
        if new_time != old_time:
            counter = pdf_tex(filename, success, counter)
            old_time = new_time
        time.sleep(timeout)


def pdf_tex(texfile, print_success, counter):
    if not os.path.exists(texfile):
        raise IOError("No such file {:s}".format(texfile))

    if not texfile.endswith(".tex"):
        raise IOError("Must supply a file with suffix '.tex' (you supplied {:s})".format(texfile))

    tex_dir, tex_filename = os.path.split(texfile)
    temp_dir = tempfile.mkdtemp()

    tex_process = pexpect.spawn("pdflatex -output-directory={:s} {:s}".format(temp_dir, texfile))
    was_success = True
    while True:
        i = tex_process.expect(["!", pexpect.EOF])
        if i == 0:
            was_success = False
            tex_process.interact()
        elif i == 1:
            if was_success and print_success:
                counter += 1
                print("[{:s}] Compilation {:,d} successful!".format(str(datetime.datetime.today()), counter))
            break

    pdf_filename = "{:s}.pdf".format(tex_filename[:-4])
    if os.path.exists(os.path.join(temp_dir, pdf_filename)):
        shutil.move(os.path.join(temp_dir, pdf_filename), os.path.join(tex_dir, pdf_filename))
    shutil.rmtree(temp_dir)
    return counter

if __name__ == '__main__':
    tidy()