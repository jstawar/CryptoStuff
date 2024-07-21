#!/usr/bin/env python3

import os
import sys
import datetime
import urllib.request
import zipfile
from pathlib import Path

def downloadAndUnzip(address, date_start, date_end, ticker, out_dir):
  curr = date_start
  Path(out_dir).mkdir(parents=True, exist_ok=True)
  try:
    while curr <= date_end:
      file_name = ticker + "-trades-" + str(curr) + ".zip"
      download_url = address + ticker + "/" + file_name
      save_path = out_dir + file_name

      dl_file = urllib.request.urlopen(download_url)
      length = dl_file.getheader('content-length')
      if length:
        length = int(length)
        blocksize = max(4096,length//100)

      with open(save_path, 'wb') as out_file:
        dl_progress = 0
        print("\nFile Download: {}".format(save_path))
        while True:
          buf = dl_file.read(blocksize)
          if not buf:
            break
          dl_progress += len(buf)
          out_file.write(buf)
          done = int(50 * dl_progress / length)
          sys.stdout.write("\r[%s%s]" % ('#' * done, '.' * (50-done)) )
          sys.stdout.flush()

      with zipfile.ZipFile(save_path, 'r') as zip_ref:
        zip_ref.extractall(out_dir)
      os.remove(save_path)
      curr = curr + datetime.timedelta(days=1)

    return True

  except Exception as e:
    print(f'Exception: {e}')
    return False
    

if __name__ == "__main__":
  address = 'https://data.binance.vision/data/spot/daily/trades/'
  ticker = sys.argv[1] # "ETHUSDT", "BTCUSDT"
  date_start = datetime.datetime.strptime(sys.argv[2], '%Y%m%d').date()
  date_end = datetime.datetime.strptime(sys.argv[3], '%Y%m%d').date()
  out_dir = f'/CryptoData/{ticker}/'
  ret = downloadAndUnzip(address, date_start, date_end, ticker, out_dir)
  print()
  print("Finished with status: ", "OK" if ret else "FAILED")
