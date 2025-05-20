# Your MCP Coding Master

![alt text](image.png)


Your Coding Master MCP Server that
- debugs
- codes
- helps you with code-related error!

# Available Tools

| Tool Name  | Category |
| ------------- | ------------- |
| `list_codes`  | Common  |
| `run_code`  | Debugging  |

# Debugging

## Example usage

#### Output of 'EmployeeDirectory.cs' should be:

```All Employees:
ID: 101, Name: Alice Smith, Department: Engineering, Service Years: 5
ID: 102, Name: Bob Johnson, Department: Marketing, Service Years: 2
ID: 103, Name: Charlie Williams, Department: Engineering, Service Years: 8
ID: 104, Name: Diana Brown, Department: HR, Service Years: 3
ID: 105, Name: Edward Jones, Department: Engineering, Service Years: 1

--- Engineering Department Employees with more than 3 years of service ---
ID: 101, Name: Alice Smith, Department: Engineering, Service Years: 5
ID: 103, Name: Charlie Williams, Department: Engineering, Service Years: 8

--- Names of all employees in Marketing ---
Bob Johnson
```




#### Output of 'SimpleAPIClient.cs' should be:



```Attempting to fetch data from: https://jsonplaceholder.typicode.com/todos/1
--- API Response ---
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
--- End of Response ---

Successfully fetched and displayed data.

API call attempt finished.
```


(If there's a network issue (e.g., no internet connection) or the API is down, the output will show an error message from the catch block, for example:)

```Attempting to fetch data from: https://jsonplaceholder.typicode.com/todos/1

--- Error ---
Request error: No such host is known. (jsonplaceholder.typicode.com:443) // (Error message might vary)

API call attempt finished.
```