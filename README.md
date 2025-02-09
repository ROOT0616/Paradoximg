# PNG to DDS Converter

The PNG to DDS Converter is a GUI-based application that converts PNG images into DDS format using NVIDIA's `nvcompress` tool. In addition to basic conversion, this tool provides several advanced image processing features including color adjustment, mask application, compositing with a base image, and flexible resizing options. You can also save and load your favorite settings for quick reuse.

---

# PNG to DDS コンバータ

本ツールは、NVIDIA の `nvcompress` コマンドラインツールを用いて PNG 画像を DDS 形式に変換する GUI アプリケーションです。基本の変換処理に加え、画像の色調補正、マスク適用、ベースイメージとの合成、リサイズなどの多彩な機能を搭載しています。また、一度設定したパラメータをお気に入りとして保存・読み込みできるため、再利用も簡単です。

---

## New Features / 新機能

- **マスク適用機能**  
  - 「Mask Image」コンボボックスからマスク画像を選択できます。  
  - 「Apply Mask」チェックボックスでマスク処理を有効にし、さらに「マスクを最後に適用」チェックボックスを使用することで、合成後にマスクを適用するかどうかを選べます。

- **お気に入り設定機能**  
  - 現在の各種設定を JSON ファイル（`favorite_settings.json`）に保存できます。  
  - 保存済みのお気に入り設定をコンボボックスから選択して読み込み、すぐに同じ環境で変換処理を実行可能です。

- **柔軟な画像処理オプション**  
  - 画像の色変換：事前定義されたカラーパレットから選択し、入力画像の色を一括変更できます。  
  - ベースイメージとの合成：`Base_Image` フォルダ内の画像を選び、入力画像との合成が可能です。  
  - リサイズオプション：「幅」と「高さ」を指定することで、変換前後のリサイズ処理を行うことができます。  
  - 貼り付け順序の変更：`invert paste order` チェックボックスで、合成時の貼り付け順序を反転できます。

- **ユーザーフレンドリーな GUI**  
  - 各入力フィールドにはツールチップや説明ボタンを設置し、操作方法が直感的に理解できるよう工夫しています。  
  - 変換の進行状況はプログレスバーでリアルタイムに表示されます。

---

## Prerequisites / 前提条件

1. **Python**  
   - 本ツールは Python で開発されています。（開発時は Python 3.10 を使用）  
   - [python.org](https://www.python.org/downloads/) よりダウンロードしてください。

2. **必要なライブラリ**  
   以下のライブラリが必要です。インストールされていない場合は pip を用いてインストールしてください。
   - **Tkinter**: Python 標準の GUI ライブラリ（通常は同梱されています）。
   - **numpy**: `pip install numpy`
   - **pillow (PIL)**: `pip install pillow`

3. **nvcompress**  
   - NVIDIA の Texture Tools に含まれる `nvcompress` ツールが必要です。  
   - コマンドラインから実行可能な状態にし、[NVIDIA Texture Tools Exporter](https://developer.nvidia.com/nvidia-texture-tools-exporter) からダウンロードしてください。

---

## Usage / 使い方

1. **スクリプトの起動**  
   Python でスクリプトを実行すると、GUI ウィンドウが表示されます。

2. **各種設定の入力**  
   - **入力ディレクトリ (Input Directory)**  
     - 変換対象の PNG 画像が格納されているディレクトリを指定します。  
     - 「Browse...」ボタンをクリックしてダイアログから選択してください。
     
   - **出力ディレクトリ (Output Directory)**  
     - 変換後の DDS 画像を保存するディレクトリを指定します。  
     - 「Browse...」ボタンをクリックしてディレクトリを選択します。
     
   - **圧縮フォーマット (Compression Format)**  
     - DDS の圧縮形式をドロップダウンメニューから選択します。
     
   - **幅 (Width)** と **高さ (Height)**  
     - 画像のリサイズを行う場合の寸法を数値で入力します。  
     - 両フィールドに値を入力した場合、画像は指定サイズにリサイズされ、（「Base Image」が指定されていれば）その上に合成されます。
     
   - **ベースイメージ (Base Image)**  
     - 入力画像との合成の際に使用するベースイメージを、`Base_Image` フォルダ内から選択します。
     
   - **マスク画像 (Mask Image)**  
     - マスク処理に使用する画像を、`Mask_Image` フォルダ内から選択します。
     
   - **色 (Color)**  
     - 入力画像の色変換に使用する色を、事前定義されたオプションから選択します。
     
   - **ペースト後にリサイズ (Resize after paste)**  
     - チェックすると、合成後にリサイズ処理を実行します。
     
   - **ペーストの順序を反転 (Invert paste order)**  
     - チェックすると、ベースイメージと入力画像の貼り付け順序が反転します。
     
   - **Apply Mask / マスク適用**  
     - チェックすると、指定されたマスク画像が画像合成の過程で適用されます。  
     - 「マスクを最後に適用」のチェックボックスにより、合成後にマスク処理を行うかどうかを選択できます。

3. **変換の実行**  
   - 「Convert Images」ボタンをクリックすると、設定に基づいて以下の順序で画像処理が行われます：  
     1. 入力画像の読み込みと RGBA 形式への変換  
     2. 色変換（Color 指定がある場合）  
     3. マスクの適用（「Apply Mask」が有効の場合、かつ「マスクを最後に適用」がチェックされていなければ早期に適用）  
     4. ベースイメージとの合成（貼り付け順序やリサイズ処理のオプションに従い処理）  
     5. （「マスクを最後に適用」がチェックされている場合）合成後にマスク適用  
     6. 一時 PNG として保存し、`nvcompress` により DDS 形式へ変換、その後一時ファイルを削除  
   - 変換処理中はプログレスバーで進捗が表示されます。

4. **設定のリセットとお気に入り機能**  
   - **Reset**  
     - 「Reset」ボタンをクリックすると、すべてのフィールドが初期状態にリセットされます。
   - **お気に入り設定の保存／読み込み**  
     - 「お気に入りを保存」ボタンで現在の設定を保存できます。  
     - 保存済みのお気に入りはコンボボックスから選び、「お気に入りを読み込み」ボタンで復元可能です。

---

## Disclaimer / 免責事項

This tool is provided for educational and demonstration purposes only. It has been tested under specific conditions and may not work perfectly in every environment. Use it at your own risk and always back up your important images before processing.

本ツールは教育および実証目的で開発されています。特定の環境でテスト済みですが、すべての環境での動作を保証するものではありません。使用にあたっては自己責任で行い、重要な画像は必ずバックアップを取ってからご利用ください.
