#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but without
# any warranty; without even the implied warranty of merchantability or fitness
# for a particular purpose. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

__licence__ = 'GPLv3'
__author__ = 'Amine Namouchi'
__author_email__ = 'bioinfosuite@gmail.com'


import sys
if sys.version_info[0] < 3:
    print('Python 3 is needed to run this script!')
    sys.exit(0)

from string import *
from urllib.request import urlopen
import subprocess


study = sys.argv[1]
url = 'http://www.ebi.ac.uk/ena/data/warehouse/filereport?accession='+study+'&result=read_run&fields=fastq_ftp,fastq_md5,fastq_bytes'
response = urlopen(url)
with open(study+'_files_details.txt', 'bw') as f:
    f.write(response.read())
f.close()


with open(study+'_files_details.txt', 'r') as f:
    for l in f:
        if 'ftp.sra.ebi.ac.uk' in l:
            if ';' in l:
                links = l.rstrip('\n').split('\t')[0].split(';')
                for eachLink in links:
                    cmd = ['wget', eachLink]
                    proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
                    proc.wait()
            else:
                eachLink = l.rstrip('\n').split('\t')[0]
                cmd = ['wget', eachLink]
                proc = subprocess.Popen(cmd, stderr=subprocess.STDOUT)
                proc.wait()
f.close()
