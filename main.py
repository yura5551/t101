from random import choice, shuffle, randint
from time import time


def generate_simple_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': code_max + j
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_stairway_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):
        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(i + j)
        rule = {
            'if': {
                log_oper: items
            },
            'then': i + j + 1
        }
        rules.append(rule)
    shuffle(rules)
    return rules


def generate_ring_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = generate_stairway_rules(code_max, n_max, n_generate - 1, log_oper_choice)
    log_oper = choice(log_oper_choice)  # not means and-not (neither)
    if n_max < 2:
        n_max = 2
    n_items = randint(2, n_max)
    items = []
    for i in range(0, n_items):
        items.append(code_max - i)
    rule = {
        'if': {
            log_oper: items
        },
        'then': 0
    }
    rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_random_rules(code_max, n_max, n_generate, log_oper_choice=["and", "or", "not"]):
    rules = []
    for j in range(0, n_generate):

        log_oper = choice(log_oper_choice)  # not means and-not (neither)
        if n_max < 2:
            n_max = 2
        n_items = randint(2, n_max)
        items = []
        for i in range(0, n_items):
            items.append(randint(1, code_max))
        rule = {
            'if': {
                log_oper: items
            },
            'then': randint(1, code_max)
        }
        rules.append(rule)
    shuffle(rules)
    return (rules)


def generate_seq_facts(M):
    facts = list(range(0, M))
    shuffle(facts)
    return facts


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    return facts


def parse_rules(rules):
    result = []
    for rule in rules:
        oper = ''.join(rule['if'].keys())
        result.append([oper, set(rule['if'][oper]), rule['then']])
    result.sort()
    return result


def check_validate_rules(rules):
    rules = parse_rules(rules)
    for i in range(0, len(rules) - 1):
        for j in range(i + 1, len(rules)):
            if rules[i][0] == rules[j][0] and rules[i][1] == rules[j][1] and rules[i][2] != rules[j][2]:
                rules[i][2] = rules[j][2] = -1

    return rules


def check_facts(rules, facts):
    set_facts = set(facts)
    result = []
    for rule in rules:
        if rule[0] == 'or':
            result.append(rule[2] if any([z in set_facts for z in rule[1]]) else 0)
        if rule[0] == 'and':
            result.append(rule[2] if all([z in set_facts for z in rule[1]]) else 0)
        if rule[0] == 'not':
            result.append(rule[2] if not any([z in set_facts for z in rule[1]]) else 0)

    return result


# samples:
#a = generate_simple_rules(100, 4, 10)
#print(generate_simple_rules(100, 4, 10))
#print(generate_random_rules(100, 4, 10))
#print(generate_stairway_rules(100, 4, 10, ["or"]))
#print(generate_ring_rules(100, 4, 10, ["or"]))

# generate rules and facts and check time
time_start = time()
N = 100000
M = 1000
rules = generate_simple_rules(100, 4, N)
facts = generate_rand_facts(100, M)


rules = check_validate_rules(rules)
print(f"{N} rules validated {round(time() - time_start, 6)} seconds")

# check facts vs rules
time_start = time()

# YOUR CODE HERE
check_facts(rules, facts)
print("%d facts validated vs %d rules in %f seconds" % (M, N, time() - time_start))
