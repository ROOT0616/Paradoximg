from PIL import Image
import os

def resize_images(input_folder, output_folder, size, overlay_image_path):
    # 出力フォルダが存在しない場合は作成する
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 入力フォルダ内のファイルを走査
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        try:
            # 画像を開く
            with Image.open(input_path) as image:
                # 画像をリサイズする
                resized_image = image.resize(size)

                # オーバーレイ画像を開く
                with Image.open(overlay_image_path) as overlay_image:
                    # オーバーレイ画像をリサイズする
                    resized_overlay = overlay_image.resize(size)

                    # オーバーレイ画像を合成する
                    final_image = Image.alpha_composite(resized_image.convert('RGBA'), resized_overlay.convert('RGBA'))

                    # リサイズ＆オーバーレイ画像を保存する
                    final_image.save(output_path)
        except Exception as e:
            print(f"Failed to process {filename}: {str(e)}")

# リサイズとオーバーレイを行う画像の入力フォルダと出力フォルダを指定
input_folder = "input_images"
output_folder = "output_images"

# リサイズ後のサイズを指定
resize_size = (45, 45)

# オーバーレイするイメージのパスを指定
overlay_image_path = "overlay_image.png"

# 画像をリサイズし、オーバーレイを行う
resize_images(input_folder, output_folder, resize_size, overlay_image_path)
