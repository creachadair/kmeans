## 
## Name:     Makefile
## Purpose:  Build script for KMeans module.
## Author:   M. J. Fromberger (@creachadair)
##

SRCS=KMeans.py
OTHER=Makefile setup.py

.PHONY: clean distclean dist install

clean:
	rm -f *~

install: clean
	python setup.py install

distclean: clean
	rm -rf build
	rm -f *.pyc

dist: distclean
	if [ -d "kmeans" ] ; then rm -rf "kmeans" ; fi
	if [ -f "kmeans.zip" ] ; then mv -f kmeans.zip kmeans-old.zip ; fi
	mkdir "kmeans"
	for fn in $(SRCS) $(OTHER) ; do cp $${fn} "kmeans/" ; done
	zip -9r kmeans.zip kmeans
	rm -rf "kmeans"

# Here there be dragons
