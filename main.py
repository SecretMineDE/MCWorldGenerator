#!/usr/bin/python

import sys
import pexpect
import time
import shutil
import os


def chdir_base():
    abspath = os.path.abspath(sys.argv[0])
    dname = os.path.dirname(abspath)
    os.chdir(dname)


def prepare():
    cleanup()
    shutil.copytree("server", "temp")


def cleanup():
    if os.path.exists("temp"):
        shutil.rmtree("temp")


def saveWorld(name):
    chdir_base()
    if not os.path.exists("output"):
        os.mkdir("output")
    shutil.copytree("temp/world", "output/" + name)


def runServerAndGenerate(radius=1500):
    os.chdir("temp")
    child = pexpect.spawn('java -Xms2048M -Xmx4096M -jar server.jar --nojline --log-strip-color --nogui')
    child.logfile = sys.stdout.buffer
    child.expect('Done \(', timeout=None)
    child.sendline('fcp start %i world' % radius)
    child.expect(r'Generating\sChunks:\s(\d+)\sof\s\1',
                 timeout=None)  # regex is ugly, but works.
    child.sendline('stop')
    child.expect('Stopping server', timeout=None)
    child.expect(pexpect.EOF, timeout=None)


def generateWorld(name, radius=1500):
    chdir_base()
    prepare()
    runServerAndGenerate(radius)
    saveWorld(name)


generateWorld("world2", 2000)
generateWorld("world3", 2000)
generateWorld("world4", 2000)
generateWorld("world5", 2000)
generateWorld("world6", 2000)
generateWorld("world7", 2000)
generateWorld("world8", 2000)
generateWorld("world9", 2000)
generateWorld("world10", 2000)
cleanup()
