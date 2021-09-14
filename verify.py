#!/usr/bin/env python3
# python >= 3.7

import logging
import sys, inspect
import dataclasses

from typing import List

from program import *
from policy import *

# make sure the examples and policies are loaded into current module
from existing_policy import *
from examples import *


@dataclass(frozen=True) # immutable
class StatData:
    policy: str
    program: str
    passed: str
    truth_value: str
    result_value: str
    failed_traces: List[int]

class Verification:
    prog:List[str]
    pol: List[str]
    ex_prog: List[str]
    ex_pol: List[str]
    stats: List[StatData]
    
    def __init__(self, programs: List[str], policies: List[str], ex_programs: List[str], ex_policies: List[str], reports: List[str]):
        self.prog = programs
        self.pol = policies
        self.ex_prog = ex_programs
        self.ex_pol = ex_policies
        self.reports = [x.upper() for x in reports]
    
    def verify_examples(self, the_examples: List[Examples])->bool:
        result = True
        for examples in the_examples:
            for index in range(len(examples.programs)):
                logging.info(f"----------- Verifying {examples.__class__.__name__}[ {index} ]:")
                result = (result and examples.programs[index].verify_annotations())
        return result
        
    def run(self):
        policies = self.retrieve_policy()
        examples = self.retrieve_examples()
        assert self.verify_examples(examples)
        
        self.stats = []
        for policy in policies:
            for example in examples:
                for index in range(len(example.programs)):
                    result = policy.verify(example.programs[index])
                    result_value="N/A"
                    pass_value="N/A"
                    if result is not None:
                        result_value =Utils.bool_str(len(result)==0)
                        pass_value = Utils.bool_pass(example.programs[index].secure==(len(result)==0), example.programs[index].is_controversial)
                    self.stats.append(StatData(policy=policy.__class__.__name__,
                        program=f"{example.__class__.__name__} [ {index} ]", 
                        passed=pass_value,
                        truth_value=Utils.bool_str(example.programs[index].secure), 
                        result_value=result_value, 
                        failed_traces=result))
            assert examples == self.retrieve_examples(), f"Policy {policy.__class__.__name__} modifies the program data! Programs are read-only!"
            
    def print_stats(self):
        line_width=120
        print("\n")
        print('-'*line_width)
        format_str=" {:>40}  |  {:>20}  |  {:>5}  | {:>6}  |  {:>6}  |  {} "
        print(format_str.format("Program            ", "Policy   ", "PASS",
                "Truth", "Result", "Failed Traces"))
        print('-'*line_width)
        for result in self.stats:
            if  any([x in result.passed for x in self.reports]):
                print(format_str.format(result.program, result.policy, result.passed, result.truth_value, result.result_value,  result.failed_traces))

    def retrieve_examples(self) -> List[Examples]:
        examples = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.ismodule(obj) and obj.__package__ == "examples":
                for name2, obj2 in inspect.getmembers(obj):
                    if inspect.isclass(obj2) and issubclass(obj2, Examples) and not obj2 == Examples:
                        if Utils.is_included(name2, self.prog, self.ex_prog):
                            examples.append(obj2())
        return examples
    
    def retrieve_policy(self) -> List[Policy]:
        policies = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and issubclass(obj, Policy) and not obj == Policy:
                if Utils.is_included(name, self.pol, self.ex_pol):
                    policies.append(obj())
        return policies
