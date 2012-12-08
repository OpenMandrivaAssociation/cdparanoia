%define	major	0
%define	fullname %{name}-III-%version
%define	libname		%mklibname cdda %{major}
%define develname	%mklibname cdda -d

Summary:	Utility to copy digital audio CDs
Name:		cdparanoia
Version:	10.2
Release:	11
Epoch:		1
License:	GPLv2+ and LGPLv2+
Group:		Sound
URL:		http://www.xiph.org/paranoia/ 
Source0:	http://downloads.xiph.org/releases/cdparanoia/%{fullname}.src.tgz
Patch0:		cdparanoia-III-alpha9.8-includes.patch
Patch1:		cdparanoia-III-10.2-gcc43.patch
Patch2:		cdparanoia-III-10.2-format-security.patch

%description
This CDDA reader distribution ('cdparanoia') reads audio from the CDROM
directly as data, with no analog step between, and writes the data to a file
or pipe as .wav, .aifc or as raw 16 bit linear PCM.

cdparanoia is a complete rewrite of Heiko Eissfeldt's 'cdda2wav' program,
and generally is much better at succeeding to read difficult discs with
cheap drives.

%package -n	%{libname}
Summary:	Libraries for cdparanoia
Group:		Sound

%description -n	%{libname}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%package -n	%{develname}
Summary:	Development libraries for cdparanoia
Group:		Development/C
Provides:	libcdda-devel = %{EVRD}
Provides:	cdda-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Obsoletes:	%{mklibname cdda 0 -d} < %{EVRD}

%description -n	%{develname}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%prep
%setup -q -n %{fullname}
%patch0 -p1 -b .includes
%patch1 -p1 -b .gcc43
%patch2 -p1 -b .fs

autoconf

%build
%configure2_5x --libdir=%{_libdir}/cdparanoia
# (gb) don't use fortify, this package has ugly abuse of memcpy() that we can't cope with if it's a macro
# XXX would be better to define scsi cmds constants instead...
export RPM_OPT_FLAGS="$(echo %{optflags} |sed s/-Wp,-D_FORTIFY_SOURCE=.//)"
make OPT="-fsigned-char -finline-functions -Dsize16='short' -Dsize32='int' $RPM_OPT_FLAGS"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_docdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_mandir}/man1

%makeinstall \
	BINDIR=%{buildroot}%{_bindir} \
	INCLUDEDIR=%{buildroot}%{_includedir} \
	LIBDIR=%{buildroot}%{_libdir} \
	MANDIR=%{buildroot}%{_mandir}

install -m644 cdparanoia.1 %{buildroot}%{_mandir}/man1/

# Fix permissions to avoid unstripped-binary-or-object rpmlint error
chmod 0755 %{buildroot}%{_libdir}/*.so.%{major}*

%files
%defattr(644,root,root,755)
%doc README 
%attr(755,root,root) %{_bindir}/cdparanoia
%attr(644,root,root) %{_mandir}/man1/cdparanoia.1*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so



%changelog
* Wed Feb 22 2012 abf
- The release updated by ABF

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:10.2-8mdv2011.0
+ Revision: 663360
- mass rebuild

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1:10.2-7mdv2011.0
+ Revision: 603820
- rebuild

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 1:10.2-6mdv2010.1
+ Revision: 540305
- rebuild so that shared libraries are properly stripped again

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 1:10.2-5mdv2010.1
+ Revision: 540012
- rebuild so that shared libraries are properly stripped again

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1:10.2-4mdv2010.1
+ Revision: 520019
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1:10.2-3mdv2010.0
+ Revision: 413225
- rebuild

* Sun Feb 15 2009 Colin Guthrie <cguthrie@mandriva.org> 1:10.2-2mdv2009.1
+ Revision: 340502
- Drop cputoolize patch (it seems to break things)
- Rediff includes patch for new fuzz policy
- Add patch from Gentoo for gcc43 (gtbz#238378)
- Fix format-security issues

* Thu Oct 16 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:10.2-1mdv2009.1
+ Revision: 294213
- new version

* Thu Oct 16 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:10.1-1mdv2009.1
+ Revision: 294200
- new version
- fix source URL

* Thu Aug 07 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:10.1-1mdv2009.0
+ Revision: 266441
- new version
- update license

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1:10.0-2mdv2009.0
+ Revision: 264345
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 GÃ¶tz Waschk <waschk@mandriva.org> 1:10.0-1mdv2009.0
+ Revision: 217475
- new version
- drop patch 2
- update license
- use the right configure macro
- get rid of the roman version number

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> IIIa9.8-13mdv2008.1
+ Revision: 136289
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Sep 09 2007 Adam Williamson <awilliamson@mandriva.org> IIIa9.8-13mdv2008.0
+ Revision: 83222
- rebuild for 2008
- don't package license
- drop unneeded Buildrequires autoconf2.1
- Fedora license policy
- new devel policy


* Fri Jan 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> IIIa9.8-12mdv2007.0
+ Revision: 108123
- Import cdparanoia

* Fri Jan 12 2007 GÃ¶tz Waschk <waschk@mandriva.org> IIIa9.8-12mdv2007.1
- Rebuild

* Tue Mar 21 2006 Götz Waschk <waschk@mandriva.org> IIIa9.8-11mdk
* Tue Mar 21 2006 GÃ¶tz Waschk <waschk@mandriva.org> IIIa9.8-11mdk
- Rebuild
- use mkrel

* Thu Aug 18 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 9.8-10mdk
- don't build with fortify

* Wed Jun 09 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> IIIa9.8-9mdk
- fix gcc-3.4 build (P2)
- buildrequires
- cosmetics

