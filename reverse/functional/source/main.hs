module Main where

import System.Environment (getArgs)
import Data.Char (ord)
import Control.Concurrent (threadDelay)

-- Define a custom type for modular arithmetic operations
newtype ModInt = ModInt { getValue :: Integer } deriving (Show, Eq)

-- Define a modulus value for the modular arithmetic
modulus :: Integer
modulus = 1000000007

-- Modular addition
modAdd :: ModInt -> ModInt -> ModInt
modAdd (ModInt x) (ModInt y) = ModInt ((x + y) `mod` modulus)

-- Modular subtraction
modSub :: ModInt -> ModInt -> ModInt
modSub (ModInt x) (ModInt y) = ModInt ((x - y + modulus) `mod` modulus)

-- Modular multiplication
modMul :: ModInt -> ModInt -> ModInt
modMul (ModInt x) (ModInt y) = ModInt ((x * y) `mod` modulus)

-- Modular exponentiation
modExp :: ModInt -> Integer -> ModInt
modExp (ModInt x) n = ModInt (powMod x n modulus)

-- Modular inversion (using Fermat's Little Theorem)
modInv :: ModInt -> ModInt
modInv (ModInt x) = modExp (ModInt x) (modulus - 2)

-- Fast exponentiation with modulo
powMod :: Integer -> Integer -> Integer -> Integer
powMod _ 0 _ = 1
powMod base exp' mod' = 
    let half = powMod base (exp' `div` 2) mod'
        halfSquared = (half * half) `mod` mod'
    in if exp' `mod` 2 == 0 then halfSquared else (base * halfSquared) `mod` mod'

-- Complicated function with recursive calls and sleep delay
complicatedFunction :: Integer -> Integer -> IO Integer
complicatedFunction a b = do
    let result = loop1 a b (ModInt 0)
    threadDelay 3000000 -- Sleep for 3 seconds
    return (getValue result)
  where
    loop1 :: Integer -> Integer -> ModInt -> ModInt
    loop1 x y acc
      | y <= 0 = acc
      | otherwise = 
          let newAcc = modAdd acc (loop2 x y (ModInt 1) 0)
          in loop1 (x - 1) (y - 1) newAcc

    loop2 :: Integer -> Integer -> ModInt -> Integer -> ModInt
    loop2 x y modAcc idx
      | idx >= x = modAcc
      | otherwise =
          let nextModAcc = modAdd modAcc (modMul (ModInt idx) (modExp (ModInt y) (2 * idx)))
          in loop2 x y nextModAcc (idx + 1)

-- Function to apply the function to each character in the input
applyComplicatedFunction :: String -> IO ()
applyComplicatedFunction input = checkSequence input expectedValues
  where
    expectedValues = [260883060,660502790,56707938,56707938,260883060,660502790,634584031,200260288,429639680,312531986,429639680,264427048,624072856,228752755,671507957,384072754,677616060,228752755,671507957,228752755,882563116,429639680,200260288,228752755,998127277,960113301,960113301,843398876]
    
    checkSequence :: String -> [Integer] -> IO ()
    checkSequence [] _ = putStrLn "Correct!"
    checkSequence _ [] = putStrLn "Correct!"
    checkSequence (c:cs) (e:es) = do
        result <- complicatedFunction (toInteger (ord c)) 1337
        if result == e
            then do
                checkSequence cs es
            else do
                putStrLn "Wrong!"

-- Main function to process command-line arguments
main :: IO ()
main = do
    args <- getArgs
    putStrLn "Checking flag..."
    let input = if null args then "" else head args
    if length input == 28
        then applyComplicatedFunction input
        else return ()