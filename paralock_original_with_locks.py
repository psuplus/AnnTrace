
from program import *

class Paralocks(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label('D'), Label('DN')) 
        lat.add_sub(Label('N'), Label('DN'))
        lat_bot=str(lat.bot)
        self.programs = [
            Program( # ParalockExamples[0]
                secure=True, 
                comment=""" // paralock labels: h:{D}=>low, l:{}=>low
                    open(D);
                    l:= h;
                    close(D);
                    l:= h;""", 
                source_code="""
                    // h:{D}, l:{}
                    open(D); //  h:{}, l:{}
                    l:= h;
                    output(h, {}); 
                    close(D); // h:{D}, l:{}
                    l:= h;
                    output(h, {})""", 
                global_labels={'h':'D', 'l':lat_bot},
                traces=[  
                    # lat_bot ('Bot') for empty lock set(True => a) for the actor; 
                    # lat.top for no lock set(False => a) for actor;  
                    Trace(init_memory=dict(h=0), outputs=[
                        ParalockOut('l', 0, {'h': lat_bot}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1), outputs=[
                        ParalockOut('l', 1, {'h': lat_bot}, 0, 'D'), 
                        ParalockOut('l', 1, {'h': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=2), outputs=[
                        ParalockOut('l', 2, {'h': lat_bot}, 0, 'D'), 
                        ParalockOut('l', 2, {'h': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=3), outputs=[
                        ParalockOut('l', 3, {'h': lat_bot}, 0, 'D'), 
                        ParalockOut('l', 3, {'h': 'D'}, 1, lat_bot)]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[1]
                secure=True, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);  // = declassify(x, {N})
                    y:= x;
                    close(D);
                    open(N);  // = declassify(y, {}); declassify(x, {D})
                    z:=y;""", 
                source_code="""
                    // x:{D,N}, y:{N}, z:{}
                    open(D); // x:{N}; y:{N}, z:{}
                    y:= x;  
                    close(D); // x:{N, D}; y:{N}, z:{}
                    open(N); // x:{D}; y:{}, z:{} 
                    z:= y;""", 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        ParalockOut('y', 0, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 0, {'x': 'D'}, 1, 'N')]),
                    Trace(init_memory=dict(x=1), outputs=[
                        ParalockOut('y', 1, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 1, {'x': 'D'}, 1, 'N')]),
                    Trace(init_memory=dict(x=2), outputs=[
                        ParalockOut('y', 2, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 2, {'x': 'D'}, 1, 'N')]),
                    Trace(init_memory=dict(x=3), outputs=[
                        ParalockOut('y', 3, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 3, {'x': 'D'}, 1, 'N')]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[2]
                secure=False, 
                comment=""" // paralock labels: x:{D,N}=>actor1, y:{N}=>actor1, z:{}=>actor1
                    open(D);
                    y:= x mod 2;
                    close(D);
                    open(N)
                    z:= x;""", 
                source_code="""
                    // x:{D,N}, y:{N}, z:{}
                    open(D); // x:{N}; y:{N}, z:{}
                    y:= x mod 2;  
                    output(x mod 2, {N}); 
                    close(D); // x:{N, D}; y:{N}, z:{}
                    open(N); // x:{D}; y:{}, z:{}
                    z:=x;
                    output(x, {})""", 
                global_labels={'x':'DN', 'y':'N', 'z':lat_bot},
                traces=[ 
                    Trace(init_memory=dict(x=0), outputs=[
                        ParalockOut('y', 0, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 0, {'x': 'D'}, 1, 'N')]),
                    Trace(init_memory=dict(x=1), outputs=[
                        ParalockOut('y', 1, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 1, {'x': 'D'}, 1, 'N')]),
                    Trace(init_memory=dict(x=2), outputs=[
                        ParalockOut('y', 0, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 2, {'x': 'D'}, 1, 'N')]),
                    Trace(init_memory=dict(x=3), outputs=[
                        ParalockOut('y', 1, {'x': 'N'}, 0, 'D'), 
                        ParalockOut('z', 3, {'x': 'D'}, 1, 'N')]),
                ],
                lattice=lat
            ),
            Program( # ParalockExamples[3]
                secure=False, 
                comment=""" // paralock labels: h:{D}=>low, l:{}=>low h2:{N}=>low
                    if h3 then 
                        open(D) l:= h; close(D)
                    else 
                        open(D) l:=h2; close(N)
                    l:= 0;
                    """, 
                source_code="""
                    // h:{D}, l:{}
                    open(D); //  h:{}, l:{}
                    if h2 then 
                        l:= h;
                        output(l, {});
                    else 
                        l:=0
                        output(l, {});
                    close(D); // h:{D}, l:{}
                    if !h2 then 
                        l:= 0;
                        output(l, {});
                    """, 
                global_labels={'h':'D', 'l':lat_bot, 'h2':'D', 'h3':'DN'},
                traces=[  
                    # lat_bot ('Bot') for empty lock set(True => a) for the actor; 
                    # lat.top for no lock set(False => a) for actor;  
                    Trace(init_memory=dict(h=0, h2=0, h3=0), outputs=[
                        ParalockOut('l', 0, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h2=1, h3=0), outputs=[
                        ParalockOut('l', 1, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h2=1, h3=0), outputs=[
                        ParalockOut('l', 1, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h2=0, h3=0), outputs=[
                        ParalockOut('l', 0, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h2=0, h3=1), outputs=[
                        ParalockOut('l', 0, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h2=1, h3=1), outputs=[
                        ParalockOut('l', 0, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h2=1, h3=1), outputs=[
                        ParalockOut('l', 1, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h2=0, h3=1), outputs=[
                        ParalockOut('l', 1, {'h': lat_bot, 'h2': 'N', 'h3': 'DN'}, 0, 'D'),  
                        ParalockOut('l', 0, {'h': 'D', 'h2': 'N', 'h3': 'DN'}, 1, lat_bot)]),
                ],
                lattice=lat
            ),
            
        ]
class Paralocks_Gradual_Misuse(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label('D'), Label('DN')) 
        lat.add_sub(Label('N'), Label('DN'))
        lat_bot=str(lat.bot)
        self.programs = [
            Program( # Encoding of GradualRelease[1] 
                secure=True, 
                comment=""" // paralock labels: h:{D}=>low, l:{}=>low, h1:{D}=>low
                    open(D);
                    if h then l:= h1;
                    close(D);
                    l:=0; // terminating event
                    """, 
                source_code="""
                    // h:{D}, h1: {D}, l:{}
                    open(D); //  h:{}, h1: {}, l:{}
                    if h then 
                        l:= h1;
                        output(l, {});
                    close(D); // h:{D}, h1: {D},l:{}
                    l:=0;
                    output(l, {});
                    """, 
                global_labels={'h':'D', 'l':lat_bot, 'h1':'D'},
                traces=[  
                    # lat_bot ('Bot') for empty lock set(True => a) for the actor; 
                    # lat.top for no lock set(False => a) for actor;  
                    Trace(init_memory=dict(h=1, h1=0), outputs=[
                        ParalockOut('l', 0, {'h': lat_bot, 'h1': lat_bot}, 0, 'D'),
                        ParalockOut('l', 0, {'h': 'D', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h1=1), outputs=[
                        ParalockOut('l', 1, {'h': lat_bot, 'h1': lat_bot}, 0, 'D'),
                        ParalockOut('l', 0, {'h': 'D', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h1=2), outputs=[
                        ParalockOut('l', 2, {'h': lat_bot, 'h1': lat_bot}, 0, 'D'),
                        ParalockOut('l', 0, {'h': 'D', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h1=0), outputs=[
                        ParalockOut('l', 0, {'h': 'D', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h1=1), outputs=[
                        ParalockOut('l', 0, {'h': 'D', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h1=2), outputs=[
                        ParalockOut('l', 0, {'h': 'D', 'h1': 'D'}, 1, lat_bot)]),
                ],
                lattice=lat
            ),
            Program( # Encoding of the GradualRelease_Misuse[0]
                secure=False, 
                comment=""" // 
                    paralock labels: h:{N}=>low, l:{}=>low h1:{D}=>low
                    open(D);
                    if h then l:= h1;
                    close(D);
                    """, 
                source_code="""
                    // h:{N}, h1: {D}, l:{}
                    open(D); //  h:{N}, h1: {}, l:{}
                    if h then 
                        l:= h1;
                        output(l, {});
                    close(D); // h:{D}, l:{}
                    """, 
                global_labels={'h':'N', 'l':lat_bot, 'h1':'D'},
                traces=[  
                    # lat_bot ('Bot') for empty lock set(True => a) for the actor; 
                    # lat.top for no lock set(False => a) for actor;  
                    Trace(init_memory=dict(h=1, h1=0), outputs=[
                        ParalockOut('l', 0, {'h': 'N', 'h1': lat_bot}, 0, 'D'),
                        ParalockOut('l', 0, {'h': 'N', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h1=1), outputs=[
                        ParalockOut('l', 1, {'h': 'N', 'h1': lat_bot}, 0, 'D'),
                        ParalockOut('l', 0, {'h': 'N', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=1, h1=2), outputs=[
                        ParalockOut('l', 2, {'h': 'N', 'h1': lat_bot}, 0, 'D'),
                        ParalockOut('l', 0, {'h': 'N', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h1=0), outputs=[
                        ParalockOut('l', 0, {'h': 'N', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h1=1), outputs=[
                        ParalockOut('l', 0, {'h': 'N', 'h1': 'D'}, 1, lat_bot)]),
                    Trace(init_memory=dict(h=0, h1=2), outputs=[
                        ParalockOut('l', 0, {'h': 'N', 'h1': 'D'}, 1, lat_bot)]),
                ],
                lattice=lat
            )
        ]