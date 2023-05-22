import struct

def get_dds_compression_format(filename):
    with open(filename, 'rb') as f:
        # 先頭から128バイトを読み込む
        header = f.read(128)

        # ヘッダーの76から80バイト目がfourCCと呼ばれる部分で、ここに圧縮フォーマットの情報が含まれている
        fourCC = struct.unpack('4s', header[76:80])[0].decode()
        print(fourCC)
        # fourCCの値によって圧縮形式を判断
        if fourCC == 'DXT1':
            return 'DXT1'
        elif fourCC == 'DXT3':
            return 'DXT3'
        elif fourCC == 'DXT5':
            return 'DXT5'
        elif fourCC == 'BC3':
            return 'BC3'

print(get_dds_compression_format('./output_images/1.dds'))
