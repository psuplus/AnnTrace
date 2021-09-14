#!/usr/bin/env python3
# python >= 3.7

from program import *

class CryptoErasure_1(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=False,
                comment=""" syntax in CryptoErasure
                    // msg: L ->(delete) Top
                    display:=msg;
                    output(display, L);
                    compressed := gzip(msg);
                    initi store to compressed
                    display := 0;
                    msg := 0;
                    set(delete);
                    read store into tmp;
                    output(tmp, L)
                    """,
                source_code=""" 
                    // msg:L,
                    display:=msg;
                    output(display, L);
                    compressed := gzip(msg);
                    store := compressed
                    display:=0;
                    msg:=0;
                    // msg: Top
                    tmp:= store
                    output(tmp, L);""",
                persistent=False,
                traces=[
                    Trace(init_memory=dict(msg=0), outputs=[
                        Out('L', 0, {'msg': 'L'}, 0),
                        Out('L', 0, {'msg': 'Top'}, 1)]),
                    Trace(init_memory=dict(msg=1), outputs=[
                        Out('L', 1, {'msg': 'L'}, 0),
                        Out('L', 1, {'msg': 'Top'}, 1)]),
                    Trace(init_memory=dict(msg=2), outputs=[
                        Out('L', 2, {'msg': 'L'}, 0),
                        Out('L', 2, {'msg': 'Top'}, 1)]),
                    Trace(init_memory=dict(msg=3), outputs=[
                        Out('L', 3, {'msg': 'L'}, 0),
                        Out('L', 3, {'msg': 'Top'}, 1)]),
                ]
            )
        ]
class CryptoErasure_2(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=True,
                comment=""" syntax in CryptoErasure
                    // x: L ->(cnd) H
                    output(x, L);
                    x:=0;
                    set(cnd);
                    output(x, L)
                    """, 
                source_code="""
                    // x: L
                    output(x, L);
                    x:=0;
                    // x: H
                    output(x,L)""",
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 2, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('L', 3, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                ]
            ),
        ]
class CryptoErasure_3(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=False,
                comment=""" syntax in CryptoErasure
                    // x: L ->(cnd) H
                    if x>0 then set(cnd) 
                        else skip
                    """, 
                source_code=""" 
                    // x: L ->(cnd) H
                    if x>0 then set(cnd) 
                        else skip
                    output(x,L) // the attacker can see the memory of x
                    """, 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'H'}, 0)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 2, {'x': 'H'}, 0)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('L', 3, {'x': 'H'}, 0)]),
                ]
            )
        ]

class CryptoErasure_4(Examples):
    def __init__(self):
        self.programs = [
            Program(
                secure=False,
                comment=""" syntax in CryptoErasure
                    // x: L ->(cnd) H
                    output(x, L);
                    init file to x;
                    x:=0;
                    set(cnd);
                    read file to y;
                    output(y, L)
                    """, 
                source_code="""
                    // x: L 
                    output(x, L);
                    file := x;
                    x:=0;
                    // x : H
                    y:=file;
                    output(y, L)
                    """, 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 1, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 2, {'x': 'L'}, 0),
                        Out('L', 2, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('L', 3, {'x': 'L'}, 0),
                        Out('L', 3, {'x': 'H'}, 1)]),
                ]
            )
        ]