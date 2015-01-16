# tidytex
Keep LaTeX folders clean and compile automatically

# installation

`pip install git+https://github.com/ColCarroll/tidytex.git@master`
This will install [Click](http://click.pocoo.org/3/) to run from the command line, and [pexpect](http://pexpect.readthedocs.org/en/latest/) to handle output from `pdflatex`.

Also, this is just a wrapper around `pdflatex`, so you'll need to have everything installed and configured so that `$ pdflatex mytexfile.tex` works.

# usage

In a terminal/screen, run
```
    $ tidytex path/to/my/texfile.tex
    [2015-01-15 22:53:35.221573] Compilation 1 successful!
    ...
```
Then edit `texfile.tex` in the editor of your choice.  Saving `texfile.tex` will automatically generate a new pdf, without any auxiliary files.  Also see
```
colinc@colinc-mbp:~$ tidytex --help
Usage: tidytex [OPTIONS] TEXFILE

  Monitor a LaTeX file, and compile on save.  Pass in the path to the file.

  ex:
  $ tidytex ../path/to/texfile.tex

Options:
  -t, --timeout FLOAT             How frequently to check file for changes
  -s, --success / -ns, --no-success
                                  Show message on successful compilation?
  --help                          Show this message and exit.
```

# TODO
* Right now, if there is an error, the user must interact with the open terminal before monitoring of the file continues. We should kill the thread running `pdflatex` and start a new one.
* There should be an option to keep auxiliary files around
* There should be an option to turn off automatic compiling
