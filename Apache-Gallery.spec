# TODO:
# - prepare subpackage with virtual
# - configuration for apache
#
%include	/usr/lib/rpm/macros.perl
%define 	apxs		/usr/sbin/apxs
Summary:	An Apache module for creating an online gallery
Name:		Apache-Gallery
Version:	0.8
Release:	0.1
License:	Artistic
Group:		Applications/Graphics
Source0:	http://apachegallery.dk/download/%{name}-%{version}.tar.gz
# Source0-md5:	21ec1b8b11240dc6e3dbba19c6330120
#Source1:	%{name}.conf
URL:		http://apachegallery.dk/
BuildRequires:	perl-Image-Imlib2 >= 1.00
BuildRequires:	perl-Image-Info
BuildRequires:	perl-Image-Size
BuildRequires:	perl-Text-Template
BuildRequires:	perl-devel
BuildRequires:	rpm-perlprov >= 3.0.3-16
Requires:	apache-mod_perl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache::Gallery is a mod_perl handler that sits on top of your
DocumentRoot and creates an image gallery of the files and directories
there. It creates an thumbnail index of each directory and allows
viewing of pictures in different resolutions. Pictures are resized on
the fly and cached.

%prep
%setup -q

%build
%{__perl} Makefile.PL
%{__make}
#%{__make} test

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%{_mandir}/man3/*.3*
