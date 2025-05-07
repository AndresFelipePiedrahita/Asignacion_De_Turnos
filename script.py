import subprocess
import re
import os

# Constantes y configuración
RESULTADOS_DIR = "resultados"
RUTA_MAX = "max.mzn"
RUTA_MIN = "min.mzn"
RUTA_DZN = "datos.dzn"
TIEMPO_LIMITE = "60000"  # milisegundos
MAX_TURNOS_EMP = 5      # Debe coincidir con la definición en el archivo dzn

def crear_directorio(directorio: str) -> None:
    """
    Crea el directorio especificado si no existe.
    """
    os.makedirs(directorio, exist_ok=True)

def ejecutar_modelo(nombre_modelo: str, ruta_modelo: str, archivo_salida: str) -> None:
    """
    Ejecuta un modelo de MiniZinc usando el solver CBC, redireccionando la salida a un archivo.
    
    Parámetros:
      nombre_modelo: Nombre descriptivo del modelo (ej. "maximización").
      ruta_modelo: Ruta al archivo .mzn del modelo.
      archivo_salida: Nombre del archivo donde se guardará la salida.
    """
    print(f"\n▶ Ejecutando {nombre_modelo.upper()}...")
    crear_directorio(RESULTADOS_DIR)
    ruta_archivo = os.path.join(RESULTADOS_DIR, archivo_salida)

    # Ejecuta el modelo y guarda la salida en el archivo especificado
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        subprocess.run(
            ["minizinc", "--solver", "CBC", "--time-limit", TIEMPO_LIMITE, ruta_modelo, RUTA_DZN],
            stdout=f
        )

def analizar_resultado(archivo: str, tipo: str = "preferencia") -> str:
    """
    Analiza el contenido del archivo resultado y extrae información relevante.
    
    Parámetros:
      archivo: Ruta del archivo de salida generado por MiniZinc.
      tipo: Tipo de análisis ("preferencia" o "penalización"); define qué valor se extrae.
    
    Retorna:
      Un resumen en formato string con los valores y la asignación de turnos por empleado.
    """
    with open(archivo, encoding="utf-8") as f:
        contenido = f.read()

    resumen = f"📄 Resultados de {archivo}:\n"

    # Extrae el valor total (de preferencia o penalización)
    if tipo == "preferencia":
        match = re.search(r"Valor total de preferencia\s*=\s*(\d+)", contenido)
    else:
        match = re.search(r"Penalización total\s*=\s*(\d+)", contenido)
    valor_total = match.group(1) if match else "Desconocido"
    resumen += f"🔢 Valor total de {tipo}: {valor_total}\n"

    # Extrae la asignación de turnos por empleado
    resumen += "👥 Turnos asignados por empleado:\n"
    empleados = re.findall(r"Empleado (\d+):\n((?:  .+\n)+)", contenido)
    for empleado, turnos in empleados:
        resumen += f"  - Empleado {empleado}:\n"
        # Separa y procesa cada línea de turno asignado
        for turno in turnos.strip().split("\n"):
            match_turno = re.search(r"(\w+), Turno (\w+)", turno)
            if match_turno:
                dia, turno_nombre = match_turno.groups()
                resumen += f"    {dia}, Turno {turno_nombre}\n"
    resumen += "\n"
    return resumen

def guardar_informe(informe: str, nombre_archivo: str = "informe_resultados.txt") -> None:
    """
    Guarda el informe completo en un archivo dentro del directorio de resultados.
    
    Parámetros:
      informe: Texto del informe a guardar.
      nombre_archivo: Nombre del archivo donde se almacenará el informe.
    """
    crear_directorio(RESULTADOS_DIR)
    ruta_informe = os.path.join(RESULTADOS_DIR, nombre_archivo)
    with open(ruta_informe, "w", encoding="utf-8") as f:
        f.write(informe)

def main() -> None:
    """
    Función principal para ejecutar modelos, analizar resultados y generar informe.
    """
    # Ejecutar modelos
    ejecutar_modelo("maximización", RUTA_MAX, "resultado_max.txt")
    ejecutar_modelo("minimización", RUTA_MIN, "resultado_min.txt")

    # Analizar resultados
    resumen_max = analizar_resultado(os.path.join(RESULTADOS_DIR, "resultado_max.txt"), tipo="preferencia")
    resumen_min = analizar_resultado(os.path.join(RESULTADOS_DIR, "resultado_min.txt"), tipo="penalización")

    # Generar y guardar informe
    informe = (
        "📊 INFORME DE RESULTADOS DEL PROYECTO DE ASIGNACIÓN DE TURNOS (RRHH)\n"
        + "=" * 60 + "\n\n"
        + "MODELO DE MAXIMIZACIÓN:\n" + resumen_max
        + "MODELO DE MINIMIZACIÓN:\n" + resumen_min
    )
    guardar_informe(informe)

    # Mensajes de finalización
    print("\n✅ Resultados de modelos de maximización y minimización.")
    print("✅ Informe completo generado y guardado en el directorio 'resultados'.")
    print("✅ Ejecución finalizada.\n")
    print("📂 Resultados guardados en el directorio:", os.path.abspath(RESULTADOS_DIR))
    print("\n📚 Para mas informacion acerca del proyecto lee nuestro README.md o visita el siguiente link: \n")

if __name__ == "__main__":
    main()
