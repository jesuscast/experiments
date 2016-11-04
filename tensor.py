import os
from socket import gethostname

def install():
  print 'Downloading scikit-tensor...'
  import urllib
  import shutil
  os.chdir(os.path.expanduser('~/Documents'))
  urllib.urlretrieve('https://pypi.python.org/packages/e9/5e/2ce76cc8f9da0517085e17cd70210ed996aeb8f972e7080d0bc89d82bbd9/scikit-tensor-0.1.tar.gz', 'scikit-tensor.tar.gz')
  import tarfile
  t = tarfile.open('scikit-tensor.tar.gz')
  t.extractall()
  shutil.copytree('scikit-tensor-0.1/sktensor', 'site-packages/sktensor')
  shutil.rmtree('scikit-tensor-0.1')
  os.remove('scikit-tensor.tar.gz')