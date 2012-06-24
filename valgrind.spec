Summary:	An open-source memory debugger for x86-GNU/Linux
Summary(pl):	Otwarty odpluskwiacz pami�ci dla Linuksa x86
Name:		valgrind
Version:	1.0.0
Release:	1
License:	GPL
ExclusiveArch:	%{ix86}
Group:		Networking/Utilities
Source0:	http://developer.kde.org/~sewardj/%{name}-%{version}.tar.bz2
URL:		http://developer.kde.org/~sewardj/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# valgrind binaries should _never_ be stripped
# anyone knows better solution?
%define		debug	1

%description
Valgrind is a GPL'd tool to help you find memory-management problems
in your programs. When a program is run under Valgrind's supervision,
all reads and writes of memory are checked, and calls to
malloc/new/free/delete are intercepted. As a result, Valgrind can
detect problems such as:

- Use of uninitialised memory
- Reading/writing memory after it has been free'd
- Reading/writing off the end of malloc'd blocks
- Reading/writing inappropriate areas on the stack
- Memory leaks -- where pointers to malloc'd blocks are lost forever
- Passing of uninitialised and/or unaddressible memory to system calls
- Mismatched use of malloc/new/new [] vs free/delete/delete []
- Some misuses of the POSIX pthreads API

%description -l pl
Valgrind jest narz�dziem rozwi�zuj�cym problemy zwi�zane z zarz�dzaniem
pami�ci� w programach. Gdy program zostaje uruchomiony pod nadzorem
Valgrinda wszystkie odczyty i zapisy do pami�ci s� sprawdzane.
Przechwytywane s� te� odwo�ania do malloc/new/free/delete. Dzi�ki temu
mo�na wykry� nast�puj�ce problemy:

- U�ycie niezainicjalizowanej pami�ci
- Odczytywanie/zapisywanie do obszaru pami�ci, kt�ry zosta� zwolniony
- Odczytywanie/zapisywanie na ko�cach zaalokowanych blok�w
- Odczytywanie/zapisywanie niew�a�ciwych obszar�w na stosie
- Wycieki pami�ci -- gdy wska�niki do zaalokowanych blok�w s� stracone na
  zawsze
- Przekazywanie niezainicjalizowanej i/lub nieadresowalnej pami�ci do
  odwo�a� systemowych
- Niekonsekwencja w u�ywaniu malloc/new/new [] kontra free/delete/delete []
- Niekt�re nadu�ycie API POSIX pthreads

%prep
%setup -q

%build
rm -f missing
aclocal
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGEMENTS AUTHORS ChangeLog PATCHES_APPLIED
%doc README README_MISSING_SYSCALL_OR_IOCTL TODO
%doc docs/*.html
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*
%{_libdir}/%{name}
