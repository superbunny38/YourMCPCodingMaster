// Filename: EmployeeDirectory.cs
using System;
using System.Collections.Generic;
using System.Linq; // Required for LINQ

// Define a simple class to represent an Employee
public class Employee
{
    public int Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Department { get; set; }
    public int YearsOfService { get; set; }

    // Constructor
    public Employee(int id, string firstName, string lastName, string department, int yearsOfService)
    {
        Id = id;
        FirstName = firstName;
        LastName = lastName;
        Department = department;
        YearsOfService = yearsOfService;
    }

    // Override ToString for easy printing of employee details
    public override string ToString()
    {
        return $"ID: {Id}, Name: {FirstName} {LastName}, Department: {Department}, Service Years: {YearsOfService}";
    }
}

public class EmployeeDirectory
{
    public static void Main(string[] args)
    {
        // Create a list of employees
        List<Employee> employees = new List<Employee>()
        {
            new Employee(101, "Alice", "Smith", "Engineering", 5),
            new Employee(102, "Bob", "Johnson", "Marketing", 2),
            new Employee(103, "Charlie", "Williams", "Engineering", 8),
            new Employee(104, "Diana", "Brown", "HR", 3),
            new Employee(105, "Edward", "Jones", "Engineering", 1)
        };

        Console.WriteLine("All Employees:");
        foreach (var emp in employees)
        {
            Console.WriteLine(emp);
        }

        Console.WriteLine("\n--- Engineering Department Employees with more than 3 years of service ---");

        // Use LINQ to find specific employees
        // Here, we're looking for engineers with more than 3 years of service
        var experiencedEngineers = employees
                                    .Where(emp => emp.Department == "Engineering" && emp.YearsOfService > 3)
                                    .ToList(); //ToList() is optional here if only iterating once

        if (experiencedEngineers.Any()) // Check if any such employees were found
        {
            foreach (var engineer in experiencedEngineers)
            {
                Console.WriteLine(engineer);
            }
        }
        else
        {
            Console.WriteLine("No employees found matching the criteria.");
        }

        Console.WriteLine("\n--- Names of all employees in Marketing ---");
        var marketingNames = employees
                                .Where(emp => emp.Department == "Marketing")
                                .Select(emp => $"{emp.FirstName} {emp.LastName}"); // Select just their names

        foreach(var name in marketingNames)
        {
            Console.WriteLine(name);
        }
    }
}