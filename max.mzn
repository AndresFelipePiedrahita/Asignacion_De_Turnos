% ==========================================================
% Modelo de asignación de turnos
% ==========================================================
% Este modelo asigna turnos a empleados maximizando las preferencias
% y respetando restricciones como el número máximo de turnos por empleado,
% la cobertura mínima y máxima de turnos, y el descanso entre turnos consecutivos.
% ==========================================================

% --------- Parámetros (vienen de turnos.dzn) ---------
int: numEmpleados;  % Número de empleados
int: numTurnos;     % Número total de turnos (días × turnos por día)
array[1..numEmpleados, 1..numTurnos] of int: prefer;  % Preferencias de los empleados para cada turno
array[1..numEmpleados,1..numTurnos] of int: penExtra;  % Penalizaciones para cada turno
array[1..numTurnos] of int: minReq;  % Requerimientos mínimos por turno
array[1..numTurnos] of int: maxReq;  % Requerimientos máximos por turno
int: maxTurnosEmp;  % Máximo número de turnos por empleado
int: minTurnosEmp;  % Mínimo número de turnos por empleado

% Nombres de los días y turnos
array[1..7] of string: dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
array[1..2] of string: turnos = ["Diurno", "Nocturno"];

% --------- Variables de decisión ---------
% x[e,t] = 1 si el empleado e está asignado al turno t, 0 en caso contrario
array[1..numEmpleados, 1..numTurnos] of var 0..1: x;

% --------- Restricciones ---------

% Cobertura mínima y máxima por turno
constraint
  forall(t in 1..numTurnos)(
    sum(e in 1..numEmpleados)(x[e,t]) >= minReq[t] /\
    sum(e in 1..numEmpleados)(x[e,t]) <= maxReq[t]
  );

% Límite de turnos por empleado
constraint
  forall(e in 1..numEmpleados)(
    sum(t in 1..numTurnos)(x[e,t]) <= maxTurnosEmp /\
    sum(t in 1..numTurnos)(x[e,t]) >= minTurnosEmp
  );

% Descanso mínimo entre turnos consecutivos
constraint
  forall(e in 1..numEmpleados, t in 1..numTurnos-1)(
    x[e,t] + x[e,t+1] <= 1
  );

% --------- Objetivo ---------
% Maximizar las preferencias de los empleados, penalizando el exceso de turnos
solve maximize
  sum(e in 1..numEmpleados, t in 1..numTurnos)((prefer[e,t] ^ 2) * x[e,t]) -
  5000 * sum(e in 1..numEmpleados)(max(0, sum(t in 1..numTurnos)(x[e,t]) - maxTurnosEmp));

% --------- Salida ---------
% Mostrar la asignación de turnos y los días/turnos asignados a cada empleado
output [
  "Asignación x[e,t]:\n", show2d(x), "\n",
  "Valor total de preferencia = ", show(sum(e in 1..numEmpleados, t in 1..numTurnos)(prefer[e,t] * x[e,t])), "\n",
  "Turnos asignados por empleado:\n",
  concat([ "Empleado " ++ show(e) ++ ":\n" ++
           concat([ "  " ++ obtener_dia(t) ++ ", Turno " ++ obtener_turno(t) ++ "\n"
                    | t in 1..numTurnos where fix(x[e,t]) = 1 ])
           | e in 1..numEmpleados ])
];

% --------- Funciones ---------
% Función para obtener el nombre del día a partir del índice del turno
function string: obtener_dia(int: t) =
  dias[(t-1) div 2 + 1];

% Función para obtener el nombre del turno (Diurno/Nocturno) a partir del índice del turno
function string: obtener_turno(int: t) =
  turnos[(t-1) mod 2 + 1];