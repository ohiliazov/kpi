#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#define ADD "+"

void push(double *, double);
void pop(double *, double);
void validate(int, char*[]);

void parse_argument(char* item) {
	char* tail;
	double d = strtod(item, &tail);
	
	if (strtok(tail," \t")!=NULL)
		printf("Operator: %s\n", tail);
	else
		printf("Number: %f\n", d);
	if (strcmp(tail, ADD) == 0)
		printf("Addition sign");
}


void validate(int n, char* argv[]) {
	printf("Given RPN equation: ");
	for(int i=1; i<n; i++) {
		parse_argument(argv[i]);
	}
}

int main(int argc, char* argv[]) {
	if (argc == 1) {
		printf("No equation provided.");
		exit(1);
	}
	double f;

	validate(argc, argv);
	return 0;
}
