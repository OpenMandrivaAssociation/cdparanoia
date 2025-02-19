%define major 0
%define sname %{name}-III-%{version}
%define libinterface %mklibname cdda_interface %{major}
%define libparanoia %mklibname cdda_paranoia %{major}
%define devname %mklibname cdda -d

# (gb) don't use fortify, this package has ugly abuse of memcpy() that we can't cope with if it's a macro
# XXX would be better to define scsi cmds constants instead...
%undefine _fortify_cflags

Summary:	Utility to copy digital audio CDs
Name:		cdparanoia
Epoch:		1
Version:	10.2
Release:	28
License:	GPLv2+ and LGPLv2+
Group:		Sound
Url:		https://www.xiph.org/paranoia/ 
Source0:	http://downloads.xiph.org/releases/cdparanoia/%{sname}.src.tgz
# Patch from upstream to fix cdda_interface.h C++ incompatibility ("private")
# https://trac.xiph.org/changeset/15338
# https://bugzilla.redhat.com/show_bug.cgi?id=463009
Patch0:		cdparanoia-10.2-#463009.patch
# #466659
Patch1:		cdparanoia-10.2-endian.patch
Patch2:		cdparanoia-10.2-install.patch
Patch3:		cdparanoia-10.2-format-security.patch
Patch4:		cdparanoia-use-proper-gnu-config-files.patch
Patch5:		cdparanoia-10.2-ldflags.patch

%description
This CDDA reader distribution ('cdparanoia') reads audio from the CDROM
directly as data, with no analog step between, and writes the data to a file
or pipe as .wav, .aifc or as raw 16 bit linear PCM.

cdparanoia is a complete rewrite of Heiko Eissfeldt's 'cdda2wav' program,
and generally is much better at succeeding to read difficult discs with
cheap drives.

%package -n %{libinterface}
Summary:	Libraries for cdparanoia
Group:		System/Libraries
Obsoletes:	%{_lib}cdda0 < 1:10.2-12

%description -n %{libinterface}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%package -n %{libparanoia}
Summary:	Libraries for cdparanoia
Group:		System/Libraries
Conflicts:	%{_lib}cdda0 < 1:10.2-12

%description -n %{libparanoia}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%package -n %{devname}
Summary:	Development libraries for cdparanoia
Group:		Development/C
Provides:	cdda-devel = %{EVRD}
Requires:	%{libinterface} = %{EVRD}
Requires:	%{libparanoia} = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{devname}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%prep
%setup -qn %{sname}
%patch0 -p3 -b .#463009
%patch1 -p1 -b .endian
%patch2 -p1 -b .install
%patch3 -p1 -b .fmt-sec
%patch4 -p1 -b .config
%patch5 -p1 -b .ldflags

cp /usr/share/libtool/config/config.* .
autoreconf -fiv

%build
%configure \
	--includedir=%{_includedir}/cdda \
	--libdir=%{_libdir}

%make_build -j1 OPT="-fsigned-char -finline-functions -Dsize16='short' -Dsize32='int' $RPM_OPT_FLAGS" LDFLAGS="%{ldflags}"

%install
%make_install

%files
%doc README
%{_bindir}/cdparanoia
%doc %{_mandir}/man1/cdparanoia.1*

%files -n %{libinterface}
%{_libdir}/libcdda_interface.so.%{major}*

%files -n %{libparanoia}
%{_libdir}/libcdda_paranoia.so.%{major}*

%files -n %{devname}
%{_includedir}/cdda/*
%{_libdir}/*.so
%{_libdir}/*.a
