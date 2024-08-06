use std::io;
use std::io::Read;

use strum::FromRepr;

use crate::registers::{Register, RegisterIndex};
use crate::vm::{AddressReg16, VM};

#[derive(FromRepr)]
pub enum Opcode {
    Exit,
    MovReg8Const8,
    XorMemReg8Const8,
    CmpReg8Const8,
    JumpIfNotEqual,
    SubReg8Const8,
    AddReg8Const8,
    ReadStdinStack,
    PopReg8,
    DerefAddressReg16Reg8,
    XorReg8Reg8,
    WriteStdoutConst8,
    CmpReg8Reg8,
    XorReg8Const8,
}

pub trait Instruction {
    fn opcode(&self) -> Opcode;

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized;

    fn execute(&self, vm: &mut VM);

    fn len(&self) -> u8;

    fn encode(&self) -> Vec<u8>;
}

impl dyn Instruction {
    pub fn parse(next: &mut dyn FnMut() -> u8) -> Box<dyn Instruction> {
        let opcode_int = next() as usize;
        match Opcode::from_repr(opcode_int)
            .expect(format!("Unknown opcode {}", opcode_int).as_str())
        {
            Opcode::Exit => Box::new(Exit::decode(next)),
            Opcode::MovReg8Const8 => Box::new(MovReg8Const8::decode(next)),
            Opcode::XorMemReg8Const8 => Box::new(XorMemReg8Const8::decode(next)),
            Opcode::CmpReg8Const8 => Box::new(CmpReg8Const8::decode(next)),
            Opcode::JumpIfNotEqual => Box::new(JumpIfNotEqual::decode(next)),
            Opcode::SubReg8Const8 => Box::new(SubReg8Const8::decode(next)),
            Opcode::AddReg8Const8 => Box::new(AddReg8Const8::decode(next)),
            Opcode::ReadStdinStack => Box::new(ReadStdinStack::decode(next)),
            Opcode::PopReg8 => Box::new(PopReg8::decode(next)),
            Opcode::DerefAddressReg16Reg8 => Box::new(DerefAddressReg16Reg8::decode(next)),
            Opcode::XorReg8Reg8 => Box::new(XorReg8Reg8::decode(next)),
            Opcode::WriteStdoutConst8 => Box::new(WriteStdoutConst8::decode(next)),
            Opcode::CmpReg8Reg8 => Box::new(CmpReg8Reg8::decode(next)),
            Opcode::XorReg8Const8 => Box::new(XorReg8Const8::decode(next)),
        }
    }
}

pub struct MovReg8Const8 {
    pub to: RegisterIndex,
    pub value: u8,
}

impl Instruction for MovReg8Const8 {
    fn opcode(&self) -> Opcode {
        Opcode::MovReg8Const8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            to: RegisterIndex::from(next()),
            value: next(),
        }
    }

    fn execute(&self, vm: &mut VM) {
        vm.registers[self.to].value = self.value;
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.to.0 as u8, self.value]
    }
}

pub struct XorMemReg8Const8 {
    pub register: RegisterIndex,
    pub value: u8,
}

impl Instruction for XorMemReg8Const8 {
    fn opcode(&self) -> Opcode {
        Opcode::XorMemReg8Const8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            register: RegisterIndex::from(next()),
            value: next(),
        }
    }

    fn execute(&self, vm: &mut VM) {
        let address = vm.registers[self.register].value;
        vm.memory[address as usize] ^= self.value;
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.register.0, self.value]
    }
}

pub struct CmpReg8Const8 {
    pub register: RegisterIndex,
    pub comparand: u8,
}

impl Instruction for CmpReg8Const8 {
    fn opcode(&self) -> Opcode {
        Opcode::CmpReg8Const8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            register: RegisterIndex::from(next()),
            comparand: next(),
        }
    }

    fn execute(&self, vm: &mut VM) {
        vm.flags
            .set_equal(vm.registers[self.register].value == self.comparand)
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.register.0, self.comparand]
    }
}

pub struct Exit;

impl Instruction for Exit {
    fn opcode(&self) -> Opcode {
        Opcode::Exit
    }

    fn decode(_next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {}
    }

    fn execute(&self, vm: &mut VM) {
        vm.stop = true;
    }

    fn len(&self) -> u8 {
        1
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _]
    }
}

pub struct JumpIfNotEqual {
    pub address: u8,
}

impl Instruction for JumpIfNotEqual {
    fn opcode(&self) -> Opcode {
        Opcode::JumpIfNotEqual
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self { address: next() }
    }

    fn execute(&self, vm: &mut VM) {
        if !vm.flags.equal() {
            vm.registers[Register::PC].value = self.address;
        }
    }

    fn len(&self) -> u8 {
        2
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.address]
    }
}

pub struct SubReg8Const8 {
    pub register: RegisterIndex,
    pub value: u8,
}

impl Instruction for SubReg8Const8 {
    fn opcode(&self) -> Opcode {
        Opcode::SubReg8Const8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            register: RegisterIndex::from(next()),
            value: next(),
        }
    }

    fn execute(&self, vm: &mut VM) {
        vm.registers[self.register].value -= self.value;
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.register.0, self.value]
    }
}

pub struct AddReg8Const8 {
    pub register: RegisterIndex,
    pub value: u8,
}

impl Instruction for AddReg8Const8 {
    fn opcode(&self) -> Opcode {
        Opcode::AddReg8Const8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            register: RegisterIndex::from(next()),
            value: next(),
        }
    }

    fn execute(&self, vm: &mut VM) {
        vm.registers[self.register].value += self.value;
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.register.0, self.value]
    }
}

pub struct ReadStdinStack {
    pub count: u8,
}

impl Instruction for ReadStdinStack {
    fn opcode(&self) -> Opcode {
        Opcode::ReadStdinStack
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self { count: next() }
    }

    fn execute(&self, vm: &mut VM) {
        let mut bytes = vec![0; self.count as usize];
        io::stdin().read(&mut bytes).unwrap();
        bytes.reverse();

        let sp = &mut vm.registers[Register::SP];
        if (sp.value as usize + bytes.len()) > VM::STACK_RANGE.len() {
            panic!("Stack is full");
        }
        vm.memory[VM::STACK_RANGE][sp.value as usize..bytes.len()].copy_from_slice(&bytes);
        sp.value += bytes.len() as u8;
    }

    fn len(&self) -> u8 {
        2
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.count]
    }
}

pub struct PopReg8 {
    pub register: RegisterIndex,
}

impl Instruction for PopReg8 {
    fn opcode(&self) -> Opcode {
        Opcode::PopReg8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            register: RegisterIndex::from(next()),
        }
    }

    fn execute(&self, vm: &mut VM) {
        let sp = &mut vm.registers[Register::SP];
        if sp.value == 0 {
            panic!("Stack is empty");
        }
        sp.value -= 1;
        let stack = &mut vm.memory[VM::STACK_RANGE];
        vm.registers[self.register].value = stack[(sp.value) as usize];
    }

    fn len(&self) -> u8 {
        2
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.register.0]
    }
}

pub struct DerefAddressReg16Reg8 {
    pub source: AddressReg16,
    pub destination: RegisterIndex,
}

impl Instruction for DerefAddressReg16Reg8 {
    fn opcode(&self) -> Opcode {
        Opcode::DerefAddressReg16Reg8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            source: AddressReg16 {
                high: RegisterIndex::from(next()),
                low: RegisterIndex::from(next()),
            },
            destination: RegisterIndex::from(next()),
        }
    }

    fn execute(&self, vm: &mut VM) {
        let address = self.source.eval_vm(&vm);
        vm.registers[self.destination].value = vm.memory[address as usize];
    }

    fn len(&self) -> u8 {
        4
    }

    fn encode(&self) -> Vec<u8> {
        vec![
            self.opcode() as _,
            self.source.high.0,
            self.source.low.0,
            self.destination.0,
        ]
    }
}

pub struct XorReg8Reg8 {
    pub destination: RegisterIndex,
    pub source: RegisterIndex,
}

impl Instruction for XorReg8Reg8 {
    fn opcode(&self) -> Opcode {
        Opcode::XorReg8Reg8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            destination: RegisterIndex::from(next()),
            source: RegisterIndex::from(next()),
        }
    }

    fn execute(&self, vm: &mut VM) {
        let source = vm.registers[self.source].value;
        let destination = &mut vm.registers[self.destination];
        destination.value = destination.value ^ source;
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.destination.0, self.source.0]
    }
}

pub struct WriteStdoutConst8 {
    pub byte: u8,
}

impl Instruction for WriteStdoutConst8 {
    fn opcode(&self) -> Opcode {
        Opcode::WriteStdoutConst8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self { byte: next() }
    }

    fn execute(&self, _vm: &mut VM) {
        print!("{}", char::from(self.byte));
    }

    fn len(&self) -> u8 {
        2
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.byte]
    }
}

pub struct CmpReg8Reg8 {
    pub comparand1: RegisterIndex,
    pub comparand2: RegisterIndex,
}

impl Instruction for CmpReg8Reg8 {
    fn opcode(&self) -> Opcode {
        Opcode::CmpReg8Reg8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            comparand1: RegisterIndex::from(next()),
            comparand2: RegisterIndex::from(next()),
        }
    }

    fn execute(&self, vm: &mut VM) {
        vm.flags
            .set_equal(vm.registers[self.comparand1].value == vm.registers[self.comparand2].value)
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.comparand1.0, self.comparand2.0]
    }
}

pub struct XorReg8Const8 {
    pub register: RegisterIndex,
    pub value: u8,
}

impl Instruction for XorReg8Const8 {
    fn opcode(&self) -> Opcode {
        Opcode::XorReg8Const8
    }

    fn decode(next: &mut dyn FnMut() -> u8) -> Self
    where
        Self: Sized,
    {
        Self {
            register: RegisterIndex::from(next()),
            value: next(),
        }
    }

    fn execute(&self, vm: &mut VM) {
        vm.registers[self.register].value ^= self.value;
    }

    fn len(&self) -> u8 {
        3
    }

    fn encode(&self) -> Vec<u8> {
        vec![self.opcode() as _, self.register.0, self.value]
    }
}
