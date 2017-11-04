import os
from conans import ConanFile, CMake
from conans.tools import download, check_sha256, unzip


class HowardHinnantDate(ConanFile):
    name = 'date'
    version = '2.3.0'
    description = 'A date and time library based on the C++11/14/17 <chrono> header'
    url = 'https://github.com/jjones646/conan-date'
    license = 'https://github.com/jjones646/date/blob/{!s}-cmake/LICENSE.txt'.format(version)
    settings = 'os', 'compiler', 'arch', 'build_type'
    options = {
        'shared': [True, False],
        'tz_version': 'ANY'
    }
    default_options = 'shared=True', 'tz_version=2017c'
    exports_sources = 'CMakeLists.txt'
    generators = 'cmake'

    @property
    def _archive_dirname(self):
        return 'date-{!s}-cmake'.format(self.version)

    def source(self):
        download_url = 'https://github.com/jjones646/date/archive/{!s}-cmake.zip'.format(self.version)
        download(download_url, 'date.zip')
        check_sha256('date.zip', 'e5814a5cce10f683bedf06645b5612c3de5bc743b962d034227fec612b7d252c')
        unzip('date.zip')
        os.unlink('date.zip')
        os.rename(self._archive_dirname, 'date')

    def build(self):
        extra_defs = {}
        extra_defs['DATE_MAKE_PORTABLE'] = 'ON'
        extra_defs['DATE_TZDB_VERSION'] = self.options.tz_version
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
