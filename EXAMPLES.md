# InstaProcessing CPU - Examples and Documentation

## Overview

InstaProcessing CPU is a brand new type of CPU processor featuring:
- **Multiple Processing Layers**: Different layers handle different types of operations
- **Sectored Architecture**: Modular sectors group related layers for specific functionalities
- **Built-in Cache**: Performance optimization through intelligent caching
- **Flexible Instruction Set**: Support for arithmetic, logical, memory, I/O, and control operations

## Architecture

### Processing Layers

1. **Arithmetic Layer** - Handles mathematical operations (add, sub, mul, div)
2. **Logical Layer** - Handles logical operations (and, or, not, xor)
3. **Memory Layer** - Manages memory storage and retrieval
4. **I/O Layer** - Handles input/output operations
5. **Control Layer** - Manages control flow (jump, halt, nop)

### Processor Sectors

- **Compute Sector**: Contains Arithmetic and Logical layers
- **Data Sector**: Contains Memory layer
- **I/O Sector**: Contains I/O layer
- **Control Sector**: Contains Control layer

### Cache System

The processor includes a built-in cache with LRU (Least Recently Used) eviction policy for optimal performance.

## Usage Examples

### Example 1: Basic Arithmetic

```python
from processor import InstaProcessor, Instruction, InstructionType

# Create processor instance
cpu = InstaProcessor()

# Create arithmetic instructions
instructions = [
    Instruction(InstructionType.ARITHMETIC, 'add', [15, 25]),
    Instruction(InstructionType.ARITHMETIC, 'mul', [40, 2]),
]

# Execute program
results = cpu.execute_program(instructions)
print(f"Results: {results}")  # [40, 80]
```

### Example 2: Memory Operations

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

# Store and load data
program = [
    Instruction(InstructionType.MEMORY, 'store', [0, 100]),
    Instruction(InstructionType.MEMORY, 'store', [1, 200]),
    Instruction(InstructionType.MEMORY, 'load', [0]),
    Instruction(InstructionType.MEMORY, 'load', [1]),
]

results = cpu.execute_program(program)
print(f"Stored and loaded: {results}")  # [100, 200, 100, 200]
```

### Example 3: Logical Operations

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

program = [
    Instruction(InstructionType.LOGICAL, 'and', [True, False]),
    Instruction(InstructionType.LOGICAL, 'or', [True, False]),
    Instruction(InstructionType.LOGICAL, 'not', [False]),
    Instruction(InstructionType.LOGICAL, 'xor', [True, True]),
]

results = cpu.execute_program(program)
print(f"Logical results: {results}")  # [False, True, True, False]
```

### Example 4: I/O Operations

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

# Set up input buffer
cpu.io_layer.input_buffer = [10, 20, 30]

program = [
    Instruction(InstructionType.IO, 'read', []),
    Instruction(InstructionType.IO, 'write', [100]),
    Instruction(InstructionType.IO, 'read', []),
]

results = cpu.execute_program(program)
print(f"I/O results: {results}")  # [10, 100, 20]
print(f"Output buffer: {cpu.io_layer.output_buffer}")  # [100]
```

### Example 5: Complex Multi-Layer Program

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

# A program that uses multiple layers
program = [
    # Store values
    Instruction(InstructionType.MEMORY, 'store', [0, 50]),
    Instruction(InstructionType.MEMORY, 'store', [1, 30]),
    
    # Load and compute
    Instruction(InstructionType.MEMORY, 'load', [0]),
    Instruction(InstructionType.MEMORY, 'load', [1]),
    Instruction(InstructionType.ARITHMETIC, 'sub', [50, 30]),
    
    # Check if result is positive
    Instruction(InstructionType.LOGICAL, 'and', [True, True]),
    
    # Output result
    Instruction(InstructionType.IO, 'write', [20]),
]

results = cpu.execute_program(program)
print(f"Complex program results: {results}")

# Get processor statistics
stats = cpu.get_stats()
print(f"Statistics: {stats}")
```

### Example 6: Sector Management

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

# Disable compute sector
cpu.disable_sector('compute')

# This will fail because compute sector is disabled
try:
    instruction = Instruction(InstructionType.ARITHMETIC, 'add', [5, 5])
    cpu.execute_instruction(instruction)
except ValueError as e:
    print(f"Error: {e}")

# Re-enable compute sector
cpu.enable_sector('compute')

# Now it works
result = cpu.execute_instruction(instruction)
print(f"Result after enabling: {result}")  # 10
```

### Example 7: Control Flow

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

program = [
    Instruction(InstructionType.ARITHMETIC, 'add', [10, 10]),
    Instruction(InstructionType.CONTROL, 'jump', [100]),
    Instruction(InstructionType.CONTROL, 'nop', []),
    Instruction(InstructionType.CONTROL, 'halt', []),
    Instruction(InstructionType.ARITHMETIC, 'add', [20, 20]),  # Never executed
]

results = cpu.execute_program(program)
print(f"Results: {results}")
print(f"Program counter: {cpu.control_layer.program_counter}")
```

### Example 8: Processor Reset

```python
from processor import InstaProcessor, Instruction, InstructionType

cpu = InstaProcessor()

# Execute some instructions
program = [
    Instruction(InstructionType.MEMORY, 'store', [0, 42]),
    Instruction(InstructionType.ARITHMETIC, 'add', [1, 2]),
]
cpu.execute_program(program)

print(f"Before reset: {cpu.get_stats()}")

# Reset processor
cpu.reset()

print(f"After reset: {cpu.get_stats()}")
# All counters and memory cleared
```

## API Reference

### InstaProcessor

Main processor class that coordinates all layers and sectors.

**Methods:**
- `execute_instruction(instruction)` - Execute a single instruction
- `execute_program(instructions)` - Execute a list of instructions
- `reset()` - Reset processor to initial state
- `get_stats()` - Get processor statistics
- `enable_sector(name)` - Enable a specific sector
- `disable_sector(name)` - Disable a specific sector

### Instruction

Represents a single instruction to be executed.

**Parameters:**
- `type` - InstructionType enum value
- `operation` - String name of the operation
- `operands` - List of operands for the operation

### InstructionType

Enum of supported instruction types:
- `ARITHMETIC` - Mathematical operations
- `LOGICAL` - Boolean logic operations
- `MEMORY` - Memory read/write operations
- `IO` - Input/output operations
- `CONTROL` - Control flow operations

### ProcessorState

Enum of processor states:
- `IDLE` - Processor is idle
- `RUNNING` - Processor is executing
- `SUSPENDED` - Processor is suspended
- `HALTED` - Processor is halted

## Features

### Multi-Layer Architecture
The processor uses multiple specialized layers, each optimized for specific types of operations. This allows for efficient processing and easy extension.

### Sectored Design
Layers are grouped into sectors, allowing you to enable/disable entire functional units as needed.

### Built-in Cache
Automatic caching of frequently accessed data with LRU eviction policy.

### Comprehensive Statistics
Track instructions executed, cycles, memory usage, and cache performance.

### Flexible Instruction Set
Easy to extend with new operations and instruction types.

## Performance Considerations

1. **Cache Usage**: Frequently accessed memory locations benefit from cache
2. **Sector Management**: Disable unused sectors to reduce overhead
3. **Batch Execution**: Use `execute_program()` for better performance than multiple `execute_instruction()` calls
4. **Memory Management**: The memory layer has configurable size - adjust based on needs

## Future Enhancements

Possible future additions:
- Pipeline execution for parallel instruction processing
- Hardware interrupts and exception handling
- Virtual memory with paging
- Multi-core support
- SIMD (Single Instruction Multiple Data) operations
- Branch prediction
- Out-of-order execution

## Running the Examples

To run the main demonstration:

```bash
python processor.py
```

To run the tests:

```bash
python -m unittest test_processor.py
```

Or run specific test classes:

```bash
python -m unittest test_processor.TestArithmeticLayer
python -m unittest test_processor.TestInstaProcessor
```
