CXXFLAGS = -std=gnu++17 -Wall -pthread -lrt

# check if DEBUG=1 is set on the command line
ifeq ($(DEBUG),1)
  CXXFLAGS := $(CXXFLAGS) -O0 -g
else
  CXXFLAGS := $(CXXFLAGS) -O3 -march=native -flto
endif

CXX = g++

mybot: competitor.o
	$(CXX) -o mybot kirin.o competitor.o $(CXXFLAGS)

competitor.o: competitor.cpp
	$(CXX) competitor.cpp $(CXXFLAGS) -c

clean:
	rm -f competitor.o mybot
