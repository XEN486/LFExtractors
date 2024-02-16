from dataclasses import dataclass
import struct

@dataclass
class CBF:
    magic_num:   int = 0        # 4 bytes
    cbf_version: int = 0        # 4 bytes
    kernel_load: int = 0        # 4 bytes
    kernel_jump: int = 0        # 4 bytes
    kernel_size: int = 0        # 4 bytes
    crc_check:   int = 0        # 4 bytes
    kernel_img:  bytes = b''    # kernel_size bytes
    padding:     bytes = b''    # until EOF (I don't read this data)

def unpack_uint(data):
    return int.from_bytes(data, "little") # the SoC that LF uses is little-endian, so I assume that the CBF file will be little-endian aswell

def read_cbf(file_path):
    cbf_data = CBF()
    with open(file_path, 'rb') as f:
        # Summary
        cbf_data.magic_num = unpack_uint(f.read(4))
        cbf_data.cbf_version = unpack_uint(f.read(4))
        cbf_data.kernel_load = unpack_uint(f.read(4))
        cbf_data.kernel_jump = unpack_uint(f.read(4))
        cbf_data.kernel_size = unpack_uint(f.read(4))

        # CRC checksum of summary
        cbf_data.crc_check = unpack_uint(f.read(4))

        # Kernel image
        cbf_data.kernel_img = f.read(cbf_data.kernel_size) # read until kernel size finished

    return cbf_data

def main():
    cbf = read_cbf(input(str('Enter the path to the CBF file: ')))
    print(f'Summary CRC: {hex(cbf.crc_check)}')
    with open('Image', 'wb') as f:
        f.write(cbf.kernel_img)

if __name__ == '__main__':
    main()
