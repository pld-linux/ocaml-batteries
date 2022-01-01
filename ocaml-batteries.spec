#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	batteries
Summary:	OCaml Batteries Included
Summary(pl.UTF-8):	OCaml Batteries Included - baterie dołączone do OCamla
Name:		ocaml-%{module}
Version:	3.4.0
Release:	1
License:	LGPL v2.1+ with OCaml linking exception
Group:		Libraries
#Source0Download: https://github.com/ocaml-batteries-team/batteries-included/tags
Source0:	https://github.com/ocaml-batteries-team/batteries-included/archive/v%{version}/batteries-included-%{version}.tar.gz
# Source0-md5:	66b6e0b25769fc2363972c6a6ab6ac33
URL:		https://github.com/ocaml-batteries-team/batteries-included
BuildRequires:	ocaml >= 1:3.12.1
BuildRequires:	ocaml-findlib >= 1.5.3
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
"OCaml Batteries Included" or just Batteries is a community-maintained
foundation library for your OCaml projects.

This package contains files needed to run bytecode executables using
OCaml Batteries library.

%description -l pl.UTF-8
"OCaml Batteries Included" lub po prostu Batteries to utrzymywana
przez społeczność biblioteka podstawowa dla projektów w OCamlu.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki OCamla Batteries.

%package devel
Summary:	OCaml Batteries Included - development part
Summary(pl.UTF-8):	OCaml Batteries Included - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
batteries library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki batteries.

%prep
%setup -q -n batteries-included-%{version}

%build
%{__make} -j1 all

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ LICENSE README.md
%dir %{_libdir}/ocaml/batteries
%{_libdir}/ocaml/batteries/META
%{_libdir}/ocaml/batteries/battop.ml
%attr(755,root,root) %{_libdir}/ocaml/batteries/ocaml
%{_libdir}/ocaml/batteries/ocamlinit
%{_libdir}/ocaml/batteries/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/batteries/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/batteries/*.cmi
%{_libdir}/ocaml/batteries/*.cmt
%{_libdir}/ocaml/batteries/*.cmti
%{_libdir}/ocaml/batteries/*.cmo
%{_libdir}/ocaml/batteries/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/batteries/*.a
%{_libdir}/ocaml/batteries/*.cmx
%{_libdir}/ocaml/batteries/*.cmxa
%endif
%{_examplesdir}/%{name}-%{version}
