from configparser import ConfigParser
from pathlib import Path
import setuptools
 
# Read settings.ini
config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]
 
cfg_keys = "version description keywords author author_email".split()
expected = (
    cfg_keys
    + "lib_name user branch license status min_python audience language".split()
)
 
for o in expected:
    if o not in cfg:
        raise ValueError(f"Missing expected setting: {o}")
 
setup_cfg = {o: cfg[o] for o in cfg_keys}
 
licenses = {
    "apache2": (
        "Apache Software License 2.0",
        "OSI Approved :: Apache Software License",
    ),
    "mit": ("MIT License", "OSI Approved :: MIT License"),
    "gpl2": (
        "GNU General Public License v2",
        "OSI Approved :: GNU General Public License v2 (GPLv2)",
    ),
    "gpl3": (
        "GNU General Public License v3",
        "OSI Approved :: GNU General Public License v3 (GPLv3)",
    ),
    "bsd3": ("BSD License", "OSI Approved :: BSD License"),
}
 
statuses = [
    "1 - Planning",
    "2 - Pre-Alpha",
    "3 - Alpha",
    "4 - Beta",
    "5 - Production/Stable",
    "6 - Mature",
    "7 - Inactive",
]
 
py_versions = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]
 
requirements = cfg.get("requirements", "").split()
if cfg.get("pip_requirements"):
    requirements += cfg.get("pip_requirements", "").split()
 
dev_requirements = (cfg.get("dev_requirements") or "").split()
min_python = cfg["min_python"]
 
lic = licenses.get(cfg["license"].lower(), (cfg["license"], None))
 
readme_path = Path("README.md")
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
 
setuptools.setup(
    name=cfg["lib_name"],
    version=cfg["version"],
    description=cfg["description"],
    author=cfg["author"],
    author_email=cfg["author_email"],
    url=cfg["git_url"],
    license=lic[0],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    python_requires=f">={min_python}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        "Development Status :: " + statuses[int(cfg["status"])],
        "Intended Audience :: " + cfg["audience"].title(),
        "Natural Language :: " + cfg["language"].title(),
    ]
    + [
        f"Programming Language :: Python :: {v}"
        for v in py_versions
        if v >= min_python
    ]
    + (["License :: " + lic[1]] if lic[1] else []),
    entry_points={
        "console_scripts": cfg.get("console_scripts", "").split(),
        "nbdev": [f'{cfg.get("lib_path")}={cfg.get("lib_path")}._modidx:d'],
    },
)
