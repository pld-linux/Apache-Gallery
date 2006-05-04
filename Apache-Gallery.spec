#
# Conditional build:
%bcond_with	tests	# perform "make test" during build
#
%include	/usr/lib/rpm/macros.perl
%define 	apxs		/usr/sbin/apxs
%define		pdir	Apache
%define		pnam	Gallery
%define		_rc	RC3
Summary:	An Apache module for creating an online gallery
Summary(pl):	Modu³ Apache'a do tworzenia galerii online
Name:		Apache-Gallery
Version:	1.0
Release:	0.%{_rc}.2
License:	Artistic
Group:		Applications/Graphics
Source0:	http://apachegallery.dk/download/%{name}-%{version}%{_rc}.tar.gz
# Source0-md5:	a705cbecf2f124d18a3bde3fc36384e8
Source1:	%{name}.conf
Patch0:		%{name}-cache_dir.patch
URL:		http://apachegallery.dk/
BuildRequires:	apache-mod_perl-devel >= 1:1.99
%{?with_tests:BuildRequires:	apache1-mod_perl}
BuildRequires:	perl-CGI >= 3.08
BuildRequires:	perl-Image-Imlib2 >= 1.02
BuildRequires:	perl-Image-Info
BuildRequires:	perl-Image-Size
BuildRequires:	perl-Text-Template
BuildRequires:	perl-URI >= 1.23
BuildRequires:	perl-devel
BuildRequires:	perl-libapreq2
BuildRequires:	rpm-perlprov >= 3.0.3-16
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache-mod_perl >= 1:2.0.0
Conflicts:	apache-mod_autoindex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(APR::Table)' 'perl(Apache2)' 'perl(Apache::Const)' 'perl(Apache::RequestIO)' 'perl(Apache::RequestRec)' 'perl(Apache::SubRequest)'
%define		_appdir		%{_datadir}/%{name}
%define		_apacheicons	%{_appdir}/icons
%define		_cachedir	/var/cache/%{name}

%description
Apache::Gallery is a mod_perl handler that sits on top of your
DocumentRoot and creates an image gallery of the files and directories
there. It creates an thumbnail index of each directory and allows
viewing of pictures in different resolutions. Pictures are resized on
the fly and cached.

%description -l pl
Apache::Gallery to procedura obs³ugi dla modu³u mod_perl po³o¿ona w
DocumentRoot, tworz±ca galeriê obrazów z umieszczonych tam plików i
katalogów. Tworzy indeks z miniaturkami z ka¿dego katalogu i pozwala
na ogl±danie obrazków w ró¿nych rozdzielczo¶ciach. Obrazki s±
przeskalowywane w locie i buforowane.

%prep
%setup -q -n %{name}-%{version}%{_rc}
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir}/templates/{new,default},%{_apacheicons},/etc/{httpd/httpd.conf,tmpwatch},%{_cachedir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install templates/new/*.{css,tpl} $RPM_BUILD_ROOT%{_appdir}/templates/new/
install templates/default/*.{css,tpl} $RPM_BUILD_ROOT%{_appdir}/templates/default/
install htdocs/*.png $RPM_BUILD_ROOT%{_apacheicons}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/httpd.conf/09_%{name}.conf

echo "%{_cachedir} 720" > $RPM_BUILD_ROOT/etc/tmpwatch/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd reload

%triggerpostun -- Apache-Gallery < 1.0-0.RC3.2
if [ -d "/var/tmp/Apache-Gallery" ]; then
	echo "Removing old cache /var/tmp/Apache-Gallery. New location: %{_cachedir}"
	rm -rf /var/tmp/Apache-Gallery
fi

%preun
if [ "$1" = "0" ]; then
	%service -q httpd reload
fi

%files
%defattr(644,root,root,755)
%doc Changes INSTALL README TODO UPGRADE
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) /etc/httpd/httpd.conf/*%{name}.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/tmpwatch/%{name}.conf
%{perl_vendorlib}/Apache/Gallery.pm
%dir %{_appdir}
%dir %{_appdir}/templates
%dir %{_appdir}/templates/new
%{_appdir}/templates/new/*.tpl
%{_appdir}/templates/new/*.css
%dir %{_appdir}/templates/default
%{_appdir}/templates/default/*.tpl
%{_appdir}/templates/default/*.css
%dir %{_apacheicons}
%{_apacheicons}/*.png
%attr(770,root,http) %dir %{_cachedir}
%{_mandir}/man3/*.3*
