#define sint8 signed char
#include <math.h>
#include <stdio.h>

int audio2iq(double *au,int len,double band,sint8 *iq,int iqOffset,sint8 max,int times)
{
	int i,j,pos;
	static double angle=0;
	iq+=iqOffset;
	pos=0;
	for(j=0;j<len;j++)
	{
		for(i=0;i<times;i++)
		{
			angle+=(au[j]*band);
			iq[pos++]=max*cos(angle);
			iq[pos++]=max*sin(angle);
		}
	}
	//printf("len add %d\n",pos);
	return pos/2;
}
