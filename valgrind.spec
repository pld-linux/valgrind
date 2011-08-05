Summary:	An open-source memory debugger
Summary(pl.UTF-8):	Otwarty odpluskwiacz pamięci
Name:		valgrind
Version:	3.6.1
Release:	2
License:	GPL
Group:		Development/Tools
Source0:	http://valgrind.org/downloads/%{name}-%{version}.tar.bz2
# Source0-md5:	2c3aa122498baecc9d69194057ca88f5
Patch0:		%{name}-debuginfo.patch
Patch1:		%{name}-native-cpuid.patch
Patch2:		%{name}-opge.patch
Patch3:		%{name}-glibc214.patch
URL:		http://valgrind.org/
BuildRequires:	autoconf
BuildRequires:	automake
# Needs libc.a
BuildRequires:	glibc-static
BuildRequires:	libgomp-devel
Obsoletes:	valgrind-callgrind
Obsoletes:	valgrind-calltree
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*/vgpreload.*\\.so
# ld portion broken
%undefine	with_ccache

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs.
With the tools that come with Valgrind, you can automatically detect
many memory management and threading bugs, avoiding hours of
frustrating bug-hunting, making your programs more stable. You can
also perform detailed profiling to help speed up your programs.

%description -l pl.UTF-8
Valgrind jest systemem służącym do odpluskwiania i profilowania
programów na Linuksie. Używając dostarczanych z nim narzędzi można
automatycznie wykrywać wiele błędów związanych z zarządzaniem pamięcią
i wątkowaniem, dzięki czemu unika się frustrującego polowania na
błędy, a także czyni się programy bardziej stabilnymi. Możliwe jest
również dokładne profilowanie, dzięki któremu programy zaczną szybciej
pracować.

%prep
%setup -q
%patch0
%patch1 -p1
%patch2 -p1
%patch3 -p1

sed -i -e 's:^CFLAGS="-Wno-long-long":CFLAGS="$CFLAGS -Wno-long-long":' configure.in

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}

ac_cv_path_GDB=/usr/bin/gdb \
%configure \
	--enable-tls \
%if %{_lib} != "lib"
	--enable-only64bit \
%endif
	LDFLAGS="" # no strip!

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc
mv docs/index.pdf docs/valgrind_manual.pdf
mv docs/index.ps docs/valgrind_manual.ps

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README README_MISSING_SYSCALL_OR_IOCTL
%doc docs/html docs/valgrind_manual.pdf docs/valgrind_manual.ps
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*-linux
%{_libdir}/%{name}/*.a
%attr(755,root,root) %{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.supp
%{_mandir}/man1/*.1*
%{_pkgconfigdir}/*.pc
