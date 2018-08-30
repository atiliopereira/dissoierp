Dissoi-ERP
========================

Nombre código: dissoierp

Fecha de inicio: 30/04/2018

Dirección del proyecto: Atilio Pereira

Repositorio: https://github.com/atiliopereira/dissoierp.git

Web oficial: https://dissoi.com/productos/erp

Tecnología: Django-Python

Licencia: MIT

---
#Descripción
Dissoi-ERP es un software de gestión de recursos para Pymes de producción.
Con él se pretende brindar una solución completa y flexible para distintas empresas dedicadas no solo a la venta de productos, sino especialmente a aquellas que a utilizan materia prima, y crean o dan valor agregado a sus productos.

e.g. mueblerías, industrias publicitarias, gráficas, contratistas, talleres, etcétera.

##Módulos:
* Presupuestos: Costeo y seguimiento
* Producción: Ordenes de trabajo
* Ventas: Facturación, cobranza y remisiones
* Compras: Ordenes de compra, pagos y control de deudas
* Depósitos: Control de materiales e inventarios

El sistema integra todas las áreas involucradas en el proceso, pero también permite la utilización de los módulos de manera aislada.

#Funciones del sistema
###Funcionarios
- Funcionarios: Creación y modificación y consulta funcionarios
	- Nombre
	- Apellido
	- Dirección
	- E-mail
	- Fecha de ingreso
	- Observaciones
	- usuario (un funcionario puede no tener *usuario en el sistema*, pero se requiere su registro para referencias dentro del sistema)
Obs: Los permisos de usuarios se gestionan en el módulo "Auth"

###Clientes
- Clientes: Creación, modificación y consulta de datos del cliente:
	- Razón Social
	- Ruc
	- Dirección
	- Teléfono
	- E-mail
	- Vendedor (Encargado dentro de la empresa: debe ser funcionario registrado del sistema)
	- Marcas (Un cliente puede tener varias marcas asociadas)
	- Contacto (Persona con la que se tiene contacto directo o representa al cliente)

###Items
Llamamos items a los productos y/o servicios que se presupuestan y venden.

- Unidades de medida: Creación, modificación y consulta de unidades de medida de items.
	- Nombre (e.g.: metro, metro cuadrado, unidad, litros, etc.)
	- Símbolo (utilizado para abreviaturas)
	 
- Categoría de items: 	Creación, modificación y consulta de categorías para clasificación de items.
	- Nombre
	- Nombre completo (utilizado para identificar una subcategoria, anteponiendo su/s categoria/s padre/s)
	- Categoría raíz (utilizada para agrupar en las categorías principales)
	 
- Items: Creación, modificación y consulta de items.
Se usa “item” para hacer referencia tanto a servicios, productos y productos elaborados.
    - Servicio: No se controla stock.
    - Producto: Se controla Stock, puede ser insumo (no requiere orden de trabajo para retiro).
    - Elaborado: Es un producto elaborado con otros productos y servicios, puede guardarse como plantilla para reutilizar en varios presupuestos o ventas.

Campo | Producto | Servicio | Elaborado | Comentarios
--- | --- | --- | --- | ---
Tipo | ✓ | ✓ | ✓ | Predefinidos: Productos (valor por defecto), Servicio y Elaborado. 
Categoría | ✓ | ✓ | ✓ | - 
Código | ✓ | ✓ | ✓ | Usado para abreviaturas y búsquedas rápidas. 
Descripción | ✓ | ✓ | ✓ | - 
Unidad de medida | ✓ | ✓ | ✓ | - 
Costo | ✓ | ✓ | ✓ | Asociado a la compra.
Precio | ✓ | ✓ | ✓ | Asociado a la venta.
Stock actual | ✓ | ✕ | ✓ | - 
Stock mínimo | ✓ | ✕ | ✓ | Sirve para evitar desabastecimiento.
Es insumo | ✓ | ✕ | ✕ | Condición para que no se exija órden de trabajo para su retiro o compra.
Es plantilla | ✕ | ✕ | ✓ | Se usa como plantilla para volver a incluir en presupuesto o venta.
Lista de materiales | ✕ | ✕ | ✓ | Productos y servicios utilizados en la elaboración.

radas en el proceso, pero también permite la utilización de los módulos de manera aislada.