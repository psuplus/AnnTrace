#!/usr/bin/env python3
# python >= 3.7

from program import *

class GradualRelease(Examples):
    # GradualRelease assumes there is an observable low terminating event at the
    # end of the program. We will add an explicit output(0) as terminating event if need.
    def __init__(self):
        self.programs = [
            Program( # GradualRelease[0]
                secure=False, 
                comment=""" using gradual release syntax  
                    // h:H, l:L
                    l:=h
                    """, 
                source_code=""" 
                    // h:H, l:L
                    l:=h
                    output(l, L);""",
                traces=[
                    Trace(init_memory=dict(h=0), outputs=[
                        Out('L', 0, {'h': 'H'}, 1)]),
                    Trace(init_memory=dict(h=1), outputs=[
                        Out('L', 1, {'h': 'H'}, 1)]),
                    Trace(init_memory=dict(h=2), outputs=[
                        Out('L', 2, {'h': 'H'}, 1)]),  
                ]
            ),
             Program(  # GradualRelease[1] with extra terminating event
            #  Note that we change the truth value of this example 
            # See the GradualRelease_Misuses and the discussion in the paper
                secure=True,
                comment=""" using gradual release syntax
                    // h:H, l:L
                    if h then l:= declassify(h1)
                    """, 
                source_code=  # Using the encoding proved equivalent by the paper
                # see the misuse of Gradual Release discussed in the paper
                    """ 
                    // h, h1: L, l:L
                    if h then
                        l:=h1
                        output(l, L); 
                    // h, h1: H
                    output(0, L); //terminating event
                    """,
                traces=[
                    Trace(init_memory=dict(h=2, h1=0), outputs=[
                        Out('L', 0, {'h': 'L', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=1, h1=1), outputs=[
                        Out('L', 1, {'h': 'L', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=0, h1=0), outputs=[
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=0, h1=1), outputs=[
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                ]
            ),
            Program( # GradualRelease[2]
                secure=True,
                comment=""" using gradual release syntax
                    // h:H, l:L
                    l:= declassify(h)
                    """,
                source_code=""" 
                    // h:H, l:L
                    l:=h
                    output(l, L); // h: L
                    """,
                traces=[
                    Trace(init_memory=dict(h=0), outputs=[
                        Out('L', 0, {'h': 'L'}, 0)]),
                    Trace(init_memory=dict(h=1), outputs=[
                        Out('L', 1, {'h': 'L'}, 0)]),
                    Trace(init_memory=dict(h=2), outputs=[
                        Out('L', 2, {'h': 'L'}, 0)]),
                ]
            ),
            Program(  # GradualRelease[3] with extra terminating event
                secure=True,
                comment=""" using gradual release syntax
                    // h, h1:H, l:L
                    l := declassify(h!=0)
                    if l then l1:= declassify(h1)
                    """,
                source_code="""
                    // h:H, l:L
                    l:= (h != 0)
                    output(l, L); // h : L
                    if l then
                        l1:=h1
                        output(l, L);
                    output(0, L); //terminating event
                    """, 
                traces=[
                    Trace(init_memory=dict(h=2, h1=0), outputs=[
                        Out('L', 1, {'h': 'L', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'L', 'h1': 'L'}, 1),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 2)]),
                    Trace(init_memory=dict(h=1, h1=1), outputs=[
                        Out('L', 1, {'h': 'L', 'h1': 'L'}, 0),
                        Out('L', 1, {'h': 'L', 'h1': 'L'}, 1),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 2)]),
                    Trace(init_memory=dict(h=0, h1=0), outputs=[
                        Out('L', 0, {'h': 'L', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=0, h1=1), outputs=[
                        Out('L', 0, {'h': 'L', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                ]
            ),
            Program( # GradualRelease[4]
                secure=False,
                comment=""" using gradual release syntax
                    // h:H, l:L
                    h1:=h2;
                    h2:=0;
                    l1:= declassify(h2);
                    h2:=h1;
                    l2:=h2;
                    """,
                source_code="""
                    // h:H, l:L
                    h1:=h2;
                    output(h1, H);
                    h2:=0;
                    output(h2, H);
                    l1:= h2;
                    output(l1, L); // h2: L
                    h2:=h1;
                    output(h2, H);
                    l2:=h2;
                    output(l2, L);
                    """,
                traces=[
                    Trace(init_memory=dict(h2=0), outputs=[
                        Out('H', 0, {'h2': 'H'}, 0),
                        Out('H', 0, {'h2': 'H'}, 1),
                        Out('L', 0, {'h2': 'L'}, 2),
                        Out('H', 0, {'h2': 'H'}, 3),
                        Out('L', 0, {'h2': 'H'}, 4)]),
                    Trace(init_memory=dict(h2=1), outputs=[
                        Out('H', 1, {'h2': 'H'}, 0),
                        Out('H', 0, {'h2': 'H'}, 1),
                        Out('L', 0, {'h2': 'L'}, 2),
                        Out('H', 1, {'h2': 'H'}, 3),
                        Out('L', 1, {'h2': 'H'}, 4)]),
                    Trace(init_memory=dict(h2=2), outputs=[
                        Out('H', 2, {'h2': 'H'}, 0),
                        Out('H', 0, {'h2': 'H'}, 1),
                        Out('L', 0, {'h2': 'L'}, 2),
                        Out('H', 2, {'h2': 'H'}, 3),
                        Out('L', 2, {'h2': 'H'}, 4)]),
                ]
            ),
            Program( # GradualRelease[5]
                secure=True,
                comment=""" using gradual release syntax
                    // h:H, l:L
                    l:= declassify(h);
                    l:= h;
                    """,
                source_code="""
                    // h:H, l:L
                    l:= h;
                    output(L, l); // h: L
                    l:=h;
                    output(L, l); // h: H
                    """,
                traces=[
                    Trace(init_memory=dict(h=0), outputs=[
                        Out('L', 0, {'h': 'L'}, 0),
                        Out('L', 0, {'h': 'H'}, 1)]),
                    Trace(init_memory=dict(h=1), outputs=[
                        Out('L', 1, {'h': 'L'}, 0),
                        Out('L', 1, {'h': 'H'}, 1)]),
                    Trace(init_memory=dict(h=2), outputs=[
                        Out('L', 2, {'h': 'L'}, 0),
                        Out('L', 1, {'h': 'H'}, 1)]),
                ]
            )
        ]

class GradualRelease_Misuse(Examples):
    # GradualRelease assumes there is an observable low terminating event at the
    # end of the program. 
    def __init__(self):
        self.programs = [
            Program(  # Misused of GradualRelease[1] 
                secure=False,
                comment= # One might incorrectly use gradual release as:
                    """ 
                    // h:H, l:L
                    if h then l:= declassify(h1)
                    """, 
                source_code=
                    # Misused of gradual release. 
                    # This program actually can not be encoded by Gradual
                    # Release since it requires selective declassification.
                    """ 
                    // h, h1: L, l:L
                    if h then
                        l:=h1
                        output(l, L); 
                    // h, h1: H
                    output(0, L); //terminating event
                    """,
                traces=[
                    Trace(init_memory=dict(h=2, h1=0), outputs=[
                        Out('L', 0, {'h': 'H', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=1, h1=1), outputs=[
                        Out('L', 1, {'h': 'H', 'h1': 'L'}, 0),
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=0, h1=0), outputs=[
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                    Trace(init_memory=dict(h=0, h1=1), outputs=[
                        Out('L', 0, {'h': 'H', 'h1': 'H'}, 1)]),
                ]
            ),
        ]