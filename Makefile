##############################################################################
##############################################################################

.SUFFIXES:

##############################################################################

CC=g++
LINK=g++

# Where are includes and libraries?
INCPATH=/usr/local/include
LIBPATH=/usr/local/lib

##############################################################################

# debug
CFLAGS = -I $(INCPATH) -I .. -DDRAWSTUFF_TEXTURE_PATH="\"textures\"" -g -O2 -fPIC

# dropped flags
# -MT demo-crash.o  -MD -MP -MF .deps/demo-crash.Tpo

##############################################################################

LIBS = -L /usr/local/lib -lode -ldrawstuff -lpthread -framework GLUT -framework OpenGL -lm
# Alternate locations for X11 libraries
# -L/usr/X11R6/lib -L/usr/X11/lib -L/usr/lib/X11R6

##############################################################################

all: blocks
	@echo SUCCESS

blocks.o: blocks.cpp blocks.h

blocks: blocks.o
	$(LINK) -o blocks blocks.o $(LIBS)

##############################################################################

%.o: %.cpp
	$(CC) $(CFLAGS) -c $<

##############################################################################
