import json
import os.path
import subprocess

with open('langs_config.json') as f:
    config = json.load(f)

"""
This file has language specific execution code.
For each language, there is a class which has two function - 'compile' and 'run'
    => compile function : this function will compile the code and return True is compilation
                       is successful.
    => run function: this function will execute the code in isolate sandbox 
"""


class cpp:
    def compile(box_id):
        subprocess.call("cd /var/local/lib/isolate/" + str(
            box_id) + '/box;' + "g++ ./" + "code.cpp -O2 --std=c++17 -o " + "output 2> error.txt",
                        shell=True)
        if not (os.path.exists('/var/local/lib/isolate/' + str(box_id) + '/box/output')):
            return False
        return True

    def run(box_id):
        print(config['cpp']['time_limit'], flush=True)
        subprocess.call("isolate --run --cg -s --mem=" + str(config['cpp']['max_size']) +
                        " --time=" + str(config['cpp']['time_limit']) +
                        " --wall-time=" + str(config['cpp']['wall_time_limit']) +
                        " -b " + str(box_id) +
                        "--dir=in=out:noexec -o output.txt -i input.txt -M meta.ini -r error.txt ./output",
                        shell=True)


class c:
    def compile(box_id):
        subprocess.call("cd /var/local/lib/isolate/" + str(
            box_id) + '/box;' + "gcc ./" + "code.c -O2 -o " + "output 2> error.txt",
                        shell=True)
        if not (os.path.exists('/var/local/lib/isolate/' + str(box_id) + '/box/output')):
            return False
        return True

    def run(box_id):
        subprocess.call("isolate --run --cg -s --mem=" + str(config['c']['max_size']) +
                        " --time=" + str(config['c']['time_limit']) +
                        " --wall-time=" + str(config['c']['wall_time_limit']) +
                        " -b " + str(box_id) +
                        " -o output.txt -i input.txt -M meta.ini -r error.txt ./output",
                        shell=True)
