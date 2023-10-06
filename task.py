import streamlit as st
from simpleai.search import CspProblem, backtrack


# Title & Header
st.title("CryptoArithmetic Puzzle")
st.header("Fill in the words")

word1 = st.text_input("Enter the first word: ")
word2 = st.text_input("Enter the second word: ")
word3 = st.text_input("Enter the third word: ")

# Extract the variables from the words
variables = set(word1 + word2 + word3)

# The list of values that each variable can take
domains = {}
for variable in variables:
    domains[variable] = list(range(10))

def constraint_unique(variables, values):
    return len(values) == len(set(values))  # remove repeated values and count
def constraint_add(variables, values):
    # Extract the numbers from the values
    numbers = []
    for value in values:
        if isinstance(value, int):
            numbers.append(str(value))
    factor1 = int(''.join([numbers[variables.index(letter)] for letter in word1]))
    factor2 = int(''.join([numbers[variables.index(letter)] for letter in word2]))
    result = int(''.join([numbers[variables.index(letter)] for letter in word3]))
    if numbers[variables.index(word3[0])] == '0':
        return False
    return (factor1 + factor2) == result
constraints = [
    ((variables), constraint_unique),
    ((variables), constraint_add),
]
problem = CspProblem(variables, domains, constraints)

if st.button("Calculate"):
    output = backtrack(problem)
    
    if output is not None:
        table_data = []
        for word in [word1, word2, word3]:
            table_data.append([word, ''.join([str(output[letter]) for letter in word])])
        st.text("Solution:", output)
        st.table(table_data)
    else:
        st.error("No solution found for the given puzzle.")