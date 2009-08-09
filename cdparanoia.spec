%define	name	cdparanoia
%define	major	0
%define	version	10.2
%define	release %mkrel 3
%define	fullname %{name}-III-%version

%define	libname		%mklibname cdda %{major}
%define develname	%mklibname cdda -d

Summary:	Utility to copy digital audio CDs
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		1
Source0:	http://downloads.xiph.org/releases/cdparanoia/%{fullname}.src.tgz
Patch0:		cdparanoia-III-alpha9.8-includes.patch
Patch1:		cdparanoia-III-10.2-gcc43.patch
Patch2:		cdparanoia-III-10.2-format-security.patch
URL:		http://www.xiph.org/paranoia/ 
License:	GPLv2+ and LGPLv2+
Group:		Sound
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
Provides:	libcdda-devel = %epoch:%{version}
Provides:	cdda-devel = %epoch:%{version}
Requires:	%{libname} = %epoch:%{version}
Obsoletes:	%{mklibname cdda 0 -d}

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
rm -rf $RPM_BUILD_ROOT
%configure2_5x --libdir=%{_libdir}/cdparanoia
# (gb) don't use fortify, this package has ugly abuse of memcpy() that we can't cope with if it's a macro
# XXX would be better to define scsi cmds constants instead...
export RPM_OPT_FLAGS="$(echo %optflags |sed s/-D_FORTIFY_SOURCE=.//)"
make OPT="-fsigned-char -finline-functions -Dsize16='short' -Dsize32='int' $RPM_OPT_FLAGS"

%clean
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_docdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

%makeinstall \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	INCLUDEDIR=$RPM_BUILD_ROOT%{_includedir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

install -m644 cdparanoia.1 $RPM_BUILD_ROOT%{_mandir}/man1/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(644,root,root,755)
%doc README 
%attr(755,root,root) %{_bindir}/cdparanoia
%attr(644,root,root) %{_mandir}/man1/cdparanoia.1*

%files -n %{libname}
%defattr(644,root,root,755)
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

