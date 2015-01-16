# tidytex
Keep LaTeX folders clean and compile automatically

# installation
`pip install git+https://github.com/ColCarroll/tidytex.git@master`

# usage

```
    $ tidytex path/to/my/texfile.tex
    [2015-01-15 22:53:35.221573] Compilation 1 successful!
    ...
```

Then saving `texfile.tex` will trigger an automatic compiling of texfile.tex.  Also, 
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
* If the user saves twice, we should abandon the current compiling and start a new one
