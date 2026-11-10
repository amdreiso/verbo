
#ifndef VERBO_H
#define VERBO_H

typedef struct {
	char native[256];
	char translation[256];
	bool revealed;
} Token;

typedef struct {
	Token *items;
	size_t count;
	size_t capacity;
} Tokens;

typedef enum {
	HOME,
	BOOK
} ePage;

#endif

