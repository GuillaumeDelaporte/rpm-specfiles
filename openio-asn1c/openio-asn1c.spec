%define		realname asn1c

Name:		openio-%{realname}
Version:	0.9.27
Release:	1%{?dist}
Summary:	Free, Open Source ASN.1 compiler

License:	BSD
URL:		http://lionet.info/asn1c
Source0:	http://lionet.info/soft/asn1c-%{version}.tar.gz

BuildRequires:	autoconf,automake,libtool
#Requires:	

%description
Compiles ASN.1 data structures into C source structures that can be
simply marshalled to/unmarshalled from: BER, DER, CER, BASIC-XER,
CXER, EXTENDED-XER, PER.


%prep
%setup -q
autoreconf -iv


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

%{__rm} -rf $RPM_BUILD_ROOT/%{_libdir}/*.la # Clean useless files
%{__mv} $RPM_BUILD_ROOT/%{_defaultdocdir}/%{realname} \
        $RPM_BUILD_ROOT/%{_defaultdocdir}/%{name}-%{version}

%files
#%doc BUGS COPYING ChangeLog FAQ README.md
#%doc TODO doc/asn1c-quick.pdf doc/asn1c-usage.pdf
%{_bindir}/*
%{_libdir}/*
%{_mandir}/man1/*
%{_datadir}/%{realname}
%{_defaultdocdir}/%{name}-%{version}


%changelog
* Tue Feb 03 2015 Romain Acciari <romain.acciari@openio.io> - 0.9.27-1
- Initial release
