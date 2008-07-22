Name: CJK
Summary: LaTeX2e macro package for Chinese/Japanese/Korean scripts
License: GPL
Group: Publishing
URL:	http://cjk.ffii.org/
Version: 4.7.0
Release: %mkrel 3

# Source0 is a tarball of the CJK files stored in the FTP directory,
# they are stored there unpacked.
Source0: http://cjk.ffii.org/cjk-%{version}.tar.gz
# font def
Source1: cjk-420-mdk.tar.bz2
Source2: zhconv.c
Source3: zhlatex
Source4: special.map.add
Source5: ttfonts.map.add
Patch1: CJK-hbf2gf.patch
Patch2: CJK-lisp.patch

Requires: tetex >= 0.9 tetex-latex >= 0.9 freetype
Requires(post): tetex tetex-latex freetype
Requires(postun): tetex tetex-latex freetype
BuildRequires:	tetex-devel
BuildRoot:	%_tmppath/%name-%version-%release-root

%description
This is a package of macros and fonts and utilities for doing
Chinese/Japanese/Korean word processing using LaTeX.
Please refer to Linux Chinese HOWTO for more details.

%package emacs
Summary: Emacs support for the CJK package
Group: Publishing
Requires: CJK = %{version}-%{release}

%description emacs
Emacs code to convert files between Mule to CJK encodings.  To use this,
put (load-library "cjk-enc") in your .emacs.  Then when you are editing a
.ltx file you can create a .cjk.ltx file in the cjk-coding by calling
M-x write-cjk-file.  After that the .cjk.ltx file will be automatically
updated when the .ltx file is saved.  Emacs will also know about the
.cjk.ltx file when it runs latex, xdvi, or dvips.

%prep

%setup -q -c
%setup -q -D -T

# Fix to the emacs lisp code

#%patch2 -p1

%build

cc $RPM_OPT_FLAGS -s -o zhconv %{SOURCE2}
cd cjk-4.7.0/utils
cd hbf2gf; chmod ugo+x ./configure ./config.sub ./config.guess;
./configure --prefix=/usr/share/texmf --with-kpathsea-dir=/usr
make
cd ../Bg5conv
cc $RPM_OPT_FLAGS -s -o bg5conv bg5conv.c
chmod ugo+x bg5latex
cd ../SJISconv
cc $RPM_OPT_FLAGS -s -o sjisconv sjisconv.c
chmod ugo+x sjislatex
cd ../CEFconv
chmod ugo+x cef5latex ceflatex cefslatex
cc $RPM_OPT_FLAGS -s -o cefconv cefconv.c
cc $RPM_OPT_FLAGS -s -o cef5conv cef5conv.c
cc $RPM_OPT_FLAGS -s -o cefsconv cefsconv.c

%install

rm -rf %{buildroot}

mkdir -p %{buildroot}/usr/share/texmf/tex/CJK
(cd cjk-4.7.0/texinput; \
 tar cf - . | (cd %{buildroot}/usr/share/texmf/tex/CJK; tar xf -))

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
cp zhconv %{buildroot}%{_bindir}
cp %{SOURCE3} %{buildroot}%{_bindir}
ln -s zhlatex %{buildroot}%{_bindir}/gbklatex
ln -s zhlatex %{buildroot}%{_bindir}/bg5latex
mkdir -p %{buildroot}/usr/share/texmf/fontname
mkdir -p %{buildroot}/usr/share/texmf/ttf2pk
cp %{SOURCE4} %{buildroot}/usr/share/texmf/fontname
cp %{SOURCE5} %{buildroot}/usr/share/texmf/ttf2pk

cd cjk-4.7.0
cd utils
 cd hbf2gf
  cp hbf2gf %{buildroot}%{_bindir}
  cp hbf2gf.1 %{buildroot}%{_mandir}/man1/hbf2gf.1
# cd ../Bg5conv
#  cp bg5conv bg5latex %{buildroot}%{_bindir}
#  cp bg5conv.1 %{buildroot}%{_mandir}/man1
 cd ../CEFconv
  cp cefconv ceflatex cef5conv cef5latex cefsconv cefslatex \
		%{buildroot}%{_bindir}
  cp cef5conv.1 cefconv.1 cefsconv.1 %{buildroot}%{_mandir}/man1
 cd ../SJISconv
  cp sjisconv sjislatex %{buildroot}%{_bindir}
  cp sjisconv.1 %{buildroot}%{_mandir}/man1
 cd ..
cd ..

# CJK TrueType fonts for Mandriva
tar xjf %{SOURCE1} -C %{buildroot}/usr/share

mkdir -p %{buildroot}/usr/share/emacs/site-lisp
(cd utils/lisp && \
 cp *.el emacs-20.3/*.el %{buildroot}/usr/share/emacs/site-lisp)

%post
(cd /usr/share/texmf/fontname; cat special.map.add >> special.map)
(cd /usr/share/texmf/ttf2pk; cat ttfonts.map.add >> ttfonts.map)
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%postun
(cd /usr/share/texmf/fontname; \
mv -f special.map special.map.sav; \
sed -e '/CJK begin/,/CJK end/d' special.map.sav > special.map)
(cd /usr/share/texmf/ttf2pk; \
mv -f ttfonts.map ttfonts.map.sav; \
sed -e '/CJK begin/,/CJK end/d' ttfonts.map.sav > ttfonts.map)
[ -x /usr/bin/texhash ] && /usr/bin/env - /usr/bin/texhash 2> /dev/null
exit 0

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc cjk-4.7.0/doc/*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/texmf/fontname/*
%{_datadir}/texmf/fonts/tfm/*
%{_datadir}/texmf/fonts/truetype
%{_datadir}/texmf/tex/CJK
%{_datadir}/texmf/tex/latex/CJK
%{_datadir}/texmf/ttf2pk

%files emacs
%defattr(-,root,root)
/usr/share/emacs/site-lisp/*.el
