from setuptools import setup, Extension
from Cython.Build import cythonize

import glob, os, platform

machine = platform.machine()

# TODO: build submodule with cmake
compile_flags = ['-march=native','-std=c++11','-fpic', '-O3']

source_root_dir = os.path.join('RandomX', 'src')
sources = []
sources.extend(glob.glob('**/*.c', root_dir=source_root_dir, recursive=True))
sources.extend(glob.glob('**/*.cpp', root_dir=source_root_dir, recursive=True))
sources.extend(glob.glob('**/*.S', root_dir=source_root_dir, recursive=True))
sources = [source for source in sources if 'jit_' not in source and  'tests' not in source]
if machine in ['i386', 'i686', 'x86_64']:
    sources.extend(['jit_compiler_x86.cpp', 'jit_compiler_x86_static.S'])
elif machine in ['aarch64_be', 'aarch64', 'armv8b', 'armv8l']:
    sources.extend(['jit_compiler_a64_static.s', 'jit_compiler_a64.cpp'])
    compile_flags.append('-DHAVE_HWCAP')
elif machine.startswith('ppc'):
    compile_flags.append('-mcpu=native')
sources = [os.path.join(source_root_dir,source) for source in sources]

setup(
    name='RandomX',
    version=open('version').read(),
    description='RandomX Proof-of-Work Hasher',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    package_dir={'randomx': 'randomx'},
    packages=['randomx'],
    url='https://github.com/xloem/RandomX-Python',
    keywords=['randomx', 'crypto', 'cryptocurrency', 'blockchain', 'pow'],
    classifiers=[
      'Programming Language :: Python :: 3',
      'Operating System :: OS Independent',
    ],
    include_package_data=True,
    package_data={'': ['*.pyx', '*.pxd', '*.inc', '*.S', '*.h', '*.c', '*.hpp', '*.cpp']},
    ext_modules=cythonize(
        Extension(
            'randomx', [
                os.path.join('randomx','randomx.pyx'),
                *[source for source in sources if source.endswith('.c') or source.endswith('.cpp')]
            ],
            include_dirs=[os.path.join('RandomX','src')],
            extra_objects=[source for source in sources if source.endswith('.S')],
            extra_compile_args=compile_flags,
            #libraries=['randomx'],
            language='c++',
        ),
        compiler_directives=dict(
            language_level='3',
            embedsignature=True
        )
    )
)
