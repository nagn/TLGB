from distutils.core import setup

setup(name="Garrison Builder",
      version="127.0",
      author="Ron Paul 2012",
      url="https://github.com/nagn/TLGB/",
      license="GNU General Public License (GPL)",
      scripts=["run.py"],
      windows=[{"script": "run.py"}],
      options={"py2exe": {"skip_archive": True, "includes": ["sip"]}})