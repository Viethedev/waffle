from enum import Enum
import re

__all__ = ["Instr", "WaffleStack"]

# Bytecode definition
class Instruction(Enum):
    # Stack operations
    push = 1; pop = 2; duplicate = 3; swap = 4
    # Local variables operations
    load = 10; store = 11
    # Arithmetic & logic
    add = 20; subtract = 21; multiply = 22; divide = 23; negate = 24
    # Comparison
    equal = 30; smaller = 31; bigger = 32
    # Control flow
    jump = 40; truejump = 41; falsejump = 42
    # Function calls
    call = 52; goback = 53
    # Program lifecycle
    halt = 255

Instr = Instruction

# Frame implementation
class Frame:
    __slots__ = ("locals", "origin")

    def __init__(self, origin: int):
        self.locals = {}
        self.origin = origin


# VM implementation
class WaffleStack:
    __slots__ = (
        "_address",
        "_datastack",
        "_framestack",
        "_frame",
        "_dispatch",
        "_running",
    )
    # Precompiled regex patterns for performance
    INT_PATTERN = re.compile(r"^[+-]?\d+$")
    FLOAT_PATTERN = re.compile(r"^[+-]?(?:\d+\.\d*|\.\d+)$")

    # Initialize a WaffleStack - Waffle's VM
    def __init__(self):
        self._address = 0
        self._datastack = []
        self._framestack = []
        self._frame = None
        self._running = True

        self._dispatch = {
            Instruction.push: self._push,
            Instruction.pop: self._pop,
            Instruction.duplicate: self._duplicate,
            Instruction.swap: self._swap,
            Instruction.load: self._load,
            Instruction.store: self._store,
            Instruction.add: self._add,
            Instruction.subtract: self._subtract,
            Instruction.multiply: self._multiply,
            Instruction.divide: self._divide,
            Instruction.negate: self._negate,
            Instruction.equal: self._equal,
            Instruction.smaller: self._smaller,
            Instruction.bigger: self._bigger,
            Instruction.jump: self._jump,
            Instruction.truejump: self._truejump,
            Instruction.falsejump: self._falsejump,
            Instruction.call: self._call,
            Instruction.goback: self._goback,
            Instruction.halt: self._halt,
        }

    # ===== Stack ops =====
    def _push(self, value):
        self._datastack.append(value)

    def _pop(self):
        return self._datastack.pop()

    def _duplicate(self):
        self._datastack.append(self.datastack[-1])

    def _swap(self):
        a, b = self._datastack[-2:]
        self._datastack[-2:] = [b, a]

    # ===== Locals =====
    def _load(self, key):
        self._push(self._frame.locals[key])

    def _store(self, key):
        self._frame.locals[key] = self._pop()

    # ===== Arithmetic =====
    def _add(self):
        b = self._pop()
        a = self._pop()
        self._push(a + b)

    def _subtract(self):
        b = self._pop()
        a = self._pop()
        self._push(a - b)

    def _multiply(self):
        b = self._pop()
        a = self._pop()
        self._push(a * b)

    def _divide(self):
        b = self._pop()
        a = self._pop()
        self._push(a / b)

    def _negate(self):
        self._push(-self._pop())

    # ===== Comparison =====
    def _equal(self):
        b = self._pop()
        a = self._pop()
        self._push(a == b)

    def _smaller(self):
        b = self._pop()
        a = self._pop()
        self._push(a < b)

    def _bigger(self):
        b = self._pop()
        a = self._pop()
        self._push(a > b)

    # ===== Control flow =====
    def _jump(self, address):
        self._address = address - 1

    def _truejump(self, address):
        if self._pop():
            self._jump(address)

    def _falsejump(self, address):
        if not self._pop():
            self._jump(address)

    # ===== Calls =====
    def _call(self, target):
        self._framestack.append(self._frame)
        self._frame = Frame(self._address)
        self._address = target - 1

    def _goback(self):
        finished = self._frame
        self._frame = self._framestack.pop()
        self._address = finished.origin

    # ===== Lifecycle =====
    def _halt(self):
        self._running = False

    # ===== Execution =====
    def execute(self, bytecodes):
        self._address = 0
        self._running = True
        self._datastack.clear()
        self._framestack.clear()
        self._frame = Frame(0)

        while self._running and self._address < len(bytecodes):
            op, *args = bytecodes[self._address]
            self._dispatch[op](*args)
            self._address += 1

    def read(self, filename: str):
        f = open(filename, "r")
        bytecodes = []
        for line in f.read().split("\n"):
            if line == "":
                continue
            opcode, *args = line.split(" ", maxsplit=1)
            args = [self._parse_args(el) for el in args]
            bytecode = (Instruction[opcode.lower()], *args)
            bytecodes.append(bytecode)
        f.close()
        return bytecodes

    def _parse_args(self, source):   
        source = source.strip()
        if self.INT_PATTERN.fullmatch(source):
            return int(source)
        elif self.FLOAT_PATTERN.fullmatch(source):
            return float(source)
        else:
            return source[1: -1]

    # Internal reference
    @property
    def datastack(self):
        return self._datastack

    @property
    def current_frame(self):
        return self._frame
