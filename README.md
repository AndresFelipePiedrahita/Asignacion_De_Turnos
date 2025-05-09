# Proyecto de Asignación de Turnos con MiniZinc

## Introducción
Este proyecto tiene como objetivo resolver un problema de asignación de turnos para empleados utilizando MiniZinc, una herramienta de modelado para problemas de optimización y satisfacción de restricciones.

### Modelos Principales
- **max.mzn:** Asigna turnos maximizando las preferencias de los empleados.
- **min.mzn:** Asigna turnos minimizando las penalizaciones asociadas a los turnos.

Ambos modelos respetan restricciones como el número mínimo y máximo de turnos por empleado, la cobertura mínima y máxima de turnos, y el descanso entre turnos consecutivos.

## ¿Cómo funciona el proyecto?
El proyecto se compone de tres partes principales:

### 1. Archivos de Entrada
- **datos.dzn:** Contiene los datos del problema, incluyendo:
    - Número de empleados y turnos.
    - Matriz de preferencias.
    - Penalizaciones y restricciones de cobertura.

**Ejemplo de parámetros:**
```
numEmpleados = 10;
numTurnos = 14;  % 2 turnos por día × 7 días
prefer = array2d(1..numEmpleados, 1..numTurnos, [
    % Preferencias de los empleados para cada turno
    3,1,4,0,2,5,1,3,2,4,0,1,2,3,
    ...
]);
minReq = [1,1,1,1,1,1,1,1,1,1,1,1,1,1];
maxReq = [3,3,3,3,3,3,3,3,3,3,3,3,3,3];
maxTurnosEmp = 8;
minTurnosEmp = 1;

penExtra = array2d(1..numEmpleados, 1..numTurnos, [
  5 - prefer[e, t] | e in 1..numEmpleados, t in 1..numTurnos
]);
```

### 2. Modelos MiniZinc
- **max.mzn:** Modelo para maximizar las preferencias de los empleados.
- **min.mzn:** Modelo para minimizar las penalizaciones asociadas a los turnos.

**Ambos modelos incluyen:**
- **Restricciones:** Cobertura mínima y máxima por turno, límite de turnos por empleado y descanso mínimo entre turnos consecutivos.
- **Objetivos:** Maximizar preferencias o minimizar penalizaciones.
- **Salida:** Asignación de turnos, valor total y turnos asignados por empleado.

**Ejemplo de salida (Maximización):**
```
Asignación x[e,t]:
[| 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1
 | 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1
 | ... ]
Valor total de preferencia = 175
Turnos asignados por empleado:
    Empleado 1:
        Martes, Turno Diurno
        Miércoles, Turno Nocturno
        Jueves, Turno Nocturno
        Domingo, Turno Nocturno
```

**Ejemplo de salida (Minimización):**
```
Asignación x[e,t]:
[| 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0
 | 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1
 | ... ]
Penalización total = 4
Turnos asignados por empleado:
Empleado 1:
  Miércoles, Turno Nocturno
Empleado 2:
  Jueves, Turno Diurno
  Domingo, Turno Nocturno
```

### 3. Script Python (script.py)
Este script automatiza la ejecución de los modelos y genera un informe de resultados.

**Funciones principales del script:**
- Llamar a MiniZinc para resolver los modelos.
- Procesar los resultados y generar un resumen en texto.
- Crear el archivo "informe_resultados.txt" con los resultados de ambos modelos.

## ¿Para qué sirve este proyecto?
El proyecto tiene aplicaciones en:
- Asignación de turnos en hospitales.
- Planificación de horarios en fábricas.
- Gestión de recursos en empresas.

## ¿Por qué usar MiniZinc?
- **Flexibilidad:** Permite modelar problemas complejos con múltiples restricciones y objetivos.
- **Compatibilidad:** Funciona con diversos solucionadores (CBC, Chuffed, Gurobi, OR-Tools, entre otros).
- **Interoperabilidad:** Se integra con lenguajes como Python y R.
- **Eficiencia:** Solucionadores avanzados optimizan el problema eficazmente.

## Cómo Ejecutar el Proyecto
1. Preparar y editar "datos.dzn" con los datos del problema.
2. Ejecutar el script Python:
     ```
     python script.py
     ```
3. Revisar el informe generado "informe_resultados.txt".

## Conclusión
Este proyecto demuestra cómo MiniZinc puede utilizarse para resolver problemas complejos de asignación de turnos de manera eficiente. La combinación de modelos de maximización y minimización permite abordar diferentes objetivos y la integración con Python facilita la automatización y el análisis de los resultados.

🚀
