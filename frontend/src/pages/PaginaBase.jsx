// Semana 13 · Ejercicio 13: plantilla común de las pantallas base de AgroTrace.
// Cada pantalla documenta su módulo, su ruta React y la ruta API prevista.
import './pages.css'

function PaginaBase({
  etiqueta,
  titulo,
  descripcion,
  rutaReact,
  rutaApi,
  modulo,
  estado,
  entidadPrincipal,
  entidades = [],
  tareas = [],
}) {
  return (
    <section className="module page-base">
      <header className="module-header">
        <div>
          <p className="eyebrow">{etiqueta}</p>
          <h1>{titulo}</h1>
          <p className="module-intro">{descripcion}</p>
        </div>
        <span className="pill">Ruta React: {rutaReact}</span>
      </header>

      <div className="page-grid">
        <article className="page-bloque page-bloque--destacado">
          <h2>Estado del módulo</h2>
          <span
            className={`estado-chip ${
              estado === 'Construido' ? 'estado-chip--listo' : 'estado-chip--planeado'
            }`}
          >
            {estado}
          </span>
          <p className="module-intro">
            <strong>App Django:</strong> <code>{modulo}</code>
          </p>
          <ul>
            {tareas.map((tarea) => (
              <li key={tarea}>{tarea}</li>
            ))}
          </ul>
        </article>

        <article className="page-bloque">
          <h2>Datos y API</h2>
          <p className="module-intro">
            <strong>Entidad principal prevista (S14):</strong>
          </p>
          <span className="entidad-chip entidad-chip--principal">
            {entidadPrincipal}
          </span>
          <div>
            {entidades.map((entidad) => (
              <span className="entidad-chip" key={entidad}>
                {entidad}
              </span>
            ))}
          </div>
          <p className="module-intro">Ruta API documentada:</p>
          <code className="ruta-api">{rutaApi}</code>
        </article>
      </div>

      <div className="nota-etapa">
        <strong>Estructura S13:</strong> esta pantalla existe para organizar el
        módulo. Los modelos, serializers y componentes de datos se implementan
        en las semanas 14 a 16.
      </div>
    </section>
  )
}

export default PaginaBase
