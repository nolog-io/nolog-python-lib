# This is a bare-bones test to ensure that there are no crashes, dead-locks, and to test performance.
# The actual client test suite is language agnostic and available in a different repository.
from nolog_mp import NoLog
import time
import gc
import sys
from multiprocessing import Pool

def work(i):
  executionBlock1 = block1.Start()
  depExec1 = executionBlock1.StartDependency(dep1)
  depExec6 = executionBlock1.StartDependency(dep6)
  depExec5 = executionBlock1.StartDependency(dep5)
  depExec1.Success()
  depExec2 = executionBlock1.StartDependency(dep2)
  depExec2.Success()
  depExec3 = executionBlock1.StartDependency(dep3)
  depExec3.Success()
  depExec4 = executionBlock1.StartDependency(dep4)
  depExec4.Success()
  depExec6.Success()
  depExec5.Success()
  if i % 2 == 0:
    executionBlock1.Success()
  else:
    executionBlock1.Fail(blockAlert, "")

def prun(r):
  r_ = range(r)
  startTime = time.time()

  with Pool(10) as p:
    p.map(work, r_)
  endTime = time.time()
  gc.collect()
  print("+++ %.20f seconds +++" % (endTime - startTime))

def drun(r):
  i = 0
  startTime = time.time()

  while i < r:
    work(i)
    i = i + 1
  endTime = time.time()
  print("--- %.20f seconds ---" % (endTime - startTime))
  gc.collect()

if __name__ == "__main__":
  NoLog.Initialize("1", "2", "3", "local")

  block1 = NoLog.CreateObjective("Block1")
  blockAlert = block1.WithAlert("Sample alert")
  dep1 = block1.AddDependency("dep1", "ac")
  dep2 = block1.AddDependency("dep2", "ac")
  dep3 = block1.AddDependency("dep3", "ac")
  dep4 = block1.AddDependency("dep4", "ac")
  dep5 = block1.AddDependency("dep5", "ac")
  dep6 = block1.AddDependency("dep6", "ac")
  # for size in [10, 100, 1000,10000, 100000]:
  #   print("RUNNING SIZE %d ---" % (size))
  #   drun(size)
  print("#######################################################")
  print("# SKIPPING SINGLE-CORE-TESTS")
  print("# Single-Core Performance is very poor in MP lib.")
  print("# Use regular NoLog library for single-core.")
  print("#######################################################")
  
  for size in [10, 100, 1000,10000, 100000]:
    print("P-RUNNING SIZE %d ---" % (size))
    prun(size)

  print("FIN")
  # Wait for 1 print and then terminate test
  time.sleep(10)
  sys.exit(1)
