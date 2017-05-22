#
# Conditional build:
%bcond_with	tests		# perform "make test" (requires libvirtd)
#
%define		pdir	Sys
%define		pnam	Virt
%include	/usr/lib/rpm/macros.perl
Summary:	Sys::Virt - Represent and manage a libvirt hypervisor connection
Summary(pl.UTF-8):	Sys::Virt - reprezentacja i zarządzanie połączeniem z hipernadzorcą libvirt
Name:		perl-Sys-Virt
Version:	2.5.0
Release:	1
License:	GPL v2+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Sys/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	d07fca31367bef924ffe5c62e0d5f18a
URL:		http://search.cpan.org/dist/Sys-Virt/
BuildRequires:	libvirt-devel >= 1.2.19
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	libvirt-daemon >= 1.2.19
BuildRequires:	perl-CPAN-Changes
BuildRequires:	perl-Test-Pod
BuildRequires:	perl-Test-Pod-Coverage
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-XML-XPath
%endif
Requires:	libvirt >= 1.2.19
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Sys::Virt module provides a Perl XS binding to the libvirt virtual
machine management APIs. This allows machines running within arbitrary
virtualization containers to be managed with a consistent API.

%description -l pl.UTF-8
Moduł Sys::Virt dostarcza wiązanie XS Perla do API zarządzania
maszynami wirtualnymi libvirt. Pozwala na zarządzanie poprzez
jednolite API maszynami wirtualnymi działającymi w dowolnych
kontenerach.

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
%doc AUTHORS Changes README
%{perl_vendorarch}/Sys/Virt.pm
%dir %{perl_vendorarch}/Sys/Virt
%{perl_vendorarch}/Sys/Virt/*.pm
%dir %{perl_vendorarch}/auto/Sys/Virt
%attr(755,root,root) %{perl_vendorarch}/auto/Sys/Virt/Virt.so
%{_mandir}/man3/Sys::Virt*.3pm*
%{_examplesdir}/%{name}-%{version}
