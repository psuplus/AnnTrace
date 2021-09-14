#!/usr/bin/env python3
# python >= 3.7

import json
import dataclasses
import logging

from dataclasses import dataclass, field
from typing import Set, List, Dict
from lattice import Label, Lattice, TwoPointLattice
from utils import Utils

@dataclass(frozen=True) # immutable
class Out:
    level: str
    value: int
    state: Dict[str, str]
    stmtID:int

    def __str__(self):
        return f"< {self.level},{self.value},{self.state},{self.stmtID} >"
    def __repr__(self):
        return self.__str__()

@dataclass(frozen=True)
class ParalockOut(Out):
    level: str
    value: int
    state: Dict[str, str]
    stmtID:int
    locks: str

    def __str__(self):
        return f"< {self.level},{self.value},{self.state},{self.stmtID},{self.locks} >"

@dataclass(frozen=True)
class Trace:
    init_memory: Dict[str, int]
    outputs: List[Out]

@dataclass(frozen=True)
class Program:
    """A Program to be verified."""
    secure: bool
    traces: List[Trace]
    is_controversial:bool = field(default=False)
    persistent:bool = field(default=True)
    lattice: Lattice = field(default=TwoPointLattice())
    source_code:str = field(default="")
    comment:str = field(default="")
    global_labels:Dict[str, str] = field(default_factory=dict)

    def get_vars(self) -> Set[str]: 
        return set(self.traces[0].init_memory.keys())

    def get_levels(self) -> Set[str]:
        return set([lab.name for lab in self.lattice.labels])

    def get_stmtIDs(self)-> Set[int]:
        id_set = []
        for trace in self.traces:
            id_set += [x.stmtId for x in trace.outputs]
        return set(id_set)

    def exists_upgrading(self)-> bool:
        var_set = self.get_vars()
        for trace in self.traces:
            for index in range(len(trace.outputs)-1):
                for x in var_set:
                    if not self.lattice.check_sub(Label(trace.outputs[index+1].state[x]), Label(trace.outputs[index].state[x])):
                        return True
        return False
    
    def exists_downgrading(self)-> bool:
        var_set = self.get_vars()
        for trace in self.traces:
            for index in range(len(trace.outputs)-1):
                for x in var_set:
                    if not self.lattice.check_sub(Label(trace.outputs[index].state[x]), Label(trace.outputs[index+1].state[x]),):
                        return True
        return False

    def is_specialized(self)->bool:
        return isinstance(self.traces[0].outputs[0], ParalockOut)

    def verify_annotations(self)->bool:
        result = True
        all_levels = set()
        for t in self.traces:
            for out in t.outputs:
                all_levels.update(set(out.state.values()))
        legal_levels = self.get_levels()
        legal_levels.update([Lattice().top.name, Lattice().bot.name])
        result = result and Utils.verify_set_with_msg(all_levels, legal_levels, 
            "All levels in state policy must be defined by the lattice!")

        all_vars = set()
        for t in self.traces:
            all_vars.update(set(t.init_memory.keys()))
            for out in t.outputs:
                all_vars.update(set(out.state.keys()))
        index=0
        for t in self.traces:
            logging.info(f"--- Trace[ {index} ]:")
            result = result and Utils.verify_set_with_msg(all_vars, set(t.init_memory.keys()), 
                "All variables must be defined in memory.")
            for out in t.outputs:
                result = result and Utils.verify_set_with_msg(all_vars, set(out.state.keys()), 
                    "All variables must be defined in a state policy.")
            index+=1
        
        result = result and Utils.verify_set_with_msg(set(), legal_levels.intersection(all_vars), "Duplicated identifier for the name of a variable or a level.")

        all_output_channel = set()
        for t in self.traces:
            for out in t.outputs:
                all_levels.add(out.level)
        result = result and Utils.verify_set_with_msg(all_output_channel, legal_levels.union(all_vars), 
                    "An output channel must be either a variable or a level.")
        return result
    

class Examples:
    programs: List[Program]
    def __eq__(self, other):
        if isinstance(other, Examples):
            if len(self.programs) != len(other.programs):
                return False
            for index in range(len(self.programs)):
                dict_self = self.programs[index].__dict__
                dict_other = other.programs[index].__dict__
                if (self.programs[index]!=other.programs[index]):
                    return False
            return True
        return False

