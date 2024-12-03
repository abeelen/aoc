from dataclasses import dataclass, field
from typing import List, Tuple, Dict, NamedTuple
import re
from tqdm import tqdm
from collections import deque

RAW="""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""

class Rule(NamedTuple):
    key: str
    test: str
    value: int
    output: str
 
@dataclass
class Workflow:
    name: str
    rules: List[Rule]
    default: str

    def __call__(self, part: dict) -> str:
        
        for rule in self.rules:
            value = part.get(rule.key)
            if rule.test == '<' and value < rule.value:
                return rule.output
            elif rule.test == '>' and value > rule.value:
                return rule.output

        return self.default

    @classmethod
    def parse_raw(cls, raw: str) -> "Workflow":
        name, raw_rules, default = re.match('(.*){(.*),(.*)}', raw).groups()
        rules = []
        for item in raw_rules.split(','):
            test, output = item.split(':')
            if test[1] not in ['<', '>']:
                raise ValueError(f'Not implemented {raw}')
            rules.append(Rule(test[0], test[1], int(test[2:]), output))
        return cls(name, rules, default)

@dataclass
class System:
    workflows: Dict[str, Workflow]
    parts: List[Dict]
    rejected: List[Dict] = field(default_factory=list)
    accepted: List[Dict] = field(default_factory=list)
    
    @classmethod
    def parse_raw(cls, raw: str) -> "System":
        workflows, parts = raw.strip().split('\n\n')
        workflows = [Workflow.parse_raw(item) for item in workflows.split('\n')]
        workflows = dict((item.name, item) for item in workflows)
        parts = [dict([(item.split('=')[0], int(item.split('=')[1])) 
                       for item in part[1:-1].split(',')])
                 for part in parts.split('\n')]
        return cls(workflows, parts)
    
    def run_parts(self) -> int:
        for part in tqdm(self.parts, leave=False):
            output = 'in'
            while output not in ['A', 'R']:
                output = self.workflows[output](part)
            if output == 'A':
                self.accepted.append(part)
            elif output == 'R':
                self.rejected.append(part)

        output = 0
        for part in self.accepted:
            output += sum(part.values())
        
        return output

    def find_accepted_wrong(self, minimum=1, maximum=4000):
        
        class Ruleset(NamedTuple):
            key: str
            history: Tuple[Rule]
        
        queue = deque([Ruleset('in', ())])
        seen = set()
        accepted = []
        
        while queue:
            key, history = queue.popleft()
            if key == 'A':
                accepted.append(history)
                continue
            if key ==  'R' or (key, history) in seen:
                continue
            seen.add((key, history))

            neg_rules = []
            for rule in self.workflows[key].rules:
                queue.append(Ruleset(rule.output, 
                                     tuple(list(history) + neg_rules + [rule,])))
                neg_rules.append(Rule(rule.key, '>=' if rule.test == '<' else '<=',
                                      rule.value, None))
                

            queue.append(Ruleset(self.workflows[key].default, tuple(neg_rules)))

        # We should have now a list of rules for each accepted case, brute force that
        

        output = 0
        for rules in accepted:
            possibilities = {'x': list(range(minimum ,maximum+1)), 
             'm': list(range(minimum, maximum+1)), 
             'a': list(range(minimum, maximum+1)), 
             's': list(range(minimum, maximum+1))}
            
            for rule in rules:
                values = possibilities[rule.key]
                if rule.test == '<':
                    values = [item for item in values if item < rule.value]
                if rule.test == '>':
                    values = [item for item in values if item > rule.value]
                elif rule.test == '>=':
                    values = [item for item in values if item >= rule.value]
                elif rule.test == '<=':
                    values = [item for item in values if item <= rule.value]
                possibilities[rule.key] = values

            _output = 1
            for items in possibilities.values():
                _output *= len(items)
            
            output += _output

        # Does not work....
        # we must count the number of distinct combinaison... 

    def count_ratings(self, intervals: Dict[str, Tuple[int, int]], key: str = 'in') -> int:
        """Try a recursive approach...."""

        if key == 'R':
            # We end up rejected
            return 0
        
        if key == 'A':
            # We end up accepted, compute the number of combinaison
            # product of the number of items in each categories
            output = 1
            for (lo, hi) in intervals.values():
                output *= (hi - lo + 1)
            return output
        

        count = 0
        default = True
        
        for rule in self.workflows[key].rules:
            lo, hi = intervals[rule.key]
            
            if rule.test == '<':
                pass_interval = (lo, rule.value-1)
                fail_interval = (rule.value, hi)
            elif rule.test == '>':
                pass_interval = (rule.value+1, hi)
                fail_interval = (lo, rule.value)
            else: 
                raise ValueError(f'Unknon test {rule}')
            
            if pass_interval[0] <= pass_interval[1]:
                # Some things are passing the test, continue the road down to the next
                pass_intervals = dict(intervals)
                pass_intervals[rule.key] = pass_interval
                count += self.count_ratings(pass_intervals, rule.output)
            if fail_interval[0] <= fail_interval[1]:
                # To the next rule
                intervals[rule.key] = fail_interval
            else:
                # Nothing left, not going to default !
                default=False
                break
            
        if default:
            count += self.count_ratings(intervals, self.workflows[key].default)

        return count       

        

SYSTEM = System.parse_raw(RAW)
assert SYSTEM.run_parts() == 19114
assert SYSTEM.count_ratings({ k: (1, 4000) for k in 'xmas'}) == 167409079868000

with open('day19.txt', 'r') as f:
    raw = f.read()
    
system = System.parse_raw(raw)
print(system.run_parts())
# part 2 must be with trees.... wrong... recursion

print(system.count_ratings({ k: (1, 4000) for k in 'xmas'}))
