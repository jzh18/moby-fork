import os
import random
import string
import subprocess
from typing import List
import json


def shell(cmd, use_popen=False, log_file=None):
    print("[shell]:", cmd)
    if not use_popen:
        os.system(cmd)
        return None
    else:
        proc = subprocess.Popen(
            cmd, stdout=log_file, stderr=log_file)
        return proc


if __name__ == '__main__':
    with open('/go/src/github.com/docker/docker/workspace/imgs_meta.json', 'r') as f:
        data = json.load(f)
    for k, v in data.items():
        original_img = v['image_name']
        log_file = f'extract_logs/{k}_original.log'
        with open(log_file, 'w+') as f:
            dockerd_proc = shell(f'dockerd', use_popen=True, log_file=f)
        shell('sleep 6')
        shell(
            f'docker pull 601375068473.dkr.ecr.eu-north-1.amazonaws.com/{original_img}')
        shell('sleep 3')
        shell(
            f'docker rmi 601375068473.dkr.ecr.eu-north-1.amazonaws.com/{original_img}')
        dockerd_proc.kill()
        shell('sleep 3')
        with open(log_file, 'r') as f:
            lines = f.readlines()
            f = open(f'extract_logs/{k}_original.csv', 'w+')
            f.write('time,filename,size\n')
            flag = '========================================'
            for l in lines:
                if flag in l:
                    l = l.replace(flag, '')
                    f.write(l)

        debloated_img = v['debloated_img_name']
        log_file = f'extract_logs/{k}_debloated.log'
        with open(log_file, 'w+') as f:
            dockerd_proc = shell(f'dockerd', use_popen=True, log_file=f)
        shell('sleep 6')
        shell(
            f'docker pull 601375068473.dkr.ecr.eu-north-1.amazonaws.com/{debloated_img}')
        shell('sleep 3')
        shell(
            f'docker rmi 601375068473.dkr.ecr.eu-north-1.amazonaws.com/{debloated_img}')
        dockerd_proc.kill()
        shell('sleep 3')
        with open(log_file, 'r') as f:
            lines = f.readlines()
            f = open(f'extract_logs/{k}_debloated.csv', 'w+')
            f.write('time,filename,size\n')
            flag = '========================================'
            for l in lines:
                if flag in l:
                    l = l.replace(flag, '')
                    f.write(l)
