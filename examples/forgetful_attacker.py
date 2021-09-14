#!/usr/bin/env python3
# python >= 3.7

from program import *

class ForgetfulAttacker_1(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("U"), lat.top)
        self.programs = [
            Program(# P1 in the paper
                secure=False, 
                source_code="""
                    // nuke1, nuke2: U
                    output(nuke1, U);
                    // nuke1, nuke2: top
                    output(nuke2, U)""", 
                traces=[
                    Trace(init_memory=dict(nuke1=0, nuke2=0), outputs=[
                        Out('U', 0, {'nuke1': 'U', 'nuke2': 'U'}, 0),
                        Out('U', 0, {'nuke1': str(lat.top), 'nuke2': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=0, nuke2=1), outputs=[
                        Out('U', 0, {'nuke1': 'U', 'nuke2': 'U'}, 0),
                        Out('U', 1, {'nuke1': str(lat.top), 'nuke2': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=1, nuke2=0), outputs=[
                        Out('U', 1, {'nuke1': 'U', 'nuke2': 'U'}, 0),
                        Out('U', 0, {'nuke1': str(lat.top), 'nuke2': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=1, nuke2=1), outputs=[
                        Out('U', 1, {'nuke1': 'U', 'nuke2': 'U'}, 0),
                        Out('U', 1, {'nuke1': str(lat.top), 'nuke2': str(lat.top)}, 1)]),
                ],
                lattice=lat
            )
        ]

class ForgetfulAttacker_2(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("U"), lat.top)
        self.programs = [
            Program(# P2 in the paper, when is insecure
                secure=False, 
                source_code="""
                    // nuke1: U
                    output(nuke1, U);
                    // nuke1: top
                    output(nuke1, U)""", 
                persistent=False, 
                traces=[
                    Trace(init_memory=dict(nuke1=0), outputs=[
                        Out('U', 0, {'nuke1': 'U'}, 0),
                        Out('U', 0, {'nuke1': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=1), outputs=[
                        Out('U', 1, {'nuke1': 'U'}, 0),
                        Out('U', 1, {'nuke1': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=2), outputs=[
                        Out('U', 2, {'nuke1': 'U'}, 0),
                        Out('U', 2, {'nuke1': str(lat.top)}, 1)]),
                ],
                lattice=lat
            ),
            Program(#  P2 in the paper, when is secure
                secure=True, 
                source_code="""
                    // nuke1: U
                    output(nuke1, U);
                    // nuke1: top
                    output(nuke1, U)""", 
                persistent=True, 
                traces=[
                    Trace(init_memory=dict(nuke1=0), outputs=[
                        Out('U', 0, {'nuke1': 'U'}, 0),
                        Out('U', 0, {'nuke1': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=1), outputs=[
                        Out('U', 1, {'nuke1': 'U'}, 0),
                        Out('U', 1, {'nuke1': str(lat.top)}, 1)]),
                    Trace(init_memory=dict(nuke1=2), outputs=[
                        Out('U', 2, {'nuke1': 'U'}, 0),
                        Out('U', 2, {'nuke1': str(lat.top)}, 1)])
                ],
                lattice=lat
            ),
        ]

class ForgetfulAttacker_3(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("C"), lat.top)
        self.programs = [
            Program(#  P4 in the paper,
                secure=False, 
                source_code="""
                    // a, b: C
                    output(a+b, C);
                    // b: C, a:Top
                    output(a, C)""", 
                persistent=False, 
                traces=[
                    Trace(init_memory=dict(a=0, b=0), outputs=[
                        Out('C', 0, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 0, {'a': str(lat.top), 'b':'C'}, 1)]),
                    Trace(init_memory=dict(a=0, b=1), outputs=[
                        Out('C', 1, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 0, {'a': str(lat.top), 'b':'C'}, 1)]),
                    Trace(init_memory=dict(a=1, b=0), outputs=[
                        Out('C', 1, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 1, {'a': str(lat.top), 'b':'C'}, 1)]),
                    Trace(init_memory=dict(a=1, b=1), outputs=[
                        Out('C', 2, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 1, {'a': str(lat.top), 'b':'C'}, 1)]),
                    Trace(init_memory=dict(a=2, b=0), outputs=[
                        Out('C', 2, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 2, {'a': str(lat.top), 'b':'C'}, 1)]),
                    Trace(init_memory=dict(a=2, b=2), outputs=[
                        Out('C', 4, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 2, {'a': str(lat.top), 'b':'C'}, 1)]),
                    Trace(init_memory=dict(a=0, b=2), outputs=[
                        Out('C', 2, {'a': 'C', 'b':'C'}, 0),
                        Out('C', 0, {'a': str(lat.top), 'b':'C'}, 1)])
                ],
                lattice=lat
            ),
        ]

class ForgetfulAttacker_4(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("A"), lat.top)
        lat.add_sub(Label("H"), lat.top)
        self.programs = [
            Program(# Figure 3 in the paper
                secure=True, 
                source_code="""
                    // x: A
                    if (x>0) then output(1, A);
                        else output(2, A);
                    // x: H
                    output(3, A)""",  
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('A', 2, {'x': 'A'}, 0),
                        Out('A', 3, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('A', 1, {'x': 'A'}, 0),
                        Out('A', 3, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('A', 1, {'x': 'A'}, 0),
                        Out('A', 3, {'x': 'H'}, 1)]),
                ],
                lattice=lat
            ),
        ]
# P3 is controversial
# P5 is designed for termination sensitive policy, so we exclude it
# P6, P7 are interactive programs. We don't support
# P9 the security policy changes the semantics of the program. We don't support this.
class ForgetfulAttacker_5(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("A"), lat.top)
        lat.add_sub(Label("B"), lat.top)
        self.programs = [
            Program(# P8 in the paper
                secure=True, 
                source_code="""
                    // x: B
                    if (x>0) then output(1, B)
                    // x: A
                    output(2, B)""",  
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('B', 1, {'x': 'B'}, 0),
                        Out('B', 2, {'x': 'A'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('B', 2, {'x': 'A'}, 1)]),
                ],
                lattice=lat
            ),
        ]