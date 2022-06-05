# RandomX
This is a python interface for https://github.com/tevador/randomx , a proof-of-work algorithm
optimized for general-purpose CPUs, based on random code execution.

## Installation

`pip3 install randomx`

## Quick-Start

```
import randomx
vm = randomx.RandomX(b'key bytes', full_mem=False, secure=True, large_pages=False)
# full_mem: whether to operate in full mode or light mode
# secure: whether to bound executable sections
# large_pages: whether to place memory in large pages
hash = vm(b'message data')
hashes = [*vm.calculate_hashes([b'message 1', b'message 2', b'message 3'])]
```
