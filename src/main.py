#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import sys
sys.dont_write_bytecode = True

import C_TO_LOGIC
import VHDL
import SYN
import SW_LIB
import MODELSIM
import VIVADO

# All main functions must be in main.c
c_file = "main.c"

print('''
██████╗ ██╗██████╗ ███████╗██╗     ██╗███╗   ██╗███████╗ ██████╗
██╔══██╗██║██╔══██╗██╔════╝██║     ██║████╗  ██║██╔════╝██╔════╝
██████╔╝██║██████╔╝█████╗  ██║     ██║██╔██╗ ██║█████╗  ██║     
██╔═══╝ ██║██╔═══╝ ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝  ██║     
██║     ██║██║     ███████╗███████╗██║██║ ╚████║███████╗╚██████╗
╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝ ╚═════╝
''')

print("TODO:")
print(" Do a better Arty7 example - hobby more likely to try something new?")
print(" Do clock crossing for real - not same mhz - make nonvolatile(same mhz) not need arrays in crossings?")
print(" Raw vhdl - black box includes, extra info via pragma - dont bother with specific IP .xci's etc yet")
print(" Fix bug of not being able to include auto gen headers in auto gend files")
print(" Parallelize parsing of func def bodies since indepdent of other func def bodies?")
print(" Only parse to logic funcs if used - should allow mixing in software C code and pipeline C together, do recursive from main's isntead of all func defs in c text")
print(" Allow global funcs inside mux with clock enable type logic - very powerful probably, but ultimately not currently limiting")
print(" Do hacky if generate with pragmas? oh gosh")
print(" Reorg ref tok cover checking and removal (collapsing,etc too?) into tree based data struct")
print(" Detect/document function types ...ex. Detect single instance funcs and record logic.is_single_inst")
print(" Add checks for globals not being used conditionally")
print(" Check for non global functions that call global functions when evaluating const")
print(" Look into intermediate representation such FIRRTL (what Yosys uses?) instead, eventually get rid of VHDL...")
print(" Cache/return once true/reorganize into timing params LOGIC_NEEDS_ code?")
print(" Solve AWS multithreaded off by one or two problem...")
print(" Support AWS PCIM port - need to write kernel driver and maybe user space wrapper?")
print(" Add constant defintion (struct+array init), use const keyword? #define init expressions? Init becomes like const ref funcs assigning ref toks")
print(" How to do module instantiation? Does that need to be macro based? #define to set 'generics'?")
print(" Relative clock crossings - not absolute specified in main/pragmas? Can point at any non-single-inst function to run in requested relative clock..")
print(" Fix for vhdl restricted words. Append _restricted?")
print(" Do auto gen unsigned to array functions now that support array_N_t")
print(" Use gcc array init instead of for loop many const ref tok assignments that are bulky?")
print(" Add timing info via syn top level without flatten, then report timing on each module? No IO regs so will paths make sense? / doesnt work for combinatorial logic? Hah syn weird top level with _top version of everything?")
print(" OPTIMIZE AWAY CONSTANTs: mult by 1 or neg 1, mult by 2 and div by 2, (floats and ints!)")
print(" When doing const ref read with many ref toks, make new 'assignment' alias of new reduced wire so future reads of the same const ref can use the single wire")
print(" Yo dummy dont make built in operations have resize() on outputs, output determined by inputs only")
print(" Add look ahead for built in functions so cast can be inferred")
print(" Remove RESOLVE_CONST_ARRAY_REF from C_AST_REF_TO_TOKENS, and max var ref / var assignement optimize to const ref and const assignment... complicated...")
print(" Consider doing constant optimization as second pass (faster than current way of optimizing as part of first pass?)? How to unroll const for-loop then?")
print(" Pragmas for reset stuff, tag global regs for reset, special clock domain handling stuff with PLL lock and such?")
print(" Allow mix of volatile and non-volatile globals by isolating logic using globals (as is done now by putting in other global func)?")
print(" Redo eq,and,or,..etc raw vhdl ops with pipelined binary trees instead of equal bit sequential stages? Bad for slicing.. probably can work")
print(" Redo old code to use for loops instead of generated code (ex. float div)")
print(" Maybe can implement variable time loops as PipelineC state machines?? Weird idea Andrew")
print(" CANNOT PROPOGATE CONSTANTS through compound references (structs, arrays)")
print(" Try big const ref funcs (not vhdl expr) in modules instead of all in one file where used? removes repeated code for faster elab?")
print(" Built in raw vhdl funcs for array copy / manipulation instead of many const rek tok loops. Built in funcs can return arrays (handled internally) but user can write such funcs  uint8*4_t[N/4] = uint8_arrayN_by_4_le(uint8_t x[N])")
print(" Multiple reads on globals from pipelined logic is maybe OK? ordering of global writes and reads a problem?, do at some point...")
print(" Auto gen <func_name>_t type which is inputs to function func(x,y,z)  struct <func_name>_t {x,y,z}")
print(" Syn each pipeline stage ... this is hard... like slicing zero clock logic ")
print(" Maybe exta luts in some places - not in add, I dont think - double check GT/GTE, etc?")
print(" Uh ceil log2 stuff doesnt work for huge consts determining bit width in python? 0x800000000000008b")
print(" Const SR/SL as vhdl funcs instead of modules..thought this was done...")


print("================== Parsing C Code to Logical Hierarchy ================================")
parser_state = C_TO_LOGIC.PARSE_FILE(c_file)

print("================== Adding Timing Information from Synthesis Tool (Vivado) ================================")
parser_state = SYN.ADD_PATH_DELAY_TO_LOOKUP(parser_state)

print("================== Doing Optional Modelsim Debug ================================")
MODELSIM.DO_OPTIONAL_DEBUG(False)

print("================== Beginning Throughput Sweep ================================")
multimain_timing_params = SYN.DO_THROUGHPUT_SWEEP(parser_state)

print("================== Writing Results of Throughput Sweep ================================")
VIVADO.WRITE_FINAL_FILES(multimain_timing_params, parser_state)
print("Done.")







