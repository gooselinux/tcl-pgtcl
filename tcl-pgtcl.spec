Name:		tcl-pgtcl
Version:	1.6.2
Release:	3%{?dist}
Summary:	A Tcl client library for PostgreSQL

Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/pgtclng/
# PostgreSQL calls their license simplified BSD, but the requirements are
# more similar to other MIT licenses.
License:	MIT

# Upstream uses a bizarre website structure that makes it difficult to give
# stable URLs for individual files.  These files can be found by following
# links from http://pgfoundry.org/projects/pgtclng/
Source0:	pgtcl%{version}.tar.gz
# Note that for some reason docs are date-labeled not version-labeled
Source1:	pgtcldocs-20070115.zip

Patch1:		pgtcl-no-rpath.patch

Provides:	pgtcl = %{version}-%{release}
# pgtcl was originally shipped as a sub-RPM of the PostgreSQL package;
# these Provides/Obsoletes give a migration path.  The cutoff EVR was
# chosen to be later than anything we are likely to ship in Fedora 12.
Provides:	postgresql-tcl = 8.5.0-1
Obsoletes:	postgresql-tcl < 8.5

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	postgresql-devel tcl-devel
BuildRequires:	autoconf

Requires:	tcl(abi) = 8.5

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%description
PostgreSQL is an advanced Object-Relational database management system.
The tcl-pgtcl package contains Pgtcl, a Tcl client library for connecting
to a PostgreSQL server.

%prep
%setup -q -n pgtcl%{version}

unzip %{SOURCE1}
PGTCLDOCDIR=`basename %{SOURCE1} .zip`
mv $PGTCLDOCDIR Pgtcl-docs

%patch1 -p1

autoconf

%build

%configure --libdir=%{tcl_sitearch} --with-tcl=%{_libdir}

# note: as of pgtcl 1.5.2, its makefile is not parallel-safe
make all

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
# we don't really need to ship the .h file
rm -f $RPM_BUILD_ROOT%{_includedir}/libpgtcl.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/tcl%{tcl_version}/pgtcl%{version}/
%doc Pgtcl-docs/*

%changelog
* Thu Jan 21 2010 Tom Lane <tgl@redhat.com> 1.6.2-3
- Correct Source: tags and comment to reflect how to get the tarball.

* Tue Nov 24 2009 Tom Lane <tgl@redhat.com> 1.6.2-2
- Fix License tag as per discussion in PyGreSQL package review request.
Related: #452321

* Fri Jun 20 2008 Tom Lane <tgl@redhat.com> 1.6.2-1
- Created package by stripping down postgresql specfile and adjusting
  to meet current packaging guidelines for Tcl extensions.
