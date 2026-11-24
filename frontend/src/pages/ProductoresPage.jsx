import PaginaBase from './PaginaBase.jsx'

function ProductoresPage() {
  return (
    <PaginaBase
      etiqueta="Parte 2 · módulo de origen"
      titulo="Productores"
      descripcion="Registro de productores y fundos de donde proviene cada lote. Es el punto de partida de la trazabilidad origen-destino."
      rutaReact="/productores"
      rutaApi="/api/productores/ · /api/fundos/"
      modulo="productores"
      estado="Planificado S14 (API fundos ya disponible)"
      entidadPrincipal="FundoProductor"
      entidades={['Productor', 'Distrito', 'CertificacionAgricola']}
      tareas={[
        'Reutilizar el serializer FundoProductor de la Semana 8.',
        'Ampliar con datos de contacto y ubicación del productor.',
        'Validar RUC/DNI y hectáreas con Decimal en el servidor.',
      ]}
    />
  )
}

export default ProductoresPage
