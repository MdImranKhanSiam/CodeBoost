{
    'stdout': 'Enter two numbers: Sum = 8\n', 
    'time': '0.003', 
    'memory': 1176, 
    'stderr': None, 
    'token': 'af953df9-73ed-4162-a5a2-be4b195b91dd', 
    'compile_output': None, 
    'message': None, 
    'status': {
        'id': 3, 
        'description': 'Accepted'
        }}



#include <iostream>
using namespace std;

int main() {
    long long A, B;
    cin >> A >> B;

    cout << A + B << endl;

    return 0;
}






#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    string name;
    int math, physics, chemistry;

    // Read full name (including spaces)
    getline(cin, name);

    // Read marks
    cin >> math >> physics >> chemistry;

    int total = math + physics + chemistry;
    double average = total / 3.0;

    char grade;

    if (average >= 80) grade = 'A';
    else if (average >= 60) grade = 'B';
    else if (average >= 40) grade = 'C';
    else grade = 'F';

    // Output formatting
    cout << "Name: " << name << "\n";
    cout << "Total: " << total << "\n";
    cout << "Average: " << fixed << setprecision(2) << average << "\n";
    cout << "Grade: " << grade;

    return 0;
}








On line 54 in submission.html
<strong>Output:</strong> <pre>${sub.stdout || '-'}</pre>