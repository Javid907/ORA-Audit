import setuptools
import os
import shutil
import fileinput

with open("README.md", "r") as fh:
    long_description = fh.read()

ora_audit_path = "/opt/ora-audit"
ora_audit_log_path = ora_audit_path + "/log"
ora_audit_report_path = ora_audit_path + "/report"


try:
    os.mkdir(ora_audit_log_path)
except OSError:
    print ("Creation of the directory %s failed" % ora_audit_log_path)
else:
    print ("Successfully created the directory %s " % ora_audit_log_path)

try:
    os.mkdir(ora_audit_report_path)
except OSError:
    print ("Creation of the directory %s failed" % ora_audit_report_path)
else:
    print ("Successfully created the directory %s " % ora_audit_report_path)

setuptools.setup(
    name="ORA-Audit",
    version="0.1.0",
    author="Javid Rzayev",
    author_email="rz.cavid@gmail.com",
    description="Audit Oracle Database and Masking sensitive Table by keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Javid907/ORA-Audit",
    packages=['module'],
    scripts=['bin/run.py'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: *NIX OS's",
    ],
    python_requires='>=3.6',
)
