LANGUAGES = {
  "45": "Assembly (NASM 2.14.02)",
  "46": "Bash (5.0.0)",
  "47": "Basic (FBC 1.07.1)",
  "75": "C (Clang 7.0.1)",
  "76": "C++ (Clang 7.0.1)",
  "48": "C (GCC 7.4.0)",
  "52": "C++ (GCC 7.4.0)",
  "49": "C (GCC 8.3.0)",
  "53": "C++ (GCC 8.3.0)",
  "50": "C (GCC 9.2.0)",
  "54": "C++ (GCC 9.2.0)",
  "86": "Clojure (1.10.1)",
  "51": "C# (Mono 6.6.0.161)",
  "77": "COBOL (GnuCOBOL 2.2)",
  "55": "Common Lisp (SBCL 2.0.0)",
  "56": "D (DMD 2.089.1)",
  "57": "Elixir (1.9.4)",
  "58": "Erlang (OTP 22.2)",
  "44": "Executable",
  "87": "F# (.NET Core SDK 3.1.202)",
  "59": "Fortran (GFortran 9.2.0)",
  "60": "Go (1.13.5)",
  "88": "Groovy (3.0.3)",
  "61": "Haskell (GHC 8.8.1)",
  "62": "Java (OpenJDK 13.0.1)",
  "63": "JavaScript (Node.js 12.14.0)",
  "78": "Kotlin (1.3.70)",
  "64": "Lua (5.3.5)",
  "89": "Multi-file program",
  "79": "Objective-C (Clang 7.0.1)",
  "65": "OCaml (4.09.0)",
  "66": "Octave (5.1.0)",
  "67": "Pascal (FPC 3.0.4)",
  "85": "Perl (5.28.1)",
  "68": "PHP (7.4.1)",
  "43": "Plain Text",
  "69": "Prolog (GNU Prolog 1.4.5)",
  "70": "Python (2.7.17)",
  "71": "Python (3.8.1)",
  "80": "R (4.0.0)",
  "72": "Ruby (2.7.0)",
  "73": "Rust (1.40.0)",
  "81": "Scala (2.13.2)",
  "82": "SQL (SQLite 3.27.2)",
  "83": "Swift (5.2.3)",
  "74": "TypeScript (3.7.4)",
  "84": "Visual Basic.Net (vbnc 0.0.0.5943)"
}





LANGUAGE_SNIPPETS = {
    "45": 'section .data\nmsg db "Welcome {name}",0\nsection .text\nglobal _start\n_start:\n    ; sys_write\n    mov edx,13\n    mov ecx,msg\n    mov ebx,1\n    mov eax,4\n    int 0x80\n    ; sys_exit\n    mov eax,1\n    int 0x80',  # Assembly NASM
    "46": 'echo "Welcome {name}"',  # Bash
    "47": 'PRINT "Welcome {name}"',  # Basic FBC
    "75": '#include <stdio.h>\nint main() {{\n    printf("Welcome {name}\\n");\n    return 0;\n}}',  # C Clang
    "76": '#include <iostream>\nusing namespace std;\nint main() {{\n    cout << "Welcome {name}" << endl;\n    return 0;\n}}',  # C++ Clang
    "48": '#include <stdio.h>\nint main() {{\n    printf("Welcome {name}\\n");\n    return 0;\n}}',  # C GCC 7.4
    "52": '#include <iostream>\nusing namespace std;\nint main() {{\n    cout << "Welcome {name}" << endl;\n    return 0;\n}}',  # C++ GCC 7.4
    "49": '#include <stdio.h>\nint main() {{\n    printf("Welcome {name}\\n");\n    return 0;\n}}',  # C GCC 8.3
    "53": '#include <iostream>\nusing namespace std;\nint main() {{\n    cout << "Welcome {name}" << endl;\n    return 0;\n}}',  # C++ GCC 8.3
    "50": '#include <stdio.h>\nint main() {{\n    printf("Welcome {name}\\n");\n    return 0;\n}}',  # C GCC 9.2
    "54": '#include <iostream>\nusing namespace std;\nint main() {{\n    cout << "Welcome {name}" << endl;\n    return 0;\n}}',  # C++ GCC 9.2
    "86": '(println "Welcome {name}")',  # Clojure
    "51": 'using System;\nclass Program {{\n    static void Main() {{\n        Console.WriteLine("Welcome {name}");\n    }}\n}}',  # C#
    "77": 'IDENTIFICATION DIVISION.\nPROGRAM-ID. WELCOME.\nPROCEDURE DIVISION.\n    DISPLAY "Welcome {name}".\n    STOP RUN.',  # COBOL
    "55": '(format t "Welcome {name}~%")',  # Common Lisp
    "56": 'import std.stdio;\nvoid main() {{\n    writeln("Welcome {name}");\n}}',  # D
    "57": 'IO.puts("Welcome {name}")',  # Elixir
    "58": 'io:format("Welcome {name}\\n").',  # Erlang
    "44": 'Welcome {name}',  # Executable / plain text
    "87": 'printfn "Welcome {name}"',  # F#
    "59": 'program welcome\nprint *, "Welcome {name}"\nend program welcome',  # Fortran
    "60": 'package main\nimport "fmt"\nfunc main() {{\n    fmt.Println("Welcome {name}")\n}}',  # Go
    "88": 'println "Welcome {name}"',  # Groovy
    "61": 'main = putStrLn "Welcome {name}"',  # Haskell
    "62": 'public class Main {{\n    public static void main(String[] args) {{\n        System.out.println("Welcome {name}");\n    }}\n}}',  # Java
    "63": 'console.log("Welcome {name}");',  # JavaScript
    "78": 'fun main() {{\n    println("Welcome {name}")\n}}',  # Kotlin
    "64": 'print("Welcome {name}")',  # Lua
    "89": '/* Multi-file program placeholder */\n// Welcome {name}',  # Multi-file
    "79": '#import <Foundation/Foundation.h>\nint main() {{\n    @autoreleasepool {{\n        NSLog(@"Welcome {name}");\n    }}\n    return 0;\n}}',  # Objective-C
    "65": 'print_endline "Welcome {name}"',  # OCaml
    "66": 'disp("Welcome {name}")',  # Octave
    "67": 'program Welcome;\nbegin\n  writeln("Welcome {name}");\nend.',  # Pascal
    "85": 'print "Welcome {name}\\n";',  # Perl
    "68": '<?php\necho "Welcome {name}\\n";\n?>',  # PHP
    "43": 'Welcome {name}',  # Plain Text
    "69": 'write("Welcome {name}"), nl.',  # Prolog
    "70": 'print "Welcome {name}"',  # Python 2
    "71": 'print("Welcome {name}")',  # Python 3
    "80": 'cat("Welcome {name}\\n")',  # R
    "72": 'puts "Welcome {name}"',  # Ruby
    "73": 'fn main() {{\n    println!("Welcome {name}");\n}}',  # Rust
    "81": 'object Main extends App {{\n  println("Welcome {name}")\n}}',  # Scala
    "82": 'SELECT "Welcome {name}";',  # SQL
    "83": 'print("Welcome {name}")',  # Swift
    "74": 'console.log("Welcome {name}");',  # TypeScript
    "84": 'Module Module1\n    Sub Main()\n        Console.WriteLine("Welcome {name}")\n    End Sub\nEnd Module'  # Visual Basic .NET
}