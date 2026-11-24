// Semana 13 · Ejercicio 7: componente base de la cafetería.
// La tarjeta solo presenta datos; el precio y el stock se leerán de la BD en S14.
function ProductoCard({ producto }) {
  const { nombre, descripcion, precio, stock } = producto

  return (
    <article className="producto-card">
      <div className="producto-card__icono" aria-hidden="true">
        ☕
      </div>
      <div className="producto-card__cuerpo">
        <h3>{nombre}</h3>
        <p>{descripcion}</p>
        <dl className="producto-card__datos">
          <div>
            <dt>Precio</dt>
            <dd>{precio ?? 'Se leerá de la BD (S14)'}</dd>
          </div>
          <div>
            <dt>Stock</dt>
            <dd>{stock ?? 'Validado en Django (S14)'}</dd>
          </div>
        </dl>
      </div>
    </article>
  )
}

export default ProductoCard
