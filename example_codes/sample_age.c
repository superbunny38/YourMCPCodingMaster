#include <stdio.h> // Include the standard input/output library

int main() { // Main function: program execution starts here

    // Declare variables to store an integer, a float, and a character
    int age = 30;
    float height = 5.9; // Height in feet
    char initial = 'J';

    // Print some initial information
    printf("--- User Profile ---\n");
    printf("Initial: %c\n", initial);
    printf("Current Age: %d years\n", age);
    printf("Height: %.1f feet\n", height); // .1f prints one decimal place

    // Perform a simple calculation
    int years_later = 5;
    int future_age = age + years_later;

    // Print the result of the calculation
    printf("In %d years, age will be: %d\n", years_later, future_age);

    // Demonstrate a conditional statement (if-else)
    if (height > 6.0) {
        printf("You're quite tall!\n");
    } else {
        printf("Average height noted.\n");
    }

    printf("--- End of Profile ---\n"); // Concluding message

    return 0; // Indicate successful program execution
}