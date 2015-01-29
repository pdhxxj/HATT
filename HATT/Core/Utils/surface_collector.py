__author__ = 'kasi'

import Queue
import datetime
import logging
import re
import threading

_SURFACE_TEXTURE_TIMESTAMPS_MESSAGE = 'SurfaceTexture update timestamps'
_SURFACE_TEXTURE_TIMESTAMP_RE = '\d+'

class SurfaceStatsCollector(object):

  class Result(object):

    def __init__(self, name, value, unit):
      self.name = name
      self.value = value
      self.unit = unit

  def __init__(self):
    self._collector_thread = None
    self._use_legacy_method = False
    self._surface_before = None
    self._get_data_event = None
    self._data_queue = None
    self._stop_event = None
    self._results = []
    self._warn_about_empty_data = True

  def DisableWarningAboutEmptyData(self):
    self._warn_about_empty_data = False

  def Start(self):
    assert not self._collector_thread
    if self._ClearSurfaceFlingerLatencyData():
      self._get_data_event = threading.Event()
      self._stop_event = threading.Event()
      self._data_queue = Queue.Queue()
      self._collector_thread = threading.Thread(target=self._CollectorThread)
      self._collector_thread.start()
    else:
      self._use_legacy_method = True
      self._surface_before = self._GetSurfaceStatsLegacy()

  def Stop(self):
    self._StorePerfResults()
    if self._collector_thread:
      self._stop_event.set()
      self._collector_thread.join()
      self._collector_thread = None

  def SampleResults(self):
    self._StorePerfResults()
    results = self.GetResults()
    self._results = []
    return results

  def GetResults(self):
    return self._results or self._GetEmptyResults()

  def _GetEmptyResults(self):
    return [
        SurfaceStatsCollector.Result('refresh_period', None, 'seconds'),
        SurfaceStatsCollector.Result('jank_count', None, 'janks'),
        SurfaceStatsCollector.Result('max_frame_delay', None, 'vsyncs'),
        SurfaceStatsCollector.Result('frame_lengths', None, 'vsyncs'),
        SurfaceStatsCollector.Result('avg_surface_fps', None, 'fps')
    ]

  @staticmethod
  def _GetNormalizedDeltas(data, refresh_period):
    deltas = [t2 - t1 for t1, t2 in zip(data, data[1:])]
    return (deltas, [delta / refresh_period for delta in deltas])

  @staticmethod
  def _CalculateResults(refresh_period, timestamps, result_suffix):
    frame_count = len(timestamps)
    #print frame_count
    seconds = timestamps[-1] - timestamps[0]
    #print seconds
    frame_lengths, normalized_frame_lengths = \
        SurfaceStatsCollector._GetNormalizedDeltas(timestamps, refresh_period)
    length_changes, normalized_changes = \
        SurfaceStatsCollector._GetNormalizedDeltas(
            frame_lengths, refresh_period)
    jankiness = [max(0, round(change)) for change in normalized_changes]
    pause_threshold = 20
    jank_count = sum(1 for change in jankiness
                     if change > 0 and change < pause_threshold)
    return [
        SurfaceStatsCollector.Result(
            'avg_surface_fps' + result_suffix,
            int(round(frame_count / seconds)), 'fps'),
        SurfaceStatsCollector.Result(
            'jank_count' + result_suffix, jank_count, 'janks'),
        SurfaceStatsCollector.Result(
            'max_frame_delay' + result_suffix,
            round(max(normalized_frame_lengths)),
            'vsyncs'),
        SurfaceStatsCollector.Result(
            'frame_lengths' + result_suffix, normalized_frame_lengths,
            'vsyncs'),
    ]

  @staticmethod
  def _CalculateBuckets(refresh_period, timestamps):
    results = []
    for pct in [0.99, 0.5]:
      sliced = timestamps[min(int(-pct * len(timestamps)), -3) : ]
      #print sliced
      results += SurfaceStatsCollector._CalculateResults(
          refresh_period, sliced, '_' + str(int(pct * 100)))
    return results

  def _StorePerfResults(self):
    if self._use_legacy_method:
      surface_after = self._GetSurfaceStatsLegacy()
      td = surface_after['timestamp'] - self._surface_before['timestamp']
      seconds = td.seconds + td.microseconds / 1e6
      frame_count = (surface_after['page_flip_count'] -
                     self._surface_before['page_flip_count'])
      self._results.append(SurfaceStatsCollector.Result(
          'avg_surface_fps', int(round(frame_count / seconds)), 'fps'))
      return
    assert self._collector_thread
    (refresh_period, timestamps) = self._GetDataFromThread()
    if not refresh_period or not len(timestamps) >= 3:
      if self._warn_about_empty_data:
        logging.warning('Surface stat data is empty')
      return
    self._results.append(SurfaceStatsCollector.Result(
        'refresh_period', refresh_period, 'seconds'))
    self._results += self._CalculateResults(refresh_period, timestamps, '')
    self._results += self._CalculateBuckets(refresh_period, timestamps)

  def _CollectorThread(self):
    last_timestamp = 0
    timestamps = []
    retries = 0
    while not self._stop_event.is_set():
      self._get_data_event.wait(1)
      try:
        refresh_period, new_timestamps = self._GetSurfaceFlingerFrameData()
        if refresh_period is None or timestamps is None:
          retries += 1
          if retries < 3:
            continue
          if last_timestamp:
            self._data_queue.put((None, None))
            self._stop_event.wait()
            break
          raise Exception('Unable to get surface flinger latency data')
        timestamps += [timestamp for timestamp in new_timestamps
                       if timestamp > last_timestamp]
        if len(timestamps):
          last_timestamp = timestamps[-1]
        if self._get_data_event.is_set():
          self._get_data_event.clear()
          self._data_queue.put((refresh_period, timestamps))
          timestamps = []
      except Exception as e:
        self._data_queue.put(e)
        raise

  def _GetDataFromThread(self):
    self._get_data_event.set()
    ret = self._data_queue.get()
    if isinstance(ret, Exception):
      raise ret
    return ret

  from Core.Utils.adb_interface import AdbInterface
  from Core.Info.app import AppInfo
  a=AdbInterface()
  t=AppInfo()

  def _ClearSurfaceFlingerLatencyData(self):
    windwosname=self.t.getFocusedPackageAndActivity()
    result=self.a.SendShellCommand(
        'dumpsys SurfaceFlinger --latency-clear '+windwosname)
    return not len(result)

  def _GetSurfaceFlingerFrameData(self):
    windowsname=self.t.getFocusedPackageAndActivity()
    results = self.a.SendShellCommand(
        'dumpsys SurfaceFlinger --latency '+windowsname).split("\r\n")
    if not len(results):
      return (None, None)
    timestamps = []
    nanoseconds_per_second = 1e9
    refresh_period = long(results[0]) / nanoseconds_per_second
    pending_fence_timestamp = (1 << 63) - 1
    for line in results[1:]:
      fields = line.split()
      if len(fields) != 3:
        continue
      timestamp = long(fields[1])
      if timestamp == pending_fence_timestamp:
        continue
      timestamp /= nanoseconds_per_second
      timestamps.append(timestamp)
    return (refresh_period, timestamps)

  def _GetSurfaceStatsLegacy(self):
    result = self.a.SendShellCommand('service call SurfaceFlinger 1013')
    if "Operation not permitted" in result:
        results=self.a.SendShellCommand("su -k service call SurfaceFlinger 1013").split("\r\n")
    else:
        results=result.split("\r\n")
    match = re.search('^Result: Parcel\((\w+)', results[0])
    cur_surface = 0
    if match:
      try:
        cur_surface = int(match.group(1), 16)
      except Exception:
        logging.error('Failed to parse current surface from ' + match.group(1))
    else:
      logging.warning('Failed to call SurfaceFlinger surface ' + results[0])
    return {
        'page_flip_count': cur_surface,
        'timestamp': datetime.datetime.now(),
    }