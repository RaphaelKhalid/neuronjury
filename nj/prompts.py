"""Coder prompts (dependency-free so every Modal image can import them)."""

SYSTEM = "You are an expert competitive programmer. You write correct, efficient Python 3."
TURN1 = ("Solve the following problem in Python 3. Read from standard input and write to standard output. "
         "Reply with only the code in a single ```python block, no explanations.\n\n{question}")
TURN2 = ("Give one input for which your program's output differs from a correct solution's output, "
         "inside an ```input block. If there is no such input, reply exactly NONE.")
