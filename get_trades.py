#!/usr/bin/env python3

import os
import sys
import datetime
import urllib.request
import zipfile
import argparse
from pathlib import Path

def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', required = True)
    parser.add_argument('--dateStart', required = True)
    parser.add_argument('--dateEnd', required = True)
    parser.add_argument('--rootDir', required = True)

    parsed = parser.parse_args()
    parsed.date_start = datetime.datetime.strptime(parsed.dateStart, '%Y%m%d').date()
    parsed.date_end = datetime.datetime.strptime(parsed.dateEnd, '%Y%m%d').date()

    return parsed


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
    
# ./get_trades.py --ticker ETHUSDT --dateStart 20240720 --dateEnd 20240806 --rootDir /CryptoData
if __name__ == "__main__":
  args = parseArgs()

  address = 'https://data.binance.vision/data/spot/daily/trades/'
  out_dir = f'{args.rootDir}/{args.ticker}/'
  ret = downloadAndUnzip(address, args.date_start, args.date_end, args.ticker, out_dir)
  print()
  print("Finished with status: ", "OK" if ret else "FAILED")
