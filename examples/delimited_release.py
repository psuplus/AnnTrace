#!/usr/bin/env python3
# python >= 3.7

from program import *

class DelimitedRelease_Avg(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=True,
                comment=""" syntax using delimted release
                    // h1, h2:H, avg:L
                    avg := declassify((h1+h2)/2, L)""",
                source_code="""
                    // h1, h2:H, avg:L,
                    // e=(h1+h2)/2 :L
                    avg := (h1+h2)/2
                    output(avg, L);""",
                traces=[
                    Trace(init_memory=dict(h1=0, h2=2,e=1), outputs=[
                        Out('L', 1, {'h1': 'H', 'h2': 'H','e':'L' }, 0)]),
                    Trace(init_memory=dict(h1=1, h2=1,e=1), outputs=[
                        Out('L', 1, {'h1': 'H', 'h2': 'H','e':'L' }, 0)]),
                    Trace(init_memory=dict(h1=2, h2=0,e=1), outputs=[
                        Out('L', 1, {'h1': 'H', 'h2': 'H','e':'L' }, 0)]),
                    Trace(init_memory=dict(h1=2, h2=2,e=2), outputs=[
                        Out('L', 2, {'h1': 'H', 'h2': 'H','e':'L' }, 0)]),
                    Trace(init_memory=dict(h1=1, h2=3,e=2), outputs=[
                        Out('L', 2, {'h1': 'H', 'h2': 'H','e':'L' }, 0)]),
                    Trace(init_memory=dict(h1=3, h2=1,e=2), outputs=[
                        Out('L', 2, {'h1': 'H', 'h2': 'H','e':'L' }, 0)]),
                ]
            ),
            Program(
                secure=False,
                comment=""" syntax using delimted release
                    // h1, h2:H, avg:L
                    h2:=h1
                    avg := declassify((h1+h2)/2, L)""", 
                source_code=""" 
                    // h1, h2:H, avg:L,
                    // e=(h1+h2)/2 :L
                    h2:=h1
                    output(h2, H);
                    avg := (h1+h2)/2
                    output(avg, L);""",
                traces=[
                    Trace(init_memory=dict(h1=0, e=1), outputs=[
                        Out('H', 0, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 0, {'h1': 'H', 'e':'L' }, 1)]),
                    Trace(init_memory=dict(h1=1, e=1), outputs=[
                        Out('H', 1, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 1, {'h1': 'H', 'e':'L' }, 1)]),
                    Trace(init_memory=dict(h1=2, e=1), outputs=[
                        Out('H', 2, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 2, {'h1': 'H', 'e':'L' }, 1)]),
                    Trace(init_memory=dict(h1=2, e=2), outputs=[
                        Out('H', 2, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 2, {'h1': 'H', 'e':'L' }, 1)]),
                    Trace(init_memory=dict(h1=1, e=2), outputs=[
                        Out('H', 1, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 1, {'h1': 'H', 'e':'L' }, 1)]),
                    Trace(init_memory=dict(h1=3, e=2), outputs=[
                        Out('H', 3, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 3, {'h1': 'H', 'e':'L' }, 1)]),
                    Trace(init_memory=dict(h1=3, e=3), outputs=[
                        Out('H', 3, {'h1': 'H', 'e':'L' }, 0),
                        Out('L', 3, {'h1': 'H', 'e':'L' }, 1)]),
                ]
            )
        ]

class DelimitedRelease_Wallet(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=True, 
                comment=""" syntax using delimted release
                    // h:H, k, l:L
                    if declassify(h>k, low) then 
                        h:= h-k;
                        l:= l+k
                    else 
                        skip""", 
                source_code=""" 
                    // h:H, k, l:L
                    // e=h>k : L
                    if (h>k) then
                        h:= h-k;
                        output(h, H);
                        l:= l+k 
                        output(l, L);
                    else
                        skip""", 
                traces=[
                    Trace(init_memory=dict(h=1, k=1, l=0, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=1, l=0, e=1), outputs=[
                        Out('H', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=2, l=-1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 1)]),
                    Trace(init_memory=dict(h=1, k=1, l=1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 0),  
                        Out('L', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=1, l=1, e=1), outputs=[
                        Out('H', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 0),  
                        Out('L', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=2, l=1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 0),  
                        Out('L', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L'}, 1)]),
                    Trace(init_memory=dict(h=1, k=3, l=1, e=0), outputs=[]),
                    Trace(init_memory=dict(h=1, k=2, l=0, e=0), outputs=[]),
                    Trace(init_memory=dict(h=0, k=2, l=1, e=0), outputs=[]),
                    Trace(init_memory=dict(h=0, k=2, l=0, e=0), outputs=[]),
                ]
            ),
            Program(
                secure=False, 
                comment=""" syntax using delimted release
                    // h:H, k, l, n:L
                    l:=0
                    while (n>=0) do {
                        k:= a^(n-1)
                        if declassify(h>k, low) then 
                            h:= h-k;
                            l:= l+k
                        n:=n-1
                    }""", 
                source_code=""" 
                    // h:H, k, l, n:L
                    // e=h>k : L
                    l:=0
                    while (n>=0) do {
                        k:= 2^n
                        if h>k then 
                            h:= h-k;
                            output(h, H);
                            l:= l+k 
                            output(l, L);
                        n:=n-1
                    }""", 
                traces=[
                    Trace(init_memory=dict(h=1, k=1, n=0, l=0, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'L', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'L', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=1, k=1, n=1, l=0, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=1, n=0, l=0, e=1), outputs=[
                        Out('H', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=1, n=1, l=0, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0), 
                        Out('H', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=1, n=2, l=0, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0), 
                        Out('H', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=2, n=0, l=-1, e=1), outputs=[
                        Out('H', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=2, k=2, n=1, l=-1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=1, k=1, n=0, l=1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=1, k=1, n=1, l=1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=4, k=2, n=0, l=1, e=1), outputs=[
                        Out('H', 3, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=4, k=2, n=1, l=1, e=1), outputs=[
                        Out('H', 2, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 3, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1),
                        Out('H', 1, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 4, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=4, k=2, n=2, l=1, e=1), outputs=[
                        Out('H', 0, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 0),  
                        Out('L', 5, {'h': 'H', 'k':'H', 'l':'L', 'e':'L', 'n':'L'}, 1)]),
                    Trace(init_memory=dict(h=0, k=2, n=0, l=1, e=0), outputs=[]),
                    Trace(init_memory=dict(h=0, k=2, n=1, l=1, e=0), outputs=[]),
                    Trace(init_memory=dict(h=0, k=1, n=0, l=0, e=0), outputs=[]),
                    Trace(init_memory=dict(h=0, k=1, n=1, l=0, e=0), outputs=[]),
                ]
            )
        ]

class DelimitedRelease_Parity(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=False,
                comment=""" syntax using delimted release
                    // h:H, l:L
                    h:=parity(h);
                    if declassify(h==1, low) then
                        l:=1
                        h:=1
                    else
                        l:=0
                        h:=0
                    """,
                source_code="""
                    // h:H, l:L
                    // h1 = (h==1) : L
                    // h2 = parity(h)
                    h:= h2;
                    if (h==1) then
                        l:=1
                        output(1, L)
                        h:=1
                        output(1, H)
                    else
                        l:=0
                        output(0, L)
                        h:=0
                        output(0, H)
                    """,
                global_labels={'h1': 'L', 'h2':'H'},
                traces=[
                    Trace(init_memory=dict(h1=0, h2=0), outputs=[
                        Out('L', 0, {'h1': 'L', 'h2': 'H'}, 2),
                        Out('H', 0, {'h1': 'L', 'h2': 'H'}, 3)]),
                    Trace(init_memory=dict(h1=0, h2=1), outputs=[
                        Out('L', 1, {'h1': 'L', 'h2': 'H'}, 0),
                        Out('H', 1, {'h1': 'L', 'h2': 'H'}, 1)]),
                    Trace(init_memory=dict(h1=1, h2=0), outputs=[
                        Out('L', 0, {'h1': 'L', 'h2': 'H'}, 2),
                        Out('H', 0, {'h1': 'L', 'h2': 'H'}, 3)]),
                    Trace(init_memory=dict(h1=1, h2=1), outputs=[
                        Out('L', 1, {'h1': 'L', 'h2': 'H'}, 0),
                        Out('H', 1, {'h1': 'L', 'h2': 'H'}, 1)])
                ]
            ),
            Program(
                secure=True, 
                comment=""" syntax using delimted release
                    // h:H, l:L
                    if declassify(parity(h), low) then
                        l:=1
                        h:=1
                    else
                        l:=0
                        h:=0
                    """,
                source_code="""
                    // h:H, l:L
                    // h2 = parity(h) :L
                    if parity(h) then
                        l:=1
                        output(1, L)
                        h:=1
                        output(1, H)
                    else
                        l:=0
                        output(0, L)
                        h:=0
                        output(0, H)
                    """,
                global_labels={'h': 'H', 'h2':'L'},
                traces=[
                    Trace(init_memory=dict(h=0, h2=0), outputs=[
                        Out('L', 0, {'h': 'H', 'h2': 'L'}, 2),
                        Out('H', 0, {'h': 'H', 'h2': 'L'}, 3)]),
                    Trace(init_memory=dict(h=0, h2=1), outputs=[
                        Out('L', 1, {'h': 'H', 'h2': 'L'}, 0),
                        Out('H', 1, {'h': 'H', 'h2': 'L'}, 1)]),
                    Trace(init_memory=dict(h=1, h2=0), outputs=[
                        Out('L', 0, {'h': 'H', 'h2': 'L'}, 2),
                        Out('H', 0, {'h': 'H', 'h2': 'L'}, 3)]),
                    Trace(init_memory=dict(h=1, h2=1), outputs=[
                        Out('L', 1, {'h': 'H', 'h2': 'L'}, 0),
                        Out('H', 1, {'h': 'H', 'h2': 'L'}, 1)])
                ]
            ),
        ]

class DelimitedRelease_Fail(Examples):
    def __init__(self):
        self.programs = [ # adapted from the example in Page 8 of Delimited Release
            Program(
                secure=False,
                comment=""" syntax using delimted release
                    // x:H, y:L
                    if false:
                        y:= declassify(x, L); // Dead code
                    // x:L
                    y:=x""",
                source_code=""" 
                    // x:L, the sensitivity of x is downgraded anywa
                    if false:
                        y:= x;
                        output(y, L)
                    y:=x
                    output(y, L)""",
                global_labels={'x':'L'}, # Delimited Release misinterpretated as x:L
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 2, {'x': 'H'}, 1)])
                ]
            )
        ]