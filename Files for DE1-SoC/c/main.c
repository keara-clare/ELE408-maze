#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <time.h>
#include <sys/mman.h>
#include "hwlib.h"
#include "soc_cv_av/socal/socal.h"
#include "soc_cv_av/socal/hps.h"
#include "soc_cv_av/socal/alt_gpio.h"
#include "hps_0.h"
#include <stdbool.h>
#include "fpga.h"
#include "hps.h"
#include "ADLX345.h"

#define HW_REGS_BASE ( ALT_STM_OFST )
#define HW_REGS_SPAN ( 0x04000000 )
#define HW_REGS_MASK ( HW_REGS_SPAN - 1 )

int Level1 = 1;		//all the way left
int Level2 = 3;
int Level3 = 2;
int Level4 = 6;
int Level5 = 4;
int Level6 = 12;
int Level7 = 8;
int Level8 = 24;
int Level9 = 16;
int Level10 = 48;	//balenced
int Level11 = 32;
int Level12 = 96;
int Level13 = 64;
int Level14 = 192;
int Level15 = 128;
int Level16 = 384;
int Level17 = 256;
int Level18 = 768;
int Level19 = 512;	//all the way right

uint8_t setLevel[] = {
   1, 3, 2, 6, 4, 12, 8, 24, 16, 48, 32, 
   96, 64, 192, 128, 384, 256, 768, 512
};

int level=0;


void cssStuff();
void hexsetdec(long value);
void htmlHeaders();
void htmlFooters();
void toggles(uint32_t switchMask);
void showOneToggle(int index, int state);
void turnedLeft(int value);
void turnedRight(int value);
int main(int argc, char *argv[])
{
	
	if(!FPGAInit()){
		printf("can't initialize fpga");
		return 0;
	}
	htmlHeaders();
/*
	int16_t X,Y,Z;
	m_file_gsensor = GsensorInit();
	bool m_bGSensorDataValid = false;
	m_bGSensorDataValid = GsensorQuery(&X,&Y,&Z);
	if(m_bGSensorDataValid){
		printf("X = %d    Y = %d    Z = %d\r\n", X, Y, Z);
	}
*/
	int16_t X,Y,Z;
	m_file_gsensor = GsensorInit();
	bool m_bGSensorDataValid = false;
	uint32_t switchMask;

	// add bubble level code
//while(1){

		m_bGSensorDataValid = GsensorQuery(&X,&Y,&Z);
		if(m_bGSensorDataValid){
			//printf("X = %d    Y = %d    Z = %d\r\n", X, Y, Z);
		}
		SwitchRead(&switchMask);
		// add your code here

		int currentX = X;
		//printf("X = %d   \n", X);
		if(X > -57 && X < 52){
			level = 9;
			FPGALedSet(setLevel[level]);
			toggles(setLevel[level]);
		}
		else if(X>52){
			turnedRight(X);
			HexSet(0,1);
		}
		else{
			turnedLeft(X);
			HexSet(0,2);
		}						
		usleep(500*1000);
	//}
	htmlFooters();
	return 1;
}
void cssStuff(){
	puts("<style>");
	puts(".switch {");
	puts("  position: relative;");
	puts("  display: inline-block;");
	puts("  width: 34px;");
	puts("  height: 60px;");
	puts("}");
	puts(".switch input {display:none;}");
	puts(".slider {");
	puts("  position: absolute;");
	puts("  cursor: pointer;");
	puts("  top: 0;");
	puts("  left: 0;");
	puts("  right: 0;");
	puts("  bottom: 0;");
	puts("  background-color: #ccc;");
	puts("  -webkit-transition: .4s;");
	puts("  transition: .4s;");
	puts("}");
	puts(".slider:before {");
	puts("  position: absolute;");
	puts("  content: \"\";");
	puts("  height: 26px;");
	puts("  width: 26px;");
	puts("  left: 4px;");
	puts("  bottom: 4px;");
	puts("  background-color: white;");
	puts("  -webkit-transition: .4s;");
	puts("  transition: .4s;");
	puts("}");
	puts("input:checked + .slider {");
	puts("  background-color: #FF0000;");
	puts("}");
	puts("input:focus + .slider {");
	puts("  box-shadow: 0 0 1px #FF0000;");
	puts("}");
	puts("input:checked + .slider:before {");
	puts("  -webkit-transform: translateY(-26px);");
	puts("  -ms-transform: translateY(-26px);");
	puts("  transform: translateY(-26px);");
	puts("}");
	puts("</style>");
}
void htmlHeaders(){
	// puts("Content-type: text/html\n");
	puts("<!DOCTYPE html>");
	puts("<head>");
	cssStuff();
	puts("<meta http-equiv=\"refresh\" content=\"1\"");
	puts("<meta charset=\"utf-8\" >");
	puts("<title>SevenSeg Display</title>");
	puts("</head>");
	puts("<body>");
}
void htmlFooters(){
	puts("</body>");
	puts("</html");
}
void toggles(uint32_t switchMask){
	int i;
	for(i=0;i<10;i++){
		showOneToggle(9-i,switchMask&(1<<(9-i)));
	}
}
void showOneToggle(int index, int state){
	puts("<label class=\"switch\">");
	printf("<input type=\"checkbox\" name=\"LED%d\"", index);
	if(state) printf(" checked");
	printf(">\n");
	puts("<div class=\"slider\"></div>");
	puts("</label>");
}
void hexsetdec(long value){
	int i;
	for(i=0; i<6; i++){
		HexSet(i,value%10);
		value /= 10;
	}
}

void turnedRight(int value){
//levels 10 -19
	
	//HexSet(0,1);
	level = 9;
	if(value> 945){
		FPGALedSet(512);
		toggles(512);
		return;
	}
	if(value> 835){
		FPGALedSet(768);
		toggles(768);
		return;
	}
	while(value>0){
		value = value-110;
		if(level<=19){
		level ++;
		//printf("val %d \n", value);
		}
	//printf("level %d \n", level);
	
	}
FPGALedSet(setLevel[level+1]);
	toggles(setLevel[level+1]);
	//FPGALedSet(setLevel[level]);
	
}
void turnedLeft(int value){
//levels 0-8
	level = 10;
	while(value<0){
		value = value + 110;
		level--;
		//printf("level %d \n", level);
//printf("val %d \n", value);
	}

	FPGALedSet(setLevel[level]);
	toggles(setLevel[level]);
}
	//FPGALedSet(setLevel[level]);




















