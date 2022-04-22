from distutils.core import setup, Extension

marvelmind_module = Extension('marvelmind_module', sources=['plugin.c', 'marvelmind.c'])

# calling setup function with theese parameters.
setup(name='python_c_marvelmind_module_extension',
      version='0.9',
      description='A Marvelmind sensor API integration to python with c backend.',
      ext_modules=[marvelmind_module],
      url='http://172.22.195.68:3000/palkovics/marvelmind_donkeycar',
      author='Mate Vagner, Palkovics Denes',
      author_email='a@b.cd')

