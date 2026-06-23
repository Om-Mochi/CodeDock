// Single line comment - should be pink (#CF3E88)
/* Multi-line comment
   This should also be green(#C3E88D)
   Testing multiple lines */

#include <iostream>
#include <iostream>     
#include <vector>
#include <string>
#include <memory>
#define MAX_SIZE 100   
#define PI 3.14159
#include <streambuf>
#include <stab.h>
#include <memory.h>
#include <arm_mve.h>
// Namespace usage - blue (#82AAFF)    
using namespace std;
// Class definition with various features
class MyClass {        // 'class' keyword red-ish (#597669), 'MyClass' blue (#82AAFF)

private:               // Keywords - red-ish (#597669)
    int member_var;    // Type 'int' - blue (#82AAFF)
    string name;       // Type 'string' - blue (#82AAFF)
    
public:
    // Constructor - function definition should be green (#C3E88D)
    MyClass(const string& n) : name(n), member_var(0) {
        // 'const', 'string' are types/keywords
        cout << "Constructor called" << endl;  // Strings - dark green (#40974e)
    }
     
    // Method definition - green (#C3E88D)
    virtual void display() const noexcept {
        // Keywords: virtual, void, const, noexcept - red-ish (#597669)
        cout << "Name: " << name << ", Value: " << member_var << endl;
    }
    unsi
    // Operator overloading
    bool operator==(const MyClass& other) const {
        return this->name == other.name;  // 'this' - yellow (#FFCB6B)
    }
    
    // Template method
    template<typename T>
    T getValue(T default_val) {
        return static_cast<T>(member_var);
    }
};

// Template class
template<class T>
class Container {
public:
    vector<T> items;   // Template usage
    
    void addItem(T item) {
        items.push_back(item);  // Method call - red-ish (#FF5370)
    }
    
    size_t getSize() const {
        return items.size();    // Method call - red-ish (#FF5370)
    }
};

// Namespace definition
namespace MyNamespace {     // 'MyNamespace' - blue (#82AAFF)
    const int CONSTANT_VALUE = 42;  // Constants - yellow (#FFCB6B)
    
    enum class Status {     // 'enum', 'class' - red-ish (#597669)
        ACTIVE,            // Constants - yellow (#FFCB6B)
        INACTIVE,
        PENDING
    };
    Status iss Status;
    
    // Function definition - green (#C3E88D)
    double calculateArea(double radius) {
        return PI * radius * radius;  // Numbers and operators
    }
}

// Global function with various number types
void testNumbers() {
    // Different number formats - all purple (#C792EA)
    int decimal = 123;
    float floating = 123.45f;
    double scientific = 1.23e-4;
    unsigned long hex = 0xFF00AA;
    auto binary = 0b11010101;
    float
    // Character literals - dark green (#40974e)
    char ch = 'A';
    char escape = '\n';
    char unicode = '\u0041';
    
    // String literals - dark green (#40974e)
    string simple = "Hello World";
    string escaped = "Line 1\nLine 2\tTabbed";
    string raw = R"(Raw string with "quotes" and \backslashes)";
}

// Function with complex syntax
template<typename T, typename U = int>
auto complexFunction(T&& param, const vector<U>& vec) -> decltype(param + vec[0]) {
    // Auto, template keywords, arrow syntax, decltype
    
    // Lambda expression
    auto lambda = [&](const T& x) -> bool {
        return x > static_cast<T>(0);
    };
    
    // STL containers and smart pointers
    unique_ptr<MyClass> ptr = make_unique<MyClass>("Test");
    shared_ptr<int> shared = make_shared<int>(42);
    weak_ptr<int> weak = shared;
    
    // Container operations
    vector<int> numbers{1, 2, 3, 4, 5};     // Brackets - magenta (#8c518e)
    map<string, int> lookup;
    pair<int, string> keyValue{1, "One"};
    
    // Control flow with operators
    for(auto& num : numbers) {              // Operators - dark (#333333)
        if(num >= 0 && num <= 100) {        // Comparison operators
            cout << num << " ";             // Stream operators
        }
    }
    
    // Exception handling
    try {
        throw runtime_error("Test exception");
    } catch(const exception& e) {
        cout << "Caught: " << e.what() << endl;
    }
    
    return param + static_cast<decltype(param)>(vec.front());
}

// Main function
int main() {                               // Function definition - green (#C3E88D)
    // Object creation and method calls
    MyClass obj("TestObject");             // Function call - light blue (#89DDFF)
    obj.display();                         // Method call - red-ish (#FF5370)
    
    // Namespace usage
    MyNamespace::Status status = MyNamespace::Status::ACTIVE;
    double area = MyNamespace::calculateArea(5.0);    // Namespace - blue (#82AAFF)
    
    // Container usage
    Container<string> stringContainer;
    stringContainer.addItem("Hello");      // Method calls - red-ish (#FF5370)
    stringContainer.addItem("World");
    
    // Pointer operations
    int* ptr = new int(10);                // Operators - dark (#333333)
    int& ref = *ptr;                       // Reference and dereference
    delete ptr;                            // Memory management
    ptr = nullptr;                         // Null pointer
    
    // Array and bracket usage
    int array[10] = {0};                   // Brackets - magenta (#8c518e)
    array[0] = 100;                        // Array access
    
    // Conditional and loops
    while(true) {                          // Keywords and brackets
        if(ref > 5) {
            break;
        } else {
            continue;
        }
    }
    
    // Switch statement
    switch(ref) {
        case 1:
            cout << "One" << endl;
            break;
        default:
            cout << "Other" << endl;
            break;
    }
    
    return 0;                              // Return statement
}
#include<
/* Final multi-line comment
   This file tests all syntax highlighting categories:
   
   Colors tested:
   - Keywords: #597669 (red-ish)
   - Types: #82AAFF (blue) 
   - Classes: #82AAFF (blue)
   - Function calls: #89DDFF (light blue)
   - Function definitions: #C3E88D (green)
   - Strings: #40974e (dark green)
   - Comments: #C3E88D (green)
   - Numbers: #C792EA (purple)
   - Constants: #FFCB6B (yellow)
   - Brackets: #8c518e (magenta)
   - Preprocessor: #FFCB6B (yellow)
   - Namespaces: #82AAFF (blue)
   - Methods: #FF5370 (red-ish)
   - Operators: #333333 (dark)
   - Default text: #8fa0b0 (light gray)
*/