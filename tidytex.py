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
    FileWatcher(texfile, success, timeout).monitor()


class FileWatcher:
    def __init__(self, texfile, print_success, timeout):
        self.texfile = texfile
        self.print_success = print_success
        self.timeout = timeout
        self.last_mod_time = None
        self.temp_dir = tempfile.mkdtemp()
        self.tex_dir, self.tex_filename = os.path.split(texfile)
        self.pdf_filename = "{:s}.pdf".format(self.tex_filename[:-4])
        self.temp_pdf = os.path.join(self.temp_dir, self.pdf_filename)
        self.permanent_pdf = os.path.join(self.tex_dir, self.pdf_filename)
        self.match_codes = [
            "!",  # some error happened
            "LaTeX Warning:.*Rerun.*",  # there are some references that need to be run
            "LaTeX Warning:.*[\r\n]",  # some warning should be printed
            pexpect.EOF  # fall through -- assume success
        ]
        self.match_responses = {
            0: lambda proc: self.process_error(proc),
            1: lambda proc: True,
            2: lambda proc: self.process_warning(proc),
            3: lambda proc: self.process_success(proc)
        }

    def _mod_time(self):
        return os.path.getmtime(self.texfile)

    def was_updated(self):
        new_time = self._mod_time()
        if new_time != self.last_mod_time:
            self.last_mod_time = new_time
            return True
        return False

    def check(self):
        if not os.path.exists(self.texfile):
            raise IOError("No such file {:s}".format(self.texfile))

        if not self.texfile.endswith(".tex"):
            raise IOError("Must supply a file with suffix '.tex' (you supplied {:s})".format(
                self.texfile))

    def spawn_compiler(self):
        self.check()
        proc = pexpect.spawn("pdflatex -output-directory={:s} {:s}".format(
            self.temp_dir,
            self.texfile), maxread=1)
        return proc

    def monitor(self):
        while True:
            if self.was_updated():
                rerun = True
                run_count = 0
                while rerun and run_count < 3:
                    run_count += 1
                    tex_process = self.spawn_compiler()
                    rerun = self.pdf_tex(tex_process)
                if rerun:
                    print("References did not resolve after {:d} tries".format(run_count))
                elif run_count > 1 and self.print_success:
                    print("Compiled {:d} times to resolve references".format(run_count))
            time.sleep(self.timeout)

    @staticmethod
    def process_error(tex_process):
        print(tex_process.before)
        j = 0
        while j != 1:
            j = tex_process.expect(["\? ", pexpect.EOF])
            print(tex_process.before)
            if j == 0:
                tex_process.sendline('')
        return False

    def process_warning(self, tex_process):
        j = 2
        while j == 2:
            print(tex_process.after)
            j = tex_process.expect(self.match_codes)
        return j

    def process_success(self, _):
        if self.print_success:
            print("[{:s}] Compilation successful!".format(str(datetime.datetime.today())))
        if os.path.exists(self.temp_pdf):
            shutil.move(self.temp_pdf, self.permanent_pdf)
        return False

    def pdf_tex(self, tex_process):
        i = tex_process.expect(self.match_codes)
        response_codes = set(range(len(self.match_codes)))
        while any(i is j for j in response_codes):
            i = self.match_responses[i](tex_process)
        return i


if __name__ == '__main__':
    tidy()