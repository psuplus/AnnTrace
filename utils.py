#!/usr/bin/env python3
# python >= 3.7

import logging
from typing import Set, List, Tuple

class Utils:
    @staticmethod
    def verify_set_with_msg(truth:Set, actual:Set, msg:str) -> bool:
        missing_items = truth -  actual
        if (len(missing_items)==0):
            logging.info(f"Passed - {msg}")
            return True
        else:
            logging.error(f"Failed - {missing_items} are missing! {msg}")
            return False
    @staticmethod
    def bool_str(result:bool)->str:
        if result==True:
            return "T"
        else:
            return "F"
    @staticmethod
    def bool_pass(result:bool, controversial:bool)->str:
        con=" "
        if controversial:
            con="?"
        if result==True:
            return "- "+con
        else:
            return "X "+con

    @staticmethod
    def is_included(name:str, includes: List[str], excludes:List[str])->bool:
        if len(includes)>0:
            return Utils.is_in_list(name, includes)
        elif len(excludes)>0:
            return not Utils.is_in_list(name, excludes)
        else:
            return True

    @staticmethod
    def is_in_list(name:str, check_list:List[str])->bool:
        for item in check_list:
            if item in name:
                return True
        return False

class R_Generator:
    len_a:int
    len_b:int
    result:List[Set[Tuple[int,int]]]

    def __init__(self, a:int, b:int):
        self.len_a = a
        self.len_b = b

    def get_all_R(self)->List[Set[Tuple[int,int]]]:
        self.result = []
        self.get_next_pair({(0,0)}, 0, 0)  # must include (0,0)
        return self.result

    def get_next_pair(self, cur_R:Set[Tuple[int,int]], index_a:int, index_b:int):
        # two possiblities of the current pair (index_a, index_b):
        next_R_1 = cur_R.copy() # (1) not add it
        next_R_2 = cur_R.copy()
        next_R_2.add((index_a, index_b)) # (2) add it

        if index_a+1 == self.len_a and index_b+1 == self.len_b: # terminate
            self.add_R(next_R_1)
            self.add_R(next_R_2)
        else:
            # three possible monotonic next pairs:
            if index_a+1 < self.len_a: # (1) (+1, - )
                self.get_next_pair(next_R_1, index_a+1, index_b)
                self.get_next_pair(next_R_2, index_a+1, index_b)
            if index_b+1 < self.len_b: # (2) ( - , +1 )
                self.get_next_pair(next_R_1, index_a, index_b+1)
                self.get_next_pair(next_R_2, index_a, index_b+1)
            if index_a+1 < self.len_a and index_b+1 < self.len_b:  # (3) (+1, +1)
                self.get_next_pair(next_R_1, index_a+1, index_b+1)
                self.get_next_pair(next_R_2, index_a+1, index_b+1)

    def add_R(self, the_R: Set[Tuple[int,int]])->None:
        if self.is_complete(the_R):
            for exist_R in self.result:
                if exist_R == the_R:
                    return
            self.result.append(the_R)

    def is_complete(self, the_R: Set[Tuple[int,int]]) ->bool:
        return len(set([i for (i,j) in the_R]))==self.len_a or len(set([j for (i,j) in the_R]))==self.len_b



if __name__ == "__main__":
    result=R_Generator(1,2).get_all_R()
    print(result,f"\n{len(result)}\n")
    assert 2==len(result)

    result=R_Generator(1,3).get_all_R()
    print(result,f"\n{len(result)}\n")
    assert 4==len(result)

    result=R_Generator(1,4).get_all_R()
    print(result,f"\n{len(result)}\n")
    assert 8==len(result)

    result=R_Generator(1,5).get_all_R()
    print(result,f"\n{len(result)}\n")
    assert 16==len(result)

    result=R_Generator(2,3).get_all_R()
    print(result,f"\n{len(result)}\n")
    assert 13==len(result)
