import PaginaBase from './PaginaBase.jsx'

function TrazabilidadPage() {
  return (
    <PaginaBase
      etiqueta="Parte 2 · módulo de trazabilidad"
      titulo="Trazabilidad"
      descripcion="Consulta del recorrido completo de un lote: fundo de origen, evaluaciones, certificaciones, transformación y destino comercial."
      rutaReact="/trazabilidad"
      rutaApi="/api/trazabilidad/ · /api/trazabilidad/{codigo_lote}/"
      modulo="trazabilidad"
      estado="Planificado S16"
      entidadPrincipal="TrazaLote"
      entidades={['HistorialEstado', 'EventoTrazabilidad', 'CertificacionLote']}
      tareas={[
        'Generar elhistórico de eventos a partir de los lotes existentes.',
        'Exponer una consulta pública por código de lote.',
        'Solo lectura para el rol de consulta; escritura restringida.',
      ]}
    />
  )
}

export default TrazabilidadPage
