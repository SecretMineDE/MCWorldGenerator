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
    child = pexpect.spawn('java -Xms2048M -Xmx2048M -jar server.jar nogui')
    child.logfile = sys.stdout.buffer
    child.expect('Done \(', timeout=None)
    child.sendline('fcp start %i world' % radius)
    child.expect('\[100\.0%\]', timeout=None)
    child.sendline('stop')
    child.expect('Stopping server', timeout=None)
    child.expect(pexpect.EOF, timeout=None)


def generateWorld(name, radius=1500):
    chdir_base()
    prepare()
    runServerAndGenerate(radius)
    saveWorld(name)


generateWorld("world2", 750)
generateWorld("world3", 500)
cleanup()