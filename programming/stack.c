// C program for array implementation of stack 
#include <stdio.h> 
#include <stdlib.h> 
#include <limits.h> 

// A structure to represent a stack 
struct Stack 
{ 
    int top; 
    unsigned capacity; 
    int* array; 
}; 
  
// function to create a stack of given capacity. It initializes size of 
// stack as 0 
struct Stack* createStack() 
{ 
    struct Stack* stack = (struct Stack*) malloc(sizeof(struct Stack)); 
    stack->capacity = 1; 
    stack->top = 0; 
    stack->array = (int*) malloc(stack->capacity * sizeof(int)); 
    return stack; 
} 
  
// Stack is full when top is equal to the last index 
int isFull(struct Stack* stack) 
{   return stack->top == stack->capacity; } 
    
// Stack is full when top is equal to the last index 
int isHalfFull(struct Stack* stack) 
{   return stack->top < stack->capacity/2; } 
  
// Stack is empty when top is equal to 0 
int isEmpty(struct Stack* stack) 
{   return stack->top == 0;  } 

// Function to resize stack capacity. It increases top by 1 
void resize(struct Stack* stack, int capacity) {
	int *new_data = (int*) malloc(capacity * sizeof(int));
	for (int i=0; i < stack->capacity, i < capacity; i++) {
		new_data[i] = stack->array[i];
	}
	free(stack->array);
    printf("Capacity changed: %d -> %d\n", stack->capacity, capacity); 
	stack->capacity = capacity;
	stack->array = new_data;
}

// Function to add an item to stack.  It increases top by 1 
void push(struct Stack* stack, int item) 
{ 
    if (isFull(stack)) {
    	printf("Stack is full.\n");
		resize(stack, stack->capacity * 2); 
	}
    stack->array[stack->top++] = item; 
    printf("%d pushed to stack\n", item); 
} 
  
// Function to remove an item from stack.  It decreases top by 1 
int pop(struct Stack* stack) 
{ 
    if (isEmpty(stack)) {
    	printf("Stack is empty.\n");
		return INT_MIN;
	}
    if (isHalfFull(stack)) resize(stack, stack->capacity/2);
    int item = stack->array[--stack->top];
    printf("%d popped from stack\n", item); 
    return item; 
}

int main() 
{ 
    struct Stack* stack = createStack(); 
  
    push(stack, 10); 
    push(stack, 20); 
    push(stack, 30); 
    pop(stack);

    return 0; 
} 
