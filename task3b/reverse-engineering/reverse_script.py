from z3 import *

def reverse_obscure_func(input_vars):
    result = BitVecVal(0, 8)
    for i in range(len(input_vars)):
        result ^= input_vars[i]
        result = (result + i) & 0xff
    return result

secret_value = 0x5A

for length in range(1, 11):
    input_variables = []
    for i in range(length):
        input_variables.append(BitVec(f'char{i}', 8))

    s = Solver()
    for var in input_variables:
        s.add(var >= 0x20, var <= 0x7E)
    s.add(reverse_obscure_func(input_variables) == secret_value)

    if s.check() == sat:
        model = s.model()
        secret_string = ''.join(chr(model[input_variables[i]].as_long()) for i in range(length))
        print(f"Secret string for length {length}: {secret_string}")
        break
    else:
        print(f"No solution found for length {length}")
