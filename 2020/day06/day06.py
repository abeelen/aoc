RAW="""abc

a
b
c

ab
ac

a
a
a
a

b"""

def help(forms: str) -> int:
    groups = forms.strip().split('\n\n')
    answers = [ set(''.join(group.split('\n'))) for group in groups]
    return sum([len(answer) for answer in answers])

assert help(RAW)== 11

with open('day06.txt') as f:
    all_forms = f.read()

print(help(all_forms))

def help2(forms: str) -> int:
    groups = forms.strip().split('\n\n')
    counts = []
    for group in groups:
        persons = group.split('\n')
        all_answers = ''.join(group.split('\n'))
        all_answered = [all_answers.count(c) == len(persons) for c in set(all_answers)]
        counts.append(sum(all_answered))
    return sum(counts)

assert help2(RAW) == 6
print(help2(all_forms))