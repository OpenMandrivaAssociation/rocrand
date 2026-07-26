# HIP random number generation library (TheRock 7.14)

Name:		rocrand
Version:	7.14.0
Release:	1
Summary:	HIP random number generation library
License:	MIT AND BSD-3-Clause
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-7.14/rocrand.tar.gz#/rocrand-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}

ExclusiveArch:	%{x86_64} %{aarch64}

%description
rocRAND host/device RNGs for HIP. Built for %%%{rocm_gpu_targets} including gfx803 on OM.

%package devel
Summary:	Development files for rocrand
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel

Provides:	rocrand-devel = %{EVRD}

%description devel
Headers and CMake package for rocrand.

%prep
%autosetup -n rocrand

export CXX=hipcc
export CC=clang
export ROCM_PATH=%{_prefix}
export HIP_PATH=%{_prefix}
# Strip host-only flags (hipcc forwards CXXFLAGS to the amdgcn device triple)
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
export LDFLAGS=$(printf '%s' "%{?__global_ldflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_TEST=OFF \
	-DBUILD_BENCHMARK=OFF \
	-DBUILD_EXAMPLE=OFF \
	-DBUILD_DOCS=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/rocrand ] && [ ! -d %{buildroot}%{_libdir}/cmake/rocrand ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/rocrand %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/rocrand/LICENSE.md
%{_libdir}/librocrand.so.*

%files devel
%{_includedir}/rocrand/
%{_libdir}/librocrand.so
%{_libdir}/cmake/rocrand/
