import os
import imageio
from PIL import Image

# 入力と出力のディレクトリを指定
input_dir = 'input_images'
output_dir = 'output_images'

# outputディレクトリが存在しない場合は作成
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 入力ディレクトリ内の全てのファイルを処理
for filename in os.listdir(input_dir):
    if filename.endswith('.dds'):
        # DDSファイルを読み込み
        dds_image = imageio.imread(os.path.join(input_dir, filename))

        # PIL Imageオブジェクトを作成
        img = Image.fromarray(dds_image)

        # ファイル名から拡張子を取り除く
        base_filename = os.path.splitext(filename)[0]

        # PNGとして出力
        img.save(os.path.join(output_dir, f'{base_filename}.png'))
