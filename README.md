# Laboratorio 2 - Teoría de la Computación

Repositorio con las soluciones del laboratorio 2. Cada ejercicio va en su propia branch.
[Video de ejecución)](https://youtu.be/1uaFaH1_GMk)

## Estructura de branches

| Branch      | Contenido                                          |
|-------------|----------------------------------------------------|
| `main`      | Este README                                        |
| `problema1` | Conversiones de expresión regular a AFN y AFD      |
| `problema2` | Balanceo de expresiones infix con pila             |
| `problema3` | Algoritmo de Shunting Yard (infix → postfix)       |

## Video de ejecución

_(pendiente: enlace de YouTube como video no listado)_

## Problema 2 — Balanceo de expresiones

```bash
cd problema2
python main.py               
python main.py otro_archivo.txt 
```

Lee el archivo línea por línea y para cada expresión imprime la traza completa de la pila
(paso, carácter, posición, acción y contenido de la pila) y el veredicto final. Los
caracteres escapados con `\` se ignoran, de modo que `\(` no cuenta como paréntesis.

Archivos:

- `pila.py` — implementación manual de la pila
- `balanceador.py` — lógica del recorrido y la traza
- `main.py` — lectura del archivo e impresión de resultados
- `expresiones.txt` — expresiones de prueba del enunciado

## Problema 3 — Shunting Yard

```bash
cd problema3
python main.py                  
python main.py otro_archivo.txt
```

Para cada expresión imprime la tokenización, la expansión de `+` y `?`, la inserción de
la concatenación explícita, la tabla de pasos del algoritmo y la expresión en postfix.

Archivos:

- `EXPLICACION.md` — explicación escrita del algoritmo
- `tokenizador.py` — separa la expresión en tokens y maneja escapes y clases
- `preprocesador.py` — expande `+` y `?`, inserta el operador de concatenación
- `shunting_yard.py` — conversión infix → postfix con la traza de pasos
- `pila.py` — la misma pila del problema 2
- `main.py` — lectura del archivo e impresión de resultados
- `expresiones.txt` — las ocho expresiones del problema 1

## Notas

- Se usa `·` como operador de concatenación en lugar de `.`, porque el punto aparece como
  carácter literal en las expresiones del enunciado.
- Las clases de caracteres como `[ae03]` se tratan como un único token literal.
- En el archivo del problema 2 se restauraron las llaves de los cuantificadores
  (`{1,2}`, `{5,30}`, `{10,20}`) que se perdieron al copiar el PDF.
