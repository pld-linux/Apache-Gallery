# TODO:
# - prepare subpackage with virtual
# - configuration for apache
# - switch to vendordirs and apache 2.x or apache1 (depending on which mod_perl is supported)
#
%include	/usr/lib/rpm/macros.perl
%define 	apxs		/usr/sbin/apxs
Summary:	An Apache module for creating an online gallery
Summary(pl):	Modu³ Apache'a do tworzenia galerii online
Name:		Apache-Gallery
Version:	0.8
Release:	0.6
License:	Artistic
Group:		Applications/Graphics
Source0:	http://apachegallery.dk/download/%{name}-%{version}.tar.gz
# Source0-md5:	21ec1b8b11240dc6e3dbba19c6330120
#Source1:	%{name}.conf
URL:		http://apachegallery.dk/
BuildRequires:	apache-mod_perl
BuildRequires:	perl-Image-Imlib2 >= 1.00
BuildRequires:	perl-Image-Info
BuildRequires:	perl-Image-Size
BuildRequires:	perl-Text-Template
BuildRequires:	perl-devel
BuildRequires:	perl-libapreq
BuildRequires:	rpm-perlprov >= 3.0.3-16
Requires:	apache-mod_perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(APR::Table)' 'perl(Apache2)' 'perl(Apache::Const)' 'perl(Apache::RequestIO)' 'perl(Apache::RequestRec)' 'perl(Apache::SubRequest)'
%define		_apacheicons	/home/httpd/icons/gallery

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
%setup -q

%build
%{__perl} Makefile.PL
%{__make}
%{__make} test

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name}/templates/{new,default},%{_apacheicons}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install templates/new/*.{css,tpl} $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/new/
install templates/default/*.{css,tpl} $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/default/
install htdocs/*.png $RPM_BUILD_ROOT%{_apacheicons}

%clean
rm -rf $RPM_BUILD_ROOT

#%post
#if [ -f /var/lock/subsys/httpd ]; then
#	/etc/rc.d/init.d/httpd restart 1>&2
#else
#	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
#fi

#%preun
#if [ "$1" = "0" ]; then
#	if [ -f /var/lock/subsys/httpd ]; then
#		/etc/rc.d/init.d/httpd restart 1>&2
#	fi
#fi

%files
%defattr(644,root,root,755)
%doc Changes INSTALL README TODO UPGRADE
%{perl_sitelib}/Apache/Gallery.pm
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/templates
%dir %{_datadir}/%{name}/templates/new
%{_datadir}/%{name}/templates/new/*.tpl
%{_datadir}/%{name}/templates/new/*.css
%dir %{_datadir}/%{name}/templates/default
%{_datadir}/%{name}/templates/default/*.tpl
%{_datadir}/%{name}/templates/default/*.css
%{_apacheicons}/*.png
%{_mandir}/man3/*.3*
