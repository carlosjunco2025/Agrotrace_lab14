import PaginaBase from './PaginaBase.jsx'

function LotesPage() {
  return (
    <PaginaBase
      etiqueta="Parte 2 · módulo de inventario"
      titulo="Lotes recepcionados"
      descripcion="Pantalla del inventario de café recepcionado: código de lote, toneladas, descarte, estado de evaluación y fundo de origen."
      rutaReact="/lotes"
      rutaApi="/api/lotes/ · /api/lotes-detallados/"
      modulo="inventario"
      estado="API actual ampliada en S12 · modelo en S14"
      entidadPrincipal="LoteRecepcionado"
      entidades={['EvaluacionCalidadLote', 'CertificacionLote', 'DetallePesoLote']}
      tareas={[
        'El panel con búsqueda, filtro y CRUD ya consume /api/lotes-detallados/.',
        'S14: detalle de pesos, descuentos y certificaciones por lote.',
        'Stock y toneladas se validan siempre en Django.',
      ]}
    />
  )
}

export default LotesPage
