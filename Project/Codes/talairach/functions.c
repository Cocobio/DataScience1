#include "stdio.h"
#include "math.h"
#include "string.h"
#include "stdlib.h"

void vec3MultiplyBy4x4Matrix(float *vec3, float *mat4, float *tmpPlaceHolder) {
	tmpPlaceHolder[0] = vec3[0]*mat4[0] + vec3[1]*mat4[1] + vec3[2]*mat4[2] + mat4[3];
	tmpPlaceHolder[1] = vec3[0]*mat4[4] + vec3[1]*mat4[5] + vec3[2]*mat4[6] + mat4[7];
	tmpPlaceHolder[2] = vec3[0]*mat4[8] + vec3[1]*mat4[9] + vec3[2]*mat4[10] + mat4[11];

	for(int i=0; i<3; i++)
		vec3[i] = tmpPlaceHolder[i];
}

void applyMatrix(
		void *pyPoints,
		int pointsSize,
		void *pyMatrix) {

	float *points = (float*) pyPoints;
	float *matrix = (float*) pyMatrix;

	float tmp[3];

	for (unsigned i=0; i<pointsSize; i+=3)
		vec3MultiplyBy4x4Matrix(points+i, matrix, tmp);
}

void readBundleFile(
		char *filePath,
		void *pyPoints,
		void *pyFiberSize,
		int curvesCount) {

	float *points = (float*) pyPoints;
	int *fibersize = (int*) pyFiberSize;

	FILE *fp;
	fp = fopen(filePath, "rb");

	for(int i=0; i<curvesCount; i++) {
		fread(fibersize+i,sizeof(int),1,fp);
		fread(points,sizeof(float),fibersize[i]*3,fp);

		points += fibersize[i]*3;
	}

	fclose(fp);
}

void saveBundlesData(
		char *outFilePath,
		void *pyPoints,
		void *pyFiberSize,
		int curvesCount) {

	float *points = (float*) pyPoints;
	int *fibersize = (int*) pyFiberSize;

	FILE *fp;
	fp = fopen(outFilePath, "wb");

	for (int i=0; i<curvesCount; i++) {
		fwrite(fibersize+i,sizeof(int),1,fp);
		fwrite(points,sizeof(float),fibersize[i]*3,fp);
		points += fibersize[i]*3;
	}

	fclose(fp);
}