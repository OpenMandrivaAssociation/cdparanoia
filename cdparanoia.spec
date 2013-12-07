%define	major	0
%define	sname	%{name}-III-%{version}
%define	libinterface	%mklibname cdda_interface %{major}
%define	libparanoia	%mklibname cdda_paranoia %{major}
%define devname	%mklibname cdda -d

Summary:	Utility to copy digital audio CDs
Name:		cdparanoia
Epoch:		1
Version:	10.2
Release:	16
License:	GPLv2+ and LGPLv2+
Group:		Sound
Url:		http://www.xiph.org/paranoia/ 
Source0:	http://downloads.xiph.org/releases/cdparanoia/%{sname}.src.tgz
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

%package -n	%{libinterface}
Summary:	Libraries for cdparanoia
Group:		System/Libraries
Obsoletes:	%{_lib}cdda0 < 1:10.2-12

%description -n	%{libinterface}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%package -n	%{libparanoia}
Summary:	Libraries for cdparanoia
Group:		System/Libraries
Conflicts:	%{_lib}cdda0 < 1:10.2-12

%description -n	%{libparanoia}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%package -n	%{devname}
Summary:	Development libraries for cdparanoia
Group:		Development/C
Provides:	cdda-devel = %{EVRD}
Requires:	%{libinterface} = %{EVRD}
Requires:	%{libparanoia} = %{EVRD}

%description -n	%{devname}
This is the development libraries for cdparanoia. cdparanoia is a complete
rewrite of Heiko Eissfeldt's 'cdda2wav' program, and generally is much better 
at succeeding to read difficult discs with cheap drives.

%prep
%setup -qn %{sname}
%apply_patches
autoconf

%build
%configure2_5x \
	--libdir=%{_libdir}/cdparanoia
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

rm -f %{buildroot}%{_libdir}/*.a

%files
%doc README 
%{_bindir}/cdparanoia
%{_mandir}/man1/cdparanoia.1*

%files -n %{libinterface}
%{_libdir}/libcdda_interface.so.%{major}*

%files -n %{libparanoia}
%{_libdir}/libcdda_paranoia.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

