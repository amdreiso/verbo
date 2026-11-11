
#define TB_IMPL
#include "termbox2.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include "verbo.h"

const char *TITLE = "verbo";
bool running = true;
ePage page = HOME;

Tokens tokens = {0};
Token current_token = { "Eisenfaust", "Iron fist" };
bool token_revealed = false;

void filesystem();
void handle_event(struct tb_event *event);
void render();
void token_render(Token *token);
void open_book(const char *filename);

int main(int argc, char** argv)
{
	filesystem();

	struct tb_event e;
	tb_init();

	open_book("deutsch");

	while (running) {
		tb_clear();
		render();

		tb_present();
		tb_poll_event(&e);
		handle_event(&e);
	}

	tb_shutdown();
	return 0;
}

void open_book(const char *filename)
{
	char path[256];
	char line[256];

	snprintf(path, sizeof(path), "%s/.config/verbo/books/%s", getenv("HOME"), filename);

	FILE *f = fopen(path, "r");

	if (f != NULL) {
		tb_printf(0, 0, 0, 0, "Opened book '%s'", filename);
		int y = 4;

		while (fgets(line, sizeof(line), f)) {
			char *tkn;
			char *left, *right;

			tkn = strtok(line, ",");

			while (tkn != NULL) {
				if (left == 0) {
					left = tkn;
				} else {
					right = tkn;
				}
				tkn = strtok(NULL, ",");
			}

			tb_printf(tb_width()/2, y++, 0, 0, "%s : %s", left, right);

			if (tokens.count >= tokens.capacity) {
				if (tokens.capacity == 0) tokens.capacity = 256;
				else tokens.capacity *= 2;

				tokens.items = realloc(tokens.items, tokens.capacity * sizeof(*tokens.items));
			}

			Token t = {0};
			strcpy(t.native, left);
			strcpy(t.translation, right);

			tokens.items[tokens.count++] = t;
		}
		fclose(f);
	} else {
		running = false;
		tb_shutdown();
		printf("Could not open book '%s'\npath: '%s'", filename, path);
	}
}

void filesystem()
{
	char config[256];
	char books[256];

	snprintf(config, sizeof(config), "%s/.config/verbo", getenv("HOME"));
	mkdir(config, 0700);

	snprintf(books, sizeof(books), "%s/books", config);
	mkdir(books, 0700);
}

void render()
{
	char *bookname = "deutsch";
	tb_print(tb_width()/2 - strlen(TITLE)/2, 1, 0, 0, TITLE);

	switch (page) {
		case HOME:
			break;

		case BOOK:
			tb_print(tb_width()/2 - strlen(bookname)/2, 3, TB_BLUE, 0, bookname);
			token_render(&current_token);
			break;
	}
}

void token_render(Token *token)
{
	char str[256];
	char *t = (token_revealed) ? token->translation : "???";
	snprintf(str, sizeof(str), "%s : %s", token->native, t);

	tb_print(tb_width()/2 - strlen(str)/2, tb_height()/2, 0, 0, str);
}

void handle_event(struct tb_event *e)
{
	switch (e->key) {
		case 3:
			running = false;
			break;
	}

	switch (e->ch) {
		case 'r':
			token_revealed = true;
			break;

		case 'g':
			int index = rand() % tokens.count;
			Token t = tokens.items[index];
			tb_printf(0, 10, 0, 0, "index: %d native: %s translation: %s", index, t.native, t.translation);
			break;
	}
}

