use std::fmt::{Display, Formatter};
use std::ops::Range;

use bitfield_struct::bitfield;

use crate::instruction::Instruction;
use crate::registers::{Register, RegisterIndex, RegisterSet};

#[bitfield(u8)]
pub struct Flags {
    #[bits(1)]
    pub equal: bool,

    #[bits(7)]
    __: usize,
}

/*
[0, 0x100) => instructions
[0x100, 0x300) => memory
[0x300, 0x400) => stack
 */
pub struct VM {
    pub memory: [u8; VM::VM_BOUNDARY],
    pub registers: RegisterSet,
    pub flags: Flags,
    pub stop: bool,
}

#[derive(Clone, Copy)]
pub struct Address16 {
    pub high: u8,
    pub low: u8,
}

impl Into<u16> for Address16 {
    fn into(self) -> u16 {
        let mut address = self.high as u16;
        address <<= 8;
        address |= self.low as u16;
        address
    }
}

impl From<u16> for Address16 {
    fn from(value: u16) -> Self {
        Self {
            low: value as u8,
            high: (value >> 8) as u8,
        }
    }
}

#[derive(Clone, Copy)]
pub struct AddressReg16 {
    pub high: RegisterIndex,
    pub low: RegisterIndex,
}

impl AddressReg16 {
    pub fn eval_vm(&self, vm: &VM) -> u16 {
        let mut address = vm.registers[self.high].value as u16;
        address <<= 8;
        address |= vm.registers[self.low].value as u16;
        address
    }
}

impl VM {
    pub const INSTRUCTIONS_BOUNDARY: usize = 0x100;
    pub const MEMORY_BOUNDARY: usize = 0x300;
    pub const STACK_BOUNDARY: usize = 0x400;

    pub const VM_BOUNDARY: usize = VM::STACK_BOUNDARY;

    pub const INSTRUCTIONS_RANGE: Range<usize> = 0..Self::INSTRUCTIONS_BOUNDARY;
    pub const MEMORY_RANGE: Range<usize> = Self::INSTRUCTIONS_BOUNDARY..Self::MEMORY_BOUNDARY;
    pub const STACK_RANGE: Range<usize> = Self::MEMORY_BOUNDARY..Self::STACK_BOUNDARY;

    pub fn run(&mut self, stream: &Vec<u8>) {
        assert_eq!(stream.len(), Self::VM_BOUNDARY, "Invalid address space");
        self.memory.copy_from_slice(stream.as_slice());
        loop {
            let instructions = &self.memory[VM::INSTRUCTIONS_RANGE]
                [(self.registers[Register::PC].value as usize)..];
            let mut iter = instructions.iter();
            let mut next = || match iter.next() {
                Some(value) => *value,
                None => panic!("Could not get instruction parameter"),
            };
            let instruction = <dyn Instruction>::parse(&mut next);
            let count = instruction.len();
            self.registers[Register::PC].value += count as u8;
            self.step(&instruction);
            if self.stop {
                break;
            }
        }
    }

    pub fn step(&mut self, instruction: &Box<dyn Instruction>) {
        instruction.execute(self);
    }
}

impl Display for VM {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        let mut registers = "".to_string();
        for (index, register) in self.registers.registers.iter().enumerate() {
            registers += &format!("Register[{}] = {:02x}\n", index, register.value).to_string();
        }
        let dump = |name: &str, range: Range<usize>| {
            name.to_string()
                + "\n"
                + &*hexdump::hexdump_iter(&self.memory[range])
                    .map(|line| format!("{}", line))
                    .collect::<Vec<_>>()
                    .join("\n")
        };
        let full = [
            registers,
            dump("Instructions", Self::INSTRUCTIONS_RANGE),
            dump("Memory", Self::MEMORY_RANGE),
            dump("Stack", Self::STACK_RANGE),
        ]
        .join("\n");
        write!(f, "{}", full)
    }
}
