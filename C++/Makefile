# Makefile para mi proyecto

CXX = g++
CXXFLAGS = -Wall -g

SOURCES = main.cpp modulo1.cpp modulo2.cpp
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = mi_programa

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
    $(CXX) $(OBJECTS) -o $@

%.o: %.cpp
    $(CXX) $(CXXFLAGS) -c $< -o $@

clean:
    rm -f $(OBJECTS) $(EXECUTABLE)
