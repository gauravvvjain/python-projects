import sys

for line in sys.stdin:
    # Read two integers and print their sum
    a, b = map(int, line.split())
    
    # Bug: we are multiplying instead of adding!
    print(a * b)
