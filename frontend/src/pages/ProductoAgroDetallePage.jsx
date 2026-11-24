// Semana 14 · Ejercicio 12: detalle de un registro de AgroTrace.
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import api, { mensajeDeError } from '../api.js'
import './pages.css'
import './semana14.css'

function ProductoAgroDetallePage() {
  const { id } = useParams()
  const [producto, setProducto] = useState(null)
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let activo = true
    setCargando(true)
    setError('')

    api
      .get(`productos-agro/${id}/`)
      .then((respuesta) => {
        if (activo) setProducto(respuesta.data)
      })
      .catch((fallo) => {
        if (activo) setError(mensajeDeError(fallo, 'No se pudo cargar el detalle.'))
      })
      .finally(() => {
        if (activo) setCargando(false)
      })

    return () => {
      activo = false
    }
  }, [id])

  return (
    <section className="module page-base">
      <header className="module-header">
        <div>
          <p className="eyebrow">Parte 2 · detalle del registro</p>
          <h1>{producto ? producto.nombre : 'Detalle AgroTrace'}</h1>
          <p className="module-intro">
            Ruta <code>/productos-agro/:id</code> ·{' '}
            <code>GET /api/productos-agro/{id}/</code>
          </p>
        </div>
        <Link className="s14-enlace" to="/productos-agro">
          ← Volver al listado
        </Link>
      </header>

      {cargando && <p className="s14-estado">Cargando detalle…</p>}
      {error && <p className="s14-error">Error: {error}</p>}

      {!cargando && !error && producto && (
        <div className="page-grid">
          <div className="page-bloque page-bloque--destacado">
            <h2>Identificación</h2>
            <ul>
              <li>
                <strong>Código:</strong> {producto.codigo}
              </li>
              <li>
                <strong>Productor:</strong> {producto.productor_nombre}
              </li>
              <li>
                <strong>Estado:</strong> {producto.activo ? 'Activo' : 'Inactivo'}
              </li>
            </ul>
          </div>
          <div className="page-bloque">
            <h2>Operación</h2>
            <ul>
              <li>
                <strong>Stock disponible:</strong> {producto.stock_kg} kg
              </li>
              <li>
                <strong>Precio por kg:</strong> S/ {producto.precio_kg}
              </li>
              <li>
                <strong>Valorización:</strong> S/{' '}
                {(Number(producto.stock_kg) * Number(producto.precio_kg)).toFixed(2)}
              </li>
            </ul>
            <span className="ruta-api">id = {producto.id}</span>
          </div>
        </div>
      )}
    </section>
  )
}

export default ProductoAgroDetallePage
