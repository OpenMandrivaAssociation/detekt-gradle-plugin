Name:		detekt-gradle-plugin
Version:	2.0.0.alpha.4
Release:	1
Summary:	Detekt Gradle plugin
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/detekt/detekt
# detekt tag v2.0.0-alpha.4 (60300b2d43c98eea77d36ea5d341d234d9ba4557).
# Only the detekt-gradle-plugin module. The catalog coordinate is the
# marker dev.detekt:dev.detekt.gradle.plugin. Classes are detekt-gradle-plugin.
# Maven version stays 2.0.0-alpha.4. The RPM version has no hyphen.
# BuildConfig is generated in build.sh. Sarif4k is not shaded.
# The Gradle 8.13 TestSuite overlay is compile-only and is not installed.
# com.android.tools.build:gradle, the Android plugin, is not bundled.
Source0:	detekt-gradle-plugin-%{version}.tar.gz
Provides:	mvn(dev.detekt:dev.detekt.gradle.plugin) = 2.0.0-alpha.4

BuildArch:	noarch
BuildRequires:	java-21-openjdk-devel
BuildRequires:	kotlin = 2.0.21
BuildRequires:	kotlin-libs = 2.0.21
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
BuildRequires:	gradle = 8.11.1
BuildRequires:	mvn(com.google.guava:guava) = 33.6.0-jre
BuildRequires:	mvn(org.ow2.asm:asm) = 9.11.1
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-gradle-plugin-api) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-tooling-core) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlinx:kotlinx-serialization-core) = 1.11.0
BuildRequires:	mvn(org.jetbrains.kotlinx:kotlinx-serialization-json) = 1.11.0
BuildRequires:	mvn(io.github.detekt.sarif4k:sarif4k) = 0.6.0
BuildRequires:	mvn(com.android.tools:annotations) = 32.0.0
BuildRequires:	mvn(com.android.tools.build:builder-model) = 9.0.0
BuildRequires:	mvn(com.android.tools.build:gradle-api) = 9.0.0

%description
dev.detekt:detekt-gradle-plugin 2.0.0-alpha.4, compiled from the plugin
module of detekt v2.0.0-alpha.4. The Gradle catalog coordinate is the
marker dev.detekt:dev.detekt.gradle.plugin at the same version. The
plugin properties name DetektPlugin, DetektBasePlugin, and
DetektKotlinCompilerPlugin. io.github.detekt.sarif4k:sarif4k is a
separate package. The Android Gradle Plugin is not included.

%prep
%autosetup -n detekt-gradle-plugin-%{version}
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s overlay/org/gradle/testing/base/TestSuite.java
test -s check/Check.java
test -s check/a.xml
test -s check/b.xml

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash build.sh
test -s detekt-gradle-plugin.jar
cat > detekt-gradle-plugin.pom << END
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>dev.detekt</groupId>
  <artifactId>detekt-gradle-plugin</artifactId>
  <version>2.0.0-alpha.4</version>
  <name>detekt-gradle-plugin</name>
  <description>Detekt Gradle plugin 2.0.0-alpha.4</description>
  <url>https://github.com/detekt/detekt</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>io.github.detekt.sarif4k</groupId>
      <artifactId>sarif4k</artifactId>
      <version>0.6.0</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-stdlib</artifactId>
      <version>2.0.21</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlinx</groupId>
      <artifactId>kotlinx-serialization-core</artifactId>
      <version>1.11.0</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlinx</groupId>
      <artifactId>kotlinx-serialization-json</artifactId>
      <version>1.11.0</version>
    </dependency>
  </dependencies>
</project>
END
cat > marker.pom << END
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>dev.detekt</groupId>
  <artifactId>dev.detekt.gradle.plugin</artifactId>
  <version>2.0.0-alpha.4</version>
  <packaging>pom</packaging>
  <name>dev.detekt.gradle.plugin</name>
  <description>Marker for the Detekt Gradle plugin</description>
  <url>https://github.com/detekt/detekt</url>
  <dependencies>
    <dependency>
      <groupId>dev.detekt</groupId>
      <artifactId>detekt-gradle-plugin</artifactId>
      <version>2.0.0-alpha.4</version>
    </dependency>
  </dependencies>
</project>
END

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact detekt-gradle-plugin.pom:detekt-gradle-plugin.jar \
	--file-name detekt-gradle-plugin \
	--filelist .mfiles-jar
sysjar install --buildroot %{buildroot} \
	--artifact marker.pom \
	--file-name dev.detekt.gradle.plugin \
	--filelist .mfiles-marker
awk '!seen[$0]++' .mfiles-jar .mfiles-marker > .mfiles
dirs=$(grep -c -F -x '%%dir /usr/share/sysjar/index/dev.detekt' .mfiles || true)
test "$dirs" = 1
impl="%{buildroot}/usr/share/sysjar/index/dev.detekt/detekt-gradle-plugin.sysjar"
marker="%{buildroot}/usr/share/sysjar/index/dev.detekt/dev.detekt.gradle.plugin@pom.sysjar"
test -s "$impl"
test -s "$marker"
grep -F -q '"version": "2.0.0-alpha.4"' "$impl"
grep -F -q '"artifactId": "detekt-gradle-plugin"' "$impl"
grep -F -q '"version": "2.0.0-alpha.4"' "$marker"
grep -F -q '"artifactId": "dev.detekt.gradle.plugin"' "$marker"
test -s %{buildroot}%{_javadir}/detekt-gradle-plugin.jar
jar tf %{buildroot}%{_javadir}/detekt-gradle-plugin.jar > installed-plugin.list
grep -F -qx 'META-INF/gradle-plugins/dev.detekt.properties' installed-plugin.list
if grep -F -q 'org/gradle/testing/base/TestSuite.class' installed-plugin.list; then
	exit 1
fi

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
JAR=%{buildroot}%{_javadir}/detekt-gradle-plugin.jar
STDLIB=%{_javadir}/kotlin-stdlib.jar
SARIF=%{_javadir}/sarif4k.jar
CORE=%{_javadir}/kotlinx-serialization-core.jar
JSON=%{_javadir}/kotlinx-serialization-json.jar
test -s "$JAR"
test -s "$STDLIB"
test -s "$SARIF"
test -s "$CORE"
test -s "$JSON"
mkdir -p check/out
javac --release 8 -encoding UTF-8 -proc:none -Xlint:-options \
	-cp "$JAR:$STDLIB:$SARIF:$JSON:$CORE" \
	-d check/out check/Check.java
java -cp "check/out:$JAR:$STDLIB:$SARIF:$JSON:$CORE" Check check/out.xml check/a.xml check/b.xml > check/out.txt
cat check/out.txt
grep -F -qx 'detekt_plugin_ok 2.4.0' check/out.txt

%files -f .mfiles
%license LICENSE
