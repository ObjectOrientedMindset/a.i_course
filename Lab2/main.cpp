#include <iostream>

// 152120161061 Mithat Uçar
// 152117107_2223G_Lab2 Artificial Intelligence

using namespace std;

#define MAX 1000

// Stack implementation

class Stack
{
    int last;

public:
    int a[MAX]; // Maximum size of Stack

    Stack() { last = -1; }
    bool push(int x);
    int pop();
    int top();
    void list();
    void reverse_list();
    void sort(Stack &input);
    bool isEmpty();
};

bool Stack::push(int x)
{
    if (last >= (MAX - 1))
    {
        cout << "increase the stack size";
        return false;
    }
    else
    {
        a[++last] = x;
        return true;
    }
}

int Stack::pop()
{
    if (last < 0)
    {
        cout << "Stack Underflow";
        return 0;
    }
    else
    {
        int x = a[last--];
        return x;
    }
}
int Stack::top()
{
    if (last < 0)
    {
        cout << "Stack is Empty";
        return 0;
    }
    else
    {
        int x = a[last];
        return x;
    }
}

bool Stack::isEmpty()
{
    return (last < 0);
}

void Stack::list()
{

    // print all elements in stack :
    cout << "list of the stack : " << endl;
    for (int x = last; x >= 0; x--)
    {
        cout << a[x] << endl;
    }
}

void Stack::reverse_list()
{
    // print all elements reverse order in stack :
    cout << "reverse list of the stack : " << endl;
    for (int x = 0; x <= last; x++)
    {
        cout << a[x] << endl;
    }
}

void Stack::sort(Stack &input)
{
    Stack tmpStack;

    while (!input.isEmpty())
    {
        // pop out the first element
        int tmp = input.top();
        input.pop();

        // while temporary stack is not empty and top
        // of stack is greater than temp
        while (!tmpStack.isEmpty() && tmpStack.top() > tmp)
        {
            // pop from temporary stack and push
            // it to the input stack
            input.push(tmpStack.top());
            tmpStack.pop();
        }

        // push temp in temporary of stack
        tmpStack.push(tmp);
    }
    cout << "Sorted numbers are:\n";

    while (!tmpStack.isEmpty())
    {
        cout << tmpStack.top() << endl;
        tmpStack.pop();
    }
}

// Queue implementation

class Queue
{
    int *arr;     // array to store queue elements
    int capacity; // maximum capacity of the queue
    int front;    // front points to the front element in the queue (if any)
    int rear;     // rear points to the last element in the queue
    int count;    // current size of the queue

public:
    Queue(int size = MAX);
    ~Queue();

    int dequeue();
    void enqueue(int x);
    int peek();
    int size();
    void list();
    void reverse_list();
    void sort(Queue &input);
    bool isEmpty();
    bool isFull();
};

Queue::Queue(int size)
{
    arr = new int[size];
    capacity = size;
    front = 0;
    rear = -1;
    count = 0;
}

Queue::~Queue()
{
    delete[] arr;
}

int Queue::dequeue()
{
    // check for queue underflow
    if (isEmpty())
    {
        cout << "Underflow\nProgram Terminated\n";
        exit(EXIT_FAILURE);
    }

    int x = arr[front];

    front = (front + 1) % capacity;
    count--;

    return x;
}

void Queue::enqueue(int item)
{
    // check for queue overflow
    if (isFull())
    {
        cout << "Overflow\nProgram Terminated\n";
        exit(EXIT_FAILURE);
    }

    rear = (rear + 1) % capacity;
    arr[rear] = item;
    count++;
}

int Queue::peek()
{
    if (isEmpty())
    {
        cout << "Underflow\nProgram Terminated\n";
        exit(EXIT_FAILURE);
    }
    return arr[front];
}

int Queue::size()
{
    return count;
}

bool Queue::isEmpty()
{
    return (size() == 0);
}

bool Queue::isFull()
{
    return (size() == capacity);
}

void Queue::list()
{

    // print all elements in queue :
    cout << "list of the queue : " << endl;
    for (int x = count - 1; x >= 0; x--)
    {
        cout << arr[x] << endl;
    }
}

void Queue::reverse_list()
{
    // print all elements reverse order in queue :
    cout << "reverse list of the queue : " << endl;
    for (int x = 0; x <= count - 1; x++)
    {
        cout << arr[x] << endl;
    }
}

void Queue::sort(Queue &input)
{
    Queue tmpStack;

    while (!input.isEmpty())
    {
        // pop out the first element
        int tmp = input.peek();
        input.dequeue();

        // while temporary stack is not empty and top
        // of stack is greater than temp
        while (!tmpStack.isEmpty() && tmpStack.peek() > tmp)
        {
            // pop from temporary stack and push
            // it to the input stack
            input.enqueue(tmpStack.peek());
            tmpStack.dequeue();
        }

        // push temp in temporary of stack
        tmpStack.enqueue(tmp);
    }
    cout << "Sorted numbers are:\n";

    while (!tmpStack.isEmpty())
    {
        cout << tmpStack.peek() << endl;
        tmpStack.dequeue();
    }
}

int main()
{
    // Stack Demonstration
    cout << "Stack Demonstration" << endl;

    Stack s;
    s.push(5);
    s.push(3);
    s.push(4);
    s.push(7);
    s.push(9);
    s.push(10);
    s.push(1);
    s.push(2);
    s.push(8);
    s.push(6);
    s.push(11);

    s.pop();

    s.list();
    s.reverse_list();
    s.sort(s);

    // Queue Demonstration
    // create a queue of capacity 5
    cout << "Queue Demonstration" << endl;

    Queue q(1000);

    q.enqueue(5);
    q.enqueue(3);
    q.enqueue(4);
    q.enqueue(7);
    q.enqueue(9);
    q.enqueue(10);
    q.enqueue(1);
    q.enqueue(2);
    q.enqueue(8);
    q.enqueue(6);
    q.enqueue(11);

    q.dequeue();

    q.list();
    q.reverse_list();
    q.sort(q);

    return 0;
}
