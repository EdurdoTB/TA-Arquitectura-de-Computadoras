#include<string.h>
// Funcion que recibe las areas amarillas y negras y retorna el porcentaje de color amarillo que presenta el plátano.
float registro_area(float area_A, float area_N){


    float area_Total, porcentaje_area_A, porcentaje_area_N;


        area_Total= area_A+area_N;
        porcentaje_area_A=(area_A*100)/area_Total;
        porcentaje_area_N=(area_N*100)/area_Total;  

    return porcentaje_area_A;
}

// Funcion que recibe como argumentos dos nombres y retorna "1" en caso dichos nombres contengan las mismas letras sin imoprtar si presentan mayusculas o minusculas.
// En caso contrario retornará "0".
int validar(char nombre[30],char nombre2[30]){

	char mayusculas2[30],mayusculas[30];
	int validacion;
	int tamano;
	int i=0 , cont=0;

	tamano = strlen(nombre);
	while (i<tamano){
		
		if(nombre[i] == nombre2[i]){
			cont++;
		}
		else if(nombre[i]==nombre2[i]+32){
			cont++;
		}
		i++;
		
	}
	if(cont==tamano){
		validacion=1;
	}
	else{
		validacion=0;
	}
	return validacion;
	
}




