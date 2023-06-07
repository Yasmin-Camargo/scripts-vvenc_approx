import subprocess
import os
import itertools
import time
import sys

from datetime import datetime

# Main settings
HOME = '/home/pc-hegel/Documentos/experimentos-2023'

# Output files
LOGS_BASE = HOME + '/outputs/logs-pin'
BINARY_OUTPUT = HOME + "/outputs/bitstreams"

if not os.path.isdir(LOGS_BASE):
    os.mkdir(LOGS_BASE)

if not os.path.isdir(BINARY_OUTPUT):
    os.mkdir(BINARY_OUTPUT)

# PIN
PIN_BASE = HOME + '/pin/pin3.19'
PIN_TOOL_BASE = HOME + \
    '/pin/error_injection_pintool_levels_final_2021_version_yas/obj-intel64/memapprox-efficient-bitdepth.so'
PIN_CMD = PIN_BASE + '/pin'

# VTM
VTM_BASE = HOME + '/vvenc-approx'
ENCODERAPP = VTM_BASE + '/bin/release-shared/vvencFFapp'
CFG_BASE = VTM_BASE + '/cfg'

CFGS = (
        #"randomaccess_faster.cfg",
        #"randomaccess_fast.cfg",
        "randomaccess_medium.cfg",
        #"randomaccess_slow.cfg",
        #"randomaccess_slower.cfg",
        )

PER_SEQUENCE_CFG_BASE = VTM_BASE + '/cfg/per-sequence'
# VIDEOS_BASE = HOME + '/../Videos'
VIDEOS_BASE = HOME + '/videos'
VIDEOS = [
    'BQMall_832x480_60.yuv',
    'BasketballDrill_832x480_50.yuv',
    'RaceHorsesC_832x480_30.yuv',
    'PartyScene_832x480_50.yuv',
    
    #'BQSquare_416x240_60.yuv',
    #'RaceHorses_416x240_30.yuv',
    #'BasketballDrive_1920x1080_50.yuv',
]

# Max number of instances running in parallel
MAX_PROCS_PARALLEL = 4

# Parameters
QP_LEVELS = [
    '22',
    '27',
    '32',
    '37'
]
REPETITIONS = 10
FRAMES = '17'

# BERs = [
#     ('0',	  '0'),	    ('0',	  '1E-03'),	('0',	  '1E-04'),
#     ('0',     '1E-05'),	('0',	  '1E-06'),	('0',	  '1E-07'),
#     ('1E-03', '0'),	    ('1E-03', '1E-03'),	('1E-03', '1E-04'),
#     ('1E-03', '1E-05'),	('1E-03', '1E-06'),	('1E-03', '1E-07'),
#     ('1E-04', '0'),	    ('1E-04', '1E-03'),	('1E-04', '1E-04'),
#     ('1E-04', '1E-05'),	('1E-04', '1E-06'),	('1E-04', '1E-07'),
#     ('1E-05', '0'),	    ('1E-05', '1E-03'),	('1E-05', '1E-04'),
#     ('1E-05', '1E-05'),	('1E-05', '1E-06'),	('1E-05', '1E-07'),
#     ('1E-06', '0'),	    ('1E-06', '1E-03'),	('1E-06', '1E-04'),
#     ('1E-06', '1E-05'),	('1E-06', '1E-06'),	('1E-06', '1E-07'),
#     ('1E-07', '0'),	    ('1E-07', '1E-03'),	('1E-07', '1E-04'),
#     ('1E-07', '1E-05'),	('1E-07', '1E-06'),	('1E-07', '1E-07')
# ]

BERs = [('0', '0'), ('1E-03', '1E-03'), ('1E-04', '1E-04'), ('1E-05', '1E-05'), ('1E-06', '1E-06'), ('1E-07', '1E-07')]
#BERs = [('0', '0'), ('1E-07', '1E-07')]

def getCurrentBranch():
    os.chdir(VTM_BASE)
    output = os.popen('git status').read()
    currentBranch = output.split()[2]
    os.chdir(f'{HOME}/scripts')
    return currentBranch

def is_log_complete(log_path):
    if not os.path.isfile(log_path):
        return False

    with open(log_path) as log:
        lines = log.read().splitlines()

        # Return false if the file is empty
        if len(lines) == 0:
            return False

        last_line = lines[-1]

        # If the execution ended correctly, the last line will display the total time
        return True if "Total" in last_line else False


processes = list()

simtotal = len(VIDEOS) * len(QP_LEVELS) * len(BERs) * REPETITIONS * len(CFGS)
simrun = 0

print(f'[{datetime.now():(%d/%m) %H:%M:%S}] Starting simulation of {simtotal} processes')

simlogfile = open(f'{LOGS_BASE}/simulation.log', 'w')
line = 'branch\tvideo\tcfg\tqp_level\tread_ber\twrite_ber\trepetition\n'
simlogfile.write(line)

simdetailedlogfile = open(f'{LOGS_BASE}/simulation_detailed.log', 'w')
line = 'branch\tvideo\tcfg\tqp_level\tread_ber\twrite_ber\trepetition\n'
simdetailedlogfile.write(line)


for product in itertools.product(VIDEOS, CFGS, QP_LEVELS, BERs, range(REPETITIONS)):
    video, cfg, qp, bers, repetition = product
    read_ber, write_ber = bers
    branch = getCurrentBranch()

    # HDR videos have '10bit' in their file name
    bitdepth = 10 if "10bit" in video else 8
    cfg_name = cfg.split('.')[0]

    #tmp_branch = branch.replace("-", "_")
    #tmp_read_ber = read_ber.replace("-","_")
    #tmp_write_ber = write_ber.replace("-","_")
    #execution_key = f"{tmp_branch}-{video[:-4]}-{tmp_read_ber}-{tmp_write_ber}-{cfg_name}-{qp}-{repetition}"

    execution_key = f"{branch}-{video[:-4]}-{read_ber}-{write_ber}-{cfg_name}-{qp}-{repetition}"

    # Create simout file name
    simout = f"{LOGS_BASE}/{execution_key}.log"

    if is_log_complete(simout):
        print("Skipping...")
        continue

    video_title = video.split('_')[0]

    output_bin = f"{BINARY_OUTPUT}/{execution_key}.bin"
    video_config = f"{PER_SEQUENCE_CFG_BASE}/{video_title}.cfg"
    video_path = f"{VIDEOS_BASE}/{video}"
    cfg_path = f"{CFG_BASE}/{cfg}"

    # Create command string
    cmd = f"{PIN_CMD} -t {PIN_TOOL_BASE} -rd_ber {read_ber} -wr_ber {write_ber} " \
           + f"-bt_dth {bitdepth} -- {ENCODERAPP} -c {cfg_path} " \
           + f"-c {video_config} -i {video_path} -f {FRAMES} -q {qp} -b {output_bin}"

    # skip command execution when --dbg option is enabled
    if len(sys.argv) > 1:
        if sys.argv[1] == '--dbg':
            print(cmd)
            continue

    # Logging simulations

    print(f'[{datetime.now():(%d/%m) %H:%M:%S}] Video: {video[:-4]}, '
          + f'BERs: {read_ber} | {write_ber}, CFG: {cfg_name}, '
          + f'QP: {qp}, Repetition: {repetition}')

    simoutfile = open(simout, 'w')    

    line = f"{branch}\t{video}\t{cfg_name}\t{qp}\t{read_ber}\t{write_ber}\t{repetition}\n"

    simlogfile.write(line)
    simdetailedlogfile.write(line)
    simdetailedlogfile.write(f"{cmd}\n")

    # Call subprocess based on cmd
    popen = subprocess.Popen(
       cmd.split(),
       stdout=simoutfile,
       stderr=subprocess.DEVNULL
    )
    processes.append((popen, simoutfile))
    # print(cmd)

    simrun += 1

    if simrun % 10 == 0:
        print(f"[{datetime.now():(%d/%m) %H:%M:%S}] Total simulated - {simrun}/{simtotal} - "
            + f"{round(float(simrun)/simtotal*100, 2)}%")

    # If all cores are being used, wait until one process finishes
    while len(processes) >= MAX_PROCS_PARALLEL:
        for process in processes:
            popen, _ = process
            return_code = popen.poll()

            if return_code == 0:
                finished_process = process
                break
            else:
                finished_process = None

        if finished_process is not None:
            _, simoutfile = process
            simoutfile.close()

            processes.remove(finished_process)
        else:
            # Waits 5 minutes before verifying the processes again
            time.sleep(300)

#if sys.argv[1] != '--dbg':

#Wait for remaining processes
for process in processes:
    popen, simoutfile = process
    popen.wait()
    simoutfile.close()

# Close log files
simlogfile.close()
simdetailedlogfile.close()
