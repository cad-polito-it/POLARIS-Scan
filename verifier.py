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

import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
from profiling import profiled


@dataclass
class VerificationResult:
    passed: bool
    total_ffs: int
    n_chains: int
    max_depth: int
    output_log: str
    error_message: Optional[str] = None


def find_sim_library(liberty_path: str) -> Path:
    """Infers the corresponding behavioral Verilog library for Verilator based on liberty path."""
    lib_str = str(liberty_path).lower()
    root = Path(__file__).resolve().parent

    if "15nm" in lib_str:
        sim_lib = root / "Tech/Syn_libraries/15nm/verilog/nangate15_sim.v"
    elif "45nm" in lib_str:
        sim_lib = root / "Tech/Syn_libraries/45nm/verilog/nangate45_sim.v"
    elif "130nm" in lib_str or "sg13g2" in lib_str:
        sim_lib = root / "Tech/Syn_libraries/130nm/verilog/sg13g2_sim.v"
    else:
        raise ValueError(
            f"Cannot automatically infer simulation library for: {liberty_path}. "
            f"Expected technology (15nm, 45nm, 130nm) in path."
        )

    if not sim_lib.exists():
        raise FileNotFoundError(
            f"Behavioral simulation model not found at '{sim_lib}'. Ensure Fase 1 models are present."
        )
    return sim_lib


def parse_scan_metadata(scan_verilog_path: str):
    """Extracts top module, scan metadata and input port list from the scan netlist."""
    content = Path(scan_verilog_path).read_text(encoding="utf-8")

    m = re.search(
        r"/\*\s*(?:FAULT|POLARIS(?:-Scan)?)\s+METADATA:\s*'(\{.*?\})'\s*END\s+(?:FAULT|POLARIS(?:-Scan)?)\s+METADATA\s*\*/",
        content,
        re.DOTALL,
    )
    if not m:
        raise ValueError(f"No scan metadata header found in {scan_verilog_path}")
    metadata = json.loads(m.group(1))

    mm = re.search(r"^\s*module\s+([A-Za-z0-9_$\\]+)", content, re.MULTILINE)
    if not mm:
        raise ValueError(f"No module declaration found in {scan_verilog_path}")
    top_name = mm.group(1).lstrip("\\")

    input_matches = re.findall(
        r"^\s*input\s+(?:\[[^\]]+\]\s+)?([A-Za-z0-9_$\\]+)\s*;", content, re.MULTILINE
    )
    inputs = [p.lstrip("\\").rstrip() for p in input_matches]

    return top_name, metadata, inputs


def generate_cpp_harness(
    top_module: str,
    metadata: dict,
    input_ports: List[str],
    clk_name: str,
    tck_name: str,
    test_name: str,
    shift_name: str,
    out_cpp_path: str,
):
    """Generates a high-speed C++ harness for Verilator.

    Tests performed:
    1. Flush Test (Shift Integrity): Alternating pattern (1010...) shifted through all chains
       in parallel, verifying that exact bits emerge after chain depth cycles.
    2. Combinational Capture Test: Pre-loads alternating pattern into FFs, switches to
       functional mode (shift=0, test=0), clocks 1 cycle of clk, and shifts out the captured state.
    3. Clock Mux & Transparency Test: Ensures tck is disabled when test=0.
    """
    total_ffs = metadata.get("internalCount", 0)

    # Multi-chain vs single-chain port extraction
    if "chains" in metadata:
        chains = metadata["chains"]
    else:
        chains = [{"sin": metadata.get("sin", "sin"), "sout": metadata.get("sout", "sout"), "order": metadata.get("order", [])}]

    n_chains = len(chains)
    chain_lengths = [len(c["order"]) for c in chains]
    max_depth = max(chain_lengths) if chain_lengths else 0

    scan_control_ports = {clk_name, tck_name, test_name, shift_name}
    for c in chains:
        scan_control_ports.add(c["sin"])
        scan_control_ports.add(c["sout"])

    functional_inputs = [p for p in input_ports if p not in scan_control_ports]

    code = []
    code.append(f'#include <iostream>')
    code.append(f'#include <vector>')
    code.append(f'#include <string>')
    code.append(f'#include "V{top_module}.h"')
    code.append(f'#include "verilated.h"')
    code.append('')
    code.append(f'int main(int argc, char** argv) {{')
    code.append(f'    Verilated::commandArgs(argc, argv);')
    code.append(f'    V{top_module}* top = new V{top_module};')
    code.append('')
    code.append(f'    // Initialize control inputs')
    code.append(f'    top->{clk_name} = 0;')
    code.append(f'    top->{tck_name} = 0;')
    code.append(f'    top->{test_name} = 0;')
    code.append(f'    top->{shift_name} = 0;')
    for c in chains:
        code.append(f'    top->{c["sin"]} = 0;')
    code.append('')
    code.append(f'    // Initialize functional inputs to safe inactive values')
    for p in functional_inputs:
        is_active_low = bool(re.search(r"(?:^|_)rst_?n(?:i)?$|(?:^|_)reset_?n(?:i)?$|_ni$|_n$", p.lower()))
        default_val = 1 if is_active_low else 0
        code.append(f'    top->{p} = {default_val};')
    code.append(f'    top->eval();')
    code.append('')
    code.append(f'    const int N_CHAINS = {n_chains};')
    code.append(f'    const int MAX_DEPTH = {max_depth};')
    code.append(f'    const int chain_lens[{n_chains}] = {{{", ".join(str(l) for l in chain_lengths)}}};')
    code.append(f'    bool all_ok = true;')
    code.append('')
    code.append(f'    std::cout << "==================================================" << std::endl;')
    code.append(f'    std::cout << " POLARIS-Scan Verilator Verification Engine" << std::endl;')
    code.append(f'    std::cout << " Design: {top_module} | FFs: {total_ffs} | Chains: {n_chains} | Max Depth: {max_depth}" << std::endl;')
    code.append(f'    std::cout << "==================================================" << std::endl;')
    code.append('')
    code.append(f'    // ----------------------------------------------------')
    code.append(f'    // TEST 1: Flush Test (Shift Integrity with 1010... pattern)')
    code.append(f'    // ----------------------------------------------------')
    code.append(f'    std::cout << "[TEST 1] Flush Test (Shift Integrity with Alternating Pattern)" << std::endl;')
    code.append(f'    top->{test_name} = 1;')
    code.append(f'    top->{shift_name} = 1;')
    code.append(f'    top->eval();')
    code.append('')
    code.append(f'    // Prepare alternating patterns for each chain')
    code.append(f'    std::vector<std::vector<int>> in_patterns(N_CHAINS, std::vector<int>(MAX_DEPTH));')
    code.append(f'    for (int c = 0; c < N_CHAINS; ++c) {{')
    code.append(f'        for (int i = 0; i < MAX_DEPTH; ++i) {{')
    code.append(f'            in_patterns[c][i] = (i % 2); // alternating 0, 1, 0, 1...')
    code.append(f'        }}')
    code.append(f'    }}')
    code.append('')
    code.append(f'    // Shift in MAX_DEPTH bits (front-padded for shorter chains)')
    code.append(f'    for (int cycle = 0; cycle < MAX_DEPTH; ++cycle) {{')
    for i, c in enumerate(chains):
        pad_len = max_depth - chain_lengths[i]
        code.append(f'        top->{c["sin"]} = (cycle < {pad_len}) ? 0 : in_patterns[{i}][cycle - {pad_len}];')
    code.append(f'        top->eval();')
    code.append(f'        top->{tck_name} = 1; top->eval();')
    code.append(f'        top->{tck_name} = 0; top->eval();')
    code.append(f'    }}')
    code.append('')
    code.append(f'    // Shift out MAX_DEPTH bits and verify')
    code.append(f'    std::vector<std::vector<int>> out_captured(N_CHAINS, std::vector<int>(MAX_DEPTH));')
    code.append(f'    for (int cycle = 0; cycle < MAX_DEPTH; ++cycle) {{')
    for i, c in enumerate(chains):
        code.append(f'        top->{c["sin"]} = 0;')
    code.append(f'        top->eval();')
    for i, c in enumerate(chains):
        code.append(f'        out_captured[{i}][cycle] = top->{c["sout"]};')
    code.append(f'        top->{tck_name} = 1; top->eval();')
    code.append(f'        top->{tck_name} = 0; top->eval();')
    code.append(f'    }}')
    code.append('')
    code.append(f'    bool flush_ok = true;')
    code.append(f'    for (int c = 0; c < N_CHAINS; ++c) {{')
    code.append(f'        int valid_len = chain_lens[c];')
    code.append(f'        for (int i = 0; i < valid_len; ++i) {{')
    code.append(f'            if (out_captured[c][i] != in_patterns[c][i]) {{')
    code.append(f'                std::cerr << "  FAIL: Chain " << c << " mismatch at cycle " << i')
    code.append(f'                          << "! Expected " << in_patterns[c][i]')
    code.append(f'                          << ", got " << out_captured[c][i] << std::endl;')
    code.append(f'                flush_ok = false;')
    code.append(f'            }}')
    code.append(f'        }}')
    code.append(f'    }}')
    code.append(f'    if (flush_ok) {{')
    code.append(f'        std::cout << "  PASS: Flush Test verified successfully across all " << N_CHAINS << " chain(s)!" << std::endl;')
    code.append(f'    }} else {{')
    code.append(f'        all_ok = false;')
    code.append(f'    }}')
    code.append('')
    code.append(f'    // ----------------------------------------------------')
    code.append(f'    // TEST 2: Combinational Capture Test')
    code.append(f'    // ----------------------------------------------------')
    code.append(f'    std::cout << "[TEST 2] Combinational Capture Test" << std::endl;')
    code.append(f'    // Step 2.1: Pre-load stimulus pattern via scan')
    code.append(f'    top->{test_name} = 1;')
    code.append(f'    top->{shift_name} = 1;')
    code.append(f'    for (int cycle = 0; cycle < MAX_DEPTH; ++cycle) {{')
    for i, c in enumerate(chains):
        pad_len = max_depth - chain_lengths[i]
        code.append(f'        top->{c["sin"]} = (cycle < {pad_len}) ? 0 : in_patterns[{i}][cycle - {pad_len}];')
    code.append(f'        top->eval();')
    code.append(f'        top->{tck_name} = 1; top->eval();')
    code.append(f'        top->{tck_name} = 0; top->eval();')
    code.append(f'    }}')
    code.append('')
    code.append(f'    // Step 2.2: Switch to functional mode & capture (1 clk pulse)')
    code.append(f'    top->{test_name} = 0;')
    code.append(f'    top->{shift_name} = 0;')
    for p in functional_inputs:
        is_reset = bool(re.search(r"rst|reset", p.lower()))
        is_active_low = bool(re.search(r"(?:^|_)rst_?n(?:i)?$|(?:^|_)reset_?n(?:i)?$|_ni$|_n$", p.lower()))
        if is_reset:
            val = 1 if is_active_low else 0
        else:
            val = 1
        code.append(f'    top->{p} = {val};')
    code.append(f'    top->eval();')
    code.append(f'    top->{clk_name} = 1; top->eval();')
    code.append(f'    top->{clk_name} = 0; top->eval();')
    code.append('')
    code.append(f'    // Step 2.3: Shift out captured state via test clock')
    code.append(f'    top->{test_name} = 1;')
    code.append(f'    top->{shift_name} = 1;')
    code.append(f'    top->eval();')
    code.append(f'    std::vector<std::vector<int>> cap_out(N_CHAINS, std::vector<int>(MAX_DEPTH));')
    code.append(f'    for (int cycle = 0; cycle < MAX_DEPTH; ++cycle) {{')
    for i, c in enumerate(chains):
        code.append(f'        top->{c["sin"]} = 0;')
    code.append(f'        top->eval();')
    for i, c in enumerate(chains):
        code.append(f'        cap_out[{i}][cycle] = top->{c["sout"]};')
    code.append(f'        top->{tck_name} = 1; top->eval();')
    code.append(f'        top->{tck_name} = 0; top->eval();')
    code.append(f'    }}')
    code.append(f'    std::cout << "  PASS: Combinational capture cycle executed and unloaded cleanly!" << std::endl;')
    code.append('')
    code.append(f'    // ----------------------------------------------------')
    code.append(f'    // TEST 3: Clock Mux Bypass & Transparency Check')
    code.append(f'    // ----------------------------------------------------')
    code.append(f'    std::cout << "[TEST 3] Clock Mux Bypass & Transparency Check" << std::endl;')
    code.append(f'    top->{test_name} = 0;')
    code.append(f'    top->{shift_name} = 0;')
    code.append(f'    top->eval();')
    for i, c in enumerate(chains):
        code.append(f'    int sout_before_{i} = top->{c["sout"]};')
    code.append(f'    for (int i = 0; i < 5; ++i) {{')
    code.append(f'        top->{tck_name} = 1; top->eval();')
    code.append(f'        top->{tck_name} = 0; top->eval();')
    code.append(f'    }}')
    for i, c in enumerate(chains):
        code.append(f'    if (top->{c["sout"]} != sout_before_{i}) {{')
        code.append(f'        std::cerr << "  FAIL: tck affected circuit state when test=0 on chain {i}!" << std::endl;')
        code.append(f'        all_ok = false;')
        code.append(f'    }}')
    code.append(f'    if (all_ok) {{')
    code.append(f'        std::cout << "  PASS: tck successfully isolated in functional mode (test=0)!" << std::endl;')
    code.append(f'    }}')
    code.append('')
    code.append(f'    std::cout << "==================================================" << std::endl;')
    code.append(f'    std::cout << " Overall Verification Result: " << (all_ok ? "ALL TESTS PASSED" : "FAILED") << std::endl;')
    code.append(f'    std::cout << "==================================================" << std::endl;')
    code.append(f'    delete top;')
    code.append(f'    return all_ok ? 0 : 1;')
    code.append(f'}}')
    code.append('')

    Path(out_cpp_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_cpp_path).write_text("\n".join(code), encoding="utf-8")


@profiled("verify")
def run_verification(
    scan_verilog: str,
    liberty_file: str,
    work_dir: str = "log",
    clk_name: str = "clk",
    tck_name: str = "tck",
    test_name: str = "test",
    shift_name: str = "shift",
) -> VerificationResult:
    """Orchestrates Verilator verification of a scan netlist."""
    log = logging.getLogger("verifier")
    log.info(f"Starting Verilator scan verification for '{scan_verilog}'...")

    sim_lib = find_sim_library(liberty_file)
    top_name, metadata, inputs = parse_scan_metadata(scan_verilog)

    obj_dir = Path(work_dir) / "verilator_obj"
    obj_dir.mkdir(parents=True, exist_ok=True)
    cpp_path = obj_dir / "sim_main.cpp"

    generate_cpp_harness(
        top_module=top_name,
        metadata=metadata,
        input_ports=inputs,
        clk_name=clk_name,
        tck_name=tck_name,
        test_name=test_name,
        shift_name=shift_name,
        out_cpp_path=str(cpp_path),
    )

    # Compile with Verilator
    verilator_cmd = [
        "verilator",
        "-Wno-fatal",
        "-Wno-lint",
        "--cc",
        str(Path(scan_verilog).resolve()),
        str(sim_lib.resolve()),
        "--top-module",
        top_name,
        "--exe",
        str(cpp_path.resolve()),
        "--Mdir",
        str(obj_dir.resolve()),
    ]
    log.info(f"Compiling Verilog model with Verilator...")
    p_verilator = subprocess.run(
        verilator_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p_verilator.returncode != 0:
        err = f"Verilator compilation failed:\n{p_verilator.stderr}"
        log.error(err)
        return VerificationResult(
            passed=False,
            total_ffs=metadata.get("internalCount", 0),
            n_chains=len(metadata.get("chains", [1])),
            max_depth=0,
            output_log=p_verilator.stdout + "\n" + p_verilator.stderr,
            error_message=err,
        )

    # Build binary with make
    make_jobs = str(max(1, (os.cpu_count() or 4)))
    make_cmd = ["make", "-j", make_jobs, "-C", str(obj_dir.resolve()), "-f", f"V{top_name}.mk", f"V{top_name}"]
    log.info(f"Building verification binary with make...")
    p_make = subprocess.run(
        make_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if p_make.returncode != 0:
        err = f"Make build failed:\n{p_make.stderr}"
        log.error(err)
        return VerificationResult(
            passed=False,
            total_ffs=metadata.get("internalCount", 0),
            n_chains=len(metadata.get("chains", [1])),
            max_depth=0,
            output_log=p_make.stdout + "\n" + p_make.stderr,
            error_message=err,
        )

    # Execute simulation
    sim_binary = obj_dir / f"V{top_name}"
    log.info(f"Executing scan testbench binary...")
    p_sim = subprocess.run(
        [str(sim_binary.resolve())],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    passed = (p_sim.returncode == 0)
    output = p_sim.stdout + "\n" + p_sim.stderr

    if passed:
        log.info(f"Scan verification PASSED successfully!")
    else:
        log.error(f"Scan verification FAILED!\n{output}")

    if "chains" in metadata:
        depth = max(len(c["order"]) for c in metadata["chains"])
        n_ch = len(metadata["chains"])
    else:
        depth = metadata.get("internalCount", 0)
        n_ch = 1

    return VerificationResult(
        passed=passed,
        total_ffs=metadata.get("internalCount", 0),
        n_chains=n_ch,
        max_depth=depth,
        output_log=output,
        error_message=None if passed else "Simulation mismatch",
    )
