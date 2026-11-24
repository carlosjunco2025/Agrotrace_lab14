// Semana 14 · Ejercicio 12: listado de la entidad principal de AgroTrace.
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api, { mensajeDeError } from '../api.js'
import './pages.css'
import './semana14.css'

function ProductosAgroPage() {
  const [productos, setProductos] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let activo = true
    setCargando(true)

    api
      .get('productos-agro/')
      .then((respuesta) => {
        if (activo) setProductos(respuesta.data)
      })
      .catch((fallo) => {
        if (activo) setError(mensajeDeError(fallo, 'No se pudo cargar AgroTrace.'))
      })
      .finally(() => {
        if (activo) setCargando(false)
      })

    return () => {
      activo = false
    }
  }, [])

  return (
    <section className="module page-base">
      <header className="module-header">
        <div>
          <p className="eyebrow">Parte 2 · proyecto integrador</p>
          <h1>Catálogo AgroTrace</h1>
          <p className="module-intro">
            Listado principal cargado con <code>GET /api/productos-agro/</code>.
            Cada tarjeta navega a <code>/productos-agro/:id</code>.
          </p>
        </div>
        <span className="pill">GET 200</span>
      </header>

      {cargando && <p className="s14-estado">Cargando catálogo agroindustrial…</p>}
      {error && <p className="s14-error">Error: {error}</p>}

      {!cargando && !error && (
        <div className="productos-grid">
          {productos.map((producto) => (
            <article className="producto-card" key={producto.id}>
              <div className="producto-card__icono" aria-hidden="true">
                🌱
              </div>
              <div className="producto-card__cuerpo">
                <h3>{producto.nombre}</h3>
                <p>
                  {producto.codigo} · {producto.productor_nombre}
                </p>
                <dl className="producto-card__datos">
                  <div>
                    <dt>Stock</dt>
                    <dd>{producto.stock_kg} kg</dd>
                  </div>
                  <div>
                    <dt>Precio/kg</dt>
                    <dd>S/ {producto.precio_kg}</dd>
                  </div>
                </dl>
                <Link className="s14-enlace" to={`/productos-agro/${producto.id}`}>
                  Ver detalle →
                </Link>
              </div>
            </article>
          ))}
        </div>
      )}

      {!cargando && !error && productos.length === 0 && (
        <p className="s14-estado">No hay productos AgroTrace registrados.</p>
      )}
    </section>
  )
}

export default ProductosAgroPage
