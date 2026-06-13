from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.toolchain import shprint
from pythonforandroid.logger import info
from pythonforandroid.util import current_directory
import sh
import os
import shutil


class PyBoyRecipe(PythonRecipe):

    version = "master"
    url = "https://github.com/Sahil-pixel/PyBoy/archive/refs/heads/master.zip"

    depends = [
        "python3",
        "numpy",
        "cython",
        "setuptools"
    ]

    site_packages_name = "pyboy"
    call_hostpython_via_targetpython = False

    # ENV
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)

        info("CC (auto): {}".format(env.get("CC")))
        info("CXX (auto): {}".format(env.get("CXX")))

        env.update({
            "PYBOY_HEADLESS": "1",
            "PYBOY_NO_SDL": "1",
            "PYTHONNOUSERSITE": "1",
            "PYTHONHOME": "",
        })

        env["CFLAGS"] = env.get("CFLAGS", "") + " -O2 -fPIC"
        env["CPPFLAGS"] = env.get("CPPFLAGS", "") + " -fPIC"

        return env

    
    # BUILD
    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        build_dir = self.get_build_dir(arch.arch)
        install_dir = self.ctx.get_python_install_dir(arch.arch)

        info("INSTALL DIR: {}".format(install_dir))

        with current_directory(build_dir):

            shprint(
                sh.Command(self.hostpython_location),
                "-m", "pip",
                "install", ".",
                "--no-deps",
                "--force-reinstall",
                "--no-cache-dir",
                "--target", install_dir,   
                _env=env,
            )
    

 

    # 
    def install_python_package(self, arch, name=None):
        pass


recipe = PyBoyRecipe()
