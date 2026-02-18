"""
Tests for the InstaProcessing CPU
"""

import unittest
from processor import (
    InstaProcessor, Instruction, InstructionType, ProcessorState,
    ArithmeticLayer, LogicalLayer, MemoryLayer, IOLayer, ControlLayer,
    ProcessorSector, Cache
)


class TestArithmeticLayer(unittest.TestCase):
    """Test the arithmetic processing layer"""
    
    def setUp(self):
        self.layer = ArithmeticLayer()
    
    def test_addition(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [5, 3])
        result = self.layer.process(instruction)
        self.assertEqual(result, 8)
    
    def test_subtraction(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'sub', [10, 4])
        result = self.layer.process(instruction)
        self.assertEqual(result, 6)
    
    def test_multiplication(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'mul', [6, 7])
        result = self.layer.process(instruction)
        self.assertEqual(result, 42)
    
    def test_division(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'div', [20, 5])
        result = self.layer.process(instruction)
        self.assertEqual(result, 4)
    
    def test_division_by_zero(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'div', [10, 0])
        result = self.layer.process(instruction)
        self.assertIsNone(result)
    
    def test_can_handle_arithmetic(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [1, 2])
        self.assertTrue(self.layer.can_handle(instruction))
    
    def test_cannot_handle_logical(self):
        instruction = Instruction(InstructionType.LOGICAL, 'and', [True, False])
        self.assertFalse(self.layer.can_handle(instruction))
    
    def test_invalid_operation(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'invalid', [1, 2])
        with self.assertRaises(ValueError):
            self.layer.process(instruction)
    
    def test_wrong_operand_count(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [1])
        with self.assertRaises(ValueError):
            self.layer.process(instruction)


class TestLogicalLayer(unittest.TestCase):
    """Test the logical processing layer"""
    
    def setUp(self):
        self.layer = LogicalLayer()
    
    def test_and_operation(self):
        instruction = Instruction(InstructionType.LOGICAL, 'and', [True, False])
        result = self.layer.process(instruction)
        self.assertFalse(result)
    
    def test_or_operation(self):
        instruction = Instruction(InstructionType.LOGICAL, 'or', [True, False])
        result = self.layer.process(instruction)
        self.assertTrue(result)
    
    def test_not_operation(self):
        instruction = Instruction(InstructionType.LOGICAL, 'not', [True])
        result = self.layer.process(instruction)
        self.assertFalse(result)
    
    def test_xor_operation(self):
        instruction = Instruction(InstructionType.LOGICAL, 'xor', [True, False])
        result = self.layer.process(instruction)
        self.assertTrue(result)
    
    def test_can_handle_logical(self):
        instruction = Instruction(InstructionType.LOGICAL, 'and', [True, True])
        self.assertTrue(self.layer.can_handle(instruction))
    
    def test_cannot_handle_arithmetic(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [1, 2])
        self.assertFalse(self.layer.can_handle(instruction))


class TestMemoryLayer(unittest.TestCase):
    """Test the memory processing layer"""
    
    def setUp(self):
        self.layer = MemoryLayer(size=100)
    
    def test_store_and_load(self):
        store_inst = Instruction(InstructionType.MEMORY, 'store', [0, 42])
        self.layer.process(store_inst)
        
        load_inst = Instruction(InstructionType.MEMORY, 'load', [0])
        result = self.layer.process(load_inst)
        self.assertEqual(result, 42)
    
    def test_load_uninitialized(self):
        instruction = Instruction(InstructionType.MEMORY, 'load', [5])
        result = self.layer.process(instruction)
        self.assertEqual(result, 0)
    
    def test_store_out_of_bounds(self):
        instruction = Instruction(InstructionType.MEMORY, 'store', [200, 10])
        with self.assertRaises(ValueError):
            self.layer.process(instruction)
    
    def test_can_handle_memory(self):
        instruction = Instruction(InstructionType.MEMORY, 'load', [0])
        self.assertTrue(self.layer.can_handle(instruction))


class TestIOLayer(unittest.TestCase):
    """Test the I/O processing layer"""
    
    def setUp(self):
        self.layer = IOLayer()
    
    def test_write_operation(self):
        instruction = Instruction(InstructionType.IO, 'write', [100])
        result = self.layer.process(instruction)
        self.assertEqual(result, 100)
        self.assertIn(100, self.layer.output_buffer)
    
    def test_read_operation(self):
        self.layer.input_buffer = [10, 20, 30]
        instruction = Instruction(InstructionType.IO, 'read', [])
        result = self.layer.process(instruction)
        self.assertEqual(result, 10)
        self.assertEqual(len(self.layer.input_buffer), 2)
    
    def test_read_empty_buffer(self):
        instruction = Instruction(InstructionType.IO, 'read', [])
        result = self.layer.process(instruction)
        self.assertIsNone(result)
    
    def test_can_handle_io(self):
        instruction = Instruction(InstructionType.IO, 'read', [])
        self.assertTrue(self.layer.can_handle(instruction))


class TestControlLayer(unittest.TestCase):
    """Test the control processing layer"""
    
    def setUp(self):
        self.layer = ControlLayer()
    
    def test_jump_operation(self):
        instruction = Instruction(InstructionType.CONTROL, 'jump', [100])
        result = self.layer.process(instruction)
        self.assertEqual(result, 100)
        self.assertEqual(self.layer.program_counter, 100)
    
    def test_halt_operation(self):
        instruction = Instruction(InstructionType.CONTROL, 'halt', [])
        result = self.layer.process(instruction)
        self.assertEqual(result, 'HALT')
    
    def test_nop_operation(self):
        instruction = Instruction(InstructionType.CONTROL, 'nop', [])
        result = self.layer.process(instruction)
        self.assertIsNone(result)
    
    def test_can_handle_control(self):
        instruction = Instruction(InstructionType.CONTROL, 'halt', [])
        self.assertTrue(self.layer.can_handle(instruction))


class TestProcessorSector(unittest.TestCase):
    """Test processor sectors"""
    
    def test_sector_execution(self):
        arithmetic_layer = ArithmeticLayer()
        sector = ProcessorSector('Test', [arithmetic_layer])
        
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [5, 3])
        result = sector.execute(instruction)
        self.assertEqual(result, 8)
    
    def test_disabled_sector(self):
        arithmetic_layer = ArithmeticLayer()
        sector = ProcessorSector('Test', [arithmetic_layer])
        sector.enabled = False
        
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [5, 3])
        with self.assertRaises(RuntimeError):
            sector.execute(instruction)
    
    def test_no_layer_handles_instruction(self):
        arithmetic_layer = ArithmeticLayer()
        sector = ProcessorSector('Test', [arithmetic_layer])
        
        instruction = Instruction(InstructionType.LOGICAL, 'and', [True, False])
        with self.assertRaises(ValueError):
            sector.execute(instruction)


class TestCache(unittest.TestCase):
    """Test the cache mechanism"""
    
    def test_cache_put_and_get(self):
        cache = Cache(size=10)
        cache.put('key1', 'value1')
        result = cache.get('key1')
        self.assertEqual(result, 'value1')
    
    def test_cache_miss(self):
        cache = Cache(size=10)
        result = cache.get('nonexistent')
        self.assertIsNone(result)
    
    def test_cache_eviction(self):
        cache = Cache(size=2)
        cache.put('key1', 'value1')
        cache.put('key2', 'value2')
        cache.put('key3', 'value3')  # Should evict key1
        
        self.assertIsNone(cache.get('key1'))
        self.assertEqual(cache.get('key2'), 'value2')
        self.assertEqual(cache.get('key3'), 'value3')


class TestInstaProcessor(unittest.TestCase):
    """Test the complete InstaProcessor"""
    
    def setUp(self):
        self.processor = InstaProcessor()
    
    def test_initial_state(self):
        self.assertEqual(self.processor.state, ProcessorState.IDLE)
        self.assertEqual(self.processor.instructions_executed, 0)
    
    def test_execute_arithmetic_instruction(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [10, 20])
        result = self.processor.execute_instruction(instruction)
        self.assertEqual(result, 30)
        self.assertEqual(self.processor.instructions_executed, 1)
    
    def test_execute_program(self):
        program = [
            Instruction(InstructionType.ARITHMETIC, 'add', [5, 5]),
            Instruction(InstructionType.ARITHMETIC, 'mul', [10, 2]),
        ]
        results = self.processor.execute_program(program)
        self.assertEqual(results, [10, 20])
    
    def test_memory_operations(self):
        program = [
            Instruction(InstructionType.MEMORY, 'store', [0, 99]),
            Instruction(InstructionType.MEMORY, 'load', [0]),
        ]
        results = self.processor.execute_program(program)
        self.assertEqual(results[0], 99)
        self.assertEqual(results[1], 99)
    
    def test_logical_operations(self):
        program = [
            Instruction(InstructionType.LOGICAL, 'and', [True, True]),
            Instruction(InstructionType.LOGICAL, 'or', [False, True]),
        ]
        results = self.processor.execute_program(program)
        self.assertEqual(results, [True, True])
    
    def test_halt_instruction(self):
        program = [
            Instruction(InstructionType.ARITHMETIC, 'add', [1, 2]),
            Instruction(InstructionType.CONTROL, 'halt', []),
            Instruction(InstructionType.ARITHMETIC, 'add', [3, 4]),
        ]
        results = self.processor.execute_program(program)
        self.assertEqual(len(results), 2)  # First instruction and halt result
        self.assertEqual(results[0], 3)  # First add result
        self.assertEqual(results[1], 'HALT')  # Halt result
        self.assertEqual(self.processor.state, ProcessorState.HALTED)
    
    def test_reset(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [1, 2])
        self.processor.execute_instruction(instruction)
        
        self.processor.reset()
        
        self.assertEqual(self.processor.state, ProcessorState.IDLE)
        self.assertEqual(self.processor.instructions_executed, 0)
        self.assertEqual(len(self.processor.memory_layer.memory), 0)
    
    def test_get_stats(self):
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [1, 2])
        self.processor.execute_instruction(instruction)
        
        stats = self.processor.get_stats()
        self.assertEqual(stats['instructions_executed'], 1)
        self.assertEqual(stats['cycles'], 1)
        self.assertIn('state', stats)
    
    def test_enable_disable_sector(self):
        self.processor.disable_sector('compute')
        
        instruction = Instruction(InstructionType.ARITHMETIC, 'add', [1, 2])
        with self.assertRaises(ValueError):
            self.processor.execute_instruction(instruction)
        
        self.processor.enable_sector('compute')
        result = self.processor.execute_instruction(instruction)
        self.assertEqual(result, 3)
    
    def test_io_operations(self):
        self.processor.io_layer.input_buffer = [42]
        program = [
            Instruction(InstructionType.IO, 'read', []),
            Instruction(InstructionType.IO, 'write', [100]),
        ]
        results = self.processor.execute_program(program)
        self.assertEqual(results[0], 42)
        self.assertEqual(results[1], 100)
        self.assertIn(100, self.processor.io_layer.output_buffer)
    
    def test_complex_program(self):
        """Test a complex program that uses multiple layers and sectors"""
        program = [
            # Store values in memory
            Instruction(InstructionType.MEMORY, 'store', [0, 10]),
            Instruction(InstructionType.MEMORY, 'store', [1, 20]),
            # Load and compute
            Instruction(InstructionType.MEMORY, 'load', [0]),
            Instruction(InstructionType.MEMORY, 'load', [1]),
            Instruction(InstructionType.ARITHMETIC, 'add', [10, 20]),
            # Logical operation
            Instruction(InstructionType.LOGICAL, 'and', [True, True]),
            # I/O operation
            Instruction(InstructionType.IO, 'write', [30]),
        ]
        results = self.processor.execute_program(program)
        
        self.assertEqual(results[0], 10)  # First store
        self.assertEqual(results[1], 20)  # Second store
        self.assertEqual(results[2], 10)  # First load
        self.assertEqual(results[3], 20)  # Second load
        self.assertEqual(results[4], 30)  # Arithmetic
        self.assertEqual(results[5], True)  # Logical
        self.assertEqual(results[6], 30)  # I/O write


if __name__ == '__main__':
    unittest.main()
