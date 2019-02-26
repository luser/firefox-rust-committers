Firefox committers touching Rust code
=====================================

This repository contains data about the number of Rust vs. C/C++ commits
and commit authors in Firefox and instructions for reproducing the output.


Instructions
============

1. Clone the [`mozilla-central`](https://hg.mozilla.org/mozilla-central) Mercurial repository:

   `hg clone https://hg.mozilla.org/mozilla-central`
2. Clone the [`version-control-tools`](https://hg.mozilla.org/hgcustom/version-control-tools/) repository:

   `hg clone https://hg.mozilla.org/hgcustom/version-control-tools/`
3. Enable the `mozext` and `firefoxtree` extensions in `.hgrc`:

   ```
   [extensions]
   mozext = /path/to/version-control-tools/hgext/mozext
   firefoxtree = /path/to/version-control-tools/hgext/firefoxtree
   ```

4. Sync pushlog data:

   ```
   hg pushlogsync
   ```

5. Run queries (in mozilla-central clone):

   ```
   # List all commits that touched files ending in .rs.
   TZ=UTC hg log -r 'filelog("glob:**.rs")' --template '{firstpushdate|hgdate},{author|email},{node|short}\n' > firefox-rust-committers.csv
   # List all commits that touched files ending in C/C++ file extensions,
   # starting from 2015-05-09, when the first Rust code landed in Firefox.
   TZ=UTC hg log -r 'filelog("re:\.(c|cpp|cc|m|mm|h)") & firstpushdate(">2015-05-09")' --template '{firstpushdate|hgdate},{author|email},{node|short}\n' > firefox-cpp-committers.csv
   ```

6. Create virtualenv:

   ```
   virtualenv venv
   . venv/bin/activate
   pip install arrow plotly
   ```

7. Run script to generate graphs:

   ```
   python committers.py firefox-rust-committers.csv firefox-cpp-committers.csv docs/index.html
   ```
