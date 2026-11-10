
CC = gcc
TARGET = verbo
OBJ = main.c
CLIBS = -Wall -w

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET) $(CLIBS)

