from waffle import WaffleStack, Instruction

# ==== Test ====
def run(program):
    vm = WaffleStack()
    vm.execute(program)
    return vm

def test_push_pop():
    vm = run([
        (Instruction.push, 1),
        (Instruction.push, 2),
        (Instruction.pop,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [1]

def test_duplicate():
    vm = run([
        (Instruction.push, 5),
        (Instruction.duplicate,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [5, 5]

def test_swap():
    vm = run([
        (Instruction.push, 1),
        (Instruction.push, 2),
        (Instruction.swap,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [2, 1]

def test_arithmetic():
    vm = run([
        (Instruction.push, 2),
        (Instruction.push, 3),
        (Instruction.add,),
        (Instruction.push, 4),
        (Instruction.multiply,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [20]

def test_negate():
    vm = run([
        (Instruction.push, 5),
        (Instruction.negate,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [-5]

def test_equal():
    vm = run([
        (Instruction.push, 3),
        (Instruction.push, 3),
        (Instruction.equal,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [True]

def test_smaller_bigger():
    vm = run([
        (Instruction.push, 2),
        (Instruction.push, 5),
        (Instruction.smaller,),
        (Instruction.push, 7),
        (Instruction.push, 3),
        (Instruction.bigger,),
        (Instruction.halt,)
    ])
    assert vm.datastack == [True, True]

def test_store_load():
    vm = run([
        (Instruction.push, 42),
        (Instruction.store, 0),
        (Instruction.load, 0),
        (Instruction.halt,)
    ])
    assert vm.datastack == [42]
    assert vm.current_frame.locals[0] == 42

def test_jump():
    vm = run([
        (Instruction.jump, 3),
        (Instruction.push, "bad"),
        (Instruction.halt,),
        (Instruction.push, "ok"),
        (Instruction.halt,)
    ])
    assert vm.datastack == ["ok"]

def test_falsejump():
    vm = run([
        (Instruction.push, 1),
        (Instruction.push, 2),
        (Instruction.equal,),        # False
        (Instruction.falsejump, 7),
        (Instruction.push, "bad"),
        (Instruction.store, 0),
        (Instruction.jump, 9),
        (Instruction.push, "ok"),
        (Instruction.store, 0),
        (Instruction.halt,)
    ])
    assert vm.current_frame.locals[0] == "ok"

def test_call_and_return():
    vm = run([
        # main
        (Instruction.call, 4),
        (Instruction.halt,),

        # function @4
        (Instruction.push, 99),
        (Instruction.store, 0),
        (Instruction.goback,),
    ])

    assert vm.current_frame.locals == {}          # main locals unchanged
    assert vm.datastack == []

def test_halt_stops_execution():
    vm = run([
        (Instruction.push, 1),
        (Instruction.halt,),
        (Instruction.push, 2),
    ])
    assert vm.datastack == [1]

def test_read_file():
    vm = WaffleStack()
    bytecodes = vm.read("tests/test.txt")
    vm.execute(bytecodes)
    assert vm.datastack == ["I can read"]