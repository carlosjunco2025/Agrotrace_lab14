// Semana 13 · Ejercicio 7: pantalla base de la cafetería (estructura S13).
// Los modelos, la API y la carga real de datos se escriben en la Semana 14.
import ProductoCard from '../components/ProductoCard.jsx'
import './pages.css'

const PRODUCTOS_BASE = [
  {
    id: 'estructura-1',
    nombre: 'Café de origen',
    descripcion: 'Catálogo de bebidas: modelo Producto previsto para S14.',
  },
  {
    id: 'estructura-2',
    nombre: 'Combo desayuno',
    descripcion: 'Ejemplo de producto compuesto; precio se calculará en el servidor.',
  },
  {
    id: 'estructura-3',
    nombre: 'Repostería',
    descripcion: 'Categoría adicional del módulo de catálogo de la cafetería.',
  },
]

function ProductosPage() {
  return (
    <section className="module page-base">
      <header className="module-header">
        <div>
          <p className="eyebrow">Parte 1 · cafetería de práctica</p>
          <h1>Productos</h1>
          <p className="module-intro">
            Estructura inicial creada en la Semana 13. Aquí se conectará el
            catálogo con <code>/api/productos/</code> cuando los modelos se
            programen en la Semana 14.
          </p>
        </div>
        <span className="pill">Ruta React: /productos</span>
      </header>

      <div className="productos-grid">
        {PRODUCTOS_BASE.map((producto) => (
          <ProductoCard key={producto.id} producto={producto} />
        ))}
      </div>

      <div className="nota-etapa">
        <strong>Etapa actual:</strong> arquitectura y carpetas. Los valores de
        precio y stock no se escriben en el navegador: se leerán de la base de
        datos y se validarán en Django.
      </div>
    </section>
  )
}

export default ProductosPage
