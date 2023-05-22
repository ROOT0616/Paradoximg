from PIL import Image
import os

def resize_images(input_folder, output_folder, new_size):
    # フォルダ内の全ての画像ファイルを取得
    file_list = os.listdir(input_folder)

    for file_name in file_list:
        # 画像ファイルのパスを作成
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        try:
            # 画像を開く
            image = Image.open(input_path)

            # アルファチャンネルを持つ画像の場合、不透明部分を黒に変換
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                image = image.convert('RGBA')
                datas = image.getdata()
                new_data = []
                for item in datas:
                    # 不透明度が255（完全不透明）の場合はピクセルを黒に変換
                    if item[3] == 255:
                        new_data.append((0, 0, 0, 255))
                    else:
                        new_data.append(item)
                image.putdata(new_data)

            # 画像をリサイズ
            resized_image = image.resize(new_size)

            # リサイズされた画像を保存
            resized_image.save(output_path)

        except IOError:
            print(f"Failed to resize image: {file_name}")

# 使用例
input_folder = 'input_images'  # 入力フォルダのパスを指定
output_folder = 'output_images'  # 出力フォルダのパスを指定
new_size = (24, 24)  # 新しいサイズを指定

resize_images(input_folder, output_folder, new_size)
