import os
import datetime
import pexpect
import tempfile
import shutil
import time
import click
import sys


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


class FileWatcher:
    def __init__(self, filename):
        self.filename = filename
        self.last_mod_time = self._mod_time()

    def _mod_time(self):
        return os.path.getmtime(self.filename)

    def was_updated(self):
        new_time = self._mod_time()
        if new_time != self.last_mod_time:
            self.last_mod_time = new_time
            return True
        return False


def monitor_file(filename, success, timeout):
    file_watcher = FileWatcher(filename)
    tex_process, temp_dir = spawn_compiler(filename)
    pdf_tex(tex_process, filename, temp_dir, success)
    while True:
        if file_watcher.was_updated():
            tex_process, temp_dir = spawn_compiler(filename)
            pdf_tex(tex_process, filename, temp_dir, success)
        time.sleep(timeout)


def print_process(tex_process):
    print tex_process.before


def spawn_compiler(texfile):
    if not os.path.exists(texfile):
        raise IOError("No such file {:s}".format(texfile))

    if not texfile.endswith(".tex"):
        raise IOError("Must supply a file with suffix '.tex' (you supplied {:s})".format(texfile))

    temp_dir = tempfile.mkdtemp()

    return pexpect.spawn("pdflatex -output-directory={:s} {:s}".format(temp_dir, texfile), maxread=10000), temp_dir


def pdf_tex(tex_process, texfile, temp_dir, print_success):
    was_success = True
    i = tex_process.expect(["!", pexpect.EOF])
    if i == 0:
        tex_process.sendline('')
        print_process(tex_process)
        j = 0
        while j != 1:
            j = tex_process.expect(["!", pexpect.EOF])
            print_process(tex_process)
            if j == 0:
                tex_process.sendline('')
    elif i == 1:
        if was_success and print_success:
            print("[{:s}] Compilation successful!".format(str(datetime.datetime.today())))

    tex_dir, tex_filename = os.path.split(texfile)
    pdf_filename = "{:s}.pdf".format(tex_filename[:-4])
    if os.path.exists(os.path.join(temp_dir, pdf_filename)):
        shutil.move(os.path.join(temp_dir, pdf_filename), os.path.join(tex_dir, pdf_filename))
    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    tidy()