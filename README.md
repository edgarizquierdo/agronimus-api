
# Agronimus API – Versión Final (NDVI/NDWI + Clima)

## Endpoints

- `/` – Prueba de conexión
- `/logo` – Devuelve el logo
- `/generar-informe` – Genera informe para una parcela usando datos NDVI, NDWI

## Cómo usar

Enviar un POST a `/generar-informe` con:
```json
{
  "nombre": "(1)153T",
  "fecha": "2025-04-15"
}
```

Retorna un archivo de informe `.txt` (PDF en próximas versiones).
