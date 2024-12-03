from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, NamedTuple
from collections import deque


class Message(NamedTuple):
    dst: str
    src: str
    pulse: bool

@dataclass
class Machines:
    broadcaster: List[str]    
    flips: Dict[str, list]
    conjuctions: Dict[str, List[str]]

    flip_states: Dict[str, bool] = field(default_factory=dict)
    conjuctions_memory: defaultdict[Dict] = field(default_factory=lambda: defaultdict(dict))
   
    @classmethod
    def parse_raw(cls, raw: str) -> "Machines":
        broadcaster: List[str] = []
        flip_flops: Dict[str, list] = defaultdict(list)
        conjuctions: Dict[str, list] = defaultdict(list)

        for line in raw.split('\n'):
            name, destination = line.split(' -> ')
            if name.startswith('%'):
                #flip flop module
                name = name.strip('%')
                flip_flops[name] += destination.split(', ')
            elif name.startswith('&'):
                # conjuction module
                name = name.strip('&')
                conjuctions[name] += destination.split(', ')
            elif name == 'broadcaster':
                broadcaster += destination.split(', ')
            else:
                raise ValueError(f'Unknown instruction {line}')

        return cls(broadcaster, flip_flops, conjuctions)
    
    def __post_init__(self):
        """Initialize the state of the machines"""
        
        # All the flips starts with False
        for flip in self.flips:
            self.flip_states[flip] = False
            
        # Connections starts with a low memory for each input modules
        # for key in self.conjuctions.keys():
        #     self.conjuctions_memory[key] = {flip: False for flip, flip_items in self.flips.items() if key in flip_items}
        for key, dsts in self.flips.items():
            for item in dsts:
                if item in self.conjuctions:
                    self.conjuctions_memory[item][key] = False

    def press_buttons(self, buttons=1):
        
        low_pulses = 0
        high_pulses = 0
        
        for _ in range(buttons):
            lo, hi = self.run()
            low_pulses +=  lo
            high_pulses += hi
            
        return low_pulses * high_pulses
 
    def wait_rx(self):
        
        from tqdm import tqdm
        pbar = tqdm(leave=False)
        i = 0
        done = False
        while not done:
            i += 1
            pbar.update(i)
            _ = self.run()
            if self.conjuctions_memory['rx'] and all(self.conjuctions_memory['rx'].values()):
                done = True
        return i
                
    def press_looking(self, buttons=1, look_for=None):

        seen = defaultdict(list)
               
        for i in range(buttons):
            
            queue = deque()
            # Press the button, send a low to the broadcaster
            queue.append(Message('broadcaster', 'button', False))
            
            while queue:
                # print('\n'.join([str(self.flip_states), str(self.conjuctions_memory), str(queue), '']))
                msg = queue.popleft()
                if msg.src in look_for and msg.pulse:
                    seen[msg.src].append(i)

                if msg.dst in self.flips and msg.pulse is False:
                    # However, if a flip-flop module receives a low pulse, 
                    # it flips between on and off. If it was off, it turns on 
                    # and sends a high pulse. If it was on, 
                    # it turns off and sends a low pulse.
                    self.flip_states[msg.dst] = not self.flip_states[msg.dst]
                    for dst in self.flips[msg.dst]:
                        queue.append(Message(dst, msg.dst, self.flip_states[msg.dst]))
                elif msg.dst in self.conjuctions:
                    # When a pulse is received, the conjunction module 
                    # - first updates its memory for that input. 
                    # - Then, if it remembers high pulses for all inputs, 
                    #   it sends a low pulse; otherwise, it sends a high pulse.   
                    self.conjuctions_memory[msg.dst][msg.src] = msg.pulse
                    pulse = not all(self.conjuctions_memory[msg.dst].values())
                    for dst in self.conjuctions[msg.dst]:
                        queue.append(Message(dst, msg.dst, pulse))
                    
                elif msg.dst == 'broadcaster':
                    for dst in self.broadcaster:
                        queue.append(Message(dst, 'broadcaster', msg.pulse))
        
        return seen
        
    
    def run(self):

        low_pulses = 0
        high_pulses = 0
        
        queue = deque()
        # Press the button, send a low to the broadcaster
        queue.append(Message('broadcaster', 'button', False))
        
        while queue:
            # print('\n'.join([str(self.flip_states), str(self.conjuctions_memory), str(queue), '']))
            msg = queue.popleft()

            if msg.pulse: 
                high_pulses += 1
            else:
                low_pulses += 1
                
            if msg.dst in self.flips and msg.pulse is False:
                # However, if a flip-flop module receives a low pulse, 
                # it flips between on and off. If it was off, it turns on 
                # and sends a high pulse. If it was on, 
                # it turns off and sends a low pulse.
                self.flip_states[msg.dst] = not self.flip_states[msg.dst]
                for dst in self.flips[msg.dst]:
                    queue.append(Message(dst, msg.dst, self.flip_states[msg.dst]))
            elif msg.dst in self.conjuctions:
                # When a pulse is received, the conjunction module 
                # - first updates its memory for that input. 
                # - Then, if it remembers high pulses for all inputs, 
                #   it sends a low pulse; otherwise, it sends a high pulse.   
                self.conjuctions_memory[msg.dst][msg.src] = msg.pulse
                pulse = not all(self.conjuctions_memory[msg.dst].values())
                for dst in self.conjuctions[msg.dst]:
                    queue.append(Message(dst, msg.dst, pulse))
                
            elif msg.dst == 'broadcaster':
                for dst in self.broadcaster:
                    queue.append(Message(dst, 'broadcaster', msg.pulse))
        
        return low_pulses, high_pulses
        

RAW="""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
 
MACHINES = Machines.parse_raw(RAW)
assert MACHINES.run() == (8, 4)
assert all([item == 0 for item in MACHINES.flip_states.values()])
assert all([item == 0 for con in MACHINES.conjuctions_memory.values() for item in con.values()])
assert MACHINES.press_buttons(buttons=1_000) == 32_000_000

RAW="""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""


MACHINES = Machines.parse_raw(RAW)
MACHINES.run()
assert all([item == 1 for item in MACHINES.flip_states.values()])
assert all([item == 1 for con in MACHINES.conjuctions_memory.values() for item in con.values()])
for _ in range(3):
    MACHINES.run()
assert all([item == 0 for item in MACHINES.flip_states.values()])
assert all([item == 0 for con in MACHINES.conjuctions_memory.values() for item in con.values()])    
MACHINES = Machines.parse_raw(RAW)
assert MACHINES.press_buttons(buttons=1_000) == 11687500


with open('day20.txt', 'r') as f:
    raw = f.read()
    
machines = Machines.parse_raw(raw)
print(machines.press_buttons(buttons=1_000))

# Part 2 can not be brute forced... must be cycle....
machines = Machines.parse_raw(raw)

import pydot

graph = pydot.Dot("my_graph", graph_type="graph")
for key in machines.flips:
    graph.add_node(pydot.Node(key, shape="circle"))
for key in machines.conjuctions:
    graph.add_node(pydot.Node(key, shape="square"))

for key, value in machines.flips.items():
    for dst in value:
        graph.add_edge(pydot.Edge(key, dst))

for key, value in machines.conjuctions.items():
    for dst in value:
        graph.add_edge(pydot.Edge(key, dst))

graph.write_dot('day20.dot')
graph.write_png('day20.png')


# machines.wait_rx()
look_for = [key for key, values in machines.conjuctions.items() if 'rx' in values] + \
    [key for key, values in machines.flips.items() if 'rx' in values]
print(look_for)
look_for = [key for item in look_for for key, values in machines.conjuctions.items() if item in values] + \
    [key for item in look_for for key, values in machines.flips.items() if item in values]
print(look_for)
look_for = [key for item in look_for for key, values in machines.conjuctions.items() if item in values] + \
    [key for item in look_for for key, values in machines.flips.items() if item in values]
print(look_for)
result = machines.press_looking(5000, look_for=look_for)