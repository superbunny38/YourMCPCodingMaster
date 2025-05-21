using System;

public class BasicFunctions
{
    // 1. Function to add two integers
    public static int AddNumbers(int num1, int num2)
    {
        return num1 + num2;
    }

    // 2. Function to concatenate two strings with a space in between
    public static string ConcatenateStrings(string str1, string str2)
    {
        return $"{str1} {str2}"; // Using string interpolation
        // Alternatively: return str1 + " " + str2;
    }

    // 3. Function to check if a number is even
    public static bool IsEven(int number)
    {
        return number % 2 == 0;
    }

    // Example of how to use these functions
    public static void Main(string[] args)
    {
        // Example for AddNumbers
        int numberA = 5;
        int numberB = 3;
        int sum = AddNumbers(numberA, numberB);
        Console.WriteLine($"Input: {numberA}, {numberB} | Function: AddNumbers | Output: {sum}"); // Output: 8

        // Example for ConcatenateStrings
        string firstName = "Hello";
        string lastName = "World";
        string fullName = ConcatenateStrings(firstName, lastName);
        Console.WriteLine($"Input: \"{firstName}\", \"{lastName}\" | Function: ConcatenateStrings | Output: \"{fullName}\""); // Output: "Hello World"

        // Example for IsEven
        int evenTestNumber = 4;
        bool isNumberEven = IsEven(evenTestNumber);
        Console.WriteLine($"Input: {evenTestNumber} | Function: IsEven | Output: {isNumberEven}"); // Output: True

        int oddTestNumber = 7;
        bool isNumberOdd = IsEven(oddTestNumber); // This will be false
        Console.WriteLine($"Input: {oddTestNumber} | Function: IsEven | Output: {isNumberOdd}"); // Output: False
    }
}