print("nolog_mp is an unsupported beta library")
import base64
import http.client
from http import HTTPStatus
import multiprocessing
from operator import truediv
import os
import re
from threading import Lock, Thread
from generated.source.proto.main.python.auth import auth_spec_pb2
from generated.source.proto.main.python.write import write_request_pb2
import time
from random import SystemRandom
from multiprocessing.managers import SyncManager

class _internal:
  _manager = multiprocessing.Manager()
  class validate:
    @staticmethod
    def cannot_be_none(o):
      if o is None:
        raise Exception("Invalid usage, arg cannot be None.")
      return o

  class error_bits:
    ERROR_BIT_DO_NOT_USE = 0
    ERROR_BIT_MULTIPLE_INITIALIZATION = 1
    ERROR_BIT_CLOSING_CLOSED_TRACKER = 2
    ERROR_BIT_OPEN_CHILD_OF_CLOSED_TRACKER = 4
    ERROR_BIT_CLOSING_TRACKED_AFTER_PARENT = 8
    ERROR_BIT_USED_UNREGISTERED_ALERT = 16
    ERROR_BIT_DUPLICATE_OBJECTIVE = 32
    ERROR_BIT_DUPLICATE_DEPENDENCY = 64
    ERROR_BIT_GC_BEFORE_CLOSING = 128
    ERROR_BIT_EMPTY_API_KEY = 256
    ERROR_BIT_INVALID_API_KEY = 512
    ERROR_BIT_MISSING_DEPENDENCY_TO_START_DEP = 1024
    ERROR_BIT_USED_UNREGISTERED_DEPENDENCY = 2048
  
  class notify_bits:
    NOTIFY_BIT_DO_NOT_USE = 0
    NOTIFY_BIT_SERVICE_ID_MISSING = 1
    NOTIFY_BIT_INSTANCE_ID_MISSING = 2
    NOTIFY_BIT_FORGOT_TO_INITIALIZE = 4
    NOTIFY_BIT_EMPTY_API_KEY = 8
    NOTIFY_BIT_INVALID_API_KEY = 16

  class errorhandler:
    def __init__(self):
      self.__errors = _internal._manager.list()
      self.__error_bits = multiprocessing.Value("i", 0)
      self.__notify_bits = multiprocessing.Value("i", 0)
      self.__lock = multiprocessing.Lock()
      
    def safe_get_errors(self):
      self.__lock.acquire()
      bits = self.__error_bits.value
      errors = []
      for err in self.__errors:
        errors.append(err)
      self.__lock.release()
      return bits, errors

    def safe_add_error(self, err: str, bit: int):
      if bit == _internal.error_bits.ERROR_BIT_DO_NOT_USE:
        raise Exception("Found invalid error bit: ERROR_BIT_DO_NOT_USE")
      self.__lock.acquire()
      if self.__error_bits.value & bit:
        self.__lock.release()
        return
      self.__error_bits.value |= bit
      self.__errors.append(err)
      self.__lock.release()

    def safe_notify(self, notification: str, bit: int):
      if bit == _internal.notify_bits.NOTIFY_BIT_DO_NOT_USE:
        raise Exception("Found invalid notify bit.")
      self.__lock.acquire()
      if self.__notify_bits.value & bit:
        self.__lock.release()
        return
      self.__notify_bits.value |= bit
      self.__lock.release()
      print("NoLog Notification: Initialization failed because " + notification)
    
    def safe_has_error(self):
      self.__lock.acquire()
      has_error = self.__error_bits.value > 0
      self.__lock.release()
      return has_error

  class alert:
    def __init__(self, core_alert: str, max_invocation_count:int, parent:"_internal.base_counter"):
      if parent == None:
        raise Exception("Parent cannot be NONE for alert")
      if core_alert is None:
        core_alert = "empty-string core alert"
      if len(core_alert) > 200:
        core_alert = core_alert[0:200-3]+"..." 
      self.__max_invocation_count = max_invocation_count
      self.__invocation_count = 0
      self.__count = multiprocessing.Value("i", 0)
      self.__samples = _internal._manager.list()
      self.__last_count = 0
      self.__last_samples = []
      self.__parent = parent
      self.__core_alert = core_alert
      self.__last_timestamp = 0

    def get_core_alert(self):
      return self.__core_alert

    def safe_with_context(self, caller, context:str):
      if caller != self.__parent:
        return False
      if context is None:
        context = ""
      if len(context) > 1000:
        context = context[0:1000-3]+"..."
      self.__count.get_lock().acquire()
      count = self.__count.value
      self.__count.value = count + 1
      self.__count.get_lock().release()
      if count < 300 and count % 100 == 0:
        self.__samples.append(context)
      return True
    
    def safe_sample_alerts(self):
      self.__count.get_lock().acquire()
      count = self.__count.value
      if self.__invocation_count == 0 and count == 0:
        self.__count = 0
      self.__count.get_lock().release()
      if self.__invocation_count == 0:
        if count == 0:
          return False, None, None, None
        self.__last_samples = []
        for sample in self.__samples:
          self.__last_samples.append(sample)
        self.__last_count = count
        self.__last_timestamp = int(time.time())
        self.__samples = _internal._manager.list()
      self.__invocation_count = (self.__invocation_count + 1)%self.__max_invocation_count
      return True, self.__last_samples, self.__last_count, self.__last_timestamp

  class base_counter:
    def __init__(self, name, nolog_init, failure_window: int, parent=None, action=None):
      self.__name = name
      self.__action = action
      self.__lock = Lock()
      self.__nolog_init = nolog_init
      self.__failure_window = failure_window
      self.__successful = multiprocessing.Value("i", 0)
      self.__failing = multiprocessing.Value("i", 0)
      self.__success_history = []
      self.__failing_history = []
      self.__errors = _internal.errorhandler()
      self.__parent = parent
      self.__children = {}
      self.__alerts = []
    
    def get_parent(self):
      return self.__parent
      
    def safe_with_alert(self, core_alert: str, max_invocation_count:int):
      alert = _internal.alert(core_alert, max_invocation_count, self)
      self.__lock.acquire()
      self.__alerts.append(alert)
      self.__lock.release()
      return alert
    
    def proto_data(self):
      self.__successful.get_lock().acquire()
      self.__failing.get_lock().acquire()
      successful = self.__successful.value 
      self.__successful.value=0
      self.__successful.get_lock().release()
      failing = self.__failing.value 
      self.__failing.value=0
      self.__failing.get_lock().release()
      self.__success_history.append(successful)
      self.__failing_history.append(failing)
      history_size = len(self.__failing_history)
      if history_size > self.__failure_window:
        newStartIndex = history_size-self.__failure_window
        self.__success_history = self.__success_history[newStartIndex:history_size]
        self.__failing_history = self.__failing_history[newStartIndex:history_size]
      success = True
      for failed in self.__failing_history:
        if failed > 0:
          success = False
          break
      children = []
      for child in self.__children:
        children.append(self.__children[child])
      alerts = []
      for alert in self.__alerts:
        alerts.append(alert)
      return self.__name, self.__action, success, successful, failing, children, alerts
    
    def safe_add_child(self, name, action, failure_window):
      key = name+":"+action
      self.__lock.acquire()
      if key in self.__children:
        self.get_errors().safe_add_error(
          "Called AddDependency multiple times with same name:action (%s)" % key,
          _internal.error_bits.ERROR_BIT_DUPLICATE_DEPENDENCY)
      else:
        bc = _internal.base_counter(name, self.__nolog_init, failure_window, self, action)
        self.__children[key] = bc
      bc = self.__children[key]
      self.__lock.release()
      return bc

    def safe_update_init(self, is_initialized:bool):
      self.__lock.acquire()
      self.__nolog_init = is_initialized
      children = self.__children.copy()
      self.__lock.release()
      for child in children:
        child:_internal.base_counter
        child.safe_update_init(is_initialized)
    
    def safe_increment(self, inc_success, inc_fail):
      if inc_success > 0:
        self.__successful.get_lock().acquire()
        self.__successful.value+=inc_success
        self.__successful.get_lock().release()
      if inc_fail > 0:
        self.__failing.get_lock().acquire()
        self.__failing.value+=inc_fail
        self.__failing.get_lock().release()
      
    def get_errors(self):
      return self.__errors
    
    def safe_start(self):
      self.__lock.acquire()
      if self.__nolog_init == False:
        self.__lock.release()
        self.__errors.safe_notify(
          "Did you forget to Initialize NoLog? Found %s.start() call before nolog.Initialize()" % self._name,
          _internal.notify_bits.NOTIFY_BIT_FORGOT_TO_INITIALIZE)
        return _internal.tracker._disabled_tracker
      self.__lock.release()
      return _internal.tracker(self)

  class tracker():
    _disabled_tracker = None
    __bit_closed = 2

    def __init__(self, parent:"_internal.base_counter", disabled:bool=False):
      self.__lock = Lock()
      self.__parent = parent
      self.__closed_states = multiprocessing.Value("i", 0)
      self.__disabled = disabled
      self.__children = []
    
    def error_parent(self):
      return self.__parent.get_parent() if self.__parent.get_parent() is not None else self.__parent

    def __safe_parent_closed(self):
      closed = self.__closed_states.value & _internal.tracker.__bit_closed > 0
      if not closed:
          self.error_parent().get_errors().safe_add_error(
            "Bad Monitoring State: Objective Tracker closed before DependencyTracker.",
            _internal.error_bits.ERROR_BIT_OPEN_CHILD_OF_CLOSED_TRACKER)

    def __unsafe_close_children(self):
      for child in self.__children:
        child:_internal.tracker
        child.__safe_parent_closed()
      self.__children.clear()
    
    def safe_success(self):
      if self.__disabled:
        return
      self.__closed_states.get_lock().acquire()
      self.__unsafe_close_children()
      if self.__closed_states.value & _internal.tracker.__bit_closed > 0:
        self.__closed_states.get_lock().release()
        self.error_parent().get_errors().safe_add_error(
          "Bad Monitoring State: Tracker closed twice, success() called on closed Tracker.",
          _internal.error_bits.ERROR_BIT_CLOSING_CLOSED_TRACKER)
        return
      self.__closed_states.value |= _internal.tracker.__bit_closed
      self.__closed_states.get_lock().release()
      self.__parent.safe_increment(1, 0)

    def safe_fail(self, alert: "_internal.alert", context:str):
      if self.__disabled:
        return
      self.__closed_states.get_lock().acquire()
      self.__unsafe_close_children()
      if self.__closed_states.value & _internal.tracker.__bit_closed > 0:
        self.__closed_states.get_lock().release()
        self.error_parent().get_errors().safe_add_error(
          "Bad Monitoring State: Tracker closed twice, fail() called on closed Tracker.",
          _internal.error_bits.ERROR_BIT_CLOSING_CLOSED_TRACKER)
        return
      self.__closed_states.value |= _internal.tracker.__bit_closed
      self.__closed_states.get_lock().release()
      self.__parent.safe_increment(0, 1)
      if alert is not None:
        if not alert.safe_with_context(self.__parent, context):
          self.error_parent().get_errors().safe_add_error(
            "Tried to fail() with unregistered Alert: %s" % alert.get_core_alert(),
            _internal.error_bits.ERROR_BIT_USED_UNREGISTERED_ALERT)

    def safe_start(self, parent:"_internal.base_counter"):
      if self.__disabled:
        return self
      if self.__parent != parent.get_parent():
        self.error_parent().get_errors().safe_add_error(
          "Tried to start tracking an unregistered Dependency for Objective."
          ,_internal.error_bits.ERROR_BIT_USED_UNREGISTERED_DEPENDENCY)
        return _internal.tracker._disabled_tracker
      tracker = _internal.tracker(parent)
      self.__lock.acquire()
      self.__children.append(tracker)
      self.__lock.release()
      return tracker
    
    def __del__(self):
      if self.__disabled:
        return
      closed = self.__closed_states.value & _internal.tracker.__bit_closed > 0
      self.__unsafe_close_children()
      if not closed:
        self.error_parent().get_errors().safe_add_error(
          "Tracking garbage collected before closing. Did you forget to success()/fail()?",
          _internal.error_bits.ERROR_BIT_GC_BEFORE_CLOSING)

class Alert():
  def __init__(self, alert):
    self._alert = _internal.validate.cannot_be_none(alert)

class Dependency():
    '''Dependency tracks out-of-process entities (e.g. other services, databases, or agents) that an Objective relies on.'''

    def __init__(self, base_counter:_internal.base_counter):
        self._base_counter = _internal.validate.cannot_be_none(base_counter)

    def WithAlert(self, alert: str):
      """Statically define alerts (max: 200 chars) expected to be triggered when facing problems fulfilling this Objective.
      Objective and Dependency metadata is automatically added to the Alert and does not need to be included in the
      actual alert message.
      """
      if os.getpid() != NoLog._pid:
        raise Exception("WithAlert must be called from same Process as NoLog.Initialize()")
      return Alert(self._base_counter.safe_with_alert(alert, 3))


class DependencyTracker():
  '''Dependency measures the success rate of calling a dependency and helps trigger alrets in the event of a failure.'''

  def __init__(self, tracker:_internal.tracker):
    self.__tracker = _internal.validate.cannot_be_none(tracker)

  def Success(self):
    """Success is used to mark the DependencyTracker as successfully completed.
    
    Calling Success() or Fail(...) marks this DependencyTracker as closed.
    The following result in error states that will (1) stop tracking the Objective and (2) Surface an alert on the dashboard whne possible:
      - Success() or Fail(...) is invoked again on a closed Tracker.
      - Any tracker is garbage collected without a Success() or Fail(...) call.
    """
    self.__tracker.safe_success()

  def Fail(self, alert: Alert, errorMsg: str):
    """Fail lets nolog know of the failure and the alert to display on the dashboard. Error messages (max: 1000 chars) passed to Fail() will be sampled
    before being sent onwards.
    
    Calling Success() or Fail(...) marks this DependencyTracker as closed. 
    The following result in error states that will (1) stop tracking the Objective and (2) Surface an alert on the dashboard when possible:
      - Success() or Fail(...) is invoked again on a closed Tracker.
      - This tracker is garbage collected without a Success() or Fail(...) call."""
    return self.__tracker.safe_fail(None if alert is None else alert._alert, errorMsg)

class ObjectiveTracker():
  '''ObjectiveTracker tracks a single fulfillment of a given Objective.'''

  def __init__(self, tracker:_internal.tracker):
    self.__tracker = _internal.validate.cannot_be_none(tracker)

  def Success(self):
    """Success is used to mark the ObjectiveTracker as successfully completed.

    Calling Success() or Fail(...) marks this ObjectiveTracker as closed.
    The following result in error states that will (1) stop tracking the Objective and (2) Surface an alert on the dashboard when possible:
      - Success() or Fail(...) is invoked again on a closed Tracker.
      - Any dependencies tracking started as part of this objective aren't already closed via Success() or Fail(...) calls.
      - Any tracker is garbage collected without a Success() or Fail(...) call.
    """
    self.__tracker.safe_success()

  def Fail(self, alert: Alert, errorMsg: str):
    """Fail lets nolog know of the failure and the alert to display on the dashboard. Error messages (max: 1000 chars) passed to Fail() will be sampled
    before being sent onwards.

    Calling Success() or Fail(...) marks this ObjectiveTracker as closed.
    The following result in error states that will (1) stop tracking the Objective and (2) Surface an alert on the dashboard when possible:
      - Success() or Fail(...) is invoked again on a closed Tracker.
      - Any dependencies tracking started as part of this objective aren't already closed via Success() or Fail(...) calls.
      - This tracker is garbage collected without a Success() or Fail(...) call.
    """
    self.__tracker.safe_fail(None if alert is None else alert._alert, errorMsg)
  
  def StartDependency(self, dep: Dependency):
    if dep is None:
      self.__tracker.error_parent().get_errors().safe_add_error(
        "Tried to StartDependency() without dependency (NULL).",
        _internal.error_bits.ERROR_BIT_MISSING_DEPENDENCY_TO_START_DEP)
      return _internal.tracker._disabled_tracker
    return DependencyTracker(self.__tracker.safe_start(dep._base_counter))

class Objective():
  """Objective represents a monitored service goal.
  Each service goal is registered once via a nolog.CreateObjective or nolog.CreateObjective and an
  Objective is returned to be used in code for monitoring.

  ```
  import nolog

  respondHelloObjective = NoLog.CreateObjective("RespondHello", OptConfigData(
    AlertCriteriaProvider = NoLog.CreateFailCountCriteriaProvider(1, 6)
  ))

  def respondHello(name):
    respondHello = respondHelloObjective.start()
    result = "Hello " + name + "!"
    respondHello.success()
    return result
  ```

  Any dependencies that the Objective relies on and any alerts that may be surfaced should be defined here as well.
  ```
  import nolog

  respondHelloObjective = NoLog.CreateObjective("RespondHello", OptConfigData(
    AlertCriteriaProvider = NoLog.CreateFailCountCriteriaProvider(1, 6)
  ))
  unsupportedNameAlert = respondHelloObjective.WithAlert("Unsupported name, starts with A.")
  lastNameServiceDep = respondHelloObjective.AddDependency("lastNameService")

  def respondHello(name):
    respondHello = respondHelloObjective.start()
    if name.startsWith("a") or name.startsWith("A"):
            respondHello.Fail(unsupportedNameAlert, name)
      return ""
    callLastName = lastNameServiceDep.start()
    lastName = getLastName(name)
    callLastName.success()
    result = "Hello " + name + " " + lastName + "!"
    respondHello.success()
    return result
  ```
  """

  def __init__(self, base_counter:_internal.base_counter):
    self._base_counter = base_counter

  def AddDependency(self, name: str, action: str):
    if os.getpid() != NoLog._pid:
      raise Exception("AddDependency must be called from same Process as NoLog.Initialize()")
    """Add a Dependency to this Objective used for tracking.
    Arguments:
      - dependency: the name of the dependency (max: 40 chars)
      - action: 		a description of the the feature of the dependency being relied on. (max: 40 chars)

    The three recommended approaches for action are to either:
      - 1: Pass in either a simple-descriptor for the work being performed by the dependency
        * ```AddDependency("AccountAPI", "GetOwnerFromAccount")```
      - 2: the descriptive HTTP path exposed by the dependency.
        * ```AddDependency("AccountAPI", "/get-account")```
      - 3: in the event of a database, the the table name being relied on.
        * ```AddDependency("MySqlDatabase", "Accounts")```
    """
    if name is None or name == "":
      name = "UNKNOWN"
    
    if action is None or action == "":
      action = "UNKNOWN"
    
    if len(name) > 40:
      name = name[0:(40-3)]+"..."
    
    if len(action) > 40:
      action = action[0:(40-3)]+"..."

    dep_counter = self._base_counter.safe_add_child(name, action, 6)
    return Dependency(dep_counter)

  def WithAlert(self, alert: str):
    """Statically define alerts (max: 200 chars) expected to be triggered when facing problems fulfilling this Objective.
      Objective metadata is automatically added to the Alert and does not need to be included in the actual alert message.
    """
    if os.getpid() != NoLog._pid:
      raise Exception("WithAlert must be called from same Process as NoLog.Initialize()")
    return Alert(self._base_counter.safe_with_alert(alert, 3))

  def Start(self):
    return ObjectiveTracker(self._base_counter.safe_start())

class NoLog:
  class _env_bit:
    STD = 0
    LOCAL = 1
    PERFORMANCE = 2
    PRODUCTION = 4

  __reserved_block_name = "NoLogDefault" 
  __mutex = Lock()
  __initialized = False
  __objectives = {}
  __errors = _internal.errorhandler()
  __service_id = ""
  __instanceId = ""
  __versionId = ""
  __raw_key = None
  __key = None
  __env=_env_bit.STD
  __target = None
  __shard = "0"
  __shard_token = "init"
  _pid = os.getpid()

  @staticmethod
  def __trim(name: str, length: int):
    if len(name) > length:
      return name[0:(length-3)]+"..."
    return name

  @staticmethod
  def __unsafe_create_base_proto():
    w = write_request_pb2.WriteRequest(
      ids=write_request_pb2.ServiceInstanceIdentifier(
        service_id=NoLog.__service_id,
        instance_id=NoLog.__instanceId,
        version_id=NoLog.__versionId,
      ),
      creation_timestamp=write_request_pb2.Timestamp(
        utc_creation_time=int(time.time())
      ),
      raw_information=write_request_pb2.WriteRequest.RawInformation(
        blocks=[],
      )
    )
    return w

  @staticmethod
  def __report():
    if NoLog.__errors.safe_has_error():
      return
      
    NoLog.__mutex.acquire()
    w = NoLog.__unsafe_create_base_proto()
    objectives = NoLog.__objectives.values()
    NoLog.__mutex.release()
    for obj in objectives:
      obj:Objective
      obj_name, _, obj_is_successful, obj_successful, obj_failing, obj_children, obj_alerts = obj._base_counter.proto_data()
      critical_block = write_request_pb2.WriteRequest.RawInformation.CriticalBlock(
        name=obj_name,
        counts=write_request_pb2.WriteRequest.RawInformation.Counts(
          success=obj_successful,
          failed=obj_failing
        ),
        block_dependency=[],
        state=write_request_pb2.STATE_ALL_OK if obj_is_successful else write_request_pb2.STATE_CRITICAL_FAILURE,
        alerts=[]
      )
      obj_error_bits, obj_errors = obj._base_counter.get_errors().safe_get_errors()
      if obj_error_bits > 0:
        critical_block.alerts.append(write_request_pb2.AlertInformation(
          core_alert="Objective misconfigured.",
          sampled_content=[],
          total_count=len(obj_errors),
          timestamp=int(time.time())
        ))
        for err in obj_errors:
          critical_block.alerts[0].sampled_content.append(err)
      else:
        for dep in obj_children:
          dep:_internal.base_counter
          dep_name, dep_action, dep_is_successful, dep_successful, dep_failing, _, dep_alerts = dep.proto_data()
          blockDep = write_request_pb2.WriteRequest.RawInformation.CriticalBlock.BlockDependency(
            dependency=dep_name,
            action=dep_action,
            counts=write_request_pb2.WriteRequest.RawInformation.Counts(
              success=dep_successful,
              failed=dep_failing
            ),
            state=write_request_pb2.STATE_ALL_OK if dep_is_successful else write_request_pb2.STATE_CRITICAL_FAILURE,
            alerts=[]
          )
          if not dep_is_successful and critical_block.state != write_request_pb2.STATE_ALL_OK:
            critical_block.state = write_request_pb2.STATE_DEPENDENCY_FAILURE
          for alert in dep_alerts:
            alert:_internal.alert
            needs_reporting, samples, count, timestamp = alert.safe_sample_alerts()
            if not needs_reporting:
              continue
            blockDep.alerts.append(write_request_pb2.AlertInformation(
              timestamp=timestamp,
              core_alert=alert.get_core_alert(),
              sampled_content=samples,
              total_count=count
            ))
          critical_block.block_dependency.append(blockDep)
        for alert in obj_alerts:
            alert:_internal.alert
            needs_reporting, samples, count, timestamp = alert.safe_sample_alerts()
            if not needs_reporting:
              continue
            blockDep.alerts.append(write_request_pb2.AlertInformation(
              timestamp=timestamp,
              core_alert=alert.get_core_alert(),
              sampled_content=samples,
              total_count=count
            ))
      w.raw_information.blocks.append(critical_block)
    if len(w.raw_information.blocks) == 0:
      w.raw_information.blocks.append(write_request_pb2.WriteRequest.RawInformation.CriticalBlock(
        name=NoLog.__reserved_block_name,
        block_dependency=[],
        state=write_request_pb2.STATE_NO_DATA,
      ))
    NoLog.__write_report_with_retry(w, 0)
    return

  class _retry_status_codes:
    ALL_GOOD = 0
    RETRY = 1
    BAD = 2

  @staticmethod
  def __write_report_with_retry(w:write_request_pb2.WriteRequest, attempt:int):
    if attempt >= 2:
      return
    if w == None:
      raise Exception("This should never happen, tried to __write_report_with_retry with nil data.")
    if NoLog.__write_report(w) == NoLog._retry_status_codes.RETRY:
      r = SystemRandom()
      time.sleep(r.random(0, 2))
      NoLog.__write_report_with_retry(w, attempt+1)

  @staticmethod
  def __write_report(w:write_request_pb2.WriteRequest):
    if NoLog.__env == NoLog._env_bit.STD:
      print(w)
      return NoLog._retry_status_codes.ALL_GOOD
    w.shard_info = write_request_pb2.WriteRequest.ShardInfo()
    w.shard_info.shard_token = NoLog.__shard_token
    target = NoLog.__target
    if NoLog.__env != NoLog._env_bit.LOCAL:
      target = target % NoLog.__shard
    target = target + "/be/write"
    basicToken = "Basic " + NoLog.__raw_key
    r = http.client.HTTPSConnection(target, timeout=4) if NoLog.__env is not NoLog._env_bit.LOCAL else http.client.HTTPConnection(target, timeout=4)
    r.putheader ("Authorization", basicToken)
    r.request(method="POST", body=w.SerializeToString())
    rr = r.getresponse()
    rrPb = write_request_pb2.WriteResponse()
    if rrPb.ParseFromString(r.getresponse().read()) == 0:
      return NoLog._retry_status_codes.RETRY
    if (rrPb.IsInitialized() and
      (rrPb.write_status == write_request_pb2.WriteResponseCode.FAILURE_APIKEY_CANNOT_DECRYPT or
       rrPb.write_status == write_request_pb2.WriteResponseCode.FAILURE_APIKEY_CANNOT_UNBASE64 or
       rrPb.write_status == write_request_pb2.WriteResponseCode.FAILURE_APIKEY_CANNOT_UNMARSHAL or
       rrPb.write_status == write_request_pb2.WriteResponseCode.FAILURE_APIKEY_EXPIRED or
       rrPb.write_status == write_request_pb2.WriteResponseCode.FAILURE_APIKEY_MISSING_FIELD or
       rrPb.write_status == write_request_pb2.WriteResponseCode.FAILURE_APIKEY_INVALID)):
      return NoLog._retry_status_codes.BAD
    if rr.getcode() != HTTPStatus.OK:
      return NoLog._retry_status_codes.RETRY
    if rrPb.WhichOneof('shardstate') == "ok":
      if rrPb.ok():
        return NoLog._retry_status_codes.ALL_GOOD
      else:
        return NoLog._retry_status_codes.RETRY
    elif rrPb.WhichOneof('shardstate') == "update_shard":
      if rrPb.update_shard.shard.isnumeric:
        NoLog.__shard = rrPb.update_shard.shard
        NoLog.__shard_token = rrPb.update_shard.shard_token
      else:
        NoLog.__shard = "0"
        NoLog.__shard_token = "pynonnumeric"
    return NoLog._retry_status_codes.RETRY

  @staticmethod
  def __start__reporting():
    r = SystemRandom()
    time.sleep(r.randint(0, 2))
    lastExec = time.time()
    while True:
      now = time.time()
      while now - lastExec < 10: 
        time.sleep(1)
        now = time.time()
      lastExec = now
      NoLog.__report()

  @staticmethod
  def Initialize(serviceId: str, instanceId: str, versionId: str, noLogConfig: str):
    """Initialize needs to be called in main() before the program begins monitoring with NoLog.

    Args:
        serviceId (str): The name or ID of the service being monitored. All instances for the same service should use the same identifier. (max: 40 chars)
        instanceId (str): A unique instance identifier so two different instances can be differentiated. (max: 40 chars)
        versionId (str): An ID to track the version of the software running. This is a means to disambiguiate instances running different versions of the code. (max: 10 chars)
        noLogConfig (str): NoLog API Key. Use PROD key for Production, DEV Key for Non-Prod, and "" for Local.
    """
    if noLogConfig is not None and len(noLogConfig) > 5000:
      noLogConfig = noLogConfig[0:5000]
    NoLog.__mutex.acquire()
    if NoLog.__initialized:
      NoLog.__mutex.release()
      NoLog.__errors.safe_add_error(
        "nolog.Initialize() should only be called once.",
        _internal.error_bits.ERROR_BIT_MULTIPLE_INITIALIZATION)
      return
    if noLogConfig == "":
      NoLog.__mutex.release()
      NoLog.__errors.safe_notify(
        "Cannot initialize NoLog with empty key",
        _internal.notify_bits.NOTIFY_BIT_EMPTY_API_KEY
      )
      NoLog.__errors.safe_add_error(
        "Cannot initialize NoLog with empty key",
        _internal.error_bits.ERROR_BIT_EMPTY_API_KEY)
      return
    if serviceId == None or len(serviceId) == 0:
      NoLog.__mutex.release()
      NoLog.__errors.safe_notify(
        "ServiceID is missing.",
        _internal.notify_bits.NOTIFY_BIT_SERVICE_ID_MISSING)
      return
    if instanceId == None or len(instanceId) == 0:
      NoLog.__mutex.release()
      NoLog.__errors.safe_notify(
        "InstanceId is missing.",
        _internal.notify_bits.NOTIFY_BIT_INSTANCE_ID_MISSING)
      return
    NoLog.__service_id = NoLog.__trim(serviceId, 40)
    NoLog.__instanceId = NoLog.__trim(instanceId, 40)
    NoLog.__versionId = NoLog.__trim(versionId, 10)
    NoLog.__initialized = True
    for obj in NoLog.__objectives.values():
      obj:Objective
      obj._base_counter.safe_update_init(NoLog.__initialized)
    NoLog.__raw_key = noLogConfig
    NoLog.__key = auth_spec_pb2.ClientKey()
    if not noLogConfig == "local":
      if NoLog.__key.ParseFromString(base64.decodebytes(noLogConfig)) == 0:
        NoLog.__errors.safe_notify(
          "Cannot initialize NoLog with invalid API key",
          _internal.notify_bits.NOTIFY_BIT_INVALID_API_KEY)
        NoLog.__errors.safe_add_error(
          "Cannot initialize NoLog with invalid API key",
          _internal.error_bits.ERROR_BIT_INVALID_API_KEY)
        return 
      keyregex = re.compile(r".ne")
      envs = {
        "LOCAL": NoLog._env_bit.LOCAL,
        "PERFORMANCE": NoLog._env_bit.PERFORMANCE,
        "PRODUCTION": NoLog._env_bit.PRODUCTION
      }
      targets = {
        NoLog._env_bit.LOCAL: "http://localhost:8080",
        NoLog._env_bit.PERFORMANCE: "https://performance.nolog.io/writer%s",
        NoLog._env_bit.PRODUCTION: "https://nolog.io/writer%s"
      }
      env_found = False
      for key, value in NoLog.__key.key_fields.items():
        if keyregex.fullmatch(key):
          NoLog.__env = envs[value]
          NoLog.__target = targets[NoLog.__env]
          env_found = True
          break
      if not env_found:
        NoLog.__mutex.release()
        NoLog.__errors.safe_notify(
          "Cannot initialize NoLog with invalid API key",
          _internal.notify_bits.NOTIFY_BIT_INVALID_API_KEY)
        NoLog.__errors.safe_add_error(
          "Cannot initialize NoLog with invalid API key",
          _internal.error_bits.ERROR_BIT_INVALID_API_KEY)
        return
    report_thread = Thread(target=NoLog.__start__reporting)
    report_thread.setDaemon(True)
    report_thread.start()
    NoLog.__mutex.release()

  @staticmethod
  def CreateObjective(name: str):
    if os.getpid() != NoLog._pid:
      raise Exception("CreateObjective must be called from same Process as NoLog.Initialize()")
    """CreateObjective returns an Objective (max: 40 chars) used for monitoring a Service objective.
    This should be called once to register the Objective:
    ```
      import nolog

      respondHelloObjective = NoLog.CreateObjective("RespondHello")

      def respondHello(name):
        respondHello = respondHelloObjective.start()
        result = "Hello " + name + "!"
        respondHello.success()
        return result
    ```
    """
    if name == None or len(name) == 0:
      name = "UNKNOWN"
    if name.startswith("nolog"):
      name = "custom-"+name
    if len(name) > 40:
      name = name[0:(40-3)]+"..."
    NoLog.__mutex.acquire()
    obj:Objective = NoLog.__objectives.get(name)
    if obj is None:
      obj = Objective(_internal.base_counter(name, NoLog.__initialized, 6))
      NoLog.__objectives[name]=obj
    else:
      obj._base_counter.get_errors().safe_add_error(
        "Called CreateObjective multiple times with same 'name'. Disabling tracking of Objective.",
        _internal.error_bits.ERROR_BIT_DUPLICATE_OBJECTIVE)
    NoLog.__mutex.release()
    return obj

def _setup():
  _internal.tracker._disabled_tracker = _internal.tracker(None, disabled=True)
_setup()
