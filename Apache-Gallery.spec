# TODO:
# - prepare subpackage with virtual
# - configuration for apache
#
%bcond_with	tests	# Build with tests

%include	/usr/lib/rpm/macros.perl
%define 	apxs		/usr/sbin/apxs
Summary:	An Apache module for creating an online gallery
Summary(pl):	Modu� Apache'a do tworzenia galerii online
Name:		Apache-Gallery
Version:	0.9.1
Release:	1
License:	Artistic
Group:		Applications/Graphics
Source0:	http://apachegallery.dk/download/%{name}-%{version}.tar.gz
# Source0-md5:	882e650e6fc3f059e84eca1564b5f32f
#Source1:	%{name}.conf
Patch0:		%{name}-apache2.patch
URL:		http://apachegallery.dk/
BuildRequires:	apache-mod_perl >= 1.99
%{?with_tests:BuildRequires:	apache1-mod_perl}
BuildRequires:	perl-CGI >= 2.93
BuildRequires:	perl-Image-Imlib2 >= 1.02
BuildRequires:	perl-Image-Info
BuildRequires:	perl-Image-Size
BuildRequires:	perl-Text-Template
BuildRequires:	perl-URI >= 1.23
BuildRequires:	perl-devel
BuildRequires:	perl-libapreq2
BuildRequires:	rpm-perlprov >= 3.0.3-16
Requires:	apache-mod_perl
Conflicts:	apache-mod_autoindex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq	'perl(APR::Table)' 'perl(Apache2)' 'perl(Apache::Const)' 'perl(Apache::RequestIO)' 'perl(Apache::RequestRec)' 'perl(Apache::SubRequest)'
%define		_apacheicons	/home/services/httpd/icons/gallery

%description
Apache::Gallery is a mod_perl handler that sits on top of your
DocumentRoot and creates an image gallery of the files and directories
there. It creates an thumbnail index of each directory and allows
viewing of pictures in different resolutions. Pictures are resized on
the fly and cached.

%description -l pl
Apache::Gallery to procedura obs�ugi dla modu�u mod_perl po�o�ona w
DocumentRoot, tworz�ca galeri� obraz�w z umieszczonych tam plik�w i
katalog�w. Tworzy indeks z miniaturkami z ka�dego katalogu i pozwala
na ogl�danie obrazk�w w r�nych rozdzielczo�ciach. Obrazki s�
przeskalowywane w locie i buforowane.

%prep
%setup -q
%patch0 -p1

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor

%{__make} \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

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
%{perl_vendorlib}/Apache/Gallery.pm
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/templates
%dir %{_datadir}/%{name}/templates/new
%{_datadir}/%{name}/templates/new/*.tpl
%{_datadir}/%{name}/templates/new/*.css
%dir %{_datadir}/%{name}/templates/default
%{_datadir}/%{name}/templates/default/*.tpl
%{_datadir}/%{name}/templates/default/*.css
%dir %{_apacheicons}
%{_apacheicons}/*.png
%{_mandir}/man3/*.3*