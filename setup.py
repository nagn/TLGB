#!/usr/bin/python

from distutils.core import setup
import py2exe

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>Garrison Builder</description>
<dependency>
<dependentAssembly>
    <assemblyIdentity
        type="win32"
        name="Microsoft.VC90.CRT"
        version="9.0.30729.4918"
        processorArchitecture="X86"
        publicKeyToken="1fc8b3b9a1e18e3b"
        language="*"
    />
</dependentAssembly>
</dependency>
</assembly>



"""

"""
installs manifest and icon into the .exe
but icon is still needed as we open it
for the window icon (not just the .exe)
changelog and logo are included in dist
"""

setup(
    windows = [
        {
            "script": "main.py",
            "icon_resources": [(1, "icon.ico")],
            "other_resources": [(24,1,manifest)]
        }
    ],
      data_files=["icon.ico"]
)