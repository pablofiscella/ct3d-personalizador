# Runbook — Motor IA piezas del kit

> Documentación técnica completa (procesamiento por pieza, algoritmos, deploy): **`docs/MOTOR-IA.md`**.

1. Setear `OPENAI_API_KEY` en el env del servicio (systemd `ct3d-kit.service`).
2. Asegurar Tier 2+ de OpenAI (≥20 IPM) antes de tandas grandes.
3. Subir personajes del tema (recortes/) por /dash.
4. /dash → "Generar kit con IA" (medium para borrador).
5. Revisar grilla, regenerar lo que falle, Aprobar.
6. Verificar costo real en el dashboard de OpenAI vs estimado.
7. Re-verificar id de modelo vigente (deprecaciones dic-2026).
