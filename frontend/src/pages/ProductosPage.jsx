// Semana 14 · Ejercicio 7: catálogo de la cafetería consumido desde DRF.
// El navegador sólo pide datos; precio y stock se validan en Django.
import { useEffect, useState } from 'react'
import api, { mensajeDeError } from '../api.js'
import './pages.css'
import './semana14.css'

function ProductosPage() {
  const [productos, setProductos] = useState([])
  const [busqueda, setBusqueda] = useState('')
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let activo = true
    setCargando(true)
    setError('')

    api
      .get('productos/', { params: busqueda ? { search: busqueda } : {} })
      .then((respuesta) => {
        if (activo) setProductos(respuesta.data)
      })
      .catch((fallo) => {
        if (activo) setError(mensajeDeError(fallo, 'No se pudo cargar el catálogo.'))
      })
      .finally(() => {
        if (activo) setCargando(false)
      })

    return () => {
      activo = false
    }
  }, [busqueda])

  return (
    <section className="module page-base">
      <header className="module-header">
        <div>
          <p className="eyebrow">Parte 1 · cafetería de práctica</p>
          <h1>Productos</h1>
          <p className="module-intro">
            Catálogo real leído con <code>api.get</code> desde{' '}
            <code>GET /api/productos/</code>. El precio y el stock llegan desde
            SQLite; el navegador no los calcula.
          </p>
        </div>
        <span className="pill">Ruta React: /productos</span>
      </header>

      <label className="s14-busqueda">
        Buscar por nombre (SearchFilter del ViewSet)
        <input
          type="search"
          value={busqueda}
          placeholder="Ej. Capuchino"
          onChange={(evento) => setBusqueda(evento.target.value)}
        />
      </label>

      {cargando && <p className="s14-estado">Cargando productos desde Django…</p>}
      {error && <p className="s14-error">Error: {error}</p>}

      {!cargando && !error && (
        <div className="productos-grid">
          {productos.map((producto) => (
            <article className="producto-card" key={producto.id}>
              <div className="producto-card__icono" aria-hidden="true">
                ☕
              </div>
              <div className="producto-card__cuerpo">
                <h3>{producto.nombre}</h3>
                <p>{producto.categoria_nombre}</p>
                <dl className="producto-card__datos">
                  <div>
                    <dt>Precio</dt>
                    <dd>S/ {producto.precio}</dd>
                  </div>
                  <div>
                    <dt>Stock</dt>
                    <dd>{producto.stock} und.</dd>
                  </div>
                </dl>
                <span className={producto.activo ? 's14-chip s14-chip--ok' : 's14-chip'}>
                  {producto.activo ? 'Activo' : 'Inactivo'}
                </span>
              </div>
            </article>
          ))}
        </div>
      )}

      {!cargando && !error && productos.length === 0 && (
        <p className="s14-estado">No hay productos que coincidan con la búsqueda.</p>
      )}

      <div className="nota-etapa">
        <strong>Flujo verificado:</strong> React → Axios → DefaultRouter →
        ProductoViewSet → ProductoSerializer → modelo Producto → SQLite → JSON 200.
      </div>
    </section>
  )
}

export default ProductosPage
