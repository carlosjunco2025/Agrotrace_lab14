import PaginaBase from './PaginaBase.jsx'

function PedidosPage() {
  return (
    <PaginaBase
      etiqueta="Parte 2 · módulo comercial"
      titulo="Pedidos comerciales"
      descripcion="Preventas y pedidos confirmados entre AgroTrace y sus clientes mayoristas. Distingue el carrito de la orden ya aprobada por el servidor."
      rutaReact="/pedidos"
      rutaApi="/api/pedidos-agrotrace/ · /api/precios/"
      modulo="comercializacion + pedidos"
      estado="Planificado S15"
      entidadPrincipal="PedidoComercial"
      entidades={['DetallePedido', 'PrecioContrato', 'PagoTokenizado']}
      tareas={[
        'El carrito es estado local; el pedido nace con POST validado.',
        'Precio y valorización se leen de la BD, nunca del navegador.',
        'Datos de tarjeta se tokenizan en la pasarela; no llegan al servidor.',
      ]}
    />
  )
}

export default PedidosPage
