# Adds Hello World / add() / loop examples for 35+ languages, plus "which language" advice, to zorn_data.jsonl.
import json, random
random.seed(5)
cb = lambda l, c: "```" + l + "\n" + c.strip("\n") + "\n```"
L = [  # (name, fence, hello, add, loop)
("Python","python",r'print("Hello, World!")',"def add(a, b):\n    return a + b","for i in range(1, 6):\n    print(i)"),
("JavaScript","js",r'console.log("Hello, World!");',"const add = (a, b) => a + b;","for (let i = 1; i <= 5; i++) console.log(i);"),
("TypeScript","ts",r'console.log("Hello, World!");',"const add = (a: number, b: number): number => a + b;","for (let i = 1; i <= 5; i++) {\n  console.log(i);\n}"),
("Java","java",'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',"static int add(int a, int b) {\n    return a + b;\n}","for (int i = 1; i <= 5; i++) {\n    System.out.println(i);\n}"),
("C","c",r'#include <stdio.h>'+'\nint main(void) {\n    printf("Hello, World!\\n");\n    return 0;\n}',"int add(int a, int b) {\n    return a + b;\n}",r'for (int i = 1; i <= 5; i++) {'+'\n    printf("%d\\n", i);\n}'),
("C++","cpp",'#include <iostream>\nint main() {\n    std::cout << "Hello, World!\\n";\n}',"int add(int a, int b) {\n    return a + b;\n}",'for (int i = 1; i <= 5; i++) {\n    std::cout << i << "\\n";\n}'),
("C#","csharp",'Console.WriteLine("Hello, World!");',"static int Add(int a, int b) => a + b;","for (int i = 1; i <= 5; i++)\n    Console.WriteLine(i);"),
("Go","go",'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, World!")\n}',"func add(a, b int) int {\n    return a + b\n}","for i := 1; i <= 5; i++ {\n    fmt.Println(i)\n}"),
("Rust","rust",'fn main() {\n    println!("Hello, World!");\n}',"fn add(a: i32, b: i32) -> i32 {\n    a + b\n}",'for i in 1..=5 {\n    println!("{}", i);\n}'),
("PHP","php",'<?php\necho "Hello, World!";',"function add($a, $b) {\n    return $a + $b;\n}",'for ($i = 1; $i <= 5; $i++) {\n    echo $i . "\\n";\n}'),
("Ruby","ruby",'puts "Hello, World!"',"def add(a, b)\n  a + b\nend","(1..5).each { |i| puts i }"),
("Swift","swift",'print("Hello, World!")',"func add(_ a: Int, _ b: Int) -> Int {\n    return a + b\n}","for i in 1...5 {\n    print(i)\n}"),
("Kotlin","kotlin",'fun main() {\n    println("Hello, World!")\n}',"fun add(a: Int, b: Int) = a + b","for (i in 1..5) println(i)"),
("Dart","dart","void main() {\n  print('Hello, World!');\n}","int add(int a, int b) => a + b;","for (var i = 1; i <= 5; i++) {\n  print(i);\n}"),
("Scala","scala",'object Main extends App {\n  println("Hello, World!")\n}',"def add(a: Int, b: Int): Int = a + b","for (i <- 1 to 5) println(i)"),
("R","r",'cat("Hello, World!\\n")',"add <- function(a, b) a + b","for (i in 1:5) print(i)"),
("Perl","perl",'print "Hello, World!\\n";',"sub add {\n    my ($a, $b) = @_;\n    return $a + $b;\n}",'for my $i (1..5) {\n    print "$i\\n";\n}'),
("Lua","lua",'print("Hello, World!")',"function add(a, b)\n  return a + b\nend","for i = 1, 5 do\n  print(i)\nend"),
("Haskell","haskell",'main :: IO ()\nmain = putStrLn "Hello, World!"',"add :: Int -> Int -> Int\nadd a b = a + b","mapM_ print [1..5]"),
("Elixir","elixir",'IO.puts("Hello, World!")',"defmodule Math do\n  def add(a, b), do: a + b\nend","Enum.each(1..5, &IO.puts/1)"),
("Bash","bash",'echo "Hello, World!"',"add() {\n  echo $(($1 + $2))\n}","for i in {1..5}; do\n  echo $i\ndone"),
("PowerShell","powershell",'Write-Output "Hello, World!"',"function Add($a, $b) {\n    return $a + $b\n}","1..5 | ForEach-Object { $_ }"),
("Julia","julia",'println("Hello, World!")',"add(a, b) = a + b","for i in 1:5\n    println(i)\nend"),
("Objective-C","objectivec",'#import <Foundation/Foundation.h>\nint main(void) {\n    @autoreleasepool {\n        NSLog(@"Hello, World!");\n    }\n    return 0;\n}',"int add(int a, int b) {\n    return a + b;\n}",'for (int i = 1; i <= 5; i++) {\n    NSLog(@"%d", i);\n}'),
("MATLAB","matlab","disp('Hello, World!')","function r = add(a, b)\n    r = a + b;\nend","for i = 1:5\n    disp(i)\nend"),
("Zig","zig",'const std = @import("std");\n\npub fn main() void {\n    std.debug.print("Hello, World!\\n", .{});\n}',"fn add(a: i32, b: i32) i32 {\n    return a + b;\n}",'var i: u32 = 1;\nwhile (i <= 5) : (i += 1) {\n    std.debug.print("{}\\n", .{i});\n}'),
("GDScript","gdscript",'print("Hello, World!")',"func add(a, b):\n\treturn a + b","for i in range(1, 6):\n\tprint(i)"),
("F#","fsharp",'printfn "Hello, World!"',"let add a b = a + b",'for i in 1..5 do\n    printfn "%d" i'),
("OCaml","ocaml",'let () = print_endline "Hello, World!"',"let add a b = a + b","for i = 1 to 5 do\n  print_int i; print_newline ()\ndone"),
("Clojure","clojure",'(println "Hello, World!")',"(defn add [a b]\n  (+ a b))","(doseq [i (range 1 6)]\n  (println i))"),
("Fortran","fortran",'program hello\n  print *, "Hello, World!"\nend program hello',"integer function add(a, b)\n  integer :: a, b\n  add = a + b\nend function add","do i = 1, 5\n  print *, i\nend do"),
("Visual Basic .NET","vbnet",'Console.WriteLine("Hello, World!")',"Function Add(a As Integer, b As Integer) As Integer\n    Return a + b\nEnd Function","For i = 1 To 5\n    Console.WriteLine(i)\nNext"),
("Groovy","groovy",'println "Hello, World!"',"def add(a, b) {\n    a + b\n}","(1..5).each { println it }"),
("Nim","nim",'echo "Hello, World!"',"proc add(a, b: int): int =\n  a + b","for i in 1..5:\n  echo i"),
("Crystal","crystal",'puts "Hello, World!"',"def add(a, b)\n  a + b\nend","(1..5).each { |i| puts i }"),
("Solidity","solidity","// SPDX-License-Identifier: MIT\npragma solidity ^0.8.0;\ncontract Hello {\n    string public greeting = \"Hello, World!\";\n}","function add(uint a, uint b) public pure returns (uint) {\n    return a + b;\n}","for (uint i = 1; i <= 5; i++) {\n    // do something with i\n}"),
]
rows = []
for n, f, h, a, l in L:
    rows.append({"question": f"Write Hello World in {n}.", "thinking": f"Use {n}'s standard way to print text and include any required entry point.", "answer": cb(f, h)})
    rows.append({"question": f"Write a function in {n} that adds two numbers.", "thinking": f"Declare a {n} function with two parameters and return their sum, using {n} typing and syntax rules.", "answer": cb(f, a)})
    rows.append({"question": f"Write a loop in {n} that prints the numbers 1 to 5.", "thinking": f"Use {n}'s idiomatic loop over an inclusive range 1..5.", "answer": cb(f, l)})
R = [("web front-end websites","JavaScript or TypeScript with HTML/CSS","Browsers run JavaScript natively; TypeScript adds types for larger projects."),
("data science and machine learning","Python (also R and Julia)","Python has the biggest ecosystem: NumPy, pandas, PyTorch, scikit-learn."),
("mobile apps for Android","Kotlin (or Flutter with Dart)","Kotlin is Google's preferred language for Android."),
("mobile apps for iOS","Swift","Swift is Apple's modern language for iOS and macOS."),
("games","C# (Unity), GDScript (Godot) or C++ (Unreal)","Each engine has its own main language; GDScript is the easiest to start with."),
("operating systems and embedded devices","C, C++ or Rust","They give low-level control and speed; Rust adds memory safety."),
("backend servers and APIs","Node.js, Python, Go or Java","Pick the one you know; Go is great for fast, simple servers and Java for large enterprises."),
("automation and scripting","Python, Bash or PowerShell","They are quick to write and available on most systems."),
("smart contracts","Solidity","It's the main language for Ethereum-compatible blockchains."),
("databases and reports","SQL","SQL is the standard language for querying relational databases."),
("a first programming language","Python or JavaScript","Both have simple syntax, huge communities and instant results.")]
for u, ls, why in R:
    rows.append({"question": f"Which programming language should I learn for {u}?", "thinking": f"Match the goal ({u}) to the language most used in that area, then explain why.", "answer": f"For {u}, I'd suggest **{ls}**. {why}"})
rows.append({"question": "Do you know all programming languages?", "thinking": "Be honest: I know many popular ones well, but not every language, and quality varies on rare ones.", "answer": "I know many popular languages well (Python, JavaScript, Java, C/C++, C#, Go, Rust, PHP, Ruby, Swift, Kotlin and more), but not every language in existence, and my answers on rare ones can be less reliable. Test my code and tell me the error if something fails."})
old = [json.loads(x) for x in open("zorn_data.jsonl")]
seen = {r["question"] for r in old}
rows = [r for r in rows if r["question"] not in seen]
allr = old + rows
random.shuffle(allr)
with open("zorn_data.jsonl", "w") as f:
    for r in allr: f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(rows), "added; total", len(allr))
