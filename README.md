# AgroTrace

Proyecto integrador de **trazabilidad y comercialización agroindustrial**.
Backend **Django + Django REST Framework** y frontend **React + Vite + Axios**.

- Repositorio: <https://github.com/carlosjunco2025/lab10_Agrotrace>
- Backend: `agrotrace/`, `agrotrace_config/`, `manage.py`
- Frontend: `frontend/`
- Semana 12: integración Full Stack con Axios, CORS y CRUD real.
- Semana 13: arquitectura, módulos, requisitos, reglas, apps de estructura y mapa de rutas.

---

## 1. Tipo de comercio y canales

AgroTrace es una plataforma **B2B agroindustrial** (empresa a empresa): el
productor / fundo ofrece lotes de café a compradores mayoristas, exportadores y
transformadores. El valor central es la **trazabilidad origen-destino**: cada
lote se identifica, se evalúa, se certifica y se comercializa con datos
verificables.

También existe un componente **B2C secundario y planificado**: el consumidor
final podrá consultar por código/QR el recorrido del producto (S16). Esa
consulta es de solo lectura; la venta mayorista sigue siendo B2B.

**Canales (no tipos de comercio):**

| Canal | Estado | Descripción |
|---|---|---|
| Panel web (Vite, puerto 5173) | Construido | `/dashboard`, `/lotes`, `/productores`, `/pedidos`, `/trazabilidad` |
| API REST (DRF, puerto 8000) | Construido | `/api/fundos/`, `/api/lotes/`, `/api/lotes-detallados/`, endpoints de estructura S13 |
| Consulta pública por código/QR | Planificado S16 | Mismo backend, ruta React `/trazabilidad` |
| Aplicación móvil / WhatsApp Business | Planificado | Consumiría la **misma API**, sin duplicar reglas de negocio |

El canal no cambia el tipo de comercio: m-commerce y social commerce son
**formas de llegar al cliente**; el tipo lo determina la relación comercial
(quién vende a quién). Una venta B2B puede hacerse desde web, móvil o chat y sigue siendo B2B.

---

## 2. Mapa de módulos

| Módulo | App Django / carpeta React | Estado |
|---|---|---|
| Fundos y productores | `agrotrace` + `productores` / `/productores` | API de fundos construida S8-S12; ampliación S14 |
| Lotes e inventario | `agrotrace` + `inventario` / `/lotes` | CRUD real construido S12; detalle de pesos en S14 |
| Evaluación y certificaciones | `agrotrace` / `/lotes` | Modelos y API actuales; ampliación S14 |
| Catálogo de productos | `catalogo` / `/productos` | Estructura S13; modelos y API en S14 |
| Clientes y roles | `productores` (origen) + Django Auth / panel | Estructura S13; permisos en S15 |
| Comercialización y pedidos | `comercializacion`, `pedidos` / `/pedidos` | Estructura S13; pedidos y pagos en S15 |
| Pagos tokenizados | `comercializacion` / `/pedidos` | Planificado S15 (pasarela externa) |
| Trazabilidad | `trazabilidad` / `/trazabilidad` | Estructura S13; histórico en S16 |
| Panel administrativo y seguridad | `agrotrace` + apps S13 / rutas React | Panel construido S12; roles y auditoría S15-S16 |
| Notificaciones | Planificada | Planificado S16 |

### Roles de usuario

| Rol | Qué puede hacer | Pantalla principal |
|---|---|---|
| Visitante / consulta | Consultar trazabilidad pública; sin escritura | `/trazabilidad` |
| Productor | Registrar y actualizar datos de su fundo y lotes | `/productores`, `/lotes` |
| Cliente mayorista | Ver catálogo, armar carrito y confirmar pedido | `/productos`, `/pedidos` |
| Operador | Recepcionar lotes, evaluar calidad, cambiar estados | `/lotes` |
| Administrador | Gestionar roles, precios, reportes y configuración | `/dashboard` |

---

## 3. Requisitos verificables

### Funcionales

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-01 | Listar, buscar y filtrar lotes | Alta | `GET /api/lotes-detallados/?search=LOT-2026&estado=PENDIENTE` responde 200 con solo los lotes que coinciden |
| RF-02 | Registrar un lote | Alta | `POST /api/lotes/` con datos válidos responde 201 y la fila aparece sin recargar |
| RF-03 | Editar y cambiar estado de un lote | Alta | `PATCH /api/lotes/{id}/` responde 200 y el estado queda persistido en SQLite |
| RF-04 | Eliminar un lote con confirmación | Alta | `DELETE /api/lotes/{id}/` responde 204; un segundo intento responde 404 y la tabla se sincroniza |
| RF-05 | Mostrar errores de validación por campo | Media | Un `codigo_lote` de 51 caracteres responde 400 y el mensaje aparece junto al input |
| RF-06 | Consultar la trazabilidad de un lote | Media (S16) | `GET /api/trazabilidad/{codigo_lote}/` devuelve origen, evaluaciones y destino |

### No funcionales

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RNF-01 | Respuesta rápida de la API | Alta | `GET /api/lotes-detallados/` responde en menos de 2 s con 6 registros de prueba |
| RNF-02 | Origen permitido explícito | Alta | Sin `http://localhost:5173` en `CORS_ALLOWED_ORIGINS` el navegador bloquea; con él, la petición responde 200 |
| RNF-03 | Tiempo de espera definido | Media | `api.js` usa `timeout: 5000`; pasado ese tiempo se muestra un mensaje de error, nunca una pantalla en blanco |
| RNF-04 | Sin artefactos de build versionados | Alta | `git ls-files` no devuelve `node_modules/`, `dist/` ni `.venv/` |
| RNF-05 | Calidad del código | Alta | `python manage.py check`, `npm run lint` y `npm run build` terminan sin errores |

**RF vs. RNF:** un requisito funcional describe **qué hace** el sistema (altas,
búsquedas, roles); uno no funcional describe **cómo se comporta** (velocidad,
seguridad, disponibilidad, mantenibilidad). “El sistema debe ser rápido y
seguro” no es verificable; se reescribe como RNF-01 y RNF-02 con tiempos,
orígenes y códigos concretos.

---

## 4. Reglas de negocio

| # | Regla | Dónde se aplica | Error que evita |
|---|---|---|---|
| RN-01 | El precio y la valorización se leen de la base de datos, nunca del navegador | Django (serializer / servicio de precios) | Precios manipulados desde DevTools o desactualizados |
| RN-02 | El stock / toneladas de cada lote se validan en el backend | Django (`validate_toneladas_brutas`, ORM transaccional) | Ventas por encima del stock o cantidades negativas |
| RN-03 | El dinero se maneja con `Decimal`, nunca `float` | Django (`DecimalField`) y React (`Number()` solo para mostrar) | Errores de redondeo como `0.1 + 0.2` |
| RN-04 | Los datos de tarjeta se tokenizan en la pasarela; nunca llegan al servidor propio | Pasarela externa + React (token) | Exponer PAN/CVV y ampliar alcance PCI-DSS |
| RN-05 | El carrito es estado local; el pedido confirmado existe solo tras `POST` validado | React (carrito) + Django (pedido) | Pedidos fantasma o cobros sin orden persistida |
| RN-06 | `codigo_lote` ≤ 50 caracteres; `nombre_fundo` ≤ 100 | Django (serializer) | Datos inconsistentes o desbordamiento de columna |
| RN-07 | Un lote eliminado no debe quedar en la tabla del cliente | React (`filter()` al recibir 204/404) | Acciones sobre registros inexistentes |

El stock no se controla solo en React porque el navegador es un cliente no
confiable: cualquier usuario puede modificar el JavaScript, las props o la
petición con Postman. El servidor es la única fuente de verdad y debe validar
dentro de una transacción atómica.

---

## 5. Arquitectura en capas

```text
Usuario (productor, operador, cliente o administrador)
        │
        ▼
React (pages/ + components/)          ← estado, validación visual, UX
        │  Axios (src/api.js)  ·  baseURL http://127.0.0.1:8000/api/
        │  HTTP + JSON (GET/POST/PATCH/DELETE)
        ▼
Django REST Framework                 ← URLs → Router → ViewSets
        │  Serializer: valida, convierte JSON, devuelve 200/201/204/400/404
        ▼
Django ORM → SQLite (db.sqlite3)      ← entidades, reglas y transacciones
        │
        ▼
Pasarela de pago (planificada S15)    ← token, no número de tarjeta
```

**Flujo de operación principal (registro y recepción de lote):**

1. El operador abre `/lotes` y completa el formulario con código, toneladas y fundo.
2. React valida los campos y envía `POST /api/lotes/` con Axios.
3. El serializer valida `max_length`, `toneladas_brutas > 0` y la FK del fundo.
4. El ORM crea el registro dentro de una transacción y SQLite lo persiste.
5. Django responde `201` con el JSON del lote; React actualiza la tabla con un arreglo nuevo.
6. Si hay error, responde `400` con mensajes por campo que se pintan junto al input.

**Flujo comercial planificado:** el cliente arma un carrito en React →
confirma → Django calcula el precio desde la BD, descuenta stock de forma
atómica y crea el pedido → la pasarela devuelve un token → Django registra el
pago aprobado. El servidor nunca recibe el número de tarjeta: el navegador se
lo envía directamente a la pasarela y solo comparte un token opaco.

---

## 6. Estructura del repositorio

```text
Agrotrace-Lab07/
├── manage.py
├── requirements.txt
├── README.md
├── agrotrace_config/        # settings.py, urls.py, wsgi.py
├── agrotrace/               # app base: modelos, views, serializers, API S8-S12
├── catalogo/                # S13 Parte 1: cafetería (modelos en S14)
├── pedidos/                 # S13 Parte 1 + módulo comercial AgroTrace
├── productores/             # S13 Parte 2: origen de los lotes
├── inventario/              # S13 Parte 2: lotes y stock
├── comercializacion/        # S13 Parte 2: precios y pedidos
├── trazabilidad/            # S13 Parte 2: histórico origen-destino
└── frontend/
    ├── package.json
    ├── src/
    │   ├── api.js                      # instancia Axios + errores
    │   ├── App.jsx                     # BrowserRouter y mapa de rutas
    │   ├── components/                 # piezas reutilizables + panel S12
    │   │   ├── ProductoCard.jsx        # S13 Parte 1
    │   │   ├── PanelLotes.jsx          # S12
    │   │   └── Lote*.jsx
    │   ├── pages/                      # pantallas por ruta
    │   │   ├── ProductosPage.jsx       # S13 Parte 1
    │   │   ├── PaginaBase.jsx          # plantilla de las páginas S13
    │   │   ├── DashboardPage.jsx
    │   │   ├── ProductoresPage.jsx
    │   │   ├── LotesPage.jsx
    │   │   ├── PedidosPage.jsx
    │   │   ├── TrazabilidadPage.jsx
    │   │   └── pages.css
    │   └── practica/                   # lista CRUD de la Parte 1 (S12)
    └── dist/                           # generado, NO versionado
```

---

## 7. Mapa de rutas

### API Django

| Recurso | Ruta | Métodos / estado |
|---|---|---|
| Fundos | `/api/fundos/` y `/api/fundos/{id}/` | GET, POST, PATCH, DELETE · construido |
| Lotes | `/api/lotes/` y `/api/lotes/{id}/` | GET, POST, PATCH, DELETE · construido |
| Lotes detallados | `/api/lotes-detallados/?search=&estado=` | GET · construido |
| Evaluaciones | `/api/evaluaciones/` y `/api/evaluaciones-detalladas/` | GET · construido |
| Catálogo cafetería | `/api/catalogo/` | GET metadata · estructura S13, API en S14 |
| Pedidos cafetería | `/api/pedidos/` | GET metadata · estructura S13 |
| Productores AgroTrace | `/api/productores/` | GET metadata · estructura S13, modelo en S14 |
| Inventario | `/api/inventario/` | GET metadata · estructura S13 |
| Comercialización | `/api/comercializacion/` | GET metadata · estructura S13 |
| Trazabilidad | `/api/trazabilidad/` | GET metadata · consulta por lote en S16 |
| Django Admin | `/admin/` | Panel nativo (el panel del laboratorio es React) |

### Frontend React

| Ruta React | Pantalla | Módulo |
|---|---|---|
| `/` y `/dashboard` | `DashboardPage.jsx` | Panel de control |
| `/practica` | `ListaPractica.jsx` | Parte 1 · CRUD de fundos (S12) |
| `/productos` | `ProductosPage.jsx` | Parte 1 · catálogo de la cafetería (S13) |
| `/panel` | `PanelLotes.jsx` | Parte 2 · panel de lotes (S12) |
| `/productores` | `ProductoresPage.jsx` | Origen de los lotes |
| `/lotes` | `LotesPage.jsx` | Inventario y evaluación |
| `/pedidos` | `PedidosPage.jsx` | Comercialización |
| `/trazabilidad` | `TrazabilidadPage.jsx` | Consulta origen-destino |

Una **ruta de API** devuelve datos en JSON con un código HTTP; una **ruta de
React** selecciona qué componente se dibuja en el navegador. `/api/productores/`
y `/productores` pueden referirse al mismo recurso, pero uno es la fuente de
datos y el otro es la interfaz.

---

## 8. Ejecutar y verificar

```powershell
# Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py check
python manage.py runserver 127.0.0.1:8000
```

```powershell
# Frontend (segunda terminal)
cd frontend
npm install
npm run dev
npm run lint
npm run build
```

- Django: <http://127.0.0.1:8000/api/>
- React: <http://localhost:5173/>

`node_modules/`, `dist/`, `.venv/` y `db.sqlite3` están excluidos en `.gitignore`.

## Autor

Yunior Bestard Aroche — Desarrollo de Aplicaciones Empresariales.
