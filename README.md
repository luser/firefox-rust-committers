Firefox committers touching Rust code
=====================================

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

5. Run query:

   ```
   hg log -r 'filelog("glob:**.rs")' --template '{firstpushdate|isodatesec},{author|email},{node|short}\n' > firefox-rust-committers.csv
   ```

