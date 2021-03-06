%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           openio-sds-tests
Version:        %(date +"%Y%m%d")
Release:        1%{?dist}
Summary:        OpenIO SDS Functionnal Validation

License:        LGPL
URL:            http://www.openio.io/
Source0:        testing-8ce1a074d340c3a88da8d88d1a24610a94f730c8.tar.gz

BuildArch:      noarch
BuildRequires:  python-setuptools
Requires:       python-oiopy


%description
OpenIO SDS Functionnal Validation

%prep
%setup -q -n testing.git


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root $RPM_BUILD_ROOT

%files
%{python_sitelib}/*


%changelog
* Tue Sep 15 2015 Romain Acciari <romain.acciari@openio.io>
- New release
* Tue Sep 01 2015 Romain Acciari <romain.acciari@openio.io>
- New release
* Wed Aug 26 2015 Romain Acciari <romain.acciari@openio.io>
- New release
* Tue May 12 2015 Romain Acciari <romain.acciari@openio.io>
- Update
* Mon Mar 16 2015 Guillaume Delaporte <guillaume.delaporte@openio.io>
- Make it more robust
* Mon Mar 09 2015 Guillaume Delaporte <guillaume.delaporte@openio.io>
- Initial release
