# Copyright (c) 2026 CAD & Reliability Group, DAUIN, Polytechnic of Turin
#
# Authors:
# - Gabriele Belli  - gabriele.belli [at] studenti.polito.it or gb210403 [at] gmail.com
# - Filippo Carlone  - filippo.carlone [at] studenti.polito.it or carlonefilippomm [at] gmail.com
# - Josie Esteban Rodriguez Condia  - josie.rodriguez [at] polito.it
# - Riccardo Cantoro  - riccardo.cantoro [at] polito.it
# - Matteo Sonza Reorda  - matteo.sonzareorda [at] polito.it
#
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


import shlex
import logging
import sys
#from constants import TECH_MAP


STAGES = ["chain"]

def parse_tcl(filename):
    log = logging.getLogger("parser")
    configuration = {
        'verilog_file': None,
        'clock': 'clk',
        'operations': [],
        'liberty_file' : None,
        #'tech' : None,
        'output_name' : None,
        'work_dir' : 'log',
        'sin' : 'sin',
        'sout' : 'sout',
        'shift' : 'shift',
        'tck' : 'tck',
        'test' : 'test',
        'n_chains' : 1,
    }

    def handle_read_verilog(args):
        if args: configuration['verilog_file'] = args[0]

    def handle_set_clock(args):
        if args: configuration['clock'] = args[0]

    def handle_set_operation(args):
        if args: configuration['operations'] = list(args)

    def handle_set_liberty_file(args):
        if args: configuration['liberty_file'] = args[0]

    #def handle_set_tech(args):
    #    if args: configuration['tech'] = args[0]

    def handle_set_output_name(args):
        if args: configuration['output_name'] = args[0]

    def handle_set_work_dir(args):
        if args: configuration['work_dir'] = args[0]

    def handle_set_sin(args):
        if args: configuration['sin'] = args[0]

    def handle_set_sout(args):
        if args: configuration['sout'] = args[0]

    def handle_set_shift(args):
        if args: configuration['shift'] = args[0]

    def handle_set_tck(args):
        if args: configuration['tck'] = args[0]

    def handle_set_test(args):
        if args: configuration['test'] = args[0]

    def handle_set_n_chains(args):
        if args:
            try:
                configuration['n_chains'] = int(args[0])
            except ValueError:
                raise ValueError(f"set_n_chains needs an integer, got {args[0]}")

    dispatch_table = {
        'read_verilog': handle_read_verilog,
        'set_clock': handle_set_clock,
        'set_operation': handle_set_operation,
        'set_liberty' : handle_set_liberty_file,
#        'set_tech' : handle_set_tech,
        'set_output_name' : handle_set_output_name,
        'set_work_dir' : handle_set_work_dir,
        'set_sin' : handle_set_sin,
        'set_sout' : handle_set_sout,
        'set_shift' : handle_set_shift,
        'set_tck' : handle_set_tck,
        'set_test' : handle_set_test,
        'set_n_chains' : handle_set_n_chains,
    }

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            try:
                tokens = shlex.split(line)
            except ValueError as e:
                raise ValueError(f"Syntax error in TCL file at line '{line}': {e}")

            if not tokens:
                continue

            cmd = tokens[0]
            args = tokens[1:]

            if cmd in dispatch_table:
                dispatch_table[cmd](args)
            else:
                log.warning(f"the command {cmd} is not recognized")

    # Verifica operazioni
    operations = configuration['operations']
    if not operations:
        raise ValueError("You need to specify operations via 'set_operation' in the TCL file.")

    for op in operations:
        if op not in STAGES:
            raise ValueError(f"Operation '{op}' is not supported. Only 'chain' is allowed.")

    # Controlli specifici ed esclusivi per la fase 'chain'
    if configuration['verilog_file'] is None:
        raise ValueError("When the operation is CHAIN you must provide a verilog file through 'read_verilog'.")
    if configuration['clock'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid clock name through 'set_clock'.")
    if configuration['sin'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid scan-in name through 'set_sin'.")
    if configuration['sout'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid scan-out name through 'set_sout'.")
    if configuration['shift'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid shift name through 'set_shift'.")
    if configuration['tck'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid tck name through 'set_tck'.")
    if configuration['test'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid test name through 'set_test'.")
    if configuration['n_chains'] is None:
        raise ValueError("When the operation is CHAIN you must provide a valid n_chains through 'set_n_chains'.")
    if configuration['output_name'] is None:
        if configuration['verilog_file'] is not None:
            v = configuration['verilog_file']
            if v.endswith(".synth.v"):
                configuration['output_name'] = v[:-len(".synth.v")] + ".scan.v"
            elif v.endswith(".v"):
                configuration['output_name'] = v[:-len(".v")] + ".scan.v"
            else:
                configuration['output_name'] = v + ".scan.v"
        else:
            raise ValueError("When the operation is CHAIN you must provide an output name through 'set_output_name'.")
    if configuration['liberty_file'] is None:
        raise ValueError("When the operation is CHAIN you must provide a liberty file through 'set_liberty'.")

    if configuration['n_chains'] < 1:
        raise ValueError("set_n_chains must be >= 1")

    
    #if configuration['tech'] and not configuration['liberty_file']:
    #    if configuration['tech'] not in TECH_MAP:
    #        raise ValueError(f"the tech {configuration['tech']} is not supported, choose one of: {', '.join(TECH_MAP)}")
    #    configuration['liberty_file'] = TECH_MAP[configuration['tech']]['liberty']

    return configuration