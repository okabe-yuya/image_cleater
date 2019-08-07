import os
import glob
import youtube_dl
import pandas as pd
from settings import VIDEO_DIR, URL_COLUMN_NAME


class DownloadDataset:
  """
    youtubeから動画をDLするためのclass
    youtube_dlを使用して実行を行う
    >>> txt_file_path = "download_list.txt" # 対象の動画を記述したtxtファイル
  """
  def __init__(self, file_path):
    file_extension = file_path[-4:]
    if file_extension == ".csv":
      self.download_lst = self._read_csv_get_url_list(file_path)
      print(self.download_lst)
    elif file_extension == ".txt":
      self.download_lst = self._read_txt_file_to_list(file_path)
    else:
      raise FileExistsError
    self.OPTS = {
      "outtmpl": "{VIDEO_DIR}/%(title)s.mp4".format(VIDEO_DIR=VIDEO_DIR)
    }

  def _read_csv_get_url_list(self, path):
    """
      csvファイルから「url」カラムを抽出してリストにして返す
      >>> path = "download_list.csv"
      >>> _read_csv_get_url_list(path)
      ["https://sample.com","https://sample.com","https://sample.com"]
    """
    df = pd.read_csv(path)
    return df[URL_COLUMN_NAME].tolist()

  def _read_txt_file_to_list(self, path):
    """
      txtファイルを読み込み各行をリストで返す
      >>> path = "download_list.txt"
      >>> _read_txt_file_to_list(path)
      ["a", "b", "c"]
    """
    with open(path, "r") as f:
        file = f.read()
        return file.split("\n")

  def all_download(self):
    """
      対象となるパスから全ての動画をダウンロード
      対象のパスはインスタンスの生成時にファイルパス(対象を記述したtxtファイル)を渡す
    """
    target_urls = self.download_lst
    for url in target_urls:
      info = self._download(url)
      self._rename(info)

  def _download(self, url):
    """
      対象パスの動画をyoutubeからダウンロード
      動画情報が含まれるinfoオブジェクトを返す
      >>> url = "https://www.youtube.com/sample"
      >>> _download(url)
      <'info object'>
    """
    print(f"--> fetch video from youtube: {url}")
    with youtube_dl.YoutubeDL(self.OPTS) as y:
      info = y.extract_info(url, download=True)
      print(f"--> finish {url} download")
    return info

  def _rename(self, info):
    """
      ダウンロードした動画のファイル名を変更する
      url -> 動画title名に変換
      >>> info = {"title": "test" ...}
      >>> _rename(info)
    """
    title = info.get("title", "video")
    pattern = f"{VIDEO_DIR}/{title}.mp4"
    for i, v in enumerate(glob.glob(pattern, recursive=True)):
      file_path = os.path.join(VIDEO_DIR, v)
      new_file_path = file_path.replace(' ', '_')
      os.rename(file_path, f"{i}_{new_file_path}")
      print(f"--> renaming finish {title}")


if __name__ == "__main__":
  targets_path = "download_list.csv"
  d = DownloadDataset(targets_path)
  # d.all_download()
