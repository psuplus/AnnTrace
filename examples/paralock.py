#!/usr/bin/env python3
# python >= 3.7

from program import *


class Paralock_Encoded(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label('D'), Label('DN')) 
        lat.add_sub(Label('N'), Label('DN'))
        lat_bot=str(lat.bot)
        self.programs = [
            Program( # ParalockExamples[0] - {D}
                secure=True, 
                comment=""" // paralock labels: h:{D}=>low, l:{}=>low
                    open(D);
                    l:= h;
                    close(D);
                    l:= h;""", 
                source_code=""" For attacker {D}
                    // h:{}, l:{}
                    open(D); //  h:{}, l:{}
                    l:= h;
                    output(h, {}); 
                    close(D); // h:{}, l:{}
                    l:= h;
                    output(h, {})""", 
                global_labels={'h':'D', 'l':lat_bot},
                traces=[  
                    Trace(init_memory=dict(h=0), outputs=[
                        Out(lat_bot, 0, {'h': lat_bot}, 0),  
                        Out(lat_bot, 0, {'h': lat_bot}, 1)]),
                    Trace(init_memory=dict(h=1), outputs=[
                        Out(lat_bot, 1, {'h': lat_bot}, 0), 
                        Out(lat_bot, 1, {'h': lat_bot}, 1)]),
                    Trace(init_memory=dict(h=2), outputs=[
                        Out(lat_bot, 2, {'h': lat_bot}, 0), 
                        Out(lat_bot, 2, {'h': lat_bot}, 1)]),
                    Trace(init_memory=dict(h=3), outputs=[
                        Out(lat_bot, 3, {'h': lat_bot}, 0), 
                        Out(lat_bot, 3, {'h': lat_bot}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[0] - {}
                secure=True, 
                comment=""" // paralock labels: h:{D}=>low, l:{}=>low
                    open(D);
                    l:= h;
                    close(D);
                    l:= h;""", 
                source_code=""" For attacker {}
                    // h:{D}, l:{}
                    open(D); //  h:{}, l:{}
                    l:= h; // = declassify(h)
                    output(h, {});  // release event
                    close(D); // h:{D}, l:{}
                    l:= h;
                    output(h, {})""", 
                global_labels={'h':'D', 'l':lat_bot},
                traces=[  
                    # lat_bot ('Bot') for empty lock set(True => a) for the actor; 
                    # lat.top for no lock set(False => a) for actor;  
                    Trace(init_memory=dict(h=0), outputs=[
                        Out(lat_bot, 0, {'h': lat_bot}, 0),  
                        Out(lat_bot, 0, {'h': 'D'}, 1)]),
                    Trace(init_memory=dict(h=1), outputs=[
                        Out(lat_bot, 1, {'h': lat_bot}, 0), 
                        Out(lat_bot, 1, {'h': 'D'}, 1)]),
                    Trace(init_memory=dict(h=2), outputs=[
                        Out(lat_bot, 2, {'h': lat_bot}, 0), 
                        Out(lat_bot, 2, {'h': 'D'}, 1)]),
                    Trace(init_memory=dict(h=3), outputs=[
                        Out(lat_bot, 3, {'h': lat_bot}, 0), 
                        Out(lat_bot, 3, {'h': 'D'}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[1] - {D}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);  
                    y:= x; 
                    close(D);
                    open(N);  
                    z:=y;""", 
                source_code=""" For attacker {D}
                    // x:{N}, y:{N}, z:{}
                    open(D); // x:{N}; y:{N}, z:{}
                    y:= x;  
                    output(x, {N})
                    close(D); // x:{N}; y:{N}, z:{}
                    open(N); // x:{}; y:{}, z:{} 
                    z:= y;   // = declassify(y)
                    output(y, {}) // release event
                    """, 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('N', 0, {'x': 'N'}, 0), 
                        Out(lat_bot, 0, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('N', 1, {'x': 'N'}, 0),
                        Out(lat_bot, 1, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('N', 2, {'x': 'N'}, 0), 
                        Out(lat_bot, 2, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('N', 3, {'x': 'N'}, 0), 
                        Out(lat_bot, 3, {'x': lat_bot}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[1] - {N}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);  
                    y:= x;
                    close(D);
                    open(N);  
                    z:=y;""", 
                source_code=""" For attacker {N}
                    // x:{D}, y:{}, z:{}
                    open(D); // x:{}; y:{}, z:{}
                    y:= x;   // = declassify(x)
                    output(x, {}) // release event
                    close(D); // x:{D}; y:{}, z:{}
                    open(N); // x:{D}; y:{}, z:{} 
                    z:= y;   
                    output(y, {})
                    """, 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out(lat_bot, 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 0, {'x': 'D'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out(lat_bot, 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 1, {'x': 'D'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out(lat_bot, 2, {'x': lat_bot}, 0), 
                        Out(lat_bot, 2, {'x': 'D'}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out(lat_bot, 3, {'x': lat_bot}, 0), 
                        Out(lat_bot, 3, {'x': 'D'}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[1] - {DN}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);  
                    y:= x;
                    close(D);
                    open(N);  
                    z:=y;""", 
                source_code=""" For attacker {DN}
                    // x:{}, y:{}, z:{}
                    open(D); // x:{}; y:{}, z:{}
                    y:= x;  
                    output(x, {}) 
                    close(D); // x:{}; y:{}, z:{}
                    open(N); // x:{}; y:{}, z:{} 
                    z:= y;  
                    output(y, {})
                    """, 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out(lat_bot, 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 0, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out(lat_bot, 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 1, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out(lat_bot, 2, {'x': lat_bot}, 0), 
                        Out(lat_bot, 2, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out(lat_bot, 3, {'x': lat_bot}, 0), 
                        Out(lat_bot, 3, {'x': lat_bot}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[1] - {}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);  
                    y:= x;
                    close(D);
                    open(N);  
                    z:=y;""", 
                source_code=""" For attacker {}
                    // x:{D,N}, y:{N}, z:{}
                    open(D); // x:{N}; y:{N}, z:{}
                    y:= x;   // = declassify(x)
                    output(x, {N}) // release event
                    close(D); // x:{N, D}; y:{N}, z:{}
                    open(N); // x:{D}; y:{}, z:{}
                    z:= y;  // = declassify(y)
                    output(y, {}) // release event
                    """, 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('N', 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 0, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('N', 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 1, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('N', 2, {'x': lat_bot}, 0), 
                        Out(lat_bot, 2, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('N', 3, {'x': lat_bot}, 0), 
                        Out(lat_bot, 3, {'x': lat_bot}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[2] - {D}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);
                    y:= x mod 2;
                    close(D);
                    open(N)
                    z:= x;""", 
                source_code=""" For attacker {D}
                    // x:{N}, y:{N}, z:{}
                    open(D); // x:{N}; y:{N}, z:{}
                    y:= x mod 2;  
                    output(x mod 2, {N}); 
                    close(D); // x:{N}; y:{N}, z:{}
                    open(N); // x:{}; y:{}, z:{}
                    z:=x; // = declassify(x)
                    output(x, {}) // release event all bot
                    """, 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('N', 0, {'x': 'N'}, 0), 
                        Out(lat_bot, 0, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('N', 1, {'x': 'N'}, 0), 
                        Out(lat_bot, 1, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('N', 0, {'x': 'N'}, 0), 
                        Out(lat_bot, 2, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('N', 1, {'x': 'N'}, 0), 
                        Out(lat_bot, 3, {'x': lat_bot}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[2] - {N}
                secure=False, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);
                    y:= x mod 2;
                    close(D);
                    open(N)
                    z:= x;""", 
                source_code=""" For attacker {N}
                    // x:{D}, y:{}, z:{}
                    open(D); // x:{}; y:{}, z:{}
                    y:= x mod 2;  // = declassify(x)
                    output(x mod 2, {N});  // release event all bot
                    close(D); // x:{D}; y:{}, z:{}
                    open(N); // x:{D}; y:{}, z:{}
                    z:= x;
                    output(x, {})""", 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('N', 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 0, {'x': 'D'}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('N', 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 1, {'x': 'D'}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('N', 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 2, {'x': 'D'}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('N', 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 3, {'x': 'D'}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[2] - {DN}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);
                    y:= x mod 2;
                    close(D);
                    open(N)
                    z:= x;""", 
                source_code=""" For attacker {DN}
                    // x:{}, y:{}, z:{}
                    open(D); // x:{}; y:{}, z:{}
                    y:= x mod 2;  
                    output(x mod 2, {}); 
                    close(D); // x:{}; y:{}, z:{}
                    open(N); // x:{}; y:{}, z:{}
                    z:=x;
                    output(x, {})""", 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out(lat_bot, 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 0, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out(lat_bot, 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 1, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out(lat_bot, 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 2, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out(lat_bot, 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 3, {'x': lat_bot}, 1)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[2] - {}
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);
                    y:= x mod 2;
                    close(D);
                    open(N)
                    z:= x;""", 
                source_code=""" For attacker {}
                    // x:{D,N}, y:{N}, z:{}
                    open(D); // x:{N}; y:{N}, z:{}
                    y:= x mod 2;  // = declassify(x)
                    output(x mod 2, {N}); 
                    close(D); // x:{N, D}; y:{N}, z:{}
                    open(N); // x:{D}; y:{}, z:{}
                    z:=x; // = declassify(x)
                    output(x, {})""", 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        Out('N', 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 0, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=1), outputs=[
                        Out('N', 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 1, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=2), outputs=[
                        Out('N', 0, {'x': lat_bot}, 0), 
                        Out(lat_bot, 2, {'x': lat_bot}, 1)]),
                    Trace(init_memory=dict(x=3), outputs=[
                        Out('N', 1, {'x': lat_bot}, 0), 
                        Out(lat_bot, 3, {'x': lat_bot}, 1)]),
                ],
                lattice=lat
            )
        ]