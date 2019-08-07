import cv2 as cv
import os
from settings import VIDEO_DIR, SAVE_IMAGES_DIR, FPS_ITERATION


def save_frame_range_seconds(in_video_dir, save_path, time_obj, ext="mp4"):
  """
    指定ディレクトリ内の指定拡張子のビデオのキャプチャ画像を生成する(全ファイルが対象, default=mp4)
    >>> in_video_dir = "video"
    >>> save_paht = "shot"
    # キャプションを始める秒数と終了する秒数の範囲をdictで指定
    # in_video_dirの中の動画数と要素数は一致していないとあかん
    >>> time_obj = [{"start": 0, "end": 10}, {"start"....}]
    >>> save_frame_range_seconds(in_video_dir, save_path, time_obj)
  """
  def _save_frame_range_seconds(in_video_path, save_path, start_sec, end_sec, ext='jpg'):
    """
      受け取った動画のパスと開始秒数と終了秒数からキャプション画像を生成する
      >>> in_video_path = "video/sample.mp4"
      >>> save_path = "shot"
      >>> start_sec = 0
      >>> end_sec = 10
      >>> _save_frame_range_seconds(in_video_path, save_path, start_sec, end_sec)
    """
    cap = cv.VideoCapture(in_video_path)

    if not cap.isOpened():
      raise ValueError

    os.makedirs(save_path, exist_ok=True)
    digit = len(str(int(cap.get(cv.CAP_PROP_FRAME_COUNT))))
    fps = cap.get(cv.CAP_PROP_FPS)
    unique_name = in_video_path.split("/")[1][:-4]

    for i, sec in enumerate(range(start_sec, end_sec, FPS_ITERATION)):
      n = round(fps * sec)
      cap.set(cv.CAP_PROP_POS_FRAMES, n)
      ret, frame = cap.read()

      if ret:
        save_path_ = os.path.join(save_path, f"{unique_name}_{str(i+1)}")
        print(f"--> shot: {save_path}")
        cv.imwrite('{}_{}.{}'.format(save_path_, str(n).zfill(digit), ext), frame)
        n += 1
      else:
        return

  ref_video_path = [os.path.join(in_video_dir, video) for video in os.listdir(in_video_dir)]
  ref_video_path = list(filter(lambda x: x[-4:] == f".{ext}", ref_video_path))
  [_save_frame_range_seconds(path, save_path, time_obj[i].get("start"), time_obj[i].get("end")) for i, path in enumerate(ref_video_path)]


if __name__ == "__main__":
  # 正直これはどうなのよと思う。開始位置の指定はdownload_list.txtでしておくのがベストか
  time_obj = [
    {"start": 0, "end": 60*7+15},
    {"start": 0, "end": 77},
    {"start": 30, "end": 90}
  ]
  save_frame_range_seconds("video", SAVE_IMAGES_DIR, time_obj)
