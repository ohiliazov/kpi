#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#define ADD "+"

struct Stack 
{ 
    int top; 
    unsigned capacity; 
    double* array; 
};

struct Stack* createStack(unsigned capacity) { 
    struct Stack* stack = (struct Stack*) malloc(sizeof(struct Stack)); 
    stack->capacity = capacity; 
    stack->top = -1; 
    stack->array = (double*) malloc(stack->capacity * sizeof(double)); 
    return stack; 
}

void push(struct Stack* stack, int item) { 
    stack->array[++stack->top] = item;
	printf("%d pushed to stack\n", item); 
}

double pop(struct Stack* stack) 
{
    return stack->array[stack->top--]; 
}

void calculate(struct Stack* stack, char* operator) {
	double y = pop(stack);
	double x = pop(stack);
	
	if (operator == ADD) {
		push(stack, x+y);
	}
}

void execute_rpn(struct Stack* stack, int n, char *argv[])
{
	char *tail;
	double number;

	printf("Given RPN equation: ");
	for (int i = 1; i < n; i++)
	{
		number = strtod(argv[i], &tail);
		printf("%s\n", tail);
		if (strtok(tail, " \t") == NULL) {
			push(stack, number);
		}
		else {
			calculate(stack, tail);
		}
	}
}

int main(int argc, char *argv[])
{
	if (argc == 1) {
		printf("No equation provided.");
		exit(1);
	}

	struct Stack* stack = createStack(argc-1);
	execute_rpn(stack, argc, argv);
	return 0;
}
