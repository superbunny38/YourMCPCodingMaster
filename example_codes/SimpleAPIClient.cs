// Filename: SimpleApiClient.cs
using System;
using System.Net.Http; // Required for HttpClient
using System.Threading.Tasks; // Required for Task and async/await

public class SimpleApiClient
{
    // HttpClient is intended to be instantiated once and reused throughout the life of an application.
    // Instantiating an HttpClient class for every request will exhaust the number of sockets available under heavy loads.
    private static readonly HttpClient client = new HttpClient();

    // Main method needs to be async to use await directly, or use .GetAwaiter().GetResult()
    public static async Task Main(string[] args)
    {
        // Define the URL for the API endpoint
        string apiUrl = "https://jsonplaceholder.typicode.com/todos/1"; // Fetches the first todo item

        Console.WriteLine($"Attempting to fetch data from: {apiUrl}");

        try
        {
            // Make an asynchronous GET request
            HttpResponseMessage response = await client.GetAsync(apiUrl);

            // Ensure the request was successful
            response.EnsureSuccessStatusCode(); // Throws an exception if the HTTP response status is an error code

            // Read the response content as a string asynchronously
            string responseBody = await response.Content.ReadAsStringAsync();

            Console.WriteLine("\n--- API Response ---");
            Console.WriteLine(responseBody);

            // In a real application, you would typically deserialize this JSON string into a C# object.
            // For example, using System.Text.Json.JsonSerializer or Newtonsoft.Json.
            // For simplicity, we are just printing the raw string.

            Console.WriteLine("\n--- End of Response ---");
            Console.WriteLine("\nSuccessfully fetched and displayed data.");
        }
        catch (HttpRequestException e)
        {
            Console.WriteLine("\n--- Error ---");
            Console.WriteLine($"Request error: {e.Message}");
            if (e.StatusCode.HasValue)
            {
                Console.WriteLine($"Status code: {e.StatusCode.Value}");
            }
        }
        catch (Exception ex) // Catch any other potential errors
        {
            Console.WriteLine("\n--- An unexpected error occurred ---");
            Console.WriteLine($"Error: {ex.Message}");
        }
        finally
        {
            Console.WriteLine("\nAPI call attempt finished.");
        }
    }
}