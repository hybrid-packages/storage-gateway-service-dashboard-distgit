%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name storage-gateway-dashboard
%global mod_name storage_gateway_dashboard

Name:           storage-gateway-ui
Version:        XXX
Release:        XXX
Summary:        The UI component for the OpenStack storage-gateway service
Group:          Applications/Communications
License:        ASL 2.0
URL:            https://github.com/Hybrid-Cloud/%{pypi_name}
Source0:        https://github.com/Hybrid-Cloud/%{name}/%{name}-%{upstream_version}.tar.gz

BuildRequires:  gettext
BuildRequires:  openstack-dashboard
BuildRequires:  python-devel
BuildRequires:  python-django-formtools
BuildRequires:  python-django-nose
BuildRequires:  python-mock
BuildRequires:  python-mox3
BuildRequires:  python-sgsclient
BuildRequires:  python-pbr >= 1.6
BuildRequires:  python-setuptools
BuildRequires:  python-testtools
#BuildRequires:  pbr
#BuildRequires:  babel
#BuildRequires:  django
#BuildRequires:  django-babel
#BuildRequires:  django-compressor
#BuildRequires:  django-openstack-auth
#BuildRequires:  django-pyscss

Requires:       openstack-dashboard
Requires:       PyYAML >= 3.10
Requires:       python-babel >= 2.3.4
Requires:       python-django >= 1.8
Requires:       python-iso8601 >= 0.1.11
Requires:       python-sgsclient
Requires:       python-six >= 1.9.0
#Requires:       pbr
#Requires:       babel
#Requires:       django
#Requires:       django-babel
#Requires:       django-compressor
#Requires:       django-openstack-auth
#Requires:       django-pyscss
BuildArch:      noarch

%description
storage-gateway Dashboard
Sytem package - storage-gateway-dashboard
Python package - storage-gateway-dashboard
Storage-gateway Dashboard is an extension for OpenStack Dashboard that provides a UI
for Storage-gateway.

%package doc
Summary:        Documentation for OpenStack storage-gateway dashboard
BuildRequires:  python-sphinx
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-reno

%description doc
Storage-Gateway Dashboard is an extension for OpenStack Dashboard that provides a UI
for Storage-Gateway.
This package contains the documentation.

%prep
%setup -q -n %{pypi_name}-%{upstream_version}
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

# Generate i18n files
#pushd build/lib/%{mod_name}
#django-admin compilemessages
#popd

# generate html docs
# %{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled
# Enable Horizon plugin for storage-gateway-dashboard
cp %{_builddir}/%{pypi_name}-%{upstream_version}/storage_gateway_dashboard/enabled/_70*.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;
find %{buildroot} -name djangojs.po -exec rm '{}' \;

# Find language files
#%find_lang django --all-name

%check
#export PYTHONPATH="%{_datadir}/openstack-dashboard:%{python2_sitearch}:%{python2_sitelib}:%{buildroot}%{python2_sitelib}"
#%{__python2} manage.py test storage_gateway_dashboard --settings=storage_gateway_dashboard.test.settings

%post
%systemd_postun_with_restart httpd.service

%postun
%systemd_postun_with_restart httpd.service

%files
%license LICENSE
%doc README.md
%{python2_sitelib}/storage_gateway_dashboard
%{python2_sitelib}/storage_gateway_dashboard*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/*

%files doc
%license LICENSE
# %doc doc/build/html

%changelog
