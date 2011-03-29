#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Sys
%define		pnam	Virt
%include	/usr/lib/rpm/macros.perl
Summary:	Sys::Virt - Represent and manage a libvirt hypervisor connection
#Summary(pl.UTF-8):
Name:		perl-Sys-Virt
Version:	0.2.6
Release:	1
License:	GPL
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Sys/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	a4ca5735791e132320bd8546c5deacae
URL:		http://search.cpan.org/dist/Sys-Virt/
BuildRequires:	libvirt-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Test::Pod)
BuildRequires:	perl(Test::Pod::Coverage)
BuildRequires:	perl(XML::XPath)
BuildRequires:	perl(XML::XPath::XMLParser)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Sys::Virt module provides a Perl XS binding to the libvirt virtual
machine management APIs. This allows machines running within arbitrary
virtualization containers to be managed with a consistent API.

# %description -l pl.UTF-8 # TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} -j1 \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES INSTALL README
%dir %{perl_vendorarch}/Sys
%dir %{perl_vendorarch}/Sys/Virt
%{perl_vendorarch}/Sys/*.pm
%{perl_vendorarch}/Sys/Virt/*.pm
%dir %{perl_vendorarch}/auto/Sys/Virt
%{perl_vendorarch}/auto/Sys/Virt/*.bs
%attr(755,root,root) %{perl_vendorarch}/auto/Sys/Virt/*.so
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
