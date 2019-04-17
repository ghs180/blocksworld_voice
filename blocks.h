// Defines

// object types
#define GROUND 0 // a solid floor
#define BLOCK 1 // a block
#define BALL 2 // a ball
#define UNKNOWN -1

// data structure sizes
#define MAX_N_BALLS 100
#define MAX_N_BLOCKS 100

/****************************************************************/
/****************************************************************/
// Typedefs
// todo: make mass and geometry slightly vary

typedef struct object_init
{
  int created;
  float time; // what time to create this object
  float mass; // todo: make mass slightly vary
  float dimensions[3]; // todo: make geometry slightly vary
  float xyz[3]; // location in meters
  float rpy[3]; // roll pitch yaw in radians
  float rgb[3]; // color
}
  OBJECT_INIT;

/****************************************************************/

typedef struct sim
{
  // setup variables
  int window_width;  // pixels
  int window_height;
  float xyz[3]; // viewpoint
  float hpr[3];
  float duration;  // seconds
  float time_step; // seconds
  // block sizes and masses
  float block_length; // X direction in block coordinates
  float block_width; // Y direction in block coordinates
  float block_height; // Z direction in block coordinates
  float block_mass;
  // ball sizes and masses
  float ball_radius;
  float ball_mass;

  // states
  dReal time; // what time is it?
  dReal last_time; // handy variable.
  bool printed_everything; // have we done a data dump?

  dGeomID ground;

  int n_balls;
  OBJECT_INIT balls_init[MAX_N_BALLS];
  dBodyID balls_body[MAX_N_BALLS];
  dGeomID balls_geom[MAX_N_BALLS];

  int n_blocks;
  OBJECT_INIT blocks_init[MAX_N_BLOCKS];
  dBodyID blocks_body[MAX_N_BLOCKS];
  dGeomID blocks_geom[MAX_N_BLOCKS];
}
  SIM;

/****************************************************************/

/****************************************************************/

/****************************************************************/
