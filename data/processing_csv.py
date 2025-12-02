import pandas as pd

# Ruta de entrada y salida
input_file = "./data/raw/Global_Superstore2.csv"
output_file = "./data/raw/Global_Superstore2.json"

def convert_csv_to_json():
    try:
        # Leer CSV en un DataFrame
        df = pd.read_csv(input_file, encoding="latin-1")

        # Opcional: convertir columnas numéricas
        numeric_cols = ["Sales", "Quantity", "Discount", "Profit", "Shipping Cost", "Postal Code"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

        # Opcional: convertir fechas a formato ISO
        for col in ["Order Date", "Ship Date"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%Y-%m-%d")

        # Exportar a JSON (array de objetos)
        df.to_json(output_file, orient="records", indent=2, force_ascii=False)

        print(f"✅ Conversión completa. Archivo guardado en {output_file}")

    except Exception as error:
        print(f"❌ Error en la conversión: {error}")

# Ejecutar
convert_csv_to_json()