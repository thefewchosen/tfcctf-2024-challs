use std::fs;
use std::fs::File;
use std::io::Write;

use clap::Parser;
use rand::RngCore;

use crate::instruction::*;
use crate::registers::{Register, RegisterSet};
use crate::vm::{Address16, AddressReg16, Flags, VM};

mod instruction;
mod registers;
mod vm;

pub const FLAG_INNER_LEN: usize = 32;
pub const FLAG_LEN: usize = FLAG_INNER_LEN + "TFCCTF{}".len();

fn create_challenge() {
    let printable_xor_stream = |stream: &[u8]| {
        stream
            .iter()
            .map(|byte| format!("{:02x}", byte))
            .collect::<Vec<String>>()
            .join(" ")
    };

    let mut flag = [0; FLAG_INNER_LEN / 2];
    rand::thread_rng().fill_bytes(&mut flag);
    let flag = hex::encode(&flag);
    let flag = format!("TFCCTF{{{}}}", flag);
    println!("Generated flag: {flag}");

    let mut xor_bytes = [0; FLAG_LEN];
    rand::thread_rng().fill_bytes(&mut xor_bytes);
    println!("Xor values: {}", printable_xor_stream(&xor_bytes));

    let xor_flag = flag
        .as_bytes()
        .iter()
        .zip(xor_bytes.iter())
        .map(|(&a, &b)| a ^ b)
        .collect::<Vec<_>>();
    println!("Xor flag: {}", printable_xor_stream(&xor_flag));

    /*
       R0 = FLAG_LEN;
       while (R0 != 0) {
           R3 = pop(); // read byte
           R4 = deref([R1:R2]); // xor value
           R4 ^= 0x41
           R2 += 1;
           R5 = deref([R1:R2]); // xor flag
           R5 ^= 0x41;
           R2 += 1;
           R3 ^= R4;
           if (R3 != R5) {
               fail!;
           }
       }
       success!;
    */
    let xor_instructions: Vec<Box<dyn Instruction>> = vec![
        Box::new(ReadStdinStack {
            count: FLAG_LEN as u8,
        }),
        Box::new(MovReg8Const8 {
            to: Register::R0,
            value: FLAG_LEN as u8,
        }),
        Box::new(MovReg8Const8 {
            to: Register::R1,
            value: Address16::from(VM::MEMORY_RANGE.start as u16).high,
        }),
        Box::new(MovReg8Const8 {
            to: Register::R2,
            value: Address16::from(VM::MEMORY_RANGE.start as u16).low,
        }),
        Box::new(PopReg8 {
            register: Register::R3,
        }),
        Box::new(DerefAddressReg16Reg8 {
            source: AddressReg16 {
                high: Register::R1,
                low: Register::R2,
            },
            destination: Register::R4,
        }),
        Box::new(XorReg8Const8 {
            register: Register::R4,
            value: 0x41,
        }),
        Box::new(AddReg8Const8 {
            register: Register::R2,
            value: 1,
        }),
        Box::new(DerefAddressReg16Reg8 {
            source: AddressReg16 {
                high: Register::R1,
                low: Register::R2,
            },
            destination: Register::R5,
        }),
        Box::new(XorReg8Const8 {
            register: Register::R5,
            value: 0x41,
        }),
        Box::new(AddReg8Const8 {
            register: Register::R2,
            value: 1,
        }),
        Box::new(XorReg8Reg8 {
            destination: Register::R3,
            source: Register::R4,
        }),
        Box::new(CmpReg8Reg8 {
            comparand1: Register::R3,
            comparand2: Register::R5,
        }),
        Box::new(JumpIfNotEqual { address: 0x4e }),
        Box::new(SubReg8Const8 {
            register: Register::R0,
            value: 1,
        }),
        Box::new(CmpReg8Const8 {
            register: Register::R0,
            comparand: 0,
        }),
        Box::new(JumpIfNotEqual { address: 0x1F }),
        Box::new(WriteStdoutConst8 { byte: b'Y' }),
        Box::new(WriteStdoutConst8 { byte: b'e' }),
        Box::new(WriteStdoutConst8 { byte: b'p' }),
        Box::new(WriteStdoutConst8 { byte: b'\n' }),
        Box::new(Exit {}),
        Box::new(WriteStdoutConst8 { byte: b'N' }),
        Box::new(WriteStdoutConst8 { byte: b'o' }),
        Box::new(WriteStdoutConst8 { byte: b'p' }),
        Box::new(WriteStdoutConst8 { byte: b'e' }),
        Box::new(WriteStdoutConst8 { byte: b'\n' }),
        Box::new(Exit {}),
    ];
    let plain_instructions: Vec<Box<dyn Instruction>> = vec![
        Box::new(MovReg8Const8 {
            to: Register::R0,
            value: xor_instructions
                .iter()
                .fold(0, |accumulator, item| accumulator + item.len()),
        }),
        Box::new(MovReg8Const8 {
            to: Register::R1,
            value: 0x14,
        }),
        Box::new(XorMemReg8Const8 {
            register: Register::R1,
            value: 0x41,
        }),
        Box::new(SubReg8Const8 {
            register: Register::R0,
            value: 1,
        }),
        Box::new(AddReg8Const8 {
            register: Register::R1,
            value: 1,
        }),
        Box::new(CmpReg8Const8 {
            register: Register::R0,
            comparand: 0,
        }),
        Box::new(JumpIfNotEqual { address: 6 }),
    ];
    let plain_instructions = plain_instructions
        .iter()
        .map(|item| item.encode())
        .flatten()
        .collect::<Vec<_>>();
    let xor_instructions = xor_instructions
        .iter()
        .map(|item| item.encode())
        .flatten()
        .map(|byte| byte ^ 0x41)
        .collect::<Vec<_>>();
    let mut instructions = [plain_instructions, xor_instructions].concat();
    assert!(
        instructions.len() < VM::INSTRUCTIONS_BOUNDARY,
        "Too many instructions"
    );
    instructions.resize(VM::INSTRUCTIONS_RANGE.len(), 0);
    let mut memory = vec![0u8; VM::MEMORY_RANGE.len()];
    let xor_zip = xor_flag
        .iter()
        .zip(xor_bytes.iter())
        .map(|(&a, &b)| [a ^ 0x41, b ^ 0x41])
        .flatten()
        .collect::<Vec<_>>();
    memory[0..(FLAG_LEN * 2)].copy_from_slice(&xor_zip);
    let stack = vec![0u8; VM::STACK_RANGE.len()];
    let program = [instructions, memory, stack].concat();
    let mut file = File::create("program.bin").unwrap();
    file.write(&program).unwrap();
}

#[derive(Parser)]
struct Args {
    #[arg(long)]
    file: String,
}

fn main() {
    if cfg!(debug_assertions) {
        create_challenge();
    }
    let args = Args::parse();
    let stream = fs::read(args.file).expect("Could not read file");
    let mut vm = VM {
        memory: [0; VM::VM_BOUNDARY],
        registers: RegisterSet {
            registers: [Register { value: 0 }; 16],
        },
        flags: Flags::new(),
        stop: false,
    };
    vm.run(&stream.to_vec());
    if cfg!(debug_assertions) {
        println!("{}", vm);
    }
}
