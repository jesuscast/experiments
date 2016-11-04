import os
from socket import gethostname

def install():
  print 'Downloading scipy...'
  import urllib
  import shutil
  os.chdir(os.path.expanduser('~/Documents'))
  urllib.urlretrieve('https://pypi.python.org/packages/22/41/b1538a75309ae4913cdbbdc8d1cc54cae6d37981d2759532c1aa37a41121/scipy-0.18.1.tar.gz#md5=5fb5fb7ccb113ab3a039702b6c2f3327', 'scipy.tar.gz')
  import tarfile
  t = tarfile.open('scipy.tar.gz')
  t.extractall()
  shutil.copytree('scipy-0.18.1/scipy', 'site-packages/scipy')
  shutil.rmtree('scipy-0.18.1')
  os.remove('scipy.tar.gz')