%define		snap	20030725
Summary:	An open-source memory debugger for x86-GNU/Linux
Summary(pl):	Otwarty odpluskwiacz pamiêci dla Linuksa x86
Name:		valgrind
Version:	1.9.6
Release:	1.%{snap}.1
License:	GPL
ExclusiveArch:	%{ix86}
Group:		Networking/Utilities
Source0:	http://developer.kde.org/~sewardj/%{name}-%{snap}.tar.bz2
# Source0-md5:	f09994ef936088d215902548f55c8d68
#Source0:	%{name}-%{snap}.tar.bz2
Patch0:		%{name}-sockios.patch
URL:		http://developer.kde.org/~sewardj/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Valgrind binaries should _never_ be stripped
%define		no_install_post_strip	1

# Same name as libpthread
%define		_noautoprovfiles %{_libdir}/%{name}/libpthread.so.0 %{_libdir}/%{name}/libpthread.so %{_libdir}/%{name}/valgrind.so %{_libdir}/%{name}/valgrinq.so

%description
Valgrind is a flexible tool for debugging and profiling Linux-x86
executables. The tool consists of a core, which provides a synthetic
x86 CPU in software, and a series of "skins", each of which is a
debugging or profiling tool. The architecture is modular, so that new
skins can be created easily and without disturbing the existing
structure.

A number of useful skins are supplied as standard. In summary, these
are:
- The memcheck skin detects memory-management problems in your
  programs,
- cachegrind performs detailed simulation of the I1, D1 and L2 caches
  in your CPU and so can accurately pinpoint the sources of cache misses
  in your code,
- addrcheck skin is a lightweight version of memcheck,
- helgrind is designed to find data races in multithreaded programs.

%description -l pl
Valgrind jest elastycznym narzêdziem s³u¿±cym do odpluskwiania i
profilowania programów pod Linuksem. Sk³ada siê z rdzenia
dostarczaj±cego syntetyczny emulowany procesor zgodny z x86 i ze
"skórek" bêd±cych narzêdziami o ró¿nych zastosowaniach. Architektura
programu jest modularna, wobec czego ³atwo mo¿na stworzyæ nowe skórki
nie ryzykuj±c popsucia reszty.

Standardowo dostarczone jest kilka u¿ytecznych skórek:
- memcheck wykrywa problemy z zarz±dzaniem pamiêci± w programach,
- cachegrind przeprowadza symulacjê pamiêci cache procesora w celu
  znalezienia miejsc, w których cache zawodzi,
- addrcheck jest lekk± wersj± memchecka,
- helgrind wykrywa konflikty dostêpu w wielow±tkowych programach.

%prep
%setup -q -n %{name}-%{snap}
%patch0 -p1

%build
rm -f missing
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	LDFLAGS="" # no strip!
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS AUTHORS FAQ.txt NEWS PATCHES_APPLIED
%doc README README_MISSING_SYSCALL_OR_IOCTL TODO
%doc $RPM_BUILD_ROOT%{_docdir}/valgrind/*.html
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*
%{_libdir}/%{name}
