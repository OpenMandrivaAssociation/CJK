Name: CJK
Summary: LaTeX2e macro package for Chinese/Japanese/Korean scripts
License: GPLv2+
Group: Publishing
URL:	http://cjk.ffii.org/
Version: 4.8.1
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
%setup -q -n cjk-%version

%build

cc $RPM_OPT_FLAGS -s -o zhconv %{SOURCE2}
cd utils/hbf2gf; chmod ugo+x ./configure ./config.sub ./config.guess;
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
(cd texinput; \
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
 cp *.el emacs*/*.el %{buildroot}/usr/share/emacs/site-lisp)

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
%doc doc/*
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
%{_datadir}/emacs/site-lisp/*.el


%changelog
* Wed Dec 08 2010 Oden Eriksson <oeriksson@mandriva.com> 4.8.1-3mdv2011.0
+ Revision: 616412
- the mass rebuild of 2010.0 packages

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 4.8.1-2mdv2010.0
+ Revision: 424991
- fix build
- rebuild

* Mon Aug 25 2008 Funda Wang <fwang@mandriva.org> 4.8.1-1mdv2009.0
+ Revision: 275848
- fix dir
- fix dir
- New version 4.8.1

* Tue Jul 22 2008 Thierry Vignaud <tv@mandriva.org> 4.7.0-3mdv2009.0
+ Revision: 240502
- rebuild
- kill re-definition of %%buildroot on Pixel's request
- s/Mandrake/Mandriva/
- convert prereq

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Funda Wang <fwang@mandriva.org>
    - correct source url

* Sun Apr 29 2007 Funda Wang <fwang@mandriva.org> 4.7.0-1mdv2008.0
+ Revision: 19099
- bunzip2 the patches.
- New upstream release 4.7.0
- Import CJK



* Sun Oct 31 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 4.2.0-7mdk
- fix old tar option

* Thu May 01 2003 Stefan van der Eijk <stefan@eijk.nu> 4.2.0-6mdk
- BuildRequires
- add URL

* Thu Dec 06 2001 Stefan van der Eijk <stefan@eijk.nu> 4.2.0-5mdk
- fix %%files

* Thu Sep 13 2001 Stefan van der Eijk <stefan@eijk.nu> 4.2.0-4mdk
- BuildRequires:	tetex

* Mon Jun 18 2001 David BAUDENS <baudens@mandrakesoft.com> 4.2.0-3mdk
- Use %%_tmppath for BuildRoot
- Bzip2 Sources and Patches
- Learn to setup to say nothing when it works

* Sun Jun 03 2001 Jesse Kuang <kyx@mandrakesoft.com> 4.2.0-2mdk
- change group to Publishing

* Sun Jun 03 2001 Jesse Kuang <kjx@mandrakesoft.com> 4.2.0-1mdk
- porting from CLE
- support TrueType for BIG5/GBK/GB

* Wed Jan 10 2001 Chih-Wei Huang <cwhuang@linux.org.tw>
- rebuilt for CLE v1.0
- add slant/bold to font def

* Mon Jan 17 2000 Chih-Wei Huang <cwhuang@linux.org.tw>
- Fix for Arphic Fonts

* Tue Jul 20 1999 Chih-Wei Huang <cwhuang@linux.org.tw>
- Split fonts into another packages to reduce size
- Add more Requires & Prereq

* Mon Jul 19 1999 Chih-Wei Huang <cwhuang@linux.org.tw>
- Remove Chinese fonts
- Split fonts into Japanese and Korean packages

* Thu Jun 24 1999 Chih-Wei Huang <cwhuang@linux.org.tw>
- Modify for CLE

* Tue May 18 1999 David Fox <dsf@pipeline.ucsd.edu>
- Release 5: Truetype support.
- Release 4: Moved hbf subdirectory into $TEXMF/fonts/type1
