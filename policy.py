#!/usr/bin/env python3
# python >= 3.7

import logging

from typing import Set, List, Dict, Optional
from program import *

class Closure:
    def __init__(self, var_set:Set[str]):
        self.var_set = var_set
    
    @classmethod
    def low_eq(cls, level:str, gamma: Dict[str, str], lattice:Lattice):
        return cls(set([var for var in set(gamma.keys()) if (lattice.check_sub(Label(gamma[var]), Label(level)))]))

    def closure(self, mem:Dict[str,int], traces:List[Trace])->Set[int]:
        logging.debug(f"closure::var_set={self.var_set}")
        result = set()
        index=0
        for t in traces:
            flag = True
            for (var,value) in t.init_memory.items():
                if (var in self.var_set and value != mem[var]):
                    flag = False
                    break
            if (flag):
                result.add(index)
            index+=1
        logging.debug(f"closure::result={result}")
        return result


class Filter:
    def filter(self, outputs:List[Out]) -> List[Out]:
        return outputs

class AttackerFilter(Filter):
    def __init__(self, level:str, lattice:Lattice):
        self.level = level
        self.lattice = lattice
    def filter(self, outputs:List[Out]) -> List[Out]:
        logging.debug(f"attacker_filter::inputs={outputs}, level={self.level}")
        result = [out for out in outputs if (self.lattice.check_sub(Label(out.level), Label(self.level)))]
        logging.debug(f"attacker_filter::result={result}")
        return result
    def __str__(self):
        return f"atk@{self.level}"

class StateAlignFilter(Filter):
    def __init__(self, level:str, exps:Set[str], lattice:Lattice):
        self.level = level
        self.exps = exps
        self.lattice = lattice
    def filter(self, outputs:List[Out]) -> List[Out]:
        logging.debug(f"aligned_filter::inputs={outputs}, level={self.level}, exprs={self.exps}")
        result = []
        for out in outputs:
            flag = True
            for e in self.exps:
                if (self.lattice.check_sub(Label(out.state[e]), Label(self.level))):
                    flag = False
                    break
            if flag:
                result.append(out)
        logging.debug(f"aligned_filter::result={result}")
        return result

    def __str__(self):
        return f"aligned_filter@{self.exps} > {self.level}"

class StmtFilter(Filter):
    def __init__(self, stmtID:int):
        self.stmtID = stmtID

    def filter(self, outputs:List[Out]) -> List[Out]:
        logging.debug(f"stmt_filter::inputs={outputs}, stmtID={self.stmtID}")
        result = outputs
        if self.stmtID != -1:
            result = [out for out in result if out.stmtID == self.stmtID]
        logging.debug(f"stmt_filter::result={result}")
        return result

    def __str__(self):
        return f"stmt_filter@{self.stmtID}"

class ParalockAttackerFilter(Filter):
    def __init__(self, locks:str, lattice:Lattice, global_label:Dict[str, str]):
        self.locks=locks
        self.lattice = lattice
        self.labels = global_label

    def filter(self, outputs:List[ParalockOut]) -> List[ParalockOut]:
        logging.debug(f"paralock_filter::inputs={outputs}, locks={self.locks}")
        result = [out for out in outputs if self.lattice.check_sub(Label(self.labels[out.level]), Label(self.locks))]
        logging.debug(f"paralock_filter::result={result}")
        return result
    def __str__(self):
        return f"paralock_filter@{self.locks}"

class MergedFilter(Filter):
    def __init__(self, flters:List[Filter]):
        self.flters = flters
    def filter(self, outputs:List[Out]) -> List[Out]:
        logging.debug(f"merged_filter::inputs={outputs}")
        result = outputs
        for flter in self.flters:
            result = flter.filter(result)
        logging.debug(f"merged_filter::result={result}")
        return result

    def __str__(self):
        result = "merged_filter("
        for flter in self.flters:
            result += str(flter) + ","
        result += ')'
        return result

class OutEq:
    def eq(self, out1:List[Out], out2:List[Out]) -> bool:
        logging.debug(f"OutEq::out1={out1}, out2={out2}")
        if (len(out1)!=len(out2)):
            return False
        for index in range(len(out1)):
            if (not self.item_eq(out1[index],out2[index])):
                return False
        return True
    def item_eq(self, out1:Out, out2:Out) -> bool:
        logging.debug(f"OutEq::item_eq::out1={out1}, out2={out2}")
        return out1.value == out2.value
    def __str__(self):
        return "ValueEq"

class LastValueEq(OutEq):
    def eq(self, out1:List[Out], out2:List[Out]) -> bool:
        logging.debug(f"LastValueEq::out1={out1}, out2={out2}")
        if len(out1)==0 and len(out2)==0:
            return True
        elif len(out1)==0 or len(out2)==0:
            return False
        else:
            return self.item_eq(out1[-1], out2[-1])

    def __str__(self):
        return "LastValueEq"

class SubOutValueEq(OutEq):
    def eq(self, sub:List[Out], out:List[Out]) -> bool:
        logging.debug(f"SubOutValueEq::sub={sub}, out={out}")
        if (len(sub)>len(out)):
            return False
        for start in range(len(out)-len(sub)+1):
            if super().eq(sub, out[start:start+len(sub)]):
                return True
        return False
    def __str__(self):
        return "SubOutValueEq"

class Policy:
    def verify(self, prog:Program) -> Optional[Set[int]]:
        if not self.assumptions(prog):
            return None
        failed_traces = set()
        for mem_index in range(len(prog.traces)):  # forall m
            for l in prog.get_levels(): # forall l
                if not self.verify_formula(mem_index, l, prog):
                    failed_traces.add(mem_index)
        return list(failed_traces)

    def assumptions(self, prog:Program)->bool:
        return not prog.is_specialized()

    def verify_formula(self, mem_index:int, l:str, prog:Program):
        for t in Policy.get_all_prefix_seq(prog.traces[mem_index]): #  forall prefix of t (forall i)
            logging.debug(f"verify::mem_index={mem_index}, level={l}, t={t}")
            k_out = self.attacker_knowledge(mem_index, prog, l, t)
            allow = self.allowance(mem_index, prog, l, t)
            logging.debug(f"verify::k_out={k_out}, allow={allow}")
            if not allow.issubset(k_out):
                return False
        return True
    
    def attacker_knowledge(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        return Policy.out_knowledge(prog, t, AttackerFilter(level, prog.lattice), OutEq())

    def allowance(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        the_policy = Policy.get_last_output_gamma(prog, t)
        return Closure.low_eq(level, the_policy, prog.lattice).closure(mem, prog.traces)

    @staticmethod
    def out_knowledge(prog:Program, outputs:List[Out], flt: Filter, out_eq:OutEq) -> Set[int]:
        logging.debug(f"out_knowledge::t={outputs}, filter={flt}, eq={out_eq}")
        filtered_output = flt.filter(outputs)
        result = set()
        for mem_index in range(len(prog.traces)): # forall m, 
            for t in Policy.get_all_prefix_seq(prog.traces[mem_index]): # <c,m>-> t, forall t
                if (out_eq.eq(filtered_output, flt.filter(t))):
                    result.add(mem_index)
                    break
        logging.debug(f"out_knowledge::result={result}")
        return result 

    @staticmethod
    def get_all_prefix_seq(t:Trace) -> List[List[Out]]:
        logging.debug(f"get_all_prefix_seq::t={t}")
        result = [[]]  # has to have empty for initial knowledge to be full set
        for i in range(len(t.outputs)):
            result.append(t.outputs[:i+1])
        logging.debug(f"get_all_prefix_seq::result={result}")
        return result

    @staticmethod
    def get_consistent_outputs(prog:Program, t:List[Out], flt:Filter, out_eq:OutEq)->List[List[Out]]:
        logging.debug(f"get_consistent_outputs::t={t}, filter={flt}, eq={out_eq}")
        result = []
        # out_eq = AlignedCurrentValueEq()
        t_filtered = flt.filter(t)
        for trace in prog.traces:
            for candidate in Policy.get_all_prefix_seq(trace):
                if out_eq.eq(flt.filter(candidate), t_filtered):
                    result.append(candidate)
        logging.debug(f"get_consistent_outputs::result={result}")
        return result
    
    @staticmethod
    def get_last_output_gamma(prog: Program, t:List[Out])->Dict[str, str]:
        if (len(t)>0):
            return t[-1].state  # the current policy at end of t
        return prog.global_labels
