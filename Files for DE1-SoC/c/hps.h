#ifndef HPS_H_
#define HPS_H_
#include "stdint.h"
#include "stdbool.h"
bool HPSLedSet(bool bOn);
bool IsButtonPressed();
bool GsensorQuery(int16_t *X, int16_t *Y, int16_t *Z);
int m_file_mem;
void *m_virtual_base;
bool PioInit();
// gsensor
int m_file_gsensor;
int GsensorInit();
#endif /*HPS_H_*/
