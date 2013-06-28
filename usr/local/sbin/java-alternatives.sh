#!/bin/sh

priority=2000
release=1.7.0_11
umask 0022

update-alternatives --install /usr/bin/java java /opt/oracle/jdk${release}/bin/java $priority \
    --slave /usr/bin/appletviewer appletviewer /opt/oracle/jdk${release}/bin/appletviewer \
    --slave /usr/bin/apt apt /opt/oracle/jdk${release}/bin/apt \
    --slave /usr/bin/ControlPanel ControlPanel /opt/oracle/jdk${release}/bin/ControlPanel \
    --slave /usr/bin/extcheck extcheck /opt/oracle/jdk${release}/bin/extcheck \
    --slave /usr/bin/idlj idlj /opt/oracle/jdk${release}/bin/idlj \
    --slave /usr/bin/jar jar /opt/oracle/jdk${release}/bin/jar \
    --slave /usr/bin/jarsigner jarsigner /opt/oracle/jdk${release}/bin/jarsigner \
    --slave /usr/bin/javac javac /opt/oracle/jdk${release}/bin/javac \
    --slave /usr/bin/javadoc javadoc /opt/oracle/jdk${release}/bin/javadoc \
    --slave /usr/bin/javafxpackager javafxpackager /opt/oracle/jdk${release}/bin/javafxpackager \
    --slave /usr/bin/javah javah /opt/oracle/jdk${release}/bin/javah \
    --slave /usr/bin/javap javap /opt/oracle/jdk${release}/bin/javap \
    --slave /usr/bin/java-rmi.cgi java-rmi.cgi /opt/oracle/jdk${release}/bin/java-rmi.cgi \
    --slave /usr/bin/javaws javaws /opt/oracle/jdk${release}/bin/javaws \
    --slave /usr/bin/jcmd jcmd /opt/oracle/jdk${release}/bin/jcmd \
    --slave /usr/bin/jconsole jconsole /opt/oracle/jdk${release}/bin/jconsole \
    --slave /usr/bin/jcontrol jcontrol /opt/oracle/jdk${release}/bin/jcontrol \
    --slave /usr/bin/jdb jdb /opt/oracle/jdk${release}/bin/jdb \
    --slave /usr/bin/jhat jhat /opt/oracle/jdk${release}/bin/jhat \
    --slave /usr/bin/jinfo jinfo /opt/oracle/jdk${release}/bin/jinfo \
    --slave /usr/bin/jmap jmap /opt/oracle/jdk${release}/bin/jmap \
    --slave /usr/bin/jps jps /opt/oracle/jdk${release}/bin/jps \
    --slave /usr/bin/jrunscript jrunscript /opt/oracle/jdk${release}/bin/jrunscript \
    --slave /usr/bin/jsadebugd jsadebugd /opt/oracle/jdk${release}/bin/jsadebugd \
    --slave /usr/bin/jstack jstack /opt/oracle/jdk${release}/bin/jstack \
    --slave /usr/bin/jstat jstat /opt/oracle/jdk${release}/bin/jstat \
    --slave /usr/bin/jstatd jstatd /opt/oracle/jdk${release}/bin/jstatd \
    --slave /usr/bin/jvisualvm jvisualvm /opt/oracle/jdk${release}/bin/jvisualvm \
    --slave /usr/bin/native2ascii native2ascii /opt/oracle/jdk${release}/bin/native2ascii \
    --slave /usr/bin/policytool policytool /opt/oracle/jdk${release}/bin/policytool \
    --slave /usr/bin/rmic rmic /opt/oracle/jdk${release}/bin/rmic \
    --slave /usr/bin/schemagen schemagen /opt/oracle/jdk${release}/bin/schemagen \
    --slave /usr/bin/serialver serialver /opt/oracle/jdk${release}/bin/serialver \
    --slave /usr/bin/wsgen wsgen /opt/oracle/jdk${release}/bin/wsgen \
    --slave /usr/bin/wsimport wsimport /opt/oracle/jdk${release}/bin/wsimport \
    --slave /usr/bin/xjc xjc /opt/oracle/jdk${release}/bin/xjc

for exe in keytool orbd pack200 rmid rmiregistry servertool unpack200 tnameserv; do
    update-alternatives --install /usr/bin/${exe} ${exe} /opt/oracle/jdk${release}/bin/${exe} $priority
done
