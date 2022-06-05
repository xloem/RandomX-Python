from setuptools import setup, Extension
from Cython.Build import cythonize

import glob, os, platform

machine = platform.machine()

# TODO: build submodule with cmake
compile_flags = ['-march=native','-std=c++11','-fpic', '-O3']

source_root_dir = os.path.join('RandomX', 'src')
sources = []
sources.extend(glob.glob('*.c', root_dir=source_root_dir))
sources.extend(glob.glob('*.cpp', root_dir=source_root_dir))
sources.extend(glob.glob('*.S', root_dir=source_root_dir))
sources = [source for source in sources if 'jit_' not in source]
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
    ext_modules=cythonize(
        Extension(
            'randomx', [
                'randomx.pyx',
                *[source for source in sources if source.endswith('.cpp') or source.endswith('.c')]
            ],
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
