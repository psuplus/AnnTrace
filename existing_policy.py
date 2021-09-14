#!/usr/bin/env python3
# python >= 3.7
import logging
from typing import Set, List, Dict

from policy import *
from program import *
from utils import R_Generator

class StaticNoninterference(Policy):
    def assumptions(self, prog:Program)->bool:
        if prog.is_specialized():
            return False
        static_policy = prog.traces[0].outputs[0].state.copy()
        for t in prog.traces:
            for out in t.outputs:
                for key,value in out.state.items():
                    if static_policy[key]!=value:
                        return False
        return True

class DelimitedRelease(Policy):
    def assumptions(self, prog:Program)->bool:
        if prog.is_specialized():
            return False
        return not prog.exists_upgrading()

    def allowance(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        logging.debug(f"allowance::mem={mem}, level={level}")
        the_policy = self.find_lowest_policy(prog)
        return Closure.low_eq(level, the_policy, prog.lattice).closure(mem, prog.traces)
    
    def find_lowest_policy(self, prog:Program)->Dict[str, str]:
        the_policy = (prog.traces[0].outputs[0].state).copy()
        for t in prog.traces:
            for out in t.outputs:
                for key,value in out.state.items():
                    if not prog.lattice.check_sub(Label(the_policy[key]), Label(value)):
                        the_policy[key] = value
        return the_policy 

class GradualRelease(Policy):
    def assumptions(self, prog:Program)->bool:
        if prog.is_specialized():
            return False
        return prog.persistent or not prog.exists_upgrading()

    def allowance(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        the_policy = Policy.get_last_output_gamma(prog, t)
        attacker_memory = self.out_knowledge(prog, t[:-1], AttackerFilter(level, prog.lattice), OutEq())
        low_eq = Closure.low_eq(level, the_policy, prog.lattice).closure(mem, prog.traces)
        return attacker_memory.intersection(low_eq)

class TightRelease(GradualRelease):
    def assumptions(self, prog:Program)->bool:
        if prog.is_specialized():
            return False
        return not prog.exists_upgrading()

    def allowance(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        the_policy = Policy.get_last_output_gamma(prog, t)
        return Closure.low_eq(level, the_policy, prog.lattice).closure(mem, prog.traces)

class ForgetfulAtkFull(GradualRelease):
    def assumptions(self, prog:Program)->bool:
        return not prog.is_specialized()


class ForgetfulAtkSingle(ForgetfulAtkFull):
    def attacker_knowledge(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        return Policy.out_knowledge(prog, t, AttackerFilter(level, prog.lattice), LastValueEq())


class Crypto(Policy):
    def assumptions(self, prog:Program)->bool:
        if prog.is_specialized():
            return False
        return (not prog.exists_downgrading()) and ((not prog.persistent) or (not prog.exists_upgrading()))

    def verify_formula(self, mem_index:int, l:str, prog:Program):
        for t in Policy.get_all_prefix_seq(prog.traces[mem_index]):    # get all prefix, (forall i)
            for index in range(len(t)):     # get all sub-sequence, (forall j)
                t_obs = t[index:]    # t_obs = t[i:j]
                logging.debug(f"verify::mem_index={mem_index}, level={l}, t={t}, t_obs={t_obs}")
                k_out = self.attacker_knowledge(mem_index, prog, l, t_obs)
                allow = self.allowance(mem_index, prog, l, t_obs)
                logging.debug(f"verify::k_out={k_out}, allow={allow}")
                if not allow.issubset(k_out):
                    return False
        return True
    def attacker_knowledge(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        return Policy.out_knowledge(prog, t, AttackerFilter(level, prog.lattice), SubOutValueEq())
    
    def allowance(self, mem_index: int , prog: Program, level:str, t: List[Out]) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        logging.debug(f"allowance::mem={mem}, level={level}, t={t}") 
        result = set(range(len(prog.traces)))
        for out in t:
            result = result.intersection(Closure.low_eq(level, out.state, prog.lattice).closure(mem, prog.traces))
        logging.debug(f"allowance::result={result}")
        return result

class AccordingToPolicy(Policy):
    def assumptions(self, prog:Program)->bool:
        if prog.is_specialized():
            return False
        return (not prog.persistent) or (not prog.exists_upgrading())
    
    def verify_formula(self, mem_index:int, l:str, prog:Program):
        t = prog.traces[mem_index].outputs # complete trace, not prefix
        for e in prog.get_vars(): # forall e,
            logging.debug(f"verify::mem_index={mem_index}, level={l}, t={t}, e={e}")
            k_out = self.knowledge_per_e(mem_index, prog, l, t, e)
            allow = self.allowance_per_e(mem_index, prog, l, t, e)
            logging.debug(f"verify::k_out={k_out}, allow={allow}")
            if not allow.issubset(k_out):
                return False
        return True

    def allowance_per_e(self, mem_index: int , prog: Program, level:str, t: List[Out], e:str) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        neg_e = prog.get_vars()
        neg_e.remove(e)
        return Closure(neg_e).closure(mem, prog.traces)

    def knowledge_per_e(self, mem_index: int , prog: Program, level:str, t: List[Out], e:str) -> Set[int]:
        flt = MergedFilter([AttackerFilter(level, prog.lattice), StateAlignFilter(level, {e}, prog.lattice)])
        out_eq = OutEq()
        logging.debug(f"knowledge_per_e::t={t}, filter={flt}, eq={out_eq}")
        result = set()
        for index in range(len(prog.traces)): # forall <c,m> terminated t
            t2 = prog.traces[index].outputs
            logging.debug(f"knowledge_per_e::t={mem_index}, t2={index}")
            for R in R_Generator(len(t), len(t2)).get_all_R():
                flag = True
                for (i,j) in R:
                    filtered_t = flt.filter([t[i]])
                    filtered_t2 = flt.filter([t2[j]])
                    if len(filtered_t)>0 and len(filtered_t2)>0 and not out_eq.eq(filtered_t, filtered_t2):
                        flag = False
                        break
                if flag:
                    logging.debug(f"knowledge_per_e::R={R}")
                    result.add(index)
                    break
        logging.debug(f"knowledge_per_e::result={result}")
        return result

class ParalockOrigin(Policy):
    def assumptions(self, prog:Program)->bool:
        return isinstance(prog.traces[0].outputs[0], ParalockOut) and len(prog.global_labels)>0

    def verify_formula(self, mem_index:int, l:str, prog:Program):
        for t in Policy.get_all_prefix_seq(prog.traces[mem_index]): #  forall prefix of t (forall i)
            logging.debug(f"verify::mem_index={mem_index}, level={l}, t={t}")
            if len(t)>0 and prog.lattice.check_sub(Label(t[-1].locks), Label(l)):
                logging.debug(f"verify::t.locks={t[-1].locks}, level={l}")
                k_pl_t = self.k_pl(mem_index, prog, l, t)
                k_pl_prev_t = self.k_pl(mem_index, prog, l, t[:-1])
                logging.debug(f"verify::k_t={k_pl_t}, k_prev_t={k_pl_prev_t}")
                if k_pl_t != k_pl_prev_t:
                    return False
        return True

    def k_pl(self, mem_index:int, prog:Program, l:str, t:List[Out])-> Set[int]:
        visible_var = [x for x in prog.get_vars() if prog.lattice.check_sub(Label(prog.global_labels[x]), Label(l))] 
        low_eq = Closure(visible_var).closure(prog.traces[mem_index].init_memory, prog.traces)
        if len(t)>0:
            knowledge = Policy.out_knowledge(prog, t, ParalockAttackerFilter(l, prog.lattice, prog.global_labels), OutEq())
            return low_eq.intersection(knowledge)
        else:
            return low_eq

class NonStaticPolicy(Policy):
    def verify_formula(self, mem_index:int, l:str, prog:Program):
        for t in Policy.get_all_prefix_seq(prog.traces[mem_index]): # forall prefix traces (forall i)
            for e in prog.get_vars(): # forall e,
                logging.debug(f"verify::mem_index={mem_index}, level={l}, t={t}, e={e}")
                k_out = self.knowledge_per_e(mem_index, prog, l, t, e)
                allow = self.allowance_per_e(mem_index, prog, l, t, e)
                logging.debug(f"verify::k_out={k_out}, allow={allow}")
                if not allow.issubset(k_out):
                    return False
        return True

    def allowance_per_e(self, mem_index: int , prog: Program, level:str, t: List[Out], e:str) -> Set[int]:
        mem = prog.traces[mem_index].init_memory
        neg_e = prog.get_vars()
        neg_e.remove(e)
        low_eq = Closure(neg_e).closure(mem, prog.traces)
        if prog.persistent:
            attacker_memory = self.out_knowledge(prog, t[:-1], AttackerFilter(level, prog.lattice), OutEq())
            return attacker_memory.intersection(low_eq)
        else:
            return low_eq

    def knowledge_per_e(self, mem_index: int , prog: Program, level:str, t: List[Out], e:str) -> Set[int]:
        return Policy.out_knowledge(prog, t, MergedFilter([AttackerFilter(level, prog.lattice), StateAlignFilter(level, {e}, prog.lattice)]), OutEq())

class DynamicNoninterference(NonStaticPolicy):
    def knowledge_per_e(self, mem_index: int , prog: Program, level:str, t: List[Out], e:str) -> Set[int]:
        k_out = set()
        for t_consist in Policy.get_consistent_outputs(prog, t, MergedFilter([AttackerFilter(level, prog.lattice), StateAlignFilter(level, {e}, prog.lattice)]), OutEq()):
            k_out = k_out.union(self.out_knowledge(prog, t_consist, AttackerFilter(level, prog.lattice), OutEq()))
        return k_out
