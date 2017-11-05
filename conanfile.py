import os
from conans import ConanFile, CMake
from conans.tools import download, check_sha256, unzip, os_info


class HowardHinnantDate(ConanFile):
    name = 'date'
    version = '2.3.0'
    description = 'A date and time library based on the C++11/14/17 <chrono> header'
    url = 'https://github.com/jjones646/conan-date'
    license = 'https://github.com/jjones646/date/blob/{!s}-conan/LICENSE.txt'.format(version)
    settings = 'os', 'compiler', 'arch', 'build_type'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    exports_sources = 'CMakeLists.txt'
    generators = 'cmake'

    @property
    def _archive_dirname(self):
        return 'date-{!s}-conan'.format(self.version)

    def _os_supports_zoneinfo(self):
        # We assume that Windows is the only system that does not support
        # managing updates to a central IANA timezone datebase natively.
        return not os_info.is_windows

    def build_requirements(self):
        if os_info.is_windows:
            self.build_requires('curl/[~=7]@jjones646/stable')

    def source(self):
        import distutils
        distutils.dir_util.copy_tree('/home/jonathan/Documents/date/', '/home/jonathan/.conan/data/date/2.3.0/jjones646/testing/source/date/')
        return
        download_url = 'https://github.com/jjones646/date/archive/{!s}-conan.zip'.format(self.version)
        download(download_url, 'date.zip')
        check_sha256('date.zip', 'e5814a5cce10f683bedf06645b5612c3de5bc743b962d034227fec612b7d252c')
        unzip('date.zip')
        os.unlink('date.zip')
        os.rename(self._archive_dirname, 'date')

    def build(self):
        extra_defs = {}
        extra_defs['DATE_USE_OS_TZDB'] = 'ON' if self._os_supports_zoneinfo else 'OFF'
        extra_defs['DATE_HAS_REMOTE_API'] = 'ON' if not self._os_supports_zoneinfo else 'OFF'

        # This package must manage timezone database for systems that don't manage
        # a central IANA timezone database (thank you, Windows). Updates will be applied
        # automatically by the date library. However, we must know the path where
        # this will be located when this package is built...
        # This is the reason that this install location is not exposed to consumers
        # via a conan option.
        if not self._os_supports_zoneinfo:
            p = os.path.abspath(os.getcwd())
            drive = os.path.splitdrive(p)[0]
            install_dir = os.path.join(drive, 'zoneinfo')
            extra_defs['DATE_INSTALL'] = install_dir

        cmake = CMake(self, parallel=True)
        cmake.configure(defs=extra_defs)
        cmake.build()

    def package(self):
        self.copy(pattern='*.h', dst='include', src='date/include')
        for ext in ('.dll', '.pdb'):
            self.copy(pattern='*{!s}*{!s}'.format(self.name, ext), dst='bin', src='bin', keep_path=False)
        for ext in ('.lib', '.a', '.so*', '.dylib*'):
            self.copy(pattern='*{!s}*{!s}'.format(self.name, ext), dst='lib', src='lib', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [self.name]
        if self.options.shared:
            self.cpp_info.defines.extend(['DATE_USE_DLL'])
