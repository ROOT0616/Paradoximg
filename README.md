# PNG to DDS Converter

This is a GUI tool designed to convert PNG images to DDS format. It uses the `nvcompress` command-line tool from NVIDIA's Texture Tools to perform the conversion. Additionally, it provides options to change the color of the input image and add a base image underneath.

## Prerequisites

1. **Python**: Ensure you have Python installed on your machine. The Python version used for developing this tool is Python 3.10. You can download Python from the official site: https://www.python.org/downloads/.

2. **Libraries**: Install necessary Python libraries using pip:
    - Tkinter: Tkinter is Python's de-facto standard GUI package. It is included with Python by default.
    - numpy: `pip install numpy`
    - pillow (PIL): `pip install pillow`

3. **nvcompress**: This tool uses the `nvcompress` tool from NVIDIA's Texture Tools. Ensure you have it installed and accessible from your command line. You can download it from: https://developer.nvidia.com/nvidia-texture-tools-exporter.

## Usage

1. Open the script in Python.

2. The GUI will have several fields. Here is what each field is used for:

    - **Input Directory**: Directory that contains the PNG images to be converted. Click "Browse..." to open a dialog and choose the directory.

    - **Output Directory**: Directory where the DDS images will be saved after conversion. Click "Browse..." to open a dialog and choose the directory.

    - **Compression Format**: The DDS compression format. Available options are listed in the dropdown menu.

    - **Width** and **Height**: The width and height to resize images to. If these fields and "Base Image" are filled in, each image will be resized to these dimensions and then pasted onto the base image.

    - **Base Image**: The image that will be pasted underneath each input image. The images are located in the "Base_Image" folder. The image is chosen from the dropdown menu.

    - **Color**: The color to change each input image to. Available options are listed in the dropdown menu.

    - **Resize after paste**: If this checkbox is checked, each image will be resized after being pasted onto the base image.

    - **Invert paste order**: If this checkbox is checked, the base image will be pasted onto each input image instead of the other way around.

3. Click "Convert Images" to start the conversion. The progress of the conversion will be shown in the progress bar.

4. Click "Reset" to reset all fields to their default values.

Remember, in order to perform the conversion correctly, the "Input Directory", "Output Directory", and "Compression Format" fields must be filled in. The remaining fields are optional and depend on whether you want to resize images, change their color, or paste a base image. If you want to simply convert images without any additional operations, leave the optional fields blank.

## Disclaimer

This tool was developed for educational purposes and has not been extensively tested. Use it at your own risk. Please ensure you have backup copies of any important images before using this tool.


# PNG to DDS コンバータ

このツールはPNGイメージをDDSフォーマットに変換するためのGUIツールです。NVIDIAのテクスチャツールの `nvcompress` コマンドラインツールを使用して変換を行います。また、入力画像の色を変更したり、ベースイメージを追加したりするオプションも提供しています。

## 前提条件

1. **Python**: お使いのマシンにPythonがインストールされていることを確認してください。このツールの開発に使用されたPythonのバージョンはPython 3.10です。Pythonは公式サイトからダウンロードできます: https://www.python.org/downloads/

2. **ライブラリ**: pipを使用して必要なPythonライブラリをインストールします：
    - Tkinter: TkinterはPythonのデファクトスタンダードGUIパッケージです。Pythonにはデフォルトで含まれています。
    - numpy: `pip install numpy`
    - pillow (PIL): `pip install pillow`

3. **nvcompress**: このツールはNVIDIAのテクスチャツールから `nvcompress` ツールを使用します。それがインストールされていて、コマンドラインからアクセス可能であることを確認してください。ダウンロードはこちらからできます: https://developer.nvidia.com/nvidia-texture-tools-exporter.

## 使い方

1. スクリプトをPythonで開きます。

2. GUIにはいくつかのフィールドがあります。それぞれのフィールドの用途は以下のとおりです：

    - **入力ディレクトリ**: 変換するPNG画像が含まれるディレクトリ。 "Browse..."をクリックするとダイアログが開き、ディレクトリを選択できます。

    - **出力ディレクトリ**: 変換後のDDS画像が保存されるディレクトリ。 "Browse..."をクリックするとダイアログが開き、ディレクトリを選択できます。

    - **圧縮フォーマット**: DDSの圧縮フォーマット。利用可能なオプションはドロップダウンメニューにリストされています。

    - **幅**と**高さ**: 画像をリサイズする幅と高さ。これらのフィールドと "Base Image" が入力されている場合、各画像はこれらの寸法にリサイズされ、その後ベースイメージに貼り付けられます。

    - **ベースイメージ**: 各入力画像の下に貼り付けられる画像。画像は "Base_Image" フォルダに格納されています。画像はドロップダウンメニューから選択されます。

    - **色**: 各入力画像の色を変更する色。利用可能なオプションはドロップダウンメニューにリストされています。

    - **ペースト後にリサイズ**: このチェックボックスがチェックされている場合、各画像はベースイメージに貼り付けた後にリサイズされます。

    - **ペーストの順序を反転**: このチェックボックスがチェックされている場合、ベースイメージは各入力画像に貼り付けられるのではなく、その逆になります。

3. "Convert Images"をクリックして変換を開始します。変換の進行状況はプログレスバーで表示されます。

4. "Reset"をクリックすると、すべてのフィールドがデフォルト値にリセットされます。

変換を正しく行うためには、"入力ディレクトリ"、"出力ディレクトリ"、"圧縮フォーマット"のフィールドが入力されている必要があります。残りのフィールドはオプションであり、画像をリサイズしたり、色を変更したり、ベースイメージを貼り付けたりするかどうかによります。追加の操作なしに単純に画像を変換したい場合は、オプションのフィールドを空白にしておいてください。

## 免責事項

このツールは教育目的で開発され、広範囲にわたるテストは行われていません。自己責任で使用してください。重要な画像のバックアップを持っていることを確認してから、このツールを使用してください。
