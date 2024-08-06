use std::ops::{Deref, Index, IndexMut};

#[repr(transparent)]
#[derive(Copy, Clone)]
pub struct Register {
    pub(crate) value: u8,
}

#[repr(transparent)]
#[derive(Clone, Copy)]
pub struct RegisterIndex(pub u8);

impl From<u8> for RegisterIndex {
    fn from(value: u8) -> Self {
        Self(value)
    }
}

impl Deref for Register {
    type Target = u8;

    fn deref(&self) -> &Self::Target {
        &self.value
    }
}

macro_rules! define_register_index {
    ($index:literal) => {
        paste::paste! {
            pub const [<R $index>]: RegisterIndex = RegisterIndex($index);
        }
    };
}

macro_rules! define_register {
    ($name:ident, $index:literal) => {
        pub const $name: RegisterIndex = RegisterIndex($index);
    };
}

impl Register {
    define_register_index!(0);
    define_register_index!(1);
    define_register_index!(2);
    define_register_index!(3);
    define_register_index!(4);
    define_register_index!(5);
    define_register_index!(6);
    define_register_index!(7);
    define_register!(PC, 8);
    define_register!(SP, 9);
}

#[repr(transparent)]
pub struct RegisterSet {
    pub(crate) registers: [Register; 16],
}

impl Index<RegisterIndex> for RegisterSet {
    type Output = Register;

    fn index(&self, index: RegisterIndex) -> &Self::Output {
        &self.registers[index.0 as usize]
    }
}

impl IndexMut<RegisterIndex> for RegisterSet {
    fn index_mut(&mut self, index: RegisterIndex) -> &mut Self::Output {
        &mut self.registers[index.0 as usize]
    }
}
