import math

def calculator():
    """Basic Calculator with all fundamental operations"""
    
    print("=" * 40)
    print("       BASIC CALCULATOR")
    print("=" * 40)
    print("\nAvailable Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Modulo (%)")
    print("6. Power (**)")
    print("7. Square Root (√)")
    print("8. Exit")
    print("-" * 40)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-8): ")
            
            if choice == '8':
                print("\nThank you for using the calculator. Goodbye!")
                break
            
            if choice not in ['1', '2', '3', '4', '5', '6', '7']:
                print("Invalid choice! Please enter a number between 1 and 8.")
                continue
            
            if choice == '7':
                num = float(input("Enter the number: "))
                if num < 0:
                    print("Error: Cannot calculate square root of a negative number!")
                else:
                    result = math.sqrt(num)
                    print(f"√{num} = {result}")
            else:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                if choice == '1':
                    result = num1 + num2
                    print(f"{num1} + {num2} = {result}")
                elif choice == '2':
                    result = num1 - num2
                    print(f"{num1} - {num2} = {result}")
                elif choice == '3':
                    result = num1 * num2
                    print(f"{num1} * {num2} = {result}")
                elif choice == '4':
                    if num2 == 0:
                        print("Error: Division by zero is not allowed!")
                    else:
                        result = num1 / num2
                        print(f"{num1} / {num2} = {result}")
                elif choice == '5':
                    if num2 == 0:
                        print("Error: Modulo by zero is not allowed!")
                    else:
                        result = num1 % num2
                        print(f"{num1} % {num2} = {result}")
                elif choice == '6':
                    result = num1 ** num2
                    print(f"{num1} ** {num2} = {result}")
            
        except ValueError:
            print("Error: Please enter valid numbers!")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    calculator()
        
