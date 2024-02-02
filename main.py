#!/usr/bin/python

import sys
import pexpect
import time
import shutil
import os
import re

TARGET_WORLD_NAME = os.getenv("WORLD_NAME", "world")
TARGET_WORLD_RADIUS = int(os.getenv("WORLD_RADIUS", 1000))
TARGET_ADD_SEED = os.getenv("TARGET_ADD_SEED", "true").lower() == "true"
TARGET_ADD_RADIUS = os.getenv("TARGET_ADD_RADIUS", "true").lower() == "true"

BASE_DIR = os.getenv("BASE_DIR", "/base")
TARGET_DIR = os.getenv("TARGET_DIR", "/output")
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/world")

JAVA_XMX = os.getenv("JAVA_XMX", "4096M")
JAVA_XMS = os.getenv("JAVA_XMS")

WORLD_SEED = "0"

if TARGET_WORLD_RADIUS is None or TARGET_WORLD_NAME is None:
    print("Not all arguments given")
    exit(1)


def chdir_base():
    os.makedirs(TEMP_DIR, exist_ok=True)
    os.chdir(TEMP_DIR)


def prepare():
    cleanup()
    shutil.copytree(BASE_DIR, TEMP_DIR)


def cleanup():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


def saveWorld(name, seed=None):
    print("Copying world to output...")
    chdir_base()

    final_target_dirname = name
    if TARGET_ADD_RADIUS:
        final_target_dirname += "_r" + str(TARGET_WORLD_RADIUS)

    if seed is not None and TARGET_ADD_SEED:
        final_target_dirname += "_" + str(seed)

    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR, exist_ok=True)
    shutil.copytree(os.path.join(TEMP_DIR, "world"), os.path.join(TARGET_DIR, final_target_dirname))
    print("done.")


def runServerAndGenerate(radius=1500, xmx="2048M", xms=None):
    if xms is None:
        xms = xmx

    os.chdir(TEMP_DIR)
    child = pexpect.spawn('java -Xms' + xms + ' -Xmx' + xmx + ' -jar server.jar --nogui --nojline')
    child.logfile = sys.stdout.buffer
    child.expect(r'Done \(', timeout=None)
    child.sendline('seed')
    child.expect(r'Seed: \[.*\]')
    seed_line = child.after
    child.sendline('chunky spawn')
    child.sendline('chunky shape circle')
    child.sendline('chunky radius ' + str(radius))
    child.sendline('chunky start')
    child.expect(r'\[Chunky\] Task finished for ', timeout=None)  # regex is ugly, but works.
    child.sendline('stop')
    child.expect('Stopping server', timeout=None)
    child.expect(pexpect.EOF, timeout=None)

    # remove console colors
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    seed_result = re.search(r'Seed: \[(-?\d+)\]', ansi_escape.sub('', seed_line.decode('utf-8')))
    seed = None
    if seed_result is not None and len(seed_result.groups()) == 1:
        seed = seed_result.group(1)
        print("Found seed:", seed)

    return seed


chdir_base()
prepare()
seed = runServerAndGenerate(radius=TARGET_WORLD_RADIUS, xmx=JAVA_XMX, xms=JAVA_XMS)
saveWorld(TARGET_WORLD_NAME, seed)
cleanup()
