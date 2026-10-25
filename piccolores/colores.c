#include <16F877A.h>
#fuses HS, NOWDT, NOPROTECT, NOLVP
#use delay(clock=20000000)
#use i2c(SLAVE, SDA=PIN_C4, SCL=PIN_C3, address=0x22, FORCE_HW)

#define LED_ROJO  PIN_B0
#define LED_VERDE PIN_B1  // Actualizado de "AMARILLO" a "VERDE"
#define LED_AZUL  PIN_B2

int8 r = 0, g = 0, b = 0;
int8 i2c_index = 0;
int1 nuevo_dato = FALSE;

#int_SSP
void i2c_isr() {
   int8 estado = i2c_isr_state();

   if (estado < 0x80) { // Escritura del maestro
      int8 valor = i2c_read();
      if (i2c_index == 0) r = valor;
      else if (i2c_index == 1) g = valor;
      else if (i2c_index == 2) {
         b = valor;
         nuevo_dato = TRUE;
      }
      i2c_index++;
      if (i2c_index >= 3) i2c_index = 0;
   }
}

void main() {
   set_tris_b(0x00);  // Puerto B como salida
   output_b(0x00);    // Apagar todos los LEDs

   enable_interrupts(GLOBAL);
   enable_interrupts(INT_SSP);

   while (TRUE) {
      if (nuevo_dato) {
         // Apagar todos los LEDs primero
         output_low(LED_ROJO);
         output_low(LED_VERDE);
         output_low(LED_AZUL);

         // Comparaciones con tolerancia
         int1 esRojo  = (r >= 250 && g <= 5 && b <= 5);
         int1 esVerde = (g >= 250 && r <= 5 && b <= 5);
         int1 esAzul  = (b >= 250 && r <= 5 && g <= 5);

         // Encender solo el LED correspondiente
         if (esRojo)
            output_high(LED_ROJO);
         else if (esVerde)
            output_high(LED_VERDE);
         else if (esAzul)
            output_high(LED_AZUL);

         nuevo_dato = FALSE;
      }
   }
}

