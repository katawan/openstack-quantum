#
# This is 2012.2.1 folsom stable
#

Name:		openstack-quantum
Version:	2012.2.1
Release:	1%{?dist}
Summary:	Virtual network service for OpenStack (quantum)

Group:		Applications/System
License:	ASL 2.0
URL:		http://launchpad.net/quantum/

Source0:	https://launchpad.net/quantum/folsom/%{version}/+download/quantum-%{version}.tar.gz
Source1:	quantum.logrotate
Source2:	quantum-sudoers
Source4:	quantum-server-setup
Source5:	quantum-node-setup
Source6:	quantum-dhcp-setup
Source7:	quantum-l3-setup

Source10:	quantum-server.init
Source20:	quantum-server.upstart
Source11:	quantum-linuxbridge-agent.init
Source21:	quantum-linuxbridge-agent.upstart
Source12:	quantum-openvswitch-agent.init
Source22:	quantum-openvswitch-agent.upstart
Source13:	quantum-ryu-agent.init
Source23:	quantum-ryu-agent.upstart
Source14:	quantum-nec-agent.init
Source24:	quantum-nec-agent.upstart
Source15:	quantum-dhcp-agent.init
Source25:	quantum-dhcp-agent.upstart
Source16:	quantum-l3-agent.init
Source26:	quantum-l3-agent.upstart

# This is EPEL specific and not upstream
Patch100:         openstack-quantum-newdeps.patch

#
# patches_base=2012.2.1
#

# Upstream stable branch patch https://review.openstack.org/17236
Patch1:		quantum.git-8017d0932c54078e7e18058e78f12c76d68462c7.patch

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-setuptools
# Build require these parallel versions
# as setup.py build imports quantum.openstack.common.setup
# which will then check for these
BuildRequires:	python-sqlalchemy0.7
BuildRequires:	python-webob1.0
BuildRequires:	python-paste-deploy1.5
BuildRequires:	python-routes1.12
BuildRequires:	dos2unix

Requires:	python-quantum = %{version}-%{release}
Requires:	openstack-utils
Requires:       python-keystone

Requires(post):   chkconfig
Requires(postun): initscripts
Requires(preun):  chkconfig
Requires(preun):  initscripts
Requires(pre):    shadow-utils


%description
Quantum is a virtual network service for Openstack. Just like
OpenStack Nova provides an API to dynamically request and configure
virtual servers, Quantum provides an API to dynamically request and
configure virtual networks. These networks connect "interfaces" from
other OpenStack services (e.g., virtual NICs from Nova VMs). The
Quantum API supports extensions to provide advanced network
capabilities (e.g., QoS, ACLs, network monitoring, etc.)


%package -n python-quantum
Summary:	Quantum Python libraries
Group:		Applications/System

Requires:	MySQL-python
Requires:	python-amqplib
Requires:	python-anyjson
Requires:	python-eventlet
Requires:	python-greenlet
Requires:	python-httplib2
Requires:	python-iso8601
Requires:	python-kombu
Requires:	python-lxml
Requires:	python-paste-deploy1.5
Requires:	python-routes1.12
Requires:	python-sqlalchemy0.7
Requires:	python-webob1.0
Requires:	python-netaddr
Requires:	python-qpid
Requires:	python-quantumclient >= 1:2.1.1
Requires:	sudo

%description -n python-quantum
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum Python library.


%package -n openstack-quantum-cisco
Summary:	Quantum Cisco plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}
Requires:	python-configobj


%description -n openstack-quantum-cisco
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using Cisco UCS and Nexus.


%package -n openstack-quantum-linuxbridge
Summary:	Quantum linuxbridge plugin
Group:		Applications/System

Requires:	bridge-utils
Requires:	openstack-quantum = %{version}-%{release}
Requires:	python-pyudev


%description -n openstack-quantum-linuxbridge
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks as VLANs using Linux bridging.


%package -n openstack-quantum-nicira
Summary:	Quantum Nicira plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-nicira
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using Nicira NVP.


%package -n openstack-quantum-openvswitch
Summary:	Quantum openvswitch plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}
Requires:	openvswitch


%description -n openstack-quantum-openvswitch
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using Open vSwitch.


%package -n openstack-quantum-ryu
Summary:	Quantum Ryu plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-ryu
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using the Ryu Network Operating System.


%package -n openstack-quantum-nec
Summary:	Quantum NEC plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-nec
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using the NEC OpenFlow controller.


%package -n openstack-quantum-metaplugin
Summary:	Quantum meta plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-metaplugin
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using multiple other quantum plugins.


%prep
%setup -q -n quantum-%{version}

%patch1 -p1
# Apply EPEL patch
%patch100 -p1

find quantum -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;

chmod 644 quantum/plugins/cisco/README

# Adjust configuration file content
sed -i 's/debug = True/debug = False/' etc/quantum.conf
sed -i 's/\# auth_strategy = keystone/auth_strategy = noauth/' etc/quantum.conf

# Remove unneeded dependency
sed -i '/setuptools_git/d' setup.py


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python_sitelib}/bin
rm -rf %{buildroot}%{python_sitelib}/doc
rm -rf %{buildroot}%{python_sitelib}/tools
rm -rf %{buildroot}%{python_sitelib}/quantum/tests
rm -rf %{buildroot}%{python_sitelib}/quantum/plugins/*/tests
rm -f %{buildroot}%{python_sitelib}/quantum/plugins/*/run_tests.*
rm %{buildroot}/usr/etc/init.d/quantum-server

# Install execs (using hand-coded rather than generated versions)
install -p -D -m 755 bin/quantum-debug %{buildroot}%{_bindir}/quantum-debug
install -p -D -m 755 bin/quantum-dhcp-agent %{buildroot}%{_bindir}/quantum-dhcp-agent
install -p -D -m 755 bin/quantum-dhcp-agent-dnsmasq-lease-update %{buildroot}%{_bindir}/quantum-dhcp-agent-dnsmasq-lease-update
install -p -D -m 755 bin/quantum-l3-agent %{buildroot}%{_bindir}/quantum-l3-agent
install -p -D -m 755 bin/quantum-linuxbridge-agent %{buildroot}%{_bindir}/quantum-linuxbridge-agent
install -p -D -m 755 bin/quantum-nec-agent %{buildroot}%{_bindir}/quantum-nec-agent
install -p -D -m 755 bin/quantum-netns-cleanup %{buildroot}%{_bindir}/quantum-netns-cleanup
install -p -D -m 755 bin/quantum-openvswitch-agent %{buildroot}%{_bindir}/quantum-openvswitch-agent
install -p -D -m 755 bin/quantum-rootwrap %{buildroot}%{_bindir}/quantum-rootwrap
install -p -D -m 755 bin/quantum-ryu-agent %{buildroot}%{_bindir}/quantum-ryu-agent
install -p -D -m 755 bin/quantum-server %{buildroot}%{_bindir}/quantum-server

# Move rootwrap files to proper location
install -d -m 755 %{buildroot}%{_datarootdir}/quantum/rootwrap
mv %{buildroot}/usr/etc/quantum/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/quantum/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/quantum
mv %{buildroot}/usr/etc/quantum/* %{buildroot}%{_sysconfdir}/quantum
chmod 640  %{buildroot}%{_sysconfdir}/quantum/plugins/*/*.ini

# Configure agents to use quantum-rootwrap
for f in %{buildroot}%{_sysconfdir}/quantum/plugins/*/*.ini %{buildroot}%{_sysconfdir}/quantum/*_agent.ini; do
    sed -i 's/^root_helper.*/root_helper = sudo quantum-rootwrap \/etc\/quantum\/rootwrap.conf/g' $f
done

# Configure quantum-dhcp-agent state_path
sed -i 's/state_path = \/opt\/stack\/data/state_path = \/var\/lib\/quantum/' %{buildroot}%{_sysconfdir}/quantum/dhcp_agent.ini

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-quantum

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/quantum

# Install sysv init scripts
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/quantum-server
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/quantum-linuxbridge-agent
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/quantum-openvswitch-agent
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/quantum-ryu-agent
install -p -D -m 755 %{SOURCE14} %{buildroot}%{_initrddir}/quantum-nec-agent
install -p -D -m 755 %{SOURCE15} %{buildroot}%{_initrddir}/quantum-dhcp-agent
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/quantum-l3-agent

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/quantum
install -d -m 755 %{buildroot}%{_sharedstatedir}/quantum
install -d -m 755 %{buildroot}%{_localstatedir}/log/quantum
install -d -m 755 %{buildroot}%{_localstatedir}/run/quantum

# Install setup helper scripts
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_bindir}/quantum-server-setup
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/quantum-node-setup
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_bindir}/quantum-dhcp-setup
install -p -D -m 755 %{SOURCE7} %{buildroot}%{_bindir}/quantum-l3-setup

# Install upstart jobs examples
install -p -m 644 %{SOURCE20} %{buildroot}%{_datadir}/quantum/
install -p -m 644 %{SOURCE21} %{buildroot}%{_datadir}/quantum/
install -p -m 644 %{SOURCE22} %{buildroot}%{_datadir}/quantum/
install -p -m 644 %{SOURCE23} %{buildroot}%{_datadir}/quantum/
install -p -m 644 %{SOURCE24} %{buildroot}%{_datadir}/quantum/
install -p -m 644 %{SOURCE25} %{buildroot}%{_datadir}/quantum/
install -p -m 644 %{SOURCE26} %{buildroot}%{_datadir}/quantum/

%pre
getent group quantum >/dev/null || groupadd -r quantum --gid 164
getent passwd quantum >/dev/null || \
    useradd --uid 164 -r -g quantum -d %{_sharedstatedir}/quantum -s /sbin/nologin \
    -c "OpenStack Quantum Daemons" quantum
exit 0


%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add quantum-server
fi

%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service quantum-server stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-server
    /sbin/service quantum-dhcp-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-dhcp-agent
    /sbin/service quantum-l3-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-l3-agent
fi

%postun
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service quantum-server condrestart >/dev/null 2>&1 || :
fi


%post -n openstack-quantum-linuxbridge
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add quantum-linuxbridge-agent
fi

%preun -n openstack-quantum-linuxbridge
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service quantum-linuxbridge-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-linuxbridge-agent
fi

%postun -n openstack-quantum-linuxbridge
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service quantum-linuxbridge-agent condrestart >/dev/null 2>&1 || :
fi


%post -n openstack-quantum-openvswitch
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add quantum-openvswitch-agent
fi

%preun -n openstack-quantum-openvswitch
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service quantum-openvswitch-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-openvswitch-agent
fi

%postun -n openstack-quantum-openvswitch
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service quantum-openvswitch-agent condrestart >/dev/null 2>&1 || :
fi


%post -n openstack-quantum-ryu
if [ $1 -eq 1 ] ; then
    # Initial installation
    /sbin/chkconfig --add quantum-ryu-agent
fi

%preun -n openstack-quantum-ryu
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service quantum-ryu-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-ryu-agent
fi

%postun -n openstack-quantum-ryu
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service quantum-ryu-agent condrestart >/dev/null 2>&1 || :
fi


%preun -n openstack-quantum-nec
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /sbin/service quantum-nec-agent stop >/dev/null 2>&1
    /sbin/chkconfig --del quantum-nec-agent
fi


%postun -n openstack-quantum-nec
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /sbin/service quantum-nec-agent condrestart >/dev/null 2>&1 || :
fi


%files
%doc LICENSE
%doc README
%{_bindir}/quantum-debug
%{_bindir}/quantum-dhcp-agent
%{_bindir}/quantum-dhcp-agent-dnsmasq-lease-update
%{_bindir}/quantum-dhcp-setup
%{_bindir}/quantum-l3-agent
%{_bindir}/quantum-l3-setup
%{_bindir}/quantum-netns-cleanup
%{_bindir}/quantum-node-setup
%{_bindir}/quantum-rootwrap
%{_bindir}/quantum-server
%{_bindir}/quantum-server-setup
%{_initrddir}/quantum-server
%{_initrddir}/quantum-dhcp-agent
%{_initrddir}/quantum-l3-agent
%dir %{_datadir}/quantum
%{_datadir}/quantum/quantum-server.upstart
%{_datadir}/quantum/quantum-dhcp-agent.upstart
%{_datadir}/quantum/quantum-l3-agent.upstart
%dir %{_sysconfdir}/quantum
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/api-paste.ini
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/dhcp_agent.ini
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/l3_agent.ini
%config(noreplace) %{_sysconfdir}/quantum/policy.json
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/quantum.conf
%config(noreplace) %{_sysconfdir}/quantum/rootwrap.conf
%dir %{_sysconfdir}/quantum/plugins
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config(noreplace) %{_sysconfdir}/sudoers.d/quantum
%dir %attr(0755, quantum, quantum) %{_sharedstatedir}/quantum
%dir %attr(0755, quantum, quantum) %{_localstatedir}/log/quantum
%dir %attr(0755, quantum, quantum) %{_localstatedir}/run/quantum
%dir %{_datarootdir}/quantum/rootwrap
%{_datarootdir}/quantum/rootwrap/dhcp.filters
%{_datarootdir}/quantum/rootwrap/iptables-firewall.filters
%{_datarootdir}/quantum/rootwrap/l3.filters


%files -n python-quantum
%doc LICENSE
%doc README
%{python_sitelib}/quantum
%exclude %{python_sitelib}/quantum/extensions/_credential_view.py*
%exclude %{python_sitelib}/quantum/extensions/portprofile.py*
%exclude %{python_sitelib}/quantum/extensions/novatenant.py*
%exclude %{python_sitelib}/quantum/extensions/credential.py*
%exclude %{python_sitelib}/quantum/extensions/_novatenant_view.py*
%exclude %{python_sitelib}/quantum/extensions/multiport.py*
%exclude %{python_sitelib}/quantum/extensions/_pprofiles.py*
%exclude %{python_sitelib}/quantum/extensions/qos.py*
%exclude %{python_sitelib}/quantum/extensions/_qos_view.py*
%exclude %{python_sitelib}/quantum/plugins/cisco
%exclude %{python_sitelib}/quantum/plugins/linuxbridge
%exclude %{python_sitelib}/quantum/plugins/metaplugin
%exclude %{python_sitelib}/quantum/plugins/nec
%exclude %{python_sitelib}/quantum/plugins/nicira
%exclude %{python_sitelib}/quantum/plugins/openvswitch
%exclude %{python_sitelib}/quantum/plugins/ryu
%{python_sitelib}/quantum-%%{version}-*.egg-info


%files -n openstack-quantum-cisco
%doc LICENSE
%doc quantum/plugins/cisco/README
%{python_sitelib}/quantum/extensions/_credential_view.py*
%{python_sitelib}/quantum/extensions/portprofile.py*
%{python_sitelib}/quantum/extensions/novatenant.py*
%{python_sitelib}/quantum/extensions/credential.py*
%{python_sitelib}/quantum/extensions/_novatenant_view.py*
%{python_sitelib}/quantum/extensions/multiport.py*
%{python_sitelib}/quantum/extensions/_pprofiles.py*
%{python_sitelib}/quantum/extensions/qos.py*
%{python_sitelib}/quantum/extensions/_qos_view.py*
%{python_sitelib}/quantum/plugins/cisco
%dir %{_sysconfdir}/quantum/plugins/cisco
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/cisco/*.ini


%files -n openstack-quantum-linuxbridge
%doc LICENSE
%doc quantum/plugins/linuxbridge/README
%{_bindir}/quantum-linuxbridge-agent
%{_initrddir}/quantum-linuxbridge-agent
%{_datadir}/quantum/quantum-linuxbridge-agent.upstart
%{python_sitelib}/quantum/plugins/linuxbridge
%{_datarootdir}/quantum/rootwrap/linuxbridge-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/linuxbridge
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/linuxbridge/*.ini


%files -n openstack-quantum-nicira
%doc LICENSE
%doc quantum/plugins/nicira/nicira_nvp_plugin/README
%{python_sitelib}/quantum/plugins/nicira
%dir %{_sysconfdir}/quantum/plugins/nicira
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/nicira/*.ini


%files -n openstack-quantum-openvswitch
%doc LICENSE
%doc quantum/plugins/openvswitch/README
%{_bindir}/quantum-openvswitch-agent
%{_initrddir}/quantum-openvswitch-agent
%{_datadir}/quantum/quantum-openvswitch-agent.upstart
%{python_sitelib}/quantum/plugins/openvswitch
%{_datarootdir}/quantum/rootwrap/openvswitch-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/openvswitch
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/openvswitch/*.ini


%files -n openstack-quantum-ryu
%doc LICENSE
%doc quantum/plugins/ryu/README
%{_bindir}/quantum-ryu-agent
%{_initrddir}/quantum-ryu-agent
%{_datadir}/quantum/quantum-ryu-agent.upstart
%{python_sitelib}/quantum/plugins/ryu
%{_datarootdir}/quantum/rootwrap/ryu-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/ryu
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/ryu/*.ini


%files -n openstack-quantum-nec
%doc LICENSE
%doc quantum/plugins/nec/README
%{_bindir}/quantum-nec-agent
%{_initrddir}/quantum-nec-agent
%{_datadir}/quantum/quantum-nec-agent.upstart
%{python_sitelib}/quantum/plugins/nec
%{_datarootdir}/quantum/rootwrap/nec-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/nec
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/nec/*.ini


%files -n openstack-quantum-metaplugin
%doc LICENSE
%doc quantum/plugins/metaplugin/README
%{python_sitelib}/quantum/plugins/metaplugin
%dir %{_sysconfdir}/quantum/plugins/metaplugin
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/metaplugin/*.ini


%changelog
* Wed Jan 23 2013 Martin Magr <mmagr@redhat.com> - 2012.2.1-1
- Added python-keystone requirement

* Mon Dec  3 2012 Robert Kukura <rkukura@redhat.com> - 2012.2.1-1
- Update to folsom stable 2012.2.1
- Add upstream patch: Fix rpc control_exchange regression.
- Remove workaround for missing l3_agent.ini

* Thu Nov 01 2012 Alan Pevec <apevec@redhat.com> 2012.2-2
- l3_agent not disabling namespace use lp#1060559

* Fri Sep 28 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-1
- Update to folsom final
- Require python-quantumclient >= 1:2.1.1

* Tue Aug 21 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-8
- fix database config generated by install scripts (#847785)

* Wed Jul 25 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-6
- Update to 20120715 essex stable branch snapshot

* Mon May 28 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-5
- Fix helper scripts to use the always available openstack-config util

* Mon May 07 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-4
- Fix handling of the mysql service in quantum-server-setup

* Tue May 01 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-3
- Start the services later in the boot sequence

* Wed Apr 25 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- Use parallel installed versions of python-routes and python-paste-deploy

* Thu Apr 12 2012 Pádraig Brady <pbrady@redhat.com> - 2012.1-1
- Initial essex release
