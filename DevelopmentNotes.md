# Development #

  1. TODO

# Deployment #

## Documentation ##

The online documentation accessible through Google Code in a separate repository called 'docs' which has the Mercurial URL https://docs.asq.googlecode.com/hg/ and which can be cloned to asq/docs/build on a developers machine inside asq/docs such that Sphinx builds its HTML output into the docs repository.

```
 $ cd asq/docs
 $ hg clone https://docs.asq.googlecode.com/hg/ build
```

Now we have a nested repository used for the documentation products, which we can move into:

```
 $ cd build
```

To update the documentation, we can copy the existing documentation to a new location so we have an archive of historical versions:

```
 $ hg cp html 0.9/html
```

Then the documentation can be built like so,

```
  $ cd asq/docs
  $ make html
  Making output directory...
  Running Sphinx v1.0.7
  loading pickled environment... not yet created
  building [html]: targets for 13 source files that are out of date
  updating environment: 13 added, 0 changed, 0 removed
  reading sources... [  7%] changes
  reading sources... [ 15%] differences
  reading sources... [ 23%] faq
  reading sources... [ 30%] front_matter/front_matter
  reading sources... [ 38%] index
  reading sources... [ 46%] narrative
  reading sources... [ 53%] reference/extension
  reading sources... [ 61%] reference/initiators
  reading sources... [ 69%] reference/predicates
  reading sources... [ 76%] reference/queryables
  reading sources... [ 84%] reference/record
  reading sources... [ 92%] reference/reference
  reading sources... [100%] reference/selectors
  
  ...

  done
  dumping search index... done
  dumping object inventory... done
  build succeeded, 13 warnings.

  Build finished. The HTML pages are in build/html.
```

Once committed and pushed back to Google Code:

```
  $ cd build
  $ hg commit
  $ hg push
```

The documentation is then available to browse on the web at the URLs:

  * http://docs.asq.googlecode.com/hg/html/index.html
  * http://docs.asq.googlecode.com/hg/0.9/html/index.html

# Building the source distributions #

  1. Check the contents of the MANIFEST.in file
  1. Check the contents of the README.txt file
  1. Update the CHANGES.txt file.
  1. Update asq/version.py
  1. Update setup.py

Now create the source distribution.  We create one for Windows (zip) and one for Unix (.tar.gz).

```
$ python setup.py sdist --formats=gztar,zip
running sdist
... <huge output snipped> ...
```

The archives should be present at dist/asq-0.9.tar.gz and dist/asq-0.9.zip.

Take a look at these manually and try to install them locally.

# Upload the source distributions #

Upload the source distributions to Google Code using the web interface.

# Publish to the Python Package index #

Run the sdist command again, but now with the 'upload' command to populate the PyPI

```
$ python setup.py sdist --formats=gztar,zip upload
running sdist
... <huge output snipped> ...
```

Visit the asq page on PyPI and verify that the links are good back to Google Code.

# Update the Google Code website to feature the new release #

  * Make the new uploaded packages 'Featured'
  * Make the previous release 'Deprecated'
  * Update the link to the documentation on the Administer tab to point to the correct archived version of the docs.
  * Edit the front page, if necessary.

# Tag the release #

```
$ hg tag 0.9
```
