#!/usr/bin/env python3
# python >= 3.7

from program import *

class AccordingToPolicy_Medical(Examples):
    def __init__(self):
        lat=Lattice()
        lat.add_sub(Label("session"), lat.top)
        self.programs = [
            Program(
                secure=False,
                comment=""" code in the paper:
                    // symp, diag : session ->(appEnd) Top
                    if (userReqExit) then
                        appEnd = 1
                    else
                        symp := getUserSymptoms();
                        ...
                        if (containts(symp, 'malaise') && containts(symp, 'fever') && ...) then
                            diag := 'Influenza'
                        else if ...
                            ... """,
                source_code="""
                    // user : session ->(appEnd) Top
                    symp := symptom(user) // = user
                    diag := diagnosis(symptom)  // = symptom
                    if (exit) then
                        set(appEnd)
                    output(symp, session); // check the remaining info
                    output(diag, session);// check the remaining info
                    """,
                traces=[
                    Trace(init_memory=dict(user=0, exit=1), outputs=[
                        Out('session', 0, {'user': 'Top', 'exit': 'session'}, 0),
                        Out('session', 0, {'user': 'Top', 'exit': 'session'}, 1)]),
                    Trace(init_memory=dict(user=0, exit=0), outputs=[
                        Out('session', 0, {'user': 'session', 'exit': 'session'}, 0),
                        Out('session', 0, {'user': 'session', 'exit': 'session'}, 1)]),
                    Trace(init_memory=dict(user=1, exit=1), outputs=[
                        Out('session', 1, {'user': 'Top', 'exit': 'session'}, 0),
                        Out('session', 1, {'user': 'Top', 'exit': 'session'}, 1)]),
                    Trace(init_memory=dict(user=1, exit=0), outputs=[
                        Out('session', 1, {'user': 'session', 'exit': 'session'}, 0),
                        Out('session', 1, {'user': 'session', 'exit': 'session'}, 1)]),
                ],
                lattice=lat
            ),
        ]
