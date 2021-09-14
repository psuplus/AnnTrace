#!/usr/bin/env python3
# python >= 3.7

from program import *

class Tricky(Examples):
    def __init__(self):
        self.programs = [
            Program(# Tricky[0]
                secure=True, 
                source_code="""
                    // x:H
                    output(1, L);
                    if (x == 0) output(1, L)
                    // x:L
                    if (x != 0) output(1, L)
                    output(1, L)""", 
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'H'}, 1),
                        Out('L', 1, {'x': 'L'}, 3)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'L'}, 2),
                        Out('L', 1, {'x': 'L'}, 3)])   
                ]
            ),
            Program(# Tricky[1]
                secure=False, 
                source_code="""
                    // x:L
                    output(0, L)
                    // x:H
                    if (x == 0) output(0, L)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'L'}, 0)])   
                ]
            ),
            Program(# Tricky[2]
                secure=False, 
                source_code="""
                    // x:L
                    output(0, L)
                    // x:H
                    if (x == 0) output(0, L)""", 
                persistent=True,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'L'}, 0)])   
                ]
            ),
            Program(# Tricky[3]
                secure=True, 
                source_code="""
                        // x:H
                        output(1, L);   
                        if (x == 0) output(1, L)  
                        // x:L
                        if (x != 0) output(1, L) 
                        output(1, L)""”, 
                        // x:L
                        output(x, L);
                        // x:H
                        output(0, L)""", 
                persistent=True,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'H'}, 1),
                        Out('L', 1, {'x': 'L'}, 3),
                        Out('L', 0, {'x': 'L'}, 4),
                        Out('L', 0, {'x': 'H'}, 5)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'L'}, 2),
                        Out('L', 1, {'x': 'L'}, 3),
                        Out('L', 1, {'x': 'L'}, 4),
                        Out('L', 0, {'x': 'H'}, 5)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'L'}, 2),
                        Out('L', 1, {'x': 'L'}, 3),
                        Out('L', 2, {'x': 'L'}, 4),
                        Out('L', 0, {'x': 'H'}, 5)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'L'}, 2),
                        Out('L', 1, {'x': 'L'}, 3),
                        Out('L', 3, {'x': 'L'}, 4),
                        Out('L', 0, {'x': 'H'}, 5)])    
                ]
            ),
            Program(# Tricky[4]
                secure=True, 
                source_code="""
                    // x:L
                    output(0, L);
                    if (x == 0) output(0, L), 
                    // x:H
                    output(0, L)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'L'}, 1),
                        Out('L', 0, {'x': 'H'}, 2)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 2)]),
                ]
            ),
            Program(# Tricky[5]
                secure=True, 
                source_code="""
                    // x:H
                    output(0, L);
                    // x:L
                    if (x == 0) output(1, L), 
                    // x:H
                    output(0, L),
                    // x:L
                    if (x != 0) output(1, L)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 1, {'x': 'L'}, 1),
                        Out('L', 0, {'x': 'H'}, 2)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 2),
                        Out('L', 1, {'x': 'L'}, 3)]),
                ]
            ),
            Program(# Tricky[6]
                secure=True, 
                source_code="""
                    // x:H
                    output(0, L);
                    // x:L
                    if (x == 0) output(0, L), 
                    // x:H
                    output(0, L),
                    // x:L
                    if (x != 0) output(1, L)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1),
                        Out('L', 0, {'x': 'H'}, 2)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 2),
                        Out('L', 1, {'x': 'L'}, 3)]),
                ]
            ),
        ]


class Erasure(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("M"), lat.top)
        self.programs = [
            Program(# Erasure[0]
                secure=True, 
                source_code="""
                    // credit_card: M
                    copy := credit_Card
                    output(copy, M);
                    // credit_card: Top
                    copy := 0;
                    output(copy, M)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(cc=0), outputs=[
                        Out('M', 0, {'cc': 'M'}, 0),
                        Out('M', 0, {'cc': 'Top'}, 1)]),
                    Trace(init_memory=dict(cc=1), outputs=[
                        Out('M', 1, {'cc': 'M'}, 0),
                        Out('M', 0, {'cc': 'Top'}, 1)]),
                    Trace(init_memory=dict(cc=2), outputs=[
                        Out('M', 2, {'cc': 'M'}, 0),
                        Out('M', 0, {'cc': 'Top'}, 1)])   
                ],
                lattice=lat
            ),
            Program(# Erasure[1]
                secure=False, 
                source_code="""
                    // credit_card: M
                    copy := credit_Card
                    output(copy, M);
                    // credit_card: Top
                    // no clear up
                    output(copy, M)""",
                persistent=False, 
                traces=[
                    Trace(init_memory=dict(cc=0), outputs=[
                        Out('M', 0, {'cc': 'M'}, 0),
                        Out('M', 0, {'cc': 'Top'}, 1)]),
                    Trace(init_memory=dict(cc=1), outputs=[
                        Out('M', 1, {'cc': 'M'}, 0),
                        Out('M', 1, {'cc': 'Top'}, 1)]),
                    Trace(init_memory=dict(cc=2), outputs=[
                        Out('M', 2, {'cc': 'M'}, 0),
                        Out('M', 2, {'cc': 'Top'}, 1)])   
                ],
                lattice=lat
            ),
            Program(# Erasure[2]
                secure=True, 
                source_code="""
                    // x:L
                    output(x, L);
                    // x:H
                    output(0, L)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)])   
                ]
            ),
            Program(# Erasure[3]
                secure=True, 
                source_code="""
                    // x:L
                    if (x==1) output(x, L);
                    // x:H
                    output(0, L)""", 
                persistent=False,
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)])   
                ]
            )
        ]

class Revocation(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("L"), Label("Alice"))
        self.programs = [
            Program(# Revocation[0]
                secure=True, 
                source_code="""
                    // book: Alice
                    notes := read(book); // read(x) = x mod 2;
                    output(notes, Alice);
                    // book: Top
                    output(notes, Alice)""", 
                persistent=True,
                traces=[
                    Trace(init_memory=dict(book=0), outputs=[
                        Out('Alice', 0, {'book': 'Alice'}, 0),
                        Out('Alice', 0, {'book': 'Top'}, 1)]),
                    Trace(init_memory=dict(book=1), outputs=[
                        Out('Alice', 1, {'book': 'Alice'}, 0),
                        Out('Alice', 1, {'book': 'Top'}, 1)]),
                    Trace(init_memory=dict(book=2), outputs=[
                        Out('Alice', 0, {'book': 'Alice'}, 0),
                        Out('Alice', 0, {'book': 'Top'}, 1)]),
                    Trace(init_memory=dict(book=3), outputs=[
                        Out('Alice', 1, {'book': 'Alice'}, 0),
                        Out('Alice', 1, {'book': 'Top'}, 1)])      
                ],
                lattice=lat
            ),
            Program(# Revocation[1]
                secure=False, 
                source_code="""
                    // book: Alice
                    notes := read(book); // read(x) = x mod 2;
                    output(note, Alice);
                    // book: Top
                    output(book, Alice)""", 
                persistent=True,
                traces=[
                    Trace(init_memory=dict(book=0), outputs=[
                        Out('Alice', 0, {'book': 'Alice'}, 0),
                        Out('Alice', 0, {'book': 'Top'}, 1)]),
                    Trace(init_memory=dict(book=1), outputs=[
                        Out('Alice', 1, {'book': 'Alice'}, 0),
                        Out('Alice', 1, {'book': 'Top'}, 1)]),
                    Trace(init_memory=dict(book=2), outputs=[
                        Out('Alice', 0, {'book': 'Alice'}, 0),
                        Out('Alice', 2, {'book': 'Top'}, 1)]),
                    Trace(init_memory=dict(book=3), outputs=[
                        Out('Alice', 1, {'book': 'Alice'}, 0),
                        Out('Alice', 3, {'book': 'Top'}, 1)])    
                ],
                lattice=lat
            ),
            Program(# Revocation[2]
                secure=True, 
                source_code="""
                    // x:L
                    output(x, L);
                    // x:H
                    output(0, L)""", 
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)])   
                ]
            ),
            Program(# Revocation[3]
                secure=True, 
                source_code="""
                    // x:L
                    output(x, L);
                    // x:H
                    output(x, L)""", 
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 1, {'x': 'H'}, 1)])   
                ]
            ),
            Program(# Revocation[4]
                secure=True, 
                source_code="""
                    // x:L
                    if (x==1) output(x, L);
                    // x:H
                    output(0, L)""", 
                traces=[
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'L'}, 0),
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 0, {'x': 'H'}, 1)])
                ]
            ),
            
        ]

class Declassification(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("L"), Label("Alice"))
        self.programs = [
            Program(# Declassification[0]
                secure=True, 
                source_code="""
                    // bid:Alice
                    submit:= bid;
                    output(submit, Alice);
                    // bid:L
                    output(submit, L);""", 
                traces=[
                    Trace(init_memory=dict(bid=1), outputs=[
                        Out('Alice', 1, {'bid': 'Alice'}, 0),
                        Out('L', 1, {'bid': 'L'}, 1)]),
                    Trace(init_memory=dict(bid=2), outputs=[
                        Out('Alice', 2, {'bid': 'Alice'}, 0),
                        Out('L', 2, {'bid': 'L'}, 1)])   
                ],
                lattice=lat
            ),
            Program(# Declassification[1]
                secure=False, 
                source_code="""
                    // bid:H
                    submit:= bid;
                    output(submit, L);
                    // bid:L
                    output(submit, L);""", 
                traces=[
                    Trace(init_memory={"bid": 1}, outputs=[
                        Out('L', 1, {'bid': 'Alice'}, 0),
                        Out('L', 1, {'bid': 'L'}, 1)]),
                    Trace(init_memory={"bid": 2}, outputs=[
                        Out('L', 2, {'bid': 'Alice'}, 0),
                        Out('L', 2, {'bid': 'L'}, 1)])   
                ],
                lattice=lat
            ),
            Program(# Declassification[2]
                secure=False, 
                source_code="""
                    // x:H
                    output(x, L);
                    // x:L
                    output(0, L)""", 
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)])   
                ]
            ),
            Program(# Declassification[3]
                secure=False, 
                source_code="""
                    // x:H
                    if (x == 0) output(1, L)
                    // x:L
                    output(0, L)""", 
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 1, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'L'}, 1)])   
                ]
            ),
            Program(# Declassification[4]
                secure=False, 
                source_code="""
                    // x:H
                    i := 0;
                    while (i <= x) {
                        output(0, L);
                        i++; }
                    // x:L
                    output(0, L)""", 
                traces=[
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'H'}, 0),
                        Out('L', 0, {'x': 'L'}, 1)])   
                ]
            )
        ]

class StaticProgram(Examples): # general purpose
    def __init__(self):
        self.programs = [
            Program(# StaticProgram[0]
                secure=True, 
                source_code="""
                    // x:H,y:L
                    output(x, H);
                    output(y, H);
                    output(y, L);""", 
                traces=[
                    Trace(init_memory=dict(x=1,y=1), outputs=[
                        Out('H', 1, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 1, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 1, {'x': 'H', 'y':'L'}, 2)]),
                    Trace(init_memory=dict(x=1,y=2), outputs=[
                        Out('H', 1, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 2, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 2, {'x': 'H', 'y':'L'}, 2)]),
                    Trace(init_memory=dict(x=2,y=1), outputs=[
                        Out('H', 2, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 1, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 1, {'x': 'H', 'y':'L'}, 2)]),
                    Trace(init_memory=dict(x=2,y=2), outputs=[
                        Out('H', 2, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 2, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 2, {'x': 'H', 'y':'L'}, 2)])   
                ]
            ),
           Program(# StaticProgram[1]
                secure=False, 
                source_code="""
                    // x:H,y:L
                    output(x, L);
                    output(y, H);
                    output(y, L);""", 
                traces=[
                    Trace(init_memory=dict(x=1,y=1), outputs=[
                        Out('L', 1, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 1, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 1, {'x': 'H', 'y':'L'}, 2)]),
                    Trace(init_memory=dict(x=1,y=2), outputs=[
                        Out('L', 1, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 2, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 2, {'x': 'H', 'y':'L'}, 2)]),
                    Trace(init_memory=dict(x=2,y=1), outputs=[
                        Out('L', 2, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 1, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 1, {'x': 'H', 'y':'L'}, 2)]),
                    Trace(init_memory=dict(x=2,y=2), outputs=[
                        Out('L', 2, {'x': 'H', 'y':'L'}, 0),
                        Out('H', 2, {'x': 'H', 'y':'L'}, 1),
                        Out('L', 2, {'x': 'H', 'y':'L'}, 2)])   
                ]
            )
        ]

