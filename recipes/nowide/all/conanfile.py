from conans import ConanFile, CMake, tools

class NoWideConan(ConanFile):
    name = "nowide"
    description = "The library provides an implementation of standard C and C++ library functions, such that their inputs are UTF-8--aware on Windows without requiring the Wide API. "
    topics = ("console", "windows", "wide-char")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/nephatrine/nowide-standalone"
    license = "BSL-1.0"
    settings = "os", "compiler", "build_type", "arch"

    exports_sources = "CMakeLists.txt", "patches/*"
    generators = "cmake"

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }

    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version],
                  destination=self._source_subfolder, strip_root=True)

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["NOWIDE_BUILD_SHARED"] = self.options.shared
            self._cmake.definitions["NOWIDE_BUILD_STATIC"] = not self.options.shared
            self._cmake.definitions["NOWIDE_BUILD_TESTS"] = False
            self._cmake.definitions["NOWIDE_BUILD_DOC_HTML"] = False
            self._cmake.definitions["NOWIDE_BUILD_DOC_CHM"] = False
            self._cmake.definitions["NOWIDE_BUILD_DOC_TEX"] = False
            if self.settings.os == "Windows":
                # Respect recipe consumer's choice, by stopping their CMakeLists from overriding MSVC flags
                self._cmake.definitions["NOWIDE_USE_MSVC_RUNTIME"] = False
            self._cmake.configure()
        return self._cmake

    def build(self):
        for patch in self.conan_data["patches"][self.version]:
            tools.patch(**patch)
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
