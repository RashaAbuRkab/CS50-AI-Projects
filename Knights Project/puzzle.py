from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Implication(AKnight, And(AKnight, AKnave)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, And(AKnight, BKnight)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Implication(AKnight, Biconditional(AKnight, BKnight)),
    Implication(AKnave, Not(Biconditional(AKnight, BKnight))),
    Implication(BKnight, Not(Biconditional(AKnight, BKnight))),
     Implication(BKnave, Biconditional(AKnight, BKnight))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),  # A is either a knight or a knave, not both
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    Implication(AKnight, Or(AKnight, AKnave)),  # If A is a knight, A says the truth about being a knight or knave
    Implication(AKnave, Not(Or(AKnight, AKnave))),  # If A is a knave, A lies about being a knight or knave

    Implication(BKnight, Biconditional(AKnight, AKnave)),  # B says "A said 'I am a knave'"
    Implication(BKnight, CKnave),  # B says "C is a knave"
    Implication(BKnave, Not(Biconditional(AKnight, AKnave))),  # B lies if B is a knave
    Implication(BKnave, Not(CKnave)),  # B lies if B is a knave and C is not a knave

    Implication(CKnight, AKnight),  # C says "A is a knight"
    Implication(CKnave, Not(AKnight))  # C lies if C is a knave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
