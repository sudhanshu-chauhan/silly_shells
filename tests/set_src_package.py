"""set_src_package module to set source package."""
import os
import sys


def set_src():
    """Set source package for project."""
    src_package_name = "silly_shells"
    package_list = os.path.dirname(os.path.realpath(".")).split(os.sep)

    src_package_path = os.sep.join(
        package_list[0: package_list.index(src_package_name) + 1])

    if src_package_path not in sys.path:
        sys.path.append(src_package_path)
