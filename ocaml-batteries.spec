%define		module	batteries
Summary:	OCaml Batteries Included
Name:		ocaml-%{module}
Version:	2.2
Release:	1
License:	LGPL
Group:		Libraries
Source0:	https://forge.ocamlcore.org/frs/download.php/1363/%{module}-%{version}.tar.gz
# Source0-md5:	42063b5f2da9a311ff16799b8bec4ba5
URL:		http://batteries.forge.ocamlcore.org/
#BuildRequires:	-devel
BuildRequires:	ocaml >= 3.04-7
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	TEMPLATE binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania TEMPLATE dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
TEMPLATE library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
TEMPLATE biblioteki.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} -j1 all

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $OCAMLFIND_DESTDIR/%{module}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%{_libdir}/ocaml/%{module}/battop.ml
%attr(755,root,root) %{_libdir}/ocaml/%{module}/ocaml
%{_libdir}/ocaml/%{module}/ocamlinit
%{_libdir}/ocaml/site-lib/%{module}

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/ocaml/%{module}/*.cm[xia]
%{_libdir}/ocaml/%{module}/*.cmo
%{_libdir}/ocaml/%{module}/*.mli
%{_libdir}/ocaml/%{module}/*.[ao]
%{_libdir}/ocaml/%{module}/*.cmxa
%{_examplesdir}/%{name}-%{version}
