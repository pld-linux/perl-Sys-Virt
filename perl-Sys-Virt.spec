#
# Conditional build:
%bcond_with	tests		# perform "make test" (requires libvirtd)
#
%define		pdir	Sys
%define		pnam	Virt
Summary:	Sys::Virt - Represent and manage a libvirt hypervisor connection
Summary(pl.UTF-8):	Sys::Virt - reprezentacja i zarządzanie połączeniem z hipernadzorcą libvirt
Name:		perl-Sys-Virt
Version:	6.3.0
Release:	4
License:	GPL v2+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Sys/%{pdir}-%{pnam}-v%{version}.tar.gz
# Source0-md5:	08450ac24eca20d8e96fe3f9d644ccb7
URL:		https://metacpan.org/release/Sys-Virt
BuildRequires:	libvirt-devel >= 6.3.0
BuildRequires:	perl-devel >= 1:5.16
BuildRequires:	perl-Module-Build
BuildRequires:	pkgconfig
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
%if %{with tests}
BuildRequires:	libvirt-daemon >= 6.3.0
BuildRequires:	perl-CPAN-Changes
BuildRequires:	perl-Test-Pod
BuildRequires:	perl-Test-Pod-Coverage
BuildRequires:	perl-Test-Simple
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-XML-XPath
%endif
Requires:	libvirt >= 6.3.0
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
%setup -q -n %{pdir}-%{pnam}-v%{version}

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

%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Sys/Virt/Virt.bs

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
