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
    return rules


def generate_rand_facts(code_max, M):
    facts = []
    for i in range(0, M):
        facts.append(randint(0, code_max))
    return facts


def evidence_check(rules_list, facts) -> []:
    s_list = [[], [], []]  # or and not
    result = []
    temp_it = 0
    # create list or and not
    for rule in rules_list:
        if rule != {}:
            for key in rule['if'].keys():
                if key == 'or':
                    s_list[0].append(rule)
                if key == 'and':
                    s_list[1].append(rule)
                if key == 'not':
                    s_list[2].append(rule)
    for rule in s_list[0]:  # or
        for item in rule['if']['or']:
            size = len(rule['if']['or'])
            if item in facts:
                result.append(rule['then'])
                temp_it = 0
                break
            else:
                temp_it += 1
                if temp_it == size:
                    result.append(0)
                    temp_it = 0
    for rule in s_list[1]:  # and
        for item in rule['if']['and']:
            size = len(rule['if']['and'])
            if item in facts:
                temp_it += 1
        if temp_it == size:
            result.append(rule['then'])
            temp_it = 0
        else:
            result.append(0)
            temp_it = 0

    for rule in s_list[2]:  # not
        for item in rule['if']['not']:
            size = len(rule['if']['not'])
            if item not in facts:
                temp_it += 1
        if temp_it == size:
            result.append(rule['then'])
            temp_it = 0
        else:
            result.append(0)
            temp_it = 0
    return result


def validate_rules(rules_list):
    print('.', end="")
    parse_rules = [[], [], []]  # if then validate
    for rule in rules_list:
        if rule['if']:
            parse_rules[0].append(rule['if'])
        if rule['then']:
            parse_rules[1].append(rule['then'])
    for i in range(len(rules_list) - 1):
        for j in range(i + 1, len(rules_list) - 1):
            if i >= j:
                return 0
            if parse_rules[1][i] == parse_rules[1][j]:  # if and/or A then B -> if not A then B
                if ('and' in rules_list[i].keys() and 'not' in rules_list[j].keys) or (
                        'and' in rules_list[j].keys() and 'not' in rules_list[i].keys):
                    if parse_rules[0][j]['and'] == parse_rules[0][i]['not'] or parse_rules[0][i]['and'] == \
                            parse_rules[0][j]['not']:
                        rules_list[j].clear()
                        rules_list[i].clear()
                if ('or' in rules_list[j].keys() and 'not' in rules_list[i].keys) or (
                        'or' in rules_list[i].keys() and 'not' in rules_list[j].keys):
                    if parse_rules[0][j]['or'] == parse_rules[0][i]['not'] or parse_rules[0][i]['or'] == \
                            parse_rules[0][j]['not']:
                        rules_list[j].clear()
                        rules_list[i].clear()
            if 'not' in parse_rules[0][i].keys() and 'not' in parse_rules[0][j].keys():
                # if not A then B -> if not B then A
                if parse_rules[1][i] in parse_rules[0][j]['not'] and parse_rules[1][j] in \
                        parse_rules[0][i]['not']:
                    # mutual exclusion
                    rules_list[i].clear()
                    rules_list[j].clear()
                if parse_rules[1][i] in parse_rules[0][j]['not'] and parse_rules[1][j] not in \
                        parse_rules[0][i]['not']:
                    # nesting
                    rules_list[i].clear()
                    rules_list[j].clear()
    # so so slowly ... probably need use set union
    for rule in rules_list:
        if rule != {}:
            parse_rules[2].append(rule)
    return parse_rules[2]


def main():
    number_of_rules = 10000
    number_of_facts = 1000
    rules = generate_simple_rules(100, 4, number_of_rules)
    random_rules = generate_random_rules(100, 4, number_of_rules)
    stairway_rules = generate_stairway_rules(100, 4, number_of_rules)
    ring_rules = generate_ring_rules(100, 4, number_of_rules)

    facts = generate_rand_facts(number_of_facts, number_of_rules)
    unique_facts = set(facts)

    time_start = time()
    correct_simple = validate_rules(rules)
    correct_random = validate_rules(random_rules)
    correct_stairway = validate_rules(stairway_rules)
    correct_ring = validate_rules(ring_rules)
    validate_time = time() - time_start
    print(number_of_rules, "rules validate in seconds:", validate_time)

    # facts vs rules
    time_start = time()
    evidence_check(correct_simple, unique_facts)
    evidence_check(correct_random, unique_facts)
    evidence_check(correct_stairway, unique_facts)
    evidence_check(correct_ring, unique_facts)
    check_time = time() - time_start
    print(number_of_rules, "rules check in seconds:", check_time)

    print("Finally time:",  (validate_time + check_time))


if __name__ == "__main__":
    main()
