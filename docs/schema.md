<<<<<<< HEAD
# VZLA_DEDUP — Schema

Este documento define las entidades, campos, tipos y enums usados por VZLA_DEDUP.

La especificación actual está pensada para ser compatible con:

```text
PostgreSQL 14+
MySQL 8.0+
JSONL
=======
# Schema de datos — VZLA_DEDUP

Referencia técnica completa del pipeline de exportación. Define los tipos, restricciones y valores permitidos de cada campo en los tres streams JSONL y sus tablas auxiliares.

> Compatibilidad: PostgreSQL 14+ · MySQL 8.0+  
> Última actualización: Junio 2026

---

## Convenciones globales

| Decisión | Regla |
|---|---|
| Zona horaria | UTC siempre. El `Z` al final es obligatorio en todos los timestamps. |
| Fechas | `TIMESTAMPTZ` (Postgres) / `DATETIME` (MySQL, UTC asumido en app layer) · Formato JSONL: ISO 8601 |
| Booleanos | `BOOLEAN` nativo · JSONL: `true` / `false` · Nunca `0/1`, nunca `"Si"/"No"` |
| Nulos | `null` explícito · Nunca `""`, nunca `"N/A"`, nunca `0` como sustituto · Los campos ausentes se exportan como `null`, no se omiten |
| IDs internos | UUID v4 como `VARCHAR(36)` · Nunca autoincrement — los UUIDs permiten generación offline en el scraper |
| Enums | String con valores controlados (ver sección Enums) · No usar tipo `ENUM` nativo de MySQL |
| HMAC | `VARCHAR(64)` — SHA-256 en hex · Los campos originales no se guardan en ningún momento |
| Scores | `NUMERIC(4,3)` — rango `0.000` a `1.000` |

### Estructura `location_object`

Reutilizada en múltiples tablas. Si la geocodificación falla, `lat`/`lng` quedan `null` y el registro no se descarta.

```json
{
  "raw": "El Tocuyo, Lara",
  "estado": "Lara",
  "municipio": "Morán",
  "parroquia": null,
  "lat": 9.7834,
  "lng": -69.7921
}
>>>>>>> master
```

---

<<<<<<< HEAD
## 1. Convenciones globales

| Decisión             | Valor                                                                       |
| -------------------- | --------------------------------------------------------------------------- |
| Zona horaria         | UTC siempre                                                                 |
| Fechas               | `TIMESTAMPTZ` en PostgreSQL / `DATETIME` en MySQL, asumido UTC en app layer |
| Fechas en JSONL      | `string` en formato ISO 8601                                                |
| Booleanos            | `BOOLEAN` nativo. En JSONL: `true` / `false`                                |
| Nulos                | `null` explícito                                                            |
| Strings cortos       | `VARCHAR(n)` con límite razonable                                           |
| Texto libre / listas | `TEXT` o `JSONB` en PostgreSQL / `JSON` en MySQL 8+                         |
| IDs internos         | UUID v4 como string `VARCHAR(36)`                                           |
| Enums                | String con valores controlados                                              |
| HMAC                 | `VARCHAR(64)` — SHA-256 en hex                                              |
| Confianza / scores   | `NUMERIC(4,3)` — rango `0.000` a `1.000`                                    |

---

## 2. Reglas globales JSONL

### 2.1 Fechas

Todas las fechas deben estar en UTC.

Ejemplo:

```json
"2026-06-24T14:32:00Z"
```

---

### 2.2 Booleanos

Correcto:

```json
true
```

```json
false
```

Incorrecto:

```json
1
```

```json
0
```

```json
"Si"
```

```json
"No"
```

---

### 2.3 Nulos

Correcto:

```json
null
```

Incorrecto:

```json
""
```

```json
"N/A"
```

```json
0
```

---

### 2.4 IDs internos

Los IDs internos deben ser UUID v4 como string.

Ejemplo:

```json
"a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

No usar autoincrement entero para IDs que salgan del sistema.

---

### 2.5 Enums

Los enums deben representarse como strings controlados.

No usar `ENUM` nativo de MySQL.

---

### 2.6 HMAC

Los HMAC deben ser SHA-256 en hexadecimal.

Tipo:

```text
VARCHAR(64)
```

---

### 2.7 Scores

Los scores deben estar entre:

```text
0.000 y 1.000
```

---

# Entidades

---

## 3. Entidad: `EVENT`

Tabla:

```text
events
```

### Campos

| Campo             | Tipo SQL          | Tipo JSONL        | Nullable | Valores / Notas                        |
| ----------------- | ----------------- | ----------------- | -------: | -------------------------------------- |
| `event_id`        | `VARCHAR(36)` PK  | `string`          |       no | UUID v4 generado por el sistema        |
| `name`            | `VARCHAR(255)`    | `string`          |       no | Nombre legible del evento              |
| `event_type`      | `VARCHAR(50)`     | `string`          |       no | Enum definido                          |
| `occurred_at`     | `TIMESTAMPTZ`     | `string` ISO 8601 |       no | Fecha/hora del evento                  |
| `affected_states` | `TEXT[]` / `JSON` | `array<string>`   |       sí | Lista de estados venezolanos afectados |
| `magnitude`       | `NUMERIC(4,2)`    | `number`          |       sí | Magnitud                               |
| `depth_km`        | `NUMERIC(6,2)`    | `number`          |       sí | Profundidad en kilómetros              |
| `status`          | `VARCHAR(30)`     | `string`          |       no | Enum definido                          |
| `external_ids`    | `JSONB` / `JSON`  | `object`          |       sí | IDs externos asociados                 |

### Enums

`events.event_type`:

```text
earthquake
flood
landslide
other
```

`events.status`:

```text
active
monitoring
closed
```
=======
## Entidad: EVENT

### Tabla `events`

| Campo | Tipo SQL | Tipo JSONL | Nullable | Notas |
|---|---|---|---|---|
| `event_id` | `VARCHAR(36) PK` | `string` | NO | UUID v4 generado por el sistema |
| `name` | `VARCHAR(255)` | `string` | NO | Nombre legible. Ej: `"Terremoto Yaracuy 24-06-2026"` |
| `event_type` | `VARCHAR(50)` | `string` | NO | Enum `event_type` |
| `occurred_at` | `TIMESTAMPTZ` | `string (ISO 8601)` | NO | |
| `affected_states` | `TEXT[]` / `JSON` | `array<string>` | YES | Lista de estados venezolanos afectados |
| `magnitude` | `NUMERIC(4,2)` | `number` | YES | Escala Richter / Momento |
| `depth_km` | `NUMERIC(6,2)` | `number` | YES | Profundidad en km |
| `status` | `VARCHAR(30)` | `string` | NO | Enum `event_status` |
| `external_ids` | `JSONB` / `JSON` | `object` | YES | Ej: `{"usgs": "us7000n4xy", "funvisis": "VEN-2026-001"}` |
>>>>>>> master

### Ejemplo

```json
{
  "event_id": "f0e1d2c3-b4a5-6789-0fed-cba987654321",
<<<<<<< HEAD
  "name": "Terremoto 24-06-2026",
  "event_type": "earthquake",
  "occurred_at": "2026-06-24T14:32:00Z",
  "affected_states": ["Yaracuy"],
  "magnitude": null,
  "depth_km": 12.50,
  "status": "active",
  "external_ids": {
    "usgs": "us7000n4x",
    "funvisis": "2026-001"
=======
  "name": "Terremoto Yaracuy 24-06-2026",
  "event_type": "earthquake",
  "occurred_at": "2026-06-24T14:32:00Z",
  "affected_states": ["Yaracuy", "Lara", "Portuguesa"],
  "magnitude": 7.30,
  "depth_km": 12.50,
  "status": "active",
  "external_ids": {
    "usgs": "us7000n4xy",
    "funvisis": "VEN-2026-001"
>>>>>>> master
  }
}
```

---

<<<<<<< HEAD
## 4. Entidad: `PERSON` — Identidad

Tabla:

```text
persons
```

### Campos

| Campo                 | Tipo SQL         | Tipo JSONL      | Nullable | Valores / Notas                                           |
| --------------------- | ---------------- | --------------- | -------: | --------------------------------------------------------- |
| `person_record_id`    | `VARCHAR(36)` PK | `string`        |       no | UUID v4                                                   |
| `event_id`            | `VARCHAR(36)` FK | `string`        |       no | Referencia a `events.event_id`                            |
| `full_name`           | `VARCHAR(300)`   | `string`        |       sí | Nombre normalizado                                        |
| `alternate_names`     | `JSONB` / `JSON` | `array<string>` |       sí | Nombres alternativos encontrados                          |
| `cedula_hmac`         | `VARCHAR(64)`    | `string`        |       sí | HMAC SHA-256 de la cédula                                 |
| `cedula_masked`       | `VARCHAR(15)`    | `string`        |       sí | Solo últimos dígitos visibles                             |
| `age_range`           | `JSONB` / `JSON` | `object`        |       sí | Rango de edad                                             |
| `sex`                 | `VARCHAR(10)`    | `string`        |       sí | Enum definido                                             |
| `is_minor`            | `BOOLEAN`        | `boolean`       |       sí | `true` si es menor de 18; `null` si no puede determinarse |
| `last_known_location` | `JSONB` / `JSON` | `object`        |       sí | `location_object`                                         |
| `status`              | `VARCHAR(30)`    | `string`        |       no | Enum definido                                             |
| `verification_status` | `VARCHAR(30)`    | `string`        |       no | Enum definido                                             |
| `confidence_score`    | `NUMERIC(4,3)`   | `number`        |       no | Default `0.000` si no hay datos                           |
| `source_url`          | `TEXT`           | `string`        |       sí | URL primaria del registro                                 |

### Enums

`persons.sex`:

```text
M
F
unknown
```

`persons.status`:

```text
missing
found
injured
deceased
unknown
```

`persons.verification_status`:

```text
unverified
pending
verified
conflicting
```

### `age_range`

Ejemplo:

```json
{
  "min": 30,
  "max": 40
}
```

Se usa `age_range` en lugar de edad exacta.
=======
## Entidad: PERSON — Identidad

### Tabla `persons`

| Campo | Tipo SQL | Tipo JSONL | Nullable | Notas |
|---|---|---|---|---|
| `person_record_id` | `VARCHAR(36) PK` | `string` | NO | UUID v4 |
| `event_id` | `VARCHAR(36) FK` | `string` | NO | → `events.event_id` |
| `full_name` | `VARCHAR(300)` | `string` | YES | Normalizado: sin tildes, uppercase |
| `alternate_names` | `JSONB` / `JSON` | `array<string>` | YES | Otros nombres encontrados en fuentes |
| `cedula_hmac` | `VARCHAR(64)` | `string` | YES | HMAC-SHA256 de la cédula. Para matching sin exponer el dato |
| `cedula_masked` | `VARCHAR(15)` | `string` | YES | Últimos 4 dígitos. Ej: `"V-****5821"` |
| `age_range` | `JSONB` / `JSON` | `object` | YES | `{"min": int, "max": int}`. Nunca edad exacta si no es segura |
| `sex` | `VARCHAR(10)` | `string` | YES | Enum `sex` |
| `is_minor` | `BOOLEAN` | `boolean` | YES | `true` si menor de 18. `null` si no se puede determinar |
| `last_known_location` | `JSONB` / `JSON` | `object` | YES | `location_object` |
| `status` | `VARCHAR(30)` | `string` | NO | Enum `person_status` |
| `verification_status` | `VARCHAR(30)` | `string` | NO | Enum `verification_status` |
| `confidence_score` | `NUMERIC(4,3)` | `number` | NO | `0.000` a `1.000`. Default `0.000` |
| `source_url` | `TEXT` | `string` | YES | URL de la fuente primaria |
>>>>>>> master

### Ejemplo

```json
{
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "event_id": "f0e1d2c3-b4a5-6789-0fed-cba987654321",
  "full_name": "JOSE LUIS PEREZ MARIN",
  "alternate_names": ["JOSE PEREZ", "JOSELO PEREZ MARIN"],
<<<<<<< HEAD
  "cedula_hmac": "3b4c9e2a1f...",
  "cedula_masked": "V-****5821",
  "age_range": {
    "min": 30,
    "max": 40
  },
=======
  "cedula_hmac": "3b4c9e2a1fd82f6a0bc347e1a9f2c8d5e047b3a12f9c6d71e8b405a3c2d1f9e0",
  "cedula_masked": "V-****5821",
  "age_range": {"min": 30, "max": 40},
>>>>>>> master
  "sex": "M",
  "is_minor": false,
  "last_known_location": {
    "raw": "El Tocuyo, Lara",
    "estado": "Lara",
    "municipio": "Morán",
    "parroquia": null,
    "lat": 9.7834,
    "lng": -69.7921
  },
  "status": "missing",
  "verification_status": "unverified",
  "confidence_score": 0.420,
<<<<<<< HEAD
  "source_url": "https://ejemplo.com/registro/12345"
=======
  "source_url": "https://encuentralos.org/registro/12345"
>>>>>>> master
}
```

---

<<<<<<< HEAD
## 5. Estructura: `location_object`

Estructura usada por campos de ubicación.

```json
{
  "raw": "El Tocuyo, Lara",
  "estado": "Lara",
  "municipio": "Morán",
  "parroquia": null,
  "lat": 9.7834,
  "lng": -69.7921
}
```

### Campos

| Campo       | Tipo JSONL | Nullable | Descripción                                  |
| ----------- | ---------- | -------: | -------------------------------------------- |
| `raw`       | `string`   |       sí | Valor original o descriptivo de la ubicación |
| `estado`    | `string`   |       sí | Estado                                       |
| `municipio` | `string`   |       sí | Municipio                                    |
| `parroquia` | `string`   |       sí | Parroquia                                    |
| `lat`       | `number`   |       sí | Latitud                                      |
| `lng`       | `number`   |       sí | Longitud                                     |

Si la geocodificación falla, `lat` y `lng` deben quedar como `null`.

El registro no debe descartarse por no tener coordenadas.

---

## 6. Entidad: `PERSON_NOTE` — Nota / Información adicional

Tabla:

```text
person_notes
```

### Campos base

| Campo                 | Tipo SQL         | Tipo JSONL        | Nullable | Valores / Notas                                  |
| --------------------- | ---------------- | ----------------- | -------: | ------------------------------------------------ |
| `note_record_id`      | `VARCHAR(36)` PK | `string`          |       no | UUID v4                                          |
| `person_record_id`    | `VARCHAR(36)` FK | `string`          |       no | Referencia a `persons.person_record_id`          |
| `note_type`           | `VARCHAR(30)`    | `string`          |       no | Enum definido                                    |
| `found_by`            | `VARCHAR(300)`   | `string`          |       sí | Nombre de quien encontró                         |
| `status`              | `VARCHAR(30)`    | `string`          |       no | Enum definido                                    |
| `source_date`         | `TIMESTAMPTZ`    | `string` ISO 8601 |       sí | Fecha en que ocurrió o fue publicado el hecho    |
| `entry_date`          | `TIMESTAMPTZ`    | `string` ISO 8601 |       no | Fecha en que entra el registro                   |
| `found`               | `BOOLEAN`        | `boolean`         |       sí | `true` si fue localizada; `null` si se desconoce |
| `last_known_location` | `JSONB` / `JSON` | `object`          |       sí | Mismo `location_object` que en `persons`         |

### Enums

`person_notes.note_type`:

```text
missing
injured
found
deceased
```

`person_notes.status`:

```text
active
superseded
retracted
=======
## Entidad: PERSON — Nota

Una persona puede tener múltiples notas a lo largo del tiempo. Cada nota tiene un `note_type` que determina qué campos adicionales son relevantes. Todos los campos sparse están presentes en el registro — los que no aplican van como `null`.

### Tabla `person_notes`

**Campos base (todos los tipos)**

| Campo | Tipo SQL | Tipo JSONL | Nullable | Notas |
|---|---|---|---|---|
| `note_record_id` | `VARCHAR(36) PK` | `string` | NO | UUID v4 |
| `person_record_id` | `VARCHAR(36) FK` | `string` | NO | → `persons.person_record_id` |
| `note_type` | `VARCHAR(30)` | `string` | NO | Enum `note_type` |
| `found_by` | `VARCHAR(300)` | `string` | YES | Quien reportó o encontró |
| `status` | `VARCHAR(30)` | `string` | NO | Enum `note_status` |
| `source_date` | `TIMESTAMPTZ` | `string (ISO 8601)` | YES | Cuándo ocurrió / fue publicado el hecho |
| `entry_date` | `TIMESTAMPTZ` | `string (ISO 8601)` | NO | Cuándo ingresó al sistema. Default: `NOW()` |
| `found` | `BOOLEAN` | `boolean` | YES | `true` = localizada · `null` = desconocido |
| `last_known_location` | `JSONB` / `JSON` | `object` | YES | `location_object` |

**Campos sparse por `note_type`**

| Campo | Aplica a | Tipo SQL | Tipo JSONL |
|---|---|---|---|
| `last_seen_at` | `missing` | `TIMESTAMPTZ` | `string (ISO 8601)` |
| `last_seen_location` | `missing` | `JSONB` / `JSON` | `object (location_object)` |
| `hospital_name` | `injured` | `VARCHAR(255)` | `string` |
| `hospital_municipio` | `injured` | `VARCHAR(100)` | `string` |
| `severity` | `injured` | `VARCHAR(20)` | `string` — Enum `severity` |
| `admitted_time` | `injured` | `TIMESTAMPTZ` | `string (ISO 8601)` |
| `found_at` | `found` | `TIMESTAMPTZ` | `string (ISO 8601)` |
| `deceased_at` | `deceased` | `TIMESTAMPTZ` | `string (ISO 8601)` |
| `recovery_location` | `deceased` | `JSONB` / `JSON` | `object (location_object)` |
| `identification_status` | `deceased` | `VARCHAR(30)` | `string` — Enum `identification_status` |
| `confirmed_by` | `deceased` | `VARCHAR(300)` | `string` |

### Ejemplo — `note_type: "missing"`

```json
{
  "note_record_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "note_type": "missing",
  "found_by": null,
  "status": "active",
  "source_date": "2026-06-24T18:00:00Z",
  "entry_date": "2026-06-25T03:12:44Z",
  "found": false,
  "last_known_location": {
    "raw": "El Tocuyo, Lara",
    "estado": "Lara",
    "municipio": "Morán",
    "parroquia": null,
    "lat": 9.7834,
    "lng": -69.7921
  },
  "last_seen_at": "2026-06-24T14:45:00Z",
  "last_seen_location": {
    "raw": "Mercado Municipal El Tocuyo",
    "estado": "Lara",
    "municipio": "Morán",
    "parroquia": "El Tocuyo",
    "lat": 9.7801,
    "lng": -69.7895
  },
  "hospital_name": null,
  "hospital_municipio": null,
  "severity": null,
  "admitted_time": null,
  "found_at": null,
  "deceased_at": null,
  "recovery_location": null,
  "identification_status": null,
  "confirmed_by": null
}
```

### Ejemplo — `note_type: "injured"`

```json
{
  "note_record_id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "note_type": "injured",
  "found_by": "Defensa Civil Yaracuy",
  "status": "active",
  "source_date": "2026-06-24T20:15:00Z",
  "entry_date": "2026-06-25T04:00:00Z",
  "found": true,
  "last_known_location": {
    "raw": "Hospital Central de San Felipe",
    "estado": "Yaracuy",
    "municipio": "San Felipe",
    "parroquia": null,
    "lat": 10.3393,
    "lng": -68.7442
  },
  "last_seen_at": null,
  "last_seen_location": null,
  "hospital_name": "Hospital Central de San Felipe",
  "hospital_municipio": "San Felipe",
  "severity": "grave",
  "admitted_time": "2026-06-24T20:15:00Z",
  "found_at": null,
  "deceased_at": null,
  "recovery_location": null,
  "identification_status": null,
  "confirmed_by": null
}
```

### Ejemplo — `note_type: "found"`

```json
{
  "note_record_id": "d4e5f6a7-b8c9-0123-defa-234567890123",
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "note_type": "found",
  "found_by": "Familiar — María Pérez",
  "status": "active",
  "source_date": "2026-06-26T10:00:00Z",
  "entry_date": "2026-06-26T10:45:00Z",
  "found": true,
  "last_known_location": {
    "raw": "Refugio Escuela Básica Simón Bolívar, Barquisimeto",
    "estado": "Lara",
    "municipio": "Iribarren",
    "parroquia": null,
    "lat": 10.0647,
    "lng": -69.3237
  },
  "last_seen_at": null,
  "last_seen_location": null,
  "hospital_name": null,
  "hospital_municipio": null,
  "severity": null,
  "admitted_time": null,
  "found_at": "2026-06-26T09:30:00Z",
  "deceased_at": null,
  "recovery_location": null,
  "identification_status": null,
  "confirmed_by": null
}
```

### Ejemplo — `note_type: "deceased"`

```json
{
  "note_record_id": "e5f6a7b8-c9d0-1234-efab-345678901234",
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "note_type": "deceased",
  "found_by": "Bomberos Yaracuy",
  "status": "active",
  "source_date": "2026-06-25T08:30:00Z",
  "entry_date": "2026-06-25T09:00:00Z",
  "found": true,
  "last_known_location": {
    "raw": "Sector La Encrucijada, Chivacoa",
    "estado": "Yaracuy",
    "municipio": "Bruzual",
    "parroquia": null,
    "lat": 10.1612,
    "lng": -68.9001
  },
  "last_seen_at": null,
  "last_seen_location": null,
  "hospital_name": null,
  "hospital_municipio": null,
  "severity": null,
  "admitted_time": null,
  "found_at": null,
  "deceased_at": "2026-06-24T15:10:00Z",
  "recovery_location": {
    "raw": "Sector La Encrucijada, Chivacoa",
    "estado": "Yaracuy",
    "municipio": "Bruzual",
    "parroquia": null,
    "lat": 10.1612,
    "lng": -68.9001
  },
  "identification_status": "identified",
  "confirmed_by": "Bomberos Yaracuy"
}
>>>>>>> master
```

---

<<<<<<< HEAD
## 7. Sub-campos de `person_notes` por `note_type`

Estos campos viven en la misma tabla con columnas sparse nullable.

La especificación recomienda columnas sparse en una sola tabla para simplificar consultas.

---

### 7.1 Si `note_type = "missing"`

| Campo                | Tipo SQL         | Tipo JSONL                 | Nullable |
| -------------------- | ---------------- | -------------------------- | -------: |
| `last_seen_at`       | `TIMESTAMPTZ`    | `string` ISO 8601          |       sí |
| `last_seen_location` | `JSONB` / `JSON` | `object` `location_object` |       sí |

---

### 7.2 Si `note_type = "injured"`

| Campo                | Tipo SQL       | Tipo JSONL        | Nullable |
| -------------------- | -------------- | ----------------- | -------: |
| `hospital_name`      | `VARCHAR(255)` | `string`          |       sí |
| `hospital_municipio` | `VARCHAR(100)` | `string`          |       sí |
| `severity`           | `VARCHAR(20)`  | `string`          |       sí |
| `admitted_time`      | `TIMESTAMPTZ`  | `string` ISO 8601 |       sí |

`person_notes.severity`:

```text
leve
moderado
grave
critico
unknown
=======
## Entidad: PERSON — Foto

### Tabla `person_photos`

| Campo | Tipo SQL | Tipo JSONL | Nullable | Notas |
|---|---|---|---|---|
| `photo_id` | `VARCHAR(36) PK` | `string` | NO | UUID v4 |
| `person_record_id` | `VARCHAR(36) FK` | `string` | NO | → `persons.person_record_id` |
| `url` | `TEXT` | `string` | NO | Preferir URL del CDN propio sobre la fuente original |
| `caption` | `TEXT` | `string` | YES | Texto asociado en la fuente original |
| `source_id` | `VARCHAR(36) FK` | `string` | YES | → `person_sources.source_id` |
| `uploaded_at` | `TIMESTAMPTZ` | `string (ISO 8601)` | NO | Cuándo fue ingestada la foto |

### Ejemplo

```json
{
  "photo_id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "url": "https://cdn.vzladedup.org/photos/a1b2c3d4_001.jpg",
  "caption": "Foto compartida por familiar en grupo de WhatsApp 'Desaparecidos Lara'",
  "source_id": "g7b8c9d0-e1f2-3456-abcd-567890123456",
  "uploaded_at": "2026-06-25T05:22:00Z"
}
>>>>>>> master
```

---

<<<<<<< HEAD
### 7.3 Si `note_type = "found"`

| Campo      | Tipo SQL      | Tipo JSONL        | Nullable |
| ---------- | ------------- | ----------------- | -------: |
| `found_at` | `TIMESTAMPTZ` | `string` ISO 8601 |       sí |

---

### 7.4 Si `note_type = "deceased"`

| Campo                   | Tipo SQL         | Tipo JSONL                 | Nullable |
| ----------------------- | ---------------- | -------------------------- | -------: |
| `deceased_at`           | `TIMESTAMPTZ`    | `string` ISO 8601          |       sí |
| `recovery_location`     | `JSONB` / `JSON` | `object` `location_object` |       sí |
| `identification_status` | `VARCHAR(30)`    | `string`                   |       sí |
| `confirmed_by`          | `VARCHAR(300)`   | `string`                   |       sí |

`person_notes.identification_status`:

```text
identified
unidentified
pending
=======
## Entidad: PERSON — Fuente

### Tabla `person_sources`

| Campo | Tipo SQL | Tipo JSONL | Nullable | Notas |
|---|---|---|---|---|
| `source_id` | `VARCHAR(36) PK` | `string` | NO | UUID v4 |
| `person_record_id` | `VARCHAR(36) FK` | `string` | NO | → `persons.person_record_id` |
| `source_url` | `TEXT` | `string` | NO | URL donde se encontró el dato |
| `ext_id` | `VARCHAR(255)` | `string` | YES | ID del registro en la fuente externa |
| `trust_tier` | `SMALLINT` | `number (integer)` | NO | Enum `trust_tier` |
| `fetched_at` | `TIMESTAMPTZ` | `string (ISO 8601)` | NO | Cuándo fue scrapeado |

### Ejemplo

```json
{
  "source_id": "g7b8c9d0-e1f2-3456-abcd-567890123456",
  "person_record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "source_url": "https://encuentralos.org/registro/12345",
  "ext_id": "REG-12345",
  "trust_tier": 2,
  "fetched_at": "2026-06-25T03:10:00Z"
}
>>>>>>> master
```

---

<<<<<<< HEAD
## 8. Entidad: `PERSON_PHOTO`

Tabla:

```text
person_photos
```

### Campos

| Campo              | Tipo SQL         | Tipo JSONL        | Nullable | Valores / Notas                                |
| ------------------ | ---------------- | ----------------- | -------: | ---------------------------------------------- |
| `photo_id`         | `VARCHAR(36)` PK | `string`          |       no | UUID v4                                        |
| `person_record_id` | `VARCHAR(36)` FK | `string`          |       no | Referencia a persona                           |
| `url`              | `TEXT`           | `string`          |       no | URL de la imagen                               |
| `caption`          | `TEXT`           | `string`          |       sí | Texto asociado a la foto en la fuente original |
| `source_id`        | `VARCHAR(36)` FK | `string`          |       sí | Referencia a `person_sources.source_id`        |
| `uploaded_at`      | `TIMESTAMPTZ`    | `string` ISO 8601 |       no | Cuándo fue ingestada en el sistema             |

---

## 9. Entidad: `PERSON_SOURCE` — Fuente / Corroboración

Tabla:

```text
person_sources
```

### Campos

| Campo              | Tipo SQL         | Tipo JSONL        | Nullable | Valores / Notas                         |
| ------------------ | ---------------- | ----------------- | -------: | --------------------------------------- |
| `source_id`        | `VARCHAR(36)` PK | `string`          |       no | UUID v4                                 |
| `person_record_id` | `VARCHAR(36)` FK | `string`          |       no | Referencia a `persons.person_record_id` |
| `source_url`       | `TEXT`           | `string`          |       no | URL donde se encontró el dato           |
| `ext_id`           | `VARCHAR(255)`   | `string`          |       sí | ID del registro en la fuente externa    |
| `trust_tier`       | `SMALLINT`       | `number` integer  |       no | Nivel de confianza                      |
| `fetched_at`       | `TIMESTAMPTZ`    | `string` ISO 8601 |       no | Cuándo fue scrapeado este dato          |

### `trust_tier`

```text
1 = oficial
2 = ONG
3 = social/anónimo
```

---

## 10. Entidad: `ACOPIO_CENTER`

Tabla:

```text
acopio_centers
```

### Campos

| Campo              | Tipo SQL         | Tipo JSONL                 | Nullable | Valores / Notas                |
| ------------------ | ---------------- | -------------------------- | -------: | ------------------------------ |
| `acopio_id`        | `VARCHAR(36)` PK | `string`                   |       no | UUID v4                        |
| `event_id`         | `VARCHAR(36)` FK | `string`                   |       no | Referencia a `events.event_id` |
| `name`             | `VARCHAR(300)`   | `string`                   |       no | Nombre del centro              |
| `location`         | `JSONB` / `JSON` | `object` `location_object` |       sí | Ubicación                      |
| `confidence_score` | `NUMERIC(4,3)`   | `number`                   |       no | Default `0.000`                |
| `status`           | `VARCHAR(30)`    | `string`                   |       no | Enum definido                  |
| `needs`            | `JSONB` / `JSON` | `array<string>`            |       sí | Necesidades                    |
| `last_verified_at` | `TIMESTAMPTZ`    | `string` ISO 8601          |       sí | Última verificación            |
| `managing_org`     | `VARCHAR(255)`   | `string`                   |       sí | Organización responsable       |
| `public_contact`   | `VARCHAR(300)`   | `string`                   |       sí | Contacto público               |
| `capacity`         | `INTEGER`        | `number` integer           |       sí | Capacidad                      |
| `current_load`     | `INTEGER`        | `number` integer           |       sí | Carga actual                   |

### Enums

`acopio_centers.status`:

```text
active
full
closed
unverified
```

---

# Resumen de enums

## `events.event_type`

```text
earthquake
flood
landslide
other
```

## `events.status`

```text
active
monitoring
closed
```

## `persons.sex`

```text
M
F
unknown
```

## `persons.status`

```text
missing
found
injured
deceased
unknown
```

## `persons.verification_status`

```text
unverified
pending
verified
conflicting
```

## `person_notes.note_type`

```text
missing
injured
found
deceased
```

## `person_notes.status`

```text
active
superseded
retracted
```

## `person_notes.severity`

```text
leve
moderado
grave
critico
unknown
```

## `person_notes.identification_status`

```text
identified
unidentified
pending
```

## `person_sources.trust_tier`

```text
1 = oficial
2 = ONG
3 = social/anónimo
```

## `acopio_centers.status`

```text
active
full
closed
unverified
```

---

# Notas de implementación

## UUIDs vs autoincrement

Los UUIDs permiten generar IDs en el scraper sin necesidad de consultar la DB.

Esto es importante para JSONL que se ingesta en batch.

---

## `age_range` en lugar de `age`

Se usa `age_range` porque las fuentes de crisis no siempre dan edades exactas confiables.

Guardar un rango es más honesto y evita falsos matches en deduplicación.

---

## `trust_tier` como entero

`trust_tier` se guarda como entero porque es más fácil de indexar y comparar que un string.

El mapeo semántico vive en documentación y en app layer.

---

## `needs` en acopio como array

Los centros de acopio pueden tener necesidades múltiples y cambiantes.

Un array de strings normalizado es más flexible que columnas individuales.

---

## Campos sparse en `person_notes`

La especificación recomienda una sola tabla con columnas nullable por tipo, en lugar de cuatro tablas separadas.

Esto simplifica consultas del tipo:

```text
dame todas las notas de esta persona
```
=======
## Entidad: CENTRO DE ACOPIO

### Tabla `acopio_centers`

| Campo | Tipo SQL | Tipo JSONL | Nullable | Notas |
|---|---|---|---|---|
| `acopio_id` | `VARCHAR(36) PK` | `string` | NO | UUID v4 |
| `event_id` | `VARCHAR(36) FK` | `string` | NO | → `events.event_id` |
| `name` | `VARCHAR(300)` | `string` | NO | Nombre del centro |
| `location` | `JSONB` / `JSON` | `object` | YES | `location_object` |
| `confidence_score` | `NUMERIC(4,3)` | `number` | NO | `0.000` a `1.000` |
| `status` | `VARCHAR(30)` | `string` | NO | Enum `acopio_status` |
| `needs` | `JSONB` / `JSON` | `array<string>` | YES | Keywords del enum `need_keyword`. El parser mapea texto libre antes de exportar |
| `last_verified_at` | `TIMESTAMPTZ` | `string (ISO 8601)` | YES | Última verificación humana o de agente |
| `managing_org` | `VARCHAR(255)` | `string` | YES | Organización responsable |
| `contact_hmac` | `VARCHAR(64)` | `string` | YES | HMAC-SHA256 del contacto original |
| `contact_masked` | `VARCHAR(30)` | `string` | YES | Versión para display. Ej: `"+58 412 ***7834"` |
| `capacity` | `INTEGER` | `number (integer)` | YES | Capacidad máxima en personas |
| `current_load` | `INTEGER` | `number (integer)` | YES | Personas actuales. Validar `≤ capacity` en app layer |

### Ejemplo

```json
{
  "acopio_id": "h8c9d0e1-f2a3-4567-bcde-678901234567",
  "event_id": "f0e1d2c3-b4a5-6789-0fed-cba987654321",
  "name": "Centro de Acopio Polideportivo Municipal San Felipe",
  "location": {
    "raw": "Polideportivo Municipal, San Felipe, Yaracuy",
    "estado": "Yaracuy",
    "municipio": "San Felipe",
    "parroquia": null,
    "lat": 10.3401,
    "lng": -68.7456
  },
  "confidence_score": 0.850,
  "status": "active",
  "needs": ["agua", "alimentos", "medicamentos", "colchonetas", "pañales"],
  "last_verified_at": "2026-06-26T08:00:00Z",
  "managing_org": "Cruz Roja Venezuela — Seccional Yaracuy",
  "contact_hmac": "9f1c3e7a2b4d6f8e0a2c4e6f8b0d2f4a6c8e0b2d4f6a8c0e2f4b6d8a0c2e4f6",
  "contact_masked": "+58 412 ***7834",
  "capacity": 400,
  "current_load": 283
}
```

---

## Enums

### `event_type`
| Valor | Descripción |
|---|---|
| `earthquake` | Sismo / terremoto |
| `flood` | Inundación |
| `landslide` | Deslizamiento |
| `other` | Otro tipo de evento |

### `event_status`
| Valor | Descripción |
|---|---|
| `active` | Evento en curso, datos cambiando activamente |
| `monitoring` | Estabilizado, seguimiento pasivo |
| `closed` | Cerrado, datos congelados |

### `person_status`
| Valor | Descripción |
|---|---|
| `missing` | Desaparecida, no localizada |
| `found` | Localizada con vida |
| `injured` | Localizada, herida |
| `deceased` | Fallecida |
| `unknown` | Estado no determinado |

### `verification_status`
| Valor | Descripción |
|---|---|
| `unverified` | Sin verificación, solo scraping |
| `pending` | En proceso de verificación |
| `verified` | Confirmada por fuente confiable o Validation |
| `conflicting` | Datos contradictorios entre fuentes |

### `sex`
| Valor |
|---|
| `M` |
| `F` |
| `unknown` |

### `note_type`
| Valor | Campos adicionales activos |
|---|---|
| `missing` | `last_seen_at`, `last_seen_location` |
| `injured` | `hospital_name`, `hospital_municipio`, `severity`, `admitted_time` |
| `found` | `found_at` |
| `deceased` | `deceased_at`, `recovery_location`, `identification_status`, `confirmed_by` |

### `note_status`
| Valor | Descripción |
|---|---|
| `active` | Nota vigente |
| `superseded` | Reemplazada por una nota más reciente |
| `retracted` | Retirada por error o desmentido |

### `severity`
| Valor |
|---|
| `leve` |
| `moderado` |
| `grave` |
| `critico` |
| `unknown` |

### `identification_status`
| Valor |
|---|
| `identified` |
| `unidentified` |
| `pending` |

### `trust_tier`
| Valor | Descripción |
|---|---|
| `1` | Alta confianza — hospital, organismo oficial, FUNVISIS |
| `2` | Media — ONG verificada, medio de comunicación |
| `3` | Baja — redes sociales, fuente anónima, grupo de WhatsApp |

### `acopio_status`
| Valor | Descripción |
|---|---|
| `active` | Operativo, recibiendo personas o donaciones |
| `full` | Sin capacidad disponible |
| `closed` | Cerrado |
| `unverified` | Reportado pero no confirmado |

### `need_keyword`
El parser normaliza texto libre a uno de estos valores antes de exportar. Para necesidades sin keyword existente usar `otro`.

| Keyword | Agrupa variantes como |
|---|---|
| `agua` | "agua potable", "H2O", "AGUA", "líquido" |
| `alimentos` | "comida", "víveres", "alimentos no perecederos" |
| `medicamentos` | "medicina", "medicinas", "fármacos", "pastillas" |
| `colchonetas` | "colchón", "colchoneta", "cama" |
| `ropa` | "ropa", "vestimenta", "mudas" |
| `calzado` | "zapatos", "sandalias", "botas" |
| `higiene` | "artículos de higiene", "jabón", "papel higiénico", "cloro" |
| `pañales` | "pañales bebé", "pañales adulto", "diapers" |
| `leche_formula` | "leche de fórmula", "leche para bebé", "fórmula infantil" |
| `generador` | "planta eléctrica", "generador", "electricidad" |
| `combustible` | "gasolina", "gasoil", "diesel", "combustible" |
| `herramientas` | "pala", "pico", "herramientas de rescate" |
| `voluntarios` | "voluntarios", "personal", "ayuda humana" |
| `transporte` | "vehículos", "camiones", "transporte" |
| `otro` | Cualquier necesidad sin keyword asignado |

---

## Notas de implementación

**UUIDs**: permiten generar IDs en el scraper sin tocar la DB, esencial para ingestión batch con JSONL. El equipo DB/API puede indexarlos normalmente.

**`age_range` en lugar de `age`**: las fuentes de crisis raramente dan edades exactas confiables. El rango evita falsos positivos en deduplicación y es más honesto sobre la calidad del dato.

**Columnas sparse en `person_notes`**: una sola tabla con campos nullable por tipo, en lugar de cuatro tablas separadas. Simplifica la consulta "dame todas las notas de esta persona" y permite que una misma persona tenga secuencia de estados (missing → injured → found) sin joins adicionales.

**`trust_tier` como entero**: indexable directamente. El mapeo semántico vive aquí y en app layer, no en la DB.

**`needs` como keywords**: el array mantiene flexibilidad (múltiples necesidades), pero los valores son controlados. Agregar un keyword nuevo al enum no rompe registros existentes. El campo `otro` actúa como válvula de escape auditada.

**`contact_hmac` en acopio**: el contacto de un centro puede ser el celular personal de un voluntario. El default es protegerlo — si Validation confirma que es un número institucional público, app layer puede decidir mostrarlo.
>>>>>>> master
