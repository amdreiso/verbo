
#ifndef VERBO_H
#define VERBO_H

typedef struct {
	char native[256];
	char translation[256];
} Token;

typedef struct {
	Token *items;
	int count;
	int capacity;
} Tokens;

typedef enum {
	HOME,
	BOOK
} ePage;

#endif

