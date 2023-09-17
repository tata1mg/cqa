import warnings

from setuptools import find_packages, setup
from setuptools.command.install import install

packages = find_packages(exclude=["tests"])


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        self.setup_application()  # install git hook

    def setup_application(self):
        from cqa.utils.hook import install_git_hook

        warnings.warn("installing git hook at .git/hooks/pre-commit..")
        install_git_hook()


def get_requirements():
    install_requires = []
    with open("requirements.txt", "r", encoding="utf-8") as f:
        install_requires = f.read().splitlines()
    return install_requires


setup(
    name="cqa",
    version="v0.0.1",
    description="command line tool for running code analysis tools(SAST)",
    packages=packages,
    install_requires=get_requirements(),
    entry_points={"console_scripts": ["cqa=cqa.main:main"]},
    cmdclass={"install": PostInstallCommand},
)
