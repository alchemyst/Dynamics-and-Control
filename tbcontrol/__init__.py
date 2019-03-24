from .version import __version__

class VersionError(Exception):
    pass

def expectversion(version):
    import packaging.version

    currentversion = packaging.version.parse(__version__)
    expectedversion = packaging.version.parse(version)

    if currentversion < expectedversion:
        raise VersionError(f"Please upgrade tbcontrol to at least version "
                           f"{version} - you have {__version__}.")