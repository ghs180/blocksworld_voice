/****************************************************************/

#ifdef _MSC_VER
#include "texturepath.h"
// for VC++, no precision loss complaints
#pragma warning(disable:4244 4305)  
#endif

/****************************************************************/
// select correct drawing functions (if using double version)

#ifdef dDOUBLE
#define dsDrawBox dsDrawBoxD
#define dsDrawSphere dsDrawSphereD
#endif

/****************************************************************/
