#!/usr/bin/env ruby

begin
    while true do
        user_input = STDIN.gets.chomp
        raise "Length" if user_input.length > 4
        user_input.chars.each do |c|
            raise "Blacklist" if c == '`'
            raise "Blacklist" if c == '%'
            raise "Blacklist" if c == '|'
            raise "Blacklist" if c == 'p'
        end
        eval user_input
    end
rescue Exception => e
    puts "Goodbye!"
end