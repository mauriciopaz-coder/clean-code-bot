import math

def calc(a,b,op):
    if op == "add":
        return a+b
    elif op == "sub":
        return a-b
    elif op == "mul":
        return a*b
    elif op == "div":
        return a/b
    elif op == "pow":
        return a**b
    elif op == "sqrt":
        return math.sqrt(a)
    elif op == "mod":
        return a%b

def process_list(numbers, operation):
    results = []
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i != j:
                r = calc(numbers[i], numbers[j], operation)
                results.append(r)
    return results

def print_results(results):
    for i in range(len(results)):
        print("Result " + str(i) + ": " + str(results[i]))

nums = [10, 5, 3]
res = process_list(nums, "div")
print_results(res)
