
;unsigned long long prueba( m, n, x[])
;argumentos que entran
;float
;xmm0       m
;xmm1       n

;rdi        x[]

section .text
    global _Area

_Area:
    xorpd xmm2, xmm2
    xorpd xmm3, xmm3

    mov r9, 100         ; Guardo el valor 100 en r9
    
    movss xmm2, xmm0    ; En el xmm2 guardo el valor de xmm0

    addss xmm0, xmm1    ; se almacena en xmm0 la suma 
                        ; Ahora xmm0 es Area_Total

    mulss xmm2, xmm0    ; multitplico los valores
    mulss xmm1, xmm0

    cvtsi2sd xmm3, [r9]  ; int 100 a double en xmm3

    divss xmm2, xmm3     ; divido los valores
    divss xmm1, xmm3

    ;Ahora los almaceno en la lista
_next:
    movss [rdi], xmm2   ; Guardo porcentaje_area_A en x[0]
    add    rdi, 4       ; Voy al siguiente elemento
    movss [rdi], xmm1   ; Guardo porcentaje_area_N en x[1]


_done_:
    ret

